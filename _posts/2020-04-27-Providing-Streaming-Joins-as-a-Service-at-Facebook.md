---
layout: "post"
title: "Providing Streaming Joins as a Service at Facebook"
date: "2020-05-01 11:11"
desc: Paper Summary for 'Providing Streaming Joins as a Service at Facebook'
comments: true
author: Sujith Jay Nair
tags: paper-summary data-systems streaming joins
image: /public/streamingjoins/synchronisation.png
permalink: /streaming-joins-at-facebook
---
[Providing Streaming Joins as a Service at Facebook](http://www.vldb.org/pvldb/vol11/p1809-jacques-silva.pdf).
_Jacques-Silva, G., Lei, R., Cheng, L., et al. (2018). Proceedings of the VLDB Endowment, 11(12), 1809-1821._

Stream-stream joins are a hard problem to solve at scale. _"Providing Streaming Joins as a Service at Facebook"_ provides us the overview of systems within Facebook to support stream-stream joins.

The key contributions of the paper are:
1. a stream synchronization scheme based on event-time to pace the parsing of new data and reduce memory consumption,


2. a query planner which produces streaming join plans that support application updates, and


3. a stream time estimation scheme that handles the variations on the distribution of event-times observed in real-world streams and achieves high join accuracy.

### Trade-offs in Stream-Stream Joins

Stream-stream joins have a 3-way trade-off of output latency, join accuracy, and memory footprint. One extreme of this trade-off is to provide best-effort (in terms of join accuracy) processing-time joins. Another extreme is to persist metadata associated with every joinable event on a replicated distributed store to ensure that all joinable events get matched. This approach provides excellent guarantees on output latency & join accuracy, with memory footprint sky-rocketing for large, time-skewed streams.

The approach of the paper is in the middle: it is best-effort with a facility to improve join accuracy by pacing the consumption of the input streams based on dynamically estimated watermarks on event-time.

<!--break-->

### Systems Overview

The streaming-join service is built on top of three in-house systems within Facebook: Scribe, Puma, & Stylus. A larger overview of these systems, along with other streaming systems in use within Facebook, is provided in [Realtime Data Processing at Facebook](https://research.facebook.com/publications/realtime-data-processing-at-facebook/).

- _**Scribe**_ is a persistent distributed messaging system that organises data in categories (like Kafka topics). Categories can be partitioned into multiple buckets, and a bucket is the unit of workload assignment.

- _**Puma**_ allows developers to write analytic jobs in a SQL-like DSL with Java UDFs called _Puma Query Language_ (PQL).

- _**Stylus**_ is a C++ framework for building stateless, stateful and monoid stream processing operators. Stylus also provides operators the ability to replay a Scribe stream for an earlier point in time and persist in-memory state to local or remote storage.

The use of Scribe as the data transfer mechanism between operators in Stylus means that these operators can be easily plugged into a Puma query-execution DAG (in which operators are linked via Scribe as well).

### Join Semantics
The system supports only inner-join and left-outer join. The join output can be all matching events within a window (1-to-n) or a single event within a window (1-to-1).

To maintain backward compatible, the system limits the changes a user can make to existing streaming joins. If the updated
streaming join is significantly different, users have the option of creating a view with a new name and deleting the old one. Two examples of rules an update must follow are:
1. preservation of the join equality expression, as its modification can cause resharding of the Scribe categories

2. projection of new attributes must be specified at the end of the select list, as adding an attribute in the middle of the select list would cause the join operator to consume old attribute values as the value of a different attribute.

### Query Language

For streaming-joins, the user express their joins via _PQL_ in Puma, while the join is implemented under the hoods in Stylus. A user-defined join is defined as an application:

```
00: CREATE APPLICATION sample_app;
01:
02: CREATE INPUT TABLE left (
03: eventtime, key, dim_one, metric
04: ) FROM SCRIBE("left");
05:
06: CREATE INPUT TABLE right (
07: eventtime, key, dim_two, dim_three
08: ) FROM SCRIBE("right");
09:
10: CREATE VIEW joined_streams AS
11: SELECT
12: l.eventtime AS eventtime, l.key AS key,
13: l.dim_one AS dim_one, r.dim_two AS dim_two,
14: COALESCE(r.dim_three, "example") AS dim_three,
15: ABS(l.metric) AS metric
16: FROM left AS l
17: LEFT OUTER JOIN right AS r
18: ON (l.key = r.key) AND
19: (r.eventtime BETWEEN
20: l.eventtime - INTERVAL `3 minutes' AND
21: l.eventtime + INTERVAL `3 minutes');
22:
23: CREATE TABLE result AS
24: SELECT
25: eventtime, key, dim_one, dim_two,
26: dim_three, metric
27: FROM joined_streams
28: STORAGE SCRIBE (category = "result");
```
The join view specification above has an equality expression (line 18), and a window expressed with the BETWEEN function
and using intervals on the timestamp attributes (lines 19-21).

Given a _PQL_ query as above, it is compiled into an execution plan comprised of operators. For joins, the operators involved are :
1. _Slicer_ : a Puma operator, similar to a mapper in MapReduce, which can ingest data from Scribe, evaluate expressions, do tuple-filtering, project columns, shard streams, and write data to Scribe, Hive, or other storage sinks.


2. _Join_ : a Stylus operator which can ingest data from two Scribe streams, maintain the join windows, execute the join logic, and output the result into another Scribe stream.

{% include image-caption.html file="/public/streamingjoins/plan.jpg" description="Figure 1. Logical Plan for Join query" %}

As part of the pre-join transformations on both the left (probe-side) & right side (build-side), projections are resolved, join equality & timestamp expressions are computed, and the streams are sharded as per the join-equality attribute & written into intermediary Scribe categories.

Since only inner joins or left-outer joins are supported by the system, the expressions of the left-side are evaluated before join while for the right-side, this is done after the join.

### The Join Operator
{% include image-caption.html file="/public/streamingjoins/join.png" description="Figure 2. The Join Operator" %}

As shown in Figure 2, the join operator has 3 components: (i) a stateful engine, used to process the left stream, (ii) a stateless engine, processing the right stream, and (iii) a coordinator, to bridge the two engines together.

**_Left stateful engine_** :  As events in the left stream are processed, the stateful engine looks-up matching events in the right join window. In case of a successful lookup, join results are generated. If there are no matches, the event is retained (till the window closes) in the buffer to retry later.[^1]

**_Right stateless engine_** : The stateless engine ingests the right stream and maintains a window of events that matches the specified join window for the incoming left stream events. The window is trimmed at regular intervals to expel events outside the join window. This happens when the _dynamically estimated processing time_ for the stream moves forward.[^2]

**_Coordinator_** : The coordinator brings both engines together by providing APIs for the left engine to look up matching events in the right engine, and for both engines to query the other stream's _dynamically estimated processing time_.

### Dynamically Estimated Processing Time
A stream property called _processing time_ is used in the synchronisation of the two streams. Stream synchronisation is essential to limit the memory required to buffer events needed for matching. This section is a brief overview of _processing time_; while the next section describes its use in stream synchronisation.

_Processing Time_ (PT) indicates the estimated time of a stream : a time for which we estimate that there will be no new events whose event-time has a value that is smaller than the processing time.[^3] To compute a stream's _PT_, it is divided into micro-batches with configurable size. The _PT_ for a micro-batch is then computed. Events in future micro-batches are expected to have _event-time > PT_.[^4]

The sizing of micro-batches is crucial. Larger micro-batches provide better estimates of _PT_ [^5], but increase latency in the system.

### Synchronising Streams
{% include image-caption.html file="/public/streamingjoins/synchronisation.png" description="Figure 3. The Synchronisation Algorithm" %}

Each stream computes its _PT_ independently. Stream synchronisation is performed by pausing the stream that has its _PT_ too far
ahead of the other. Synchronization uses the following formula:

$$\mathsf{ PT_{left} + Window_{upper} = PT_{right}}$$

where $$\mathsf{ PT_{left}}$$ represents the processing time estimated for the left stream, $$\mathsf{ PT_{right}}$$ is the processing time for the right stream, and $$\mathsf{Window_{upper}}$$ is the upper boundary of the window.

### Performance Evaluation

#### Join Accuracy
{% include image-caption.html file="/public/streamingjoins/accuracy.png" description="Figure 4. Join accuracy is close to
accuracy observed in Batch joins with similar join windows." %}

### Join Window Size vs. Memory Consumption
{% include image-caption.html file="/public/streamingjoins/memory.png" description="Figure 5. Memory consumption is proportional to the window size." %}

#### Join Window Size vs. Join Success Rate
{% include image-caption.html file="/public/streamingjoins/success.png" description="Figure 6. Improvement in success rate is not large when comparing a 1-hour window to a 6-hours window." %}

### Footnotes
[^1]: The stateful engine persists state into a local RocksDB instance and replicates it asynchronously to remote HDFS clusters, and hence, called stateful.

[^2]: Although it maintains an in-memory state, the engine is stateless from a system perspective. It does not checkpoint to local or remote storage. It relies on replaying data from Scribe categories for fault-tolerance.

[^3]: In Stylus, the processing time is implemented as a percentile of the processed event times, similar to Millwheel.
[^4]: If the statistic for _PT_ is an _x percentile_ statistic, the assumption is that any future micro-batch will have at most _x%_ of events with an _event-time < PT_.
[^5]: A better estimate of _PT_ is that which fulfills the low watermark assumption that at most _x%_ of events processed after a given _PT_ will have an _event-time_ smaller than it.

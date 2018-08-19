---
layout: "post"
comments: true
title: "A Simple Dichotomy for Modeling Data-Intensive Systems"
desc: A simple mental-model to designing data systems
author: Sujith Jay Nair
tags: data-systems
series: Data Systems
categories:
  - data-systems
date: "2018-08-18 11:11"
image: /public/StateVsStream.png
permalink: /data-systems/A-Simple-Dichotomy-for-Modelling-Data-Intensive-Systems/
---
**TL; DR**
This post presents a simple, almost trivial, mental-model to help think about data-intensive systems.

<!--break-->
## Cut to the chase
Large-scale data processing serves multiple purposes. At a 30,000-feet view, every purpose can be bucketed into two broad categories:
- Maintaining Materialized Views
- Processing Events

This categorization is a high, high level one I use to reason about data system design, and its utility fades fast as we delve deeper into system nitty-gritty. Silos appear within & around each of these buckets as we descend into implementation of systems, but it is still a useful one to reason about data-intensive applications.

The basis of this categorization is captured in the following statement:

`Every data system has two variables: data & query. The defining feature of the system is in the temporal nature of these variables. In every data system, either data or query is transient and the other is persistent.`

In a data system maintaining materialized views, data (or more precisely, the view of data) is persistent, and query is a transient entity flowing into & out of the system.

In a data system processing events, query is persistent and transient data flows through the system.


## I like examples
What are examples of systems which can be reasoned using this simple model?

Every database system can be looked at as a system maintaining materialized views. Data is persistent, by the very definition of a database. It provides a DSL (such as SQL) to query against this persistent data. These queries are transient; once an output is generated against the query, no record is kept of it (except logs of it, perhaps). Some queries mutate data, but that is all right. It still fits the model; we defined data to be persistent, not immutable.

Database triggers are systems processing events. A pattern is stored against a trigger, and every time a new data point satisfies this pattern, a trigger event is generated.

A class of systems which belong to the bucket of systems processing events are [CEP](https://en.wikipedia.org/wiki/Complex_event_processing) (Complex Event Processing) systems. In fact, every system which belongs to the bucket of systems processing events can be called a CEP system.

An analytics system performing batch computations, or stream processing, or implementing some form of lambda architecture is an example of a system capable of being modeled as either. The model depends on the vantage point from where you observe the system.

Every statistic, metric, aggregation, and model (machine-learned) that the system computes is a materialized view into the source data. Thus, if we view the analytics system in conjunction with the system-component storing the materialized views, i.e, from the vantage point of a consumer of the materialized views, the system exhibits the property of persistent data & transient query.

On the other hand, when viewed in disjunction with the component storing the materialized views, it exhibits the property of permanent query and transient data.

## Why does this dichotomy exist?
Data in a system exists either as state or a stream. Martin Kleppmann has a loose analogy to connect states and streams [[1]](#kleppmann-martin-designing-data-intensive-applications-the-big-ideas-behind-reliable-scalable-and-maintainable-systems--oreilly-media-inc-2017). In this analogy, State is defined as the mathematical integration (a cumulative effect) of a stream.

$$ \mathsf{\mathbf{state(now) = \int_{t = 0}^{now} stream(t)  dt }} $$

Our dichotomy is a direct effect of the two forms of data, and which form is the primary concern of your system. Systems concerned with state fall into the bucket of systems maintaining materialized views; whereas systems concerned with stream are event processing systems. In this sense, we could very well rename our categories as state systems and stream systems (although I feel these names are too generic to have any recall value).


## Why do I need this vague dichotomy?
This dichotomy could form a part of your ['W' questions](https://en.wikipedia.org/wiki/Five_Ws) when you are designing a data-intensive system: more specifically, I believe it answers the 'why' question. Let us take a step back and have a brief look at each of the basic 'W' questions we need answered when designing a large-scale data-processing application.

- ### What is the input to your system?
At the outset, we need to define the properties of the input data along the following dimensions:
  - **Bounded vs Unbounded**
  - **Order**
  - **Completeness**

  Tyler Akidau has a very lucid explanation of these concepts in his blog on [The world beyond batch: Streaming 101](https://www.oreilly.com/ideas/the-world-beyond-batch-streaming-101).

- ### How is the computation done?
Based on the answers of 'what', you could now make a choice of 'how' your computation will be performed. Two paradigms exist: **Streaming and Batch**. I refer the user again to the above blog by Akidau for a definition of these terms.

- ### Who is the consumer of the output of your system?
Is your consumer interested in the aggregated state or the processed/enriched stream? The answer to this question seems to closely resemble our dichotomy. Multiple consumers interested in both stream & aggregated state will exist for your system; this is not incoherent. As we have observed in our examples, these multiple consumers are only placed at different vantage points with respect to your system. Thus, defining consumers is an exercise of defining the vantage points to your system.

- ### Why is the computation performed?
This answer to this question is the raison d'être for your system. I believe our dichotomy captures a high-level answer to this question. Also, answering the 'why' encompasses every other 'W' question; so it helps to [start with why](https://en.wikipedia.org/wiki/Start_With_Why).


## Related Work
The central tenet of this dichotomy is an old idea; streams and databases have had separate handling and research attention since long [[2]](#abadiand-d-et-al-aurora-a-data-stream-management-system-proc-acm-sigmod-2003)[[3]](#aggarwal-charu-c-ed-data-streams-models-and-algorithms-vol-31-springer-science--business-media-2007).

However, synergy between the two cannot be overstated. Recent state-of-the-art systems, such as [Kafka](https://kafka.apache.org/) and [Samza](http://samza.apache.org/), have blurred the distinction between them. Suggested reading include [[4]](#kreps-jay-its-okay-to-store-data-in-kafka-confluent-2018-link-accessed-14-aug-2018)[[5]](#kreps-jay-why-local-state-is-a-fundamental-primitive-in-stream-processing-oreilly-media-2018-link-accessed-15-aug-2018), both by Jay Kreps, along with [[6]](#gray-jim-queues-are-databases-arxiv-preprint-cs0701158-2007) as examples of how stream systems are proving their utility as state systems.

## References
1. #### Kleppmann, Martin. Designing data-intensive applications: The big ideas behind reliable, scalable, and maintainable systems. " O'Reilly Media, Inc.", 2017
 `I particularly recommend this as a encyclopedia of data engineering concepts and practices. I would also like to credit this work as what inspired me into writing this piece.`
2. #### Abadiand, D., et al. "Aurora: A data stream management system." Proc. ACM SIGMOD. 2003.
3. #### Aggarwal, Charu C., ed. Data streams: models and algorithms. Vol. 31. Springer Science & Business Media, 2007.
4. #### Kreps, Jay. "It's Okay To Store Data In Kafka". Confluent, 2018, [Link](https://www.confluent.io/blog/okay-store-data-apache-kafka/). Accessed 14 Aug 2018.
5. #### Kreps, Jay. "Why Local State Is A Fundamental Primitive In Stream Processing". O'reilly Media, 2018, [Link](https://www.oreilly.com/ideas/why-local-state-is-a-fundamental-primitive-in-stream-processing). Accessed 15 Aug 2018.
6. #### Gray, Jim. "Queues are databases." arXiv preprint cs/0701158 (2007).
7. #### Hyde, Julian. "Data in flight." Communications of the ACM 53.1 (2010): 48-52.

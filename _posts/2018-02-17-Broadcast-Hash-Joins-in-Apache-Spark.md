---
layout: post
comments: true
title: Broadcast Hash Joins in Apache Spark
desc: A deep dive into Broadcast Hash Joins in Apache Spark SQL
author: Sujith Jay Nair
series: Apache Spark SQL
categories:
  - spark-sql
tags: apache-spark sql joins
image: /public/jointables.png
permalink: /spark/broadcast-joins
redirect_from: /spark-sql/2018/02/17/Broadcast-Hash-Joins-in-Apache-Spark/
---
![image-title-here]({{ site.baseurl }}/public/jointables.png){:class="img-responsive"}

## Introduction

This post is part of my series on Joins in Apache Spark SQL. Joins are amongst the most computationally expensive operations in Spark SQL. As a distributed SQL engine, Spark SQL implements a host of strategies to tackle the common use-cases around joins.

In this post, we will delve deep and acquaint ourselves better with the most performant of the join strategies, Broadcast Hash Join.

<!--break-->

## The 30,000-foot View
The Broadcast Hash Join (BHJ) is chosen when one of the Dataset participating in the join is known to be broadcastable. A Dataset is marked as broadcastable if its size is less than `spark.sql.autoBroadcastJoinThreshold`. We can explicitly mark a Dataset as broadcastable using broadcast hints (This would override `spark.sql.autoBroadcastJoinThreshold`; and hence could result in performance hits or OOM, if the Dataset is too large). In either case, it is broadcast to every executor machine.

Once the broadcasted Dataset is available on an executor machine, it is joined with each partition of the other Dataset. That is, for the values of the join columns for each row (in each partition) of the other Dataset, the corresponding row is fetched from the broadcasted Dataset and the join is performed.

## Let's Dive
An example would be in order to understand the nuances of Broadcast Hash Join. What better example than the 'Hello World!'' of SQL: _Employee_ and _Department_ tables. Our _Employee_ table has _id_, _name_, and _did_ columns; _Department_ table has _id_, and _name_ as columns. You know the drill; I will not bother to draw out the tables.

In Spark REPL, you can create the tables, and initiate a join on the tables as shown below:

{% gist 6f1d012fe221e7b888f6246896af6bff Initialise.md %}

As the action in the last command triggers the lazy evaluation, you will see Spark make a flurry of transformations on the data. We are interested in the bit where the join magic happens. Since the default value for `spark.sql.autoBroadcastJoinThreshold` is 10M and the size of our datasets are miniscule, BHJ is chosen as the join strategy even without us providing any hints.

The broadcasted object is of type `HashedRelation`: either a `LongHashedRelation` (when the join key is a Long or an Int) or an `UnsafeHashedRelation`(in other cases, such as a String or a Float). The `HashedRelation` subtypes are backed by either a `LongToUnsafeRowMap` or a `BytesToBytesMap`, respectively. In our case, since our join column is of String type, a `UnsafeHashedRelation` is selected.

The broadcast object is physically sent over to the executor machines using `TorrentBroadcast`, which is a BitTorrent-like implementation of `org.apache.spark.broadcast.Broadcast`.

The broadcasted object, once available at the executors, is processed by the following generated code where the actual join takes place. I have annotated the code with relevant comments. 

The important point to notice, in our case, is since both our tables are broadcastable (< 10M), _Department_ is chosen since it has a smaller estimated physical size. The section on Caveats has an item (item #3) which points to a related case where broadcast hints are explicitly mentioned against both sides. The handling remains the same.

{% gist 6f1d012fe221e7b888f6246896af6bff BroadcastHashJoin.md %}



## Caveats
Broadcast Hash Join is performed only under certain circumstances, due to limitations of broadcasting complete datasets. One of the condition is, of course, the configuration `spark.sql.autoBroadcastJoinThreshold` (which, as we know, can be overriden at one's own risk). In addition, we have the following caveats:

1. BHJ is not supported for full outer join.
2. For right outer join, Spark can only broadcast the left side. For left outer, left semi, left anti and the internal join type ExistenceJoin, Spark can only broadcast the right side.
3. If both sides have broadcast hints (only when the join type is inner-like join), the side with a smaller estimated physical size will be broadcast.

All of these stand as of Spark 2.2.0.


## You want more?
A reasonable way to understand the expected behaviour of Broadcast Hash Join is to peruse the test cases against it. You can find them [here](https://github.com/apache/spark/blob/branch-2.2/sql/core/src/test/scala/org/apache/spark/sql/execution/joins/BroadcastJoinSuite.scala). Also, check out this [talk](https://databricks.com/session/optimizing-apache-spark-sql-joins) on optimizing Spark SQL joins.

Upcoming posts in this series will explore Shuffle Hash Joins, Broadcast Nested Loop Joins and others. Tune in for them. Please leave a comment for suggestions, opinions, or just to say hello. Until next time!

P.S. A thank you to [angriestprogrammer](http://angriestprogrammer.com/) for the strip at the start of this post. The original strip can be found [here](http://angriestprogrammer.com/comic/sql_vaudeville).
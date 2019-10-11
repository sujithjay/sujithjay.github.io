---
layout: "post"
title: "Prefer Unions over Or in Spark Joins"
date: "2019-10-11 11:11"
desc: Work-Around to using Or in a Spark SQL Join Clauses
author: Sujith Jay Nair
series: Apache Spark SQL
categories:
  - spark-sql
tags: apache-spark sql joins
permalink: /spark/or-within-joins
---
A common pattern in Spark workloads is the use of an `or` operator as part of a`join`.  An example of this goes as follows:
```scala
     val resultDF = dataframe
      .join(anotherDataframe, $"cID" === $"customerID" || $"cID" === $"contactID", "left")
```

This looks straight-forward. The use of an `or` within the join makes its semantics easy to understand.  However, we should be aware of the pitfalls of such an approach.

The declarative SQL above is resolved within Spark into a physical plan which determines how this particular query gets executed. To view the query plan for the computation, we could do:

```scala
resultDF.explain()
resultDF.explain(true) /*pass true if you are interested in the logical plan of the query as well*/
```

For the purpose of our discussion we will stick to just the physical plan. For a more detailed understanding of query plans within Spark, I would recommend reading: [Deep Dive into Spark SQL’s Catalyst Optimizer](https://databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html).

In the physical plan of a join operation, Spark identifies the strategy it will use to perform the join. The most common types of join strategies are (more can be found [here](https://github.com/apache/spark/blob/master/sql/core/src/main/scala/org/apache/spark/sql/execution/SparkStrategies.scala)):
- [Broadcast Join](https://sujithjay.com/spark/broadcast-joins)
- [Shuffle Hash Join](https://sujithjay.com/spark/shuffle-hash-sort-merge-joins)
- [Sort Merge Join](https://sujithjay.com/spark/shuffle-hash-sort-merge-joins)
- **BroadcastNestedLoopJoin**

I have listed the four strategies above in the order of decreasing performance. In all cases, you do not want your joins to be resolved into a `BroadcastNestedLoopJoin` because it is just a fancy name for using nested for-loops to join your data-frames.

We now have enough background to understand the drawback of  an `or` in a join clause. We will assume the data-frames in our example are of considerable size (:big-data:). Analyzing its physical plan, you will see something similar to this:

```
== Physical Plan ==
BroadcastNestedLoopJoin BuildRight, LeftOuter, ((cID#8 = customerID#23) || (cID#8 = contactID#24))
:- *(1) Project [_1#4 AS cID#8, _2#5 AS c2#9, _3#6 AS c3#10]
:  +- *(1) SerializeFromObject [assertnotnull(input[0, scala.Tuple3, true])._1 AS _1#4, assertnotnull(input[0, scala.Tuple3, true])._2 AS _2#5, assertnotnull(input[0, scala.Tuple3, true])._3 AS _3#6]
:     +- Scan[obj#3]
+- BroadcastExchange IdentityBroadcastMode
   +- *(2) Project [_1#18 AS c1#22, _2#19 AS customerID#23, _3#20 AS contactID#24]
      +- *(2) SerializeFromObject [assertnotnull(input[0, scala.Tuple3, true])._1 AS _1#18, assertnotnull(input[0, scala.Tuple3, true])._2 AS _2#19, assertnotnull(input[0, scala.Tuple3, true])._3 AS _3#20]
         +- Scan[obj#17]
```

For many large workloads, a query plan involving a `BroadcastNestedLoopJoin` will result in an run-time exception similar to : `SparkException: Cannot broadcast the table that is larger than 8GB: 10 GB`

So, how do we work-around this? High-school boolean algebra to the rescue! Remember an `or` over two sets result in their union set. We can rewrite our example as follows:

```scala
val resultPart1 = dataframe.join(anotherDataframe, $"cID" === $"customerID", "left")
val resultPart2 = dataframe.join(anotherDataframe, $"cID" === $"contactID", "left")

val resultDF = resultPart1.unionByName(resultPart2)
```

This produces the following physical plan:

```
== Physical Plan ==
Union
:- SortMergeJoin [cID#8], [customerID#23], LeftOuter
:  :- *(2) Sort [cID#8 ASC NULLS FIRST], false, 0
:  :  +- Exchange hashpartitioning(cID#8, 200)
:  :     +- *(1) Project [_1#4 AS cID#8, _2#5 AS c2#9, _3#6 AS c3#10]
:  :        +- *(1) SerializeFromObject [assertnotnull(input[0, scala.Tuple3, true])._1 AS _1#4, assertnotnull(input[0, scala.Tuple3, true])._2 AS _2#5, assertnotnull(input[0, scala.Tuple3, true])._3 AS _3#6]
:  :           +- Scan[obj#3]
:  +- *(4) Sort [customerID#23 ASC NULLS FIRST], false, 0
:     +- Exchange hashpartitioning(customerID#23, 200)
:        +- *(3) Project [_1#18 AS c1#22, _2#19 AS customerID#23, _3#20 AS contactID#24]
:           +- *(3) SerializeFromObject [assertnotnull(input[0, scala.Tuple3, true])._1 AS _1#18, assertnotnull(input[0, scala.Tuple3, true])._2 AS _2#19, assertnotnull(input[0, scala.Tuple3, true])._3 AS _3#20]
:              +- Scan[obj#17]
+- SortMergeJoin [cID#8], [contactID#24], LeftOuter
   :- *(6) Sort [cID#8 ASC NULLS FIRST], false, 0
   :  +- ReusedExchange [cID#8, c2#9, c3#10], Exchange hashpartitioning(cID#8, 200)
   +- *(8) Sort [contactID#24 ASC NULLS FIRST], false, 0
      +- Exchange hashpartitioning(contactID#24, 200)
         +- *(7) Project [_1#18 AS c1#22, _2#19 AS customerID#23, _3#20 AS contactID#24]
            +- *(7) SerializeFromObject [assertnotnull(input[0, scala.Tuple3, true])._1 AS _1#18, assertnotnull(input[0, scala.Tuple3, true])._2 AS _2#19, assertnotnull(input[0, scala.Tuple3, true])._3 AS _3#20]
               +- Scan[obj#17]
```

As we see, the dreaded `BroadcastNestedLoopJoin` has been replaced by two `SortMergeJoins`, which has much better performance guarantees.

Also, it is important to understand why `union` is an efficient operation to be embraced every time we can use it. Union causes zero shuffling of data across executors; it is just a bookkeeping change for Spark.

I will leave you with a complete reproducible example so you can try this out in your notebook:

{% gist 097b80f7799d5d8389d1df650df377eb UnionOverOr.md %}

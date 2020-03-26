---
layout: "post"
title: "Filling Missing Data"
date: "2020-03-25 11:11"
desc: Changes to Behaviour of Missing Data Fill in Apache Spark v2.4.5
comments: true
author: Sujith Jay Nair
series: Apache Spark
categories:
  - spark
tags: apache-spark
permalink: /spark/fill
---
A recent exercise I undertook of upgrading Apache Spark for some workloads from *v2.4.3* to *v2.4.5* surfaced a number of run-time errors of the form:

```
org.apache.spark.sql.AnalysisException: Cannot resolve column name "name" among (id, place);
  at org.apache.spark.sql.Dataset$$anonfun$resolve$1.apply(Dataset.scala:223)
  at org.apache.spark.sql.Dataset$$anonfun$resolve$1.apply(Dataset.scala:223)
  at scala.Option.getOrElse(Option.scala:121)
  at org.apache.spark.sql.Dataset.resolve(Dataset.scala:222)
  at org.apache.spark.sql.Dataset.col(Dataset.scala:1274)
  at org.apache.spark.sql.DataFrameNaFunctions$$anonfun$toAttributes$2.apply(DataFrameNaFunctions.scala:475)
```

A little poking-around showed this error occurred for transformations with a similar general shape. The following is a [minimal example](https://stackoverflow.com/help/minimal-reproducible-example) to recreate it:
```scala
val df = Seq(
  ("1", "Berlin"),
  ("2", "Bombay")
  ).toDF("id", "place")

df.na.fill("empty",Seq("id", "place", "name"))
```

This looks wrong, but apparently works fine in *v2.4.3* 😲. A transformation which attempts to fill in a missing value for a column which does not exist should raise an error: *v2.4.5* does that.

<!--break-->

### Deep Dive
So, what changed? A review of the [changelog for *v2.4.5*](https://issues.apache.org/jira/secure/ReleaseNote.jspa?projectId=12315420&version=12346042) shows a number of changes touching the functionality for working with missing data in DataFrames. The relevant change here is [SPARK-29890](https://issues.apache.org/jira/browse/SPARK-29890).

[SPARK-29890](https://issues.apache.org/jira/browse/SPARK-29890) addresses the issue of *DataFrameNaFunctions.fill* not handling duplicate columns when column names are not specified. But it addresses our issue as well as a side-effect. A part of the associated pull-request is presented below: the first gist is the [*v2.4.3*](https://github.com/apache/spark/blob/c3e32bf06c35ba2580d46150923abfa795b4446a/sql/core/src/main/scala/org/apache/spark/sql/DataFrameNaFunctions.scala#L472-L508) version of a private method called *fillValue*, and the next gist, the [*v2.4.5*](https://github.com/apache/spark/blob/cee4ecbb16917fa85f02c635925e2687400aa56b/sql/core/src/main/scala/org/apache/spark/sql/DataFrameNaFunctions.scala#L501-L536) version. *fillValue* is the underlying method for every overloaded version of *DataFrameNaFunctions.fill*.

{% gist 17cf930ae9b9b135dc95457f5b8807a7 2.4.3.scala %}

{% gist 17cf930ae9b9b135dc95457f5b8807a7 2.4.5.scala %}

The crux of the change relevant to us is in the signature of *fillValue*.

*v2.4.3*  |  *v2.4.5*
--|--
`def fillValue[T](value: T, cols: Seq[String]): DataFrame`   |  `def fillValue[T](value: T, cols: Seq[Attribute]): DataFrame`  


To solve the original issue the PR addresses (i.e, handling duplicate columns when column names are not specified), the comparison of *columns* was switched from the earlier

`cols.exists(col => columnEquals(f.name, col))` to `cols.exists(_.semanticEquals(col))`

This necessitated a change in the signature of *fillValue*. However, to convert *cols* required by *fillValue* from *Seq[String]* to *Seq[Attribute]*, it is passed to a method [*toAttributes*](https://github.com/apache/spark/blob/cee4ecbb16917fa85f02c635925e2687400aa56b/sql/core/src/main/scala/org/apache/spark/sql/DataFrameNaFunctions.scala#L474-L478):


```scala
private def toAttributes(cols: Seq[String]): Seq[Attribute] = {
    cols.map(name => df.col(name).expr).collect {
      case a: Attribute => a
    }
  }
```

This method, as a side-effect, ensures the columns passed to *DataFrameNaFunctions.fill* exists in the dataframe.

In short, this change in behaviour in *DataFrameNaFunctions.fill* causes tiny pains & an improved correctness to *fill* transformations.

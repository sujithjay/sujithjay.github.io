---
layout: post
comments: true
title: "Understanding Apache Spark on YARN"
desc: understanding Apache Spark on YARN
author: Sujith Jay Nair
tags: apache-spark yarn
image: /public/Spark-Cluster-Overview.png
permalink: /2018/07/24/Understanding-Apache-Spark-on-YARN/
date: "2018-07-24 11:11"
---
**TL; DR**
Apache Spark is a lot to digest; running it on YARN even more so. I hope this post helps a bit.

<!--break-->
## Introduction
This article is a introductory reference to understanding Apache Spark on YARN. Since our data platform at [Logistimo](http://logistimo.com) runs on this infrastructure, it is imperative you (my fellow engineer) have an understanding about it before you can contribute to it. This article assumes basic familiarity with Apache Spark concepts, and will not linger on discussing them.

## Overview on YARN
YARN is a generic resource-management framework for distributed workloads; in other words, a cluster-level operating system. Although part of the Hadoop ecosystem, YARN can support a lot of varied compute-frameworks (such as Tez, and Spark) in addition to MapReduce.

The central theme of YARN is the division of resource-management functionalities into a global ResourceManager (RM) and per-application ApplicationMaster (AM). An application is the unit of scheduling on a YARN cluster; it is either a single job or a DAG of jobs (jobs here could mean a Spark job, an Hive query or any similar constructs).

{% include image-caption.html file="/public/Yarn-Architecture.gif" description="Fig. 1: YARN Architecture [1]" %}

The ResourceManager and the NodeManager form the data-computation framework. The ResourceManager is the ultimate authority that arbitrates resources among all the applications in the system. The NodeManager is the per-machine agent who is responsible for containers, monitoring their resource usage (cpu, memory, disk, network) and reporting the same to the ResourceManager/Scheduler [1].

The per-application ApplicationMaster is, in effect, a framework specific library and is tasked with negotiating resources from the ResourceManager and working with the NodeManager(s) to execute and monitor the tasks [1].


## Glossary
The first hurdle in understanding a Spark workload on YARN is understanding the various terminology associated with YARN and Spark, and see how they connect with each other. I will introduce and define the vocabulary below:

#### Application
A Spark application is the highest-level unit of computation in Spark. A Spark application can be used for a single batch job, an interactive session with multiple jobs, or a long-lived server continually satisfying requests. A Spark job can consist of more than just a single map and reduce. On the other hand, a YARN application is the unit of scheduling and resource-allocation. There is a one-to-one mapping between these two terms in case of a Spark workload on YARN; i.e, a Spark application submitted to YARN translates into a YARN application.

#### Spark Driver
To understand the driver, let us divorce ourselves from YARN for a moment, since the notion of driver is universal across Spark deployments irrespective of the cluster manager used.

{% include image-caption.html file="/public/Spark-Cluster-Overview.png" description="Fig. 2: Spark Cluster Overview [4]" %}

Spark applications are coordinated by the SparkContext (or SparkSession) object in the main program, which is called the Driver. In plain words, the code initialising SparkContext is your driver. The driver process manages the job flow and schedules tasks and is available the entire time the application is running (i.e, the driver program must listen for and accept incoming connections from its executors throughout its lifetime. As such, the driver program must be network addressable from the worker nodes) [4].

#### YARN Client
A program which submits an application to YARN is called a YARN client, as shown in the figure in the [YARN](#overview-on-yarn) section. Simple enough.

The notion of driver and how it relates to the concept of client is important to understanding Spark interactions with YARN. In particular, the location of the driver w.r.t the client & the ApplicationMaster defines the deployment mode in which a Spark application runs: YARN client mode or YARN cluster mode.

*Client mode:*
The driver program, in this mode, runs on the YARN client. Thus, the driver is not managed as part of the YARN cluster.

Take note that, since the driver is part of the client and, as mentioned above in the [Spark Driver](#spark-driver) section, the driver program must listen for and accept incoming connections from its executors throughout its lifetime, the client cannot exit till application completion.

{% include image-caption.html file="http://blog.cloudera.com/wp-content/uploads/2014/05/spark-yarn-f22.png" description="Fig. 3: YARN Client Mode [2]" %}


*Cluster mode:*
The driver program, in this mode, runs on the ApplicationMaster, which itself runs in a container on the YARN cluster. The YARN client just pulls status from the ApplicationMaster. In this case, the client could exit after application submission.

{% include image-caption.html file="http://blog.cloudera.com/wp-content/uploads/2014/05/spark-yarn-f31.png" description="Fig. 4: YARN Cluster Mode [2]" %}

#### Executor and Container
The first fact to understand is: each Spark executor runs as a YARN container [2]. This and the fact that Spark executors for an application are fixed, and so are the resources allotted to each executor, a Spark application takes up resources for its entire duration. This is in contrast with a MapReduce application which constantly returns resources at the end of each task, and is again allotted at the start of the next task.

Also, since each Spark executor runs in a YARN container, YARN & Spark configurations have a slight interference effect. I will illustrate this in the next segment.

## Configuration and Resource Tuning
With our vocabulary and concepts set, let us shift focus to the knobs & dials we have to tune to get Spark running on YARN. We will be addressing only a few important configurations (both Spark and YARN), and the relations between them.

We will first focus on some YARN configurations, and understand their implications, independent of Spark.
- *yarn.nodemanager.resource.memory-mb*

  It is the amount of physical memory, in MB, that can be allocated for containers in a node. This value has to be lower than the memory available on the node.
  ```
  <name>yarn.nodemanager.resource.memory-mb</name>
  <value>16384</value> <!-- 16 GB -->
  ```

- *yarn.scheduler.minimum-allocation-mb*

  It is the minimum allocation for every container request at the ResourceManager, in MBs.  In other words, the ResourceManager can allocate containers only in increments of this value. Thus, this provides guidance on how to split node resources into containers. Memory requests lower than this will throw a InvalidResourceRequestException.
  ```
  <name>yarn.scheduler.minimum-allocation-mb</name>
  <value>2048</value><!-- 2 GB -->
  ```
- *yarn.scheduler.maximum-allocation-mb*

  The maximum allocation for every container request at the ResourceManager, in MBs. Memory requests higher than this will throw a InvalidResourceRequestException.
  ```
  <name>yarn.scheduler.maximum-allocation-mb</name>
  <value>8192</value><!-- 8 GB -->
  ```

Thus, in summary, the above configurations mean that the ResourceManager can only allocate memory to containers in increments of *yarn.scheduler.minimum-allocation-mb* and not exceed *yarn.scheduler.maximum-allocation-mb*, and it should not be more than the total allocated memory of the node, as defined by *yarn.nodemanager.resource.memory-mb*. We will refer to this in further discussions as the YARN Boxed Memory axiom (just a fancy name to ease the discussions). A similar axiom can be stated for cores as well, although we will not be doing so in this article.

Let us now move on to certain Spark configurations. In particular, we will look at these configurations from the viewpoint of running a Spark job within YARN.

- *spark.executor.memory*

  Since every executor runs as a YARN container, it is bound by the Boxed Memory axiom. However, a source of confusion among developers is that the executors will use a memory allocation equal to *spark.executor.memory*. In essence, the memory request is equal to the sum of *spark.executor.memory* + *spark.executor.memoryOverhead*. Thus, it is this value which is bound by the Boxed Memory axiom.

- *spark.driver.memory*

  In cluster deployment mode, since the driver runs in the ApplicationMaster which in turn is managed by YARN, this property decides the memory available to the ApplicationMaster, and it is bound by the Boxed Memory axiom. But as in the case of *spark.executor.memory*, the actual value which is bound is *spark.driver.memory* + *spark.driver.memoryOverhead*.

  In case of client deployment mode, the driver memory is independent of YARN and the Boxed Memory axiom is not applicable to it. In turn, it is the value *spark.yarn.am.memory* + *spark.yarn.am.memoryOverhead* which is bound by the Boxed Memory axiom.

I hope this article serves as a concise compilation of common causes of confusions in using Apache Spark on YARN. More details can be found in the references below. Please leave a comment for suggestions, opinions, or just to say hello. Until next time!

## References
[1] "Apache Hadoop 2.9.1 – Apache Hadoop YARN". hadoop.apache.org, 2018, Available at: [Link](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html). Accessed 23 July 2018.

[2] Ryza, Sandy. "Apache Spark Resource Management And YARN App Models - Cloudera Engineering Blog". Cloudera Engineering Blog, 2018, Available at: [Link](https://blog.cloudera.com/blog/2014/05/apache-spark-resource-management-and-yarn-app-models/). Accessed 22 July 2018.

[3] "Configuration - Spark 2.3.0 Documentation". spark.apache.org, 2018, Available at: [Link](https://spark.apache.org/docs/2.3.0/configuration.html). Accessed 22 July 2018.

[4] "Cluster Mode Overview - Spark 2.3.0 Documentation". spark.apache.org, 2018, Available at: [Link](https://spark.apache.org/docs/2.3.0/cluster-overview.html). Accessed 23 July 2018.

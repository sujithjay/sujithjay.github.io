---
layout: post
comments: true
title: "Notes on Mesos"
desc: An introductory reference to Apache Mesos
author: Sujith Jay Nair
tags: mesos
permalink: /mesos
image: /public/mesos/ClusterKernel.png
date: "2019-06-06 11:11"
---
![image-title-here]({{ site.baseurl }}/public/mesos/ClusterKernel.png){:class="img-responsive"}
Mesos is a framework I have had recent acquaintance with. The only resource management framework I have known prior is Hadoop [YARN]((/spark/with-yarn)). These are my notes as I try to make friends with Mesos (he's a good boy!), and revisit the concept of cluster resource-management in general.

<!--break-->
## Overview
A proper place to start this piece would be to roughly define the distributed systems' anatomy Mesos caters to.

{% include image-caption.html file="/public/mesos/DistributedSystems.png" description="Fig. 1: Anatomy of Distributed Systems" %}

This class of distributed systems has one (or multiple) co-ordinator(s)[^1] co-ordinating execution of a program across a bunch of workers distributed within a cluster of machines. The co-ordinators have a set of desirable properties:
- Distributed
- Fault-tolerant
- Elastic

*Distributed* refers to the simultaneous execution of program tasks[^2] across multiple machines. This is nothing short of what is expected from a distributed system.

*Fault-tolerance* is the capability of the system to handle failures of a subset of workers in the cluster, and the ability to reschedule tasks away from those failing workers.

*Elasticity* is the capability of the system to optimise performance and resource utilisation in a cluster, given simultaneous workloads competing for resources. It could be considered the defining characteristic which differentiates cluster resource-management paradigms & systems; say, Mesos from [YARN]((/spark/with-yarn)), or Kubernetes. The next section explores elasticity in some depth.

## Elasticity
> An elastic system is able to adapt to workload changes by provisioning and de-provisioning resources in an autonomic manner, such that at each point in time the available resources match the current demand as closely as possible. [^3]

Elasticity, as defined above, is a scheduling problem. There are multiple approaches to having elasticity, and based on these, resource-management systems can be bucketed into the three categories. These categories, based on scheduler architectures, are borrowed from the Omega paper. [^4] [^5]

{% include image-caption.html file="/public/mesos/SchedulerArchitecture.png" description="Fig. 2: Prevalent Scheduler Architectures" %}

Mesos belongs to the second category: *two-level scheduling*. The documentation for Mesos alludes to this fact by calling Mesos *a level of indirection for scheduler frameworks*. [^6]

{% include image-caption.html file="/public/mesos/Indirection.png" description="Fig. 3: Mesos, a level of indirection" %}

## Two-Level Scheduling?
The *two-level* scheduling provided by Mesos can be described thus: A scheduler exists at the framework-level & another exists as part of Mesos (a part of the Mesos *master* ). In a cluster with heterogenous workloads, multiple frameworks function together with a single Mesos scheduler.

{% include image-caption.html file="/public/mesos/Interactions.png" description="Fig. 4: Mesos Scheduler Interactions" %}
<div></div>
The Mesos master dynamically partitions a cluster, allocating resources to the different framework schedulers. Resources are distributed to the frameworks in the form of offers, which contain only “available” resources – ones that are currently unused. [^7] An example of a resource offer is shown below.

{% include image-caption.html file="/public/mesos/Offer.png" description="Fig. 5: Mesos Resource Offer" %}


The events in the diagram are described as follows: [^8]
1. Agent 1 reports to the master that it has 4 CPUs and 4 GB of memory free. The master then invokes the allocation policy module, which tells it that framework 1 should be offered all available resources.
2. The master sends a resource offer describing what is available on agent 1 to framework 1.
3. The framework’s scheduler replies to the master with information about two tasks to run on the agent, using <2 CPUs, 1 GB RAM> for the first task, and <1 CPUs, 2 GB RAM> for the second task.
4. Finally, the master sends the tasks to the agent, which allocates appropriate resources to the framework’s executor, which in turn launches the two tasks (depicted with dotted-line borders in the figure). Because 1 CPU and 1 GB of RAM are still unallocated, the allocation module may now offer them to framework 2.


During offers, the master avoids conflicts by only offering a given resource to one framework at a time, and attempts to achieve dominant resource fairness ([DRF](https://cs.stanford.edu/~matei/papers/2011/nsdi_drf.pdf)) by choosing the order and the sizes of its offers. Because only one framework is examining a resource at a time, it effectively holds a lock on that resource for the duration of a scheduling decision. In other words, concurrency control is pessimistic.[^9]

## A note on YARN
To contrast the above discussion with YARN, resource requests from per-job application masters are sent to a single global scheduler in the resource master, which allocates resources on various machines, subject to application-specified constraints. The application masters provide job-management services, and no scheduling. So YARN is effectively a monolithic scheduler architecture.

## Notes
[^1]: In resource management systems literature, the term *co-ordinator* is used interchangeably with *scheduler*.
[^2]: Tasks here refers to sub-units of the program which are independently schedulable.
[^3]:  Herbst, Nikolas; Samuel Kounev; Ralf Reussner (2013). "[Elasticity in Cloud Computing: What It Is, and What It Is Not](https://sdqweb.ipd.kit.edu/publications/pdfs/HeKoRe2013-ICAC-Elasticity.pdf)" (PDF). Proceedings of the 10th International Conference on Autonomic Computing (ICAC 2013), San Jose, CA, June 24–28.
[^4]: The [Omega](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/41684.pdf) system is considered one of the precusors to Kubernetes. There is a fine [ACM Queue](https://queue.acm.org/detail.cfm?id=2898444) article describing this history. There are also some amazing twitter threads by [Brian Grant](https://twitter.com/bgrant0607) giving insights into the evolution from Omega to K8s, such as [this](https://twitter.com/bgrant0607/status/1102292629465661440) and [this](https://twitter.com/bgrant0607/status/1111469578603778048).
[^5]: Thanks to [Alessandro Andrioni](https://twitter.com/metamatema) for pointing me to it.
[^6]: A scheduler framework is the distributed system running on top of Mesos, eg. Spark, Storm, Hadoop. In other words, framework &asymp; distributed system.
[^7]: This is referred to as *choice of resources* in the Omega paper.
[^8]: Taken from the official Mesos [documentation](http://mesos.apache.org/documentation/latest/architecture/).
[^9]: Termed as *pessimistic interference* in the Omega paper.
[^10]: The title illustration is from [Apache Mesos as an SDK for Building Distributed Frameworks](https://www.slideshare.net/pacoid/strata-sc-2014-apache-mesos-as-an-sdk-for-building-distributed-frameworks/25) by Paco Nathan.

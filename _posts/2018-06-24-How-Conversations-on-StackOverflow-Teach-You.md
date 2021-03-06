---
layout: "post"
comments: true
title: "How Conversations on StackOverflow Teach You"
desc: An exhortation to the engineering community to share more
author: Sujith Jay Nair
tags: conversations learning culture
date: "2018-06-24 11:11"
image: /public/ourjob.png
permalink: /stackoverflow-conversations
redirect_from: /2018/06/24/How-Conversations-on-StackOverflow-Teach-You/
---
![image-title-here]({{ site.baseurl }}/public/ourjob.png){:class="img-responsive"}

**Note**: This post has some concepts on Scala collections. Do not worry if you have little interest in Scala; the point I am trying to convey has significance beyond my choice of language. This is an exhortation to the engineering community at large to share our learnings more.

<!--break-->
I was working on an open-source ticket recently where I received the following review comment:

*"IndexedSeq[_] (being backed by scala.collection.Vector) are horrifically inefficient, and we should replace that with a better IndexedSeq that's just backed by an Array."*

The reviewer here is referring to a Collection class '*immutable.IndexedSeq*'. For those new to Scala, _IndexedSeq_ is an interface which provides an Java _Array_-like API. And like any Java interface, it states this contract without constraints on the run-time of its operations.
 
In other words, it defines methods like '_head()_', '_next()_', '_hasNext()_' etc, but says nothing on how quick the implementation of these need to be. They could range from _O(1)_ to _O(N)_ in the various classes implementing the interface. The default implementation is backed by a _Vector_ which uses a tree-like structure to perform these operations. So, definitely not _O(1)_. And that is the point the reviewer is trying to make.

I was not aware of the nuances of IndexedSeq and set about in learning more about how it is implemented, and to find an _Array_-backed implementation. Although I learnt more and more about how _IndexedSeq_ work, I was at a loss on how to implement an _Array_-backed implementation without copying the entire implementing class from _scala.collections_ and making the relevant changes.

As a resort of the final sorts, I posted a question on StackOverflow. A few people responded via comments and answers; each offering a different world-view. But, what amazed me as I read and responded to their comments and answers is how little I knew on the topic and on some allied topics; how an exercise which lasted less than a few hours (between me posting the question and the final acceptance of an appropriate answer) can be so enriching.

But if we think of it, any conversation on matters we know little about (and would like to know more about) with a community which knows more will turn out to be enriching. Be it StackOverflow, Hacker News, Twitter, Reddit or any other forum. The best use of any such forum is when you cease to be just a consumer of information; but rather indulge in conversations. Tell them what you know; and let them teach you more.

Which brings me to my particular pet peeve. Why do we engineers not use the immediate community we have? Our teams are communities in themselves; each knowing something more about something than the other. How often do we share with each other things we learnt during that day? In this week? In this month? During last sprint or release? You must have learnt something! Something which surprised you; something which brought out an 'Oh!'. Why would you not share it with everyone around you? Walk up to somebody today, and say 'Did you know that ...?'. And for the greater good, share it with the wider world as well. We would all like to know.

P.S. For those of you interested in the SO post and the original open-source ticket (which is still a work in progress), check out the links below:
1. [StackOverflow Post](https://stackoverflow.com/questions/49256315/how-to-implement-an-immutable-indexedseq-in-scala-backed-by-an-array)
2. [ScalaNLP/Breeze PR](https://github.com/scalanlp/breeze/pull/695)

Also, a thank you to the awesome team at [CommitStrip](http://www.commitstrip.com/en/) for producing great comic strips, such as the one at the start of this post. The original strip can be found [here](http://www.commitstrip.com/en/2018/04/24/thats-our-job/).

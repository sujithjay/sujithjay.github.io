---
layout: "post"
title: " Defining a Platform is Hard"
date: "2021-06-07 11:11"
desc: On defining software engineering platforms
comments: true
author: Sujith Jay Nair
tags: platforms product management
permalink: /internal-platforms
---
Engineering platforms are a vague concept. Software organisations across the board agree on the need to 'platformise' layers of their stack, but struggle to define the term. The question 'what is a platform' is met with a response 'something similar to AWS, but at a higher layer of the company software stack'. [I have previously argued why this is a false analogy](/not-aws).

I think we can agree that there is a dichotomy in engineering platforms: public platforms and internal (or private) platforms. AWS S3, Snowflake, and others are examples of public platforms, while internal platforms are engineering platforms built within a software organisation to serve internal users.

My approach here is to start with a reasonable definition of platforms in general and arrive at a reasonable definition for internal platforms. This was not as straightforward as it sounds. The minimum we can gain from such an exercise is the ability to identify internal platforms in the wild (_"Is X an internal platform?"_ ). [^1]

So, what is a platform?

The Bill Gates' definition of a platform goes like this:
> <blockquoted> A platform is when the economic value to everybody that uses it, exceeds the value of the company that creates the platform.

This is a succinct description but the trouble with it is that it is a post-hoc definition: it can only identify a platform after it has started accruing value for the creators and users. Like a lagging indicator, this is useful in a limited sense. But as you might have noticed, the question we look to answer is also post-hoc (_"Is X an internal platform?"_ ). Thus the Gates' definition can be our initial template for a definition of internal platforms.

How can the above be paraphrased for internal platforms? Assuming that a company can be seen as a set of coordinating units or teams, we might say, _'an internal platform is when the economic value to every team that uses it, exceeds the cost of the platform'_.

So, by this definition, in a simple case where there is a single 'software platform' used by \\(m\\) product teams, each of which has \\(n\\) customers with a uniform revenue of \\($R\\) per customer, the cumulative value
\\(n * m * R\\) should greatly exceed \\(C\\), the cost-to-company of the platform.

This definition is almost useless. Unlike the original Gates' quote, it does not help us identify platforms from non-platforms. Everything within a company, from a set of APIs to a team of accountants in the back-office [^2], could pass off as a platform under this definition. Let us refine this further using what we know about internal platforms, and their distinct attributes.

### Cost
Before we turn to the attributes of an internal platform, a brief note on cost. As we have already seen in the above attempted definitions, the terms 'cost' and 'value' are central to the formulations. I would like to expand a bit on the term 'cost' in the context of internal platforms.

The term 'cost' includes the dollar cost of operating the platform as well as a measure of the effort required by users to use the internal platform. How do we measure the effort required by users to use the internal platform? I have previously talked about how [abstractions provided by internal platforms have to cater to an entire spectrum of users within the company, and not the median users of the system](/not-aws#1-the-middle-ground). A measurement of the effort required by users to use the internal platform is essentially a weighted average of the usability index of the platform for every user persona the platform caters to.

### Attributes of an Internal Platform
So what desirable properties do internal platforms have?

#### Scalable
Platforms inherently have to be scalable.

A typical engineering definition of scalability would be along the dimensions of reliability and fault-tolerance; the system should be reliable and fault-tolerant as usage of the system increases. But for a platform, we need to consider cost scalability as well: the marginal cost of the platform should diminish as usage increases.

An illustration of the property of cost-scalability is as follows:
Consider a platform with \\(n\\) users and an operating cost of \\(C\\). Assume that when the user-count increases to \\(n+1\\), the cost increases to \\(C+ c\_{1}\\), and when the user-count increases to \\(n+1\\), the cost increases to \\(C+ c\_{1} + c\_{2}\\). For a cost-scalable platform, \\(c\_{2} \leq c\_{1}\\). [^3]

#### Lasting
A 'lasting' platform ensures that the incremental cost to the customer grows more slowly than the incremental value to the customer.

In case of public platforms, not every platform has to be lasting. [Byrne Hobart](https://diff.substack.com/p/who-amazon-grows-with/) calls (public) platforms which follow the incremental value dictum as second-derivative platforms (a first-derivative platform being one which follows the Bill Gates' definition above).

Internal platforms always have to be lasting (a.k.a. second-derivative).

#### Serendipitous
Every platform has users who use them for use-cases they were not designed for. [^4] This also implies that a platform caters to multiple sets of users (target audiences and otherwise). I call this being serendipitous.

Contrary to the other attributes, being serendipitous is an attribute of internal platforms which can be leveraged to predict where to build an internal platform. I have previously talked about how [overloaded use-cases within a platform are a good guide to learn about the unmet needs of the users](https://sujithjay.com/not-aws#2-overloaded-use-cases). This is true even in cases where a platform has not yet been built. APIs with overloaded use-cases are excellent indicators that a platform with more general abstractions should probably take its place.

There is another explanation of why no true platform [^5] will only cater to a single user persona. Internal platforms are essentially monopolies within a company for a certain value-producing activity. And [monopolies tend to commodify their adjacent in the value chain](https://www.gwern.net/Complement). If you consider the product teams or other internal users using the internal platform as the layer adjacent to the platform in the value chain of the company, it follows naturally that internal platforms should cater to a wide spectrum of users (or use-cases) which it commodifies.


### Final Take?
A definition for internal platforms in the light of these attributes could be stated as:
> An internal platform is when a scalable, serendipitous, coherent set of APIs ensures that the incremental cost to the customer grows more slowly than the incremental value to the customer.


### Footnotes
[^1]: The best-case scenario would be if we are able to leverage the definition to identify opportunities to build internal platforms (_"Does Y require a platform?"_ ).
[^2]: Although I mention the example of a back-office of accountants here (for effect), eliminating it from any definition of a platform is easy. We can differentiate the same way we differentiate any automation from a manual performance of the same task: by introducing the constraint of consistent repeatability. Humans are error-prone in performing repetitive tasks, machines are less so.
[^3]: I use number of users here as a proxy for usage. Depending on the exact service provided by the platform, usage might not be a function of number of users alone (for example, number of API calls).
[^4]: AWS S3 was famously never designed for Data Lakes, but that is one of the major use-cases for S3 nowadays.
[^5]: [No true Scotsman](https://en.wikipedia.org/wiki/No_true_Scotsman).

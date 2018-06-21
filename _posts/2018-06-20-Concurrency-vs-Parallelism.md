---
layout: "post"
comments: true
title: "Concurrency & Parallelism"
desc: This post provides a bit of a preface on the notion of concurrency, and compares it with parallelism
author: Sujith Jay Nair
tags: concurrency parallelism
date: "2018-06-20 11:11"
permalink: /2018/06/20/Concurrency-and-Parallelism/
---

Concurrency is a much-overloaded term in computer science. Every domain of literature in computer science defines its own flavour of what concurrency means to it. To add to the confusion, "Parallelism" and "Muti-programming" are purported as synonyms to concurrency. So much for our simple minds to wrap around.

The intention of this article is to provide a bit of a preface on the notion of concurrency, and compare it with parallelism. Bear with me.

<!--break-->
## Concurrency != Parallelism
Concurrency is the use of multiple threads of control to achieve a program objective. Each thread is interleaved in (execution) space & time, and the interleaving is non-deterministic. Thus, concurrent programs are non-deterministic in general. 

The programmer coerces determinism into the program using synchronisation. Concurrency does not imply parallel execution; it is possible even on a single CPU core.

Contrast that with parallelism, which is the condition where a program utilises the multiplicity of computational hardware (several CPU cores, for instance) [1]. The idea here is about computational speedup alone. It does not entail interaction among the program components, nor between the components and external agents (such as a UI component, or the database).

So where does the notion of concurrency == parallelism come from? I would like to quote [Simon Marlow](https://github.com/simonmar), co-developer of the Glasgow Haskell Compiler and author of "Parallel and Concurrent Programming in Haskell", on this:

> It’s a natural consequence of languages with side-effects: when your language has side-effects everywhere, then any time you try to do more than one thing at a time you essentially have non-determinism caused by the interleaving of the effects from each operation.  So in side-effecty languages, the only way to get parallelism is concurrency; it’s therefore not surprising that we often see the two conflated [2].

In other words, the notion of threads of control (as defined by concurrency) makes sense only in a language with side-effects. In a purely-functional language, there are no effects to observe, and the evaluation order is irrelevant[1]. Thus, parallelism can be achieved without concurrency. 

On the other hand, in languages with side-effects, parallelism becomes a subset of concurrency. Hence, for instance, concurrency is defined as follows in Java:

> A condition that exists when at least two threads are making progress. A more generalised form of parallelism that can include time-slicing as a form of virtual parallelism [3].

The understanding of this distinction, within the realm of your language of choice, is essential to develop and reason about concurrent and parallel programs. Until next time!

## References
[1] Marlow, S. (2013). Parallel and Concurrent Programming in Haskell.

[2] GHC Mutterings. (2018). Parallelism /= Concurrency. Available at: [Link](https://ghcmutterings.wordpress.com/2009/10/06/parallelism-concurrency/) [Accessed 15 Jun. 2018].

[3] Oracle Docs. (2018). Defining Multithreading Terms (Multithreaded Programming Guide). Available at: [Link](https://docs.oracle.com/cd/E19455-01/806-5257/6je9h032b/index.html) [Accessed 10 Jun. 2018].

---
layout: "post"
title: "Skew Strikes Back"
date: "2020-09-02 11:11"
desc: Skew Strikes Back - New Developments in the Theory of Join Algorithms
comments: false
author: Sujith Jay Nair
tags: notes
permalink: /notes/skew-strikes-back

---
## Introduction
> Suppose that one is given a graph with N edges, how many distinct triangles can there be in the graph?

The two conceptual ideas of the paper:
- a theoretical basis for skew based on geometry: and a family of algorithms which provide optimal ways of avoiding skew.
- to challenge the database dogma of doing 'one join at a time': there are classes of query for which any join-project plan will be slower than the optimal run-time by a polynomial factor in data size.

## History of Join Processing
The major approaches to join processing are: _using structural information of the query_ and _using cardinality information_; the AGM bounds bring together both sets of information. [^1]

### Structural Approaches
- Algorithms rely on a structural property of a query such as acyclicity or bounded width to process joins in polynomial time.
  - For example, in acyclic query (acyclic iff it has a join tree. GYO-reduction), Yannakakis algorithm runs in ~linear time in input + output size. [^2]
- Width of a query (qw) is a measure of how far a query is from being acyclic. Acyclic queries have qw=1.
  - A family of algorithms exist which state that if the width is bounded by a constant, the query is tractable (a polynomial-time algorithm exists which can evaluate it).

### Cardinality-based Approaches
> (Structural) decomposition methods focus “only” on structural features, while they completely disregard “quantitative” aspects of the query, that may dramatically affect the query-evaluation time.

- The run time of structural approaches is \\({O(N^{w+1} log N)}\\), where _N_ is the input size and _w_ is the width measure.
- Commercial databases place little emphasis on the structural property of the queries and tremendous emphasis on the cardinality aspect; an example is how commercial databases treat complex multi-way joins as a series of pairwise joins. Such any join-project plans are destined to be slower than the optimal plans.

### Bridging the Gap
AGM defines a tight bound on the  output size of a join query as a function of input sizes and a finer notion of width. This bound, in turn, leads to the notion of `fractional query number` and `fractional hypertree width` (`fhw`). `fhw` is proven to be less than or equal to every other width measure. Leapfrog Triejoin is an example implementation of turning this bound into a join algorithm.

## [[Triangle Query]]


## Notes
[^1]: [Size bounds and query plans for relational joins](https://arxiv.org/abs/1711.03860).
[^2]: The standard in database theory is to measure run time of join algorithms in terms of input data, assuming the input query is fixed.

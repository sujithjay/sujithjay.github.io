---
layout: "post"
comments: true
title: "The Assumption of Normality in Time Series"
desc: This post tries to explain the use of Limit theorems in time-series analysis
author: Sujith Jay Nair
tags: statistics time-series
date: "2018-03-10 11:11"
permalink: /2018/03/10/The-Assumption-of-Normality-in-Time-Series/
---

The notion of normality is oft-encountered in statistics as an underlying assumption to many proofs and results; it is normal to assume normality (pun strongly intended; always wanted to use this one). In much statistical works, the assumption of normality, even if inaccurate, is amortized and ameliorated by the existence of Central Limit Theorem. Time-series analysis, sadly, does not enjoy this privilege. The assumption of independence, so core to the CLT and other Limit theorems, is poignantly absent in time-series'.

This post tries to explain the use of Limit theorems in time-series analysis. As my intended audience comprises computer scientists/engineers, and not statisticians, this post has a long preface on the premise of the problem.

<!--break-->
## Preface
### Limit Theorems
Limit theorems are a class of theorems in statistics governing the behaviour of sums of stochastic variables. The most widely used limit theorems are the Central Limit Theorem (CLT) and the Law of Large Numbers (LLN). Our focus in this post is on the Central Limit Theorem. CLT, in itself, is a family of theorems rather than one single theorem. But in every form, CLT forms a set of weak-convergence rules around the sum of stochastic variables. We will have a little more to say on weak-convergence in our section on [Convergence](#convergence).

In its more generic form, CLT states that the sum of any number of random variables generated in a stochastic process will be asymptotically distributed according to a small set of [attractor](https://en.wikipedia.org/wiki/Attractor) distributions. Notice that this general form of CLT makes no assumption on the independence of the variables; however, it is of scant use in this particular form.

In case of [_i.i.d_](https://en.wikipedia.org/wiki/Independent_and_identically_distributed_random_variables) (independent and identically distributed) stochastic variables with a finite variance, the attractor distribution is a normal distribution. In other words, if \\( x\_{i} \\) is a sequence of i.i.d random variables, with \\({Ex}\_{i} = \mu\\), \\(Var( x\_{i}) = \sigma^2\\), CLT states that,

$$\frac{\sqrt{n}}{\sigma}(\frac{1}{n}\sum_{i=1}^{n} x_{i} - \mu) \Rightarrow \mathcal{N}(0, 1)$$

In practice, how would you use this fact? A clichéd, yet pedagogical, example would be an experiment involving large number of coin flips. Suppose you choose a sample of _n_ coin flips and count the number of heads you get within the sample. If this exercise of choosing a sample is done over and over, the count of heads you get will follow an approximate normal distribution. As you increase the sample size _n_ asymptotically, the distribution will tend closer and closer to a normal distribution.


### Convergence
I make a short note here on convergence for completeness. The relevant types of convergence common in statistics and probability are,
* Almost surely, almost everywhere with probability one, \\(w.p.  1\\):


$$ \mathsf{\mathbf{X_n} \xrightarrow{a.s} \mathbf{X} : \mathbb{P} \{ \omega : \lim \mathbf{X_n} = \mathbf{X}\} = 1} $$

* In probability, in measure:


$$ \mathsf{\mathbf{X_n} \xrightarrow{p} \mathbf{X} : \lim\limits_{n} \mathbb{P} \{ \omega : |\mathbf{X_n} - \mathbf{X}| > \epsilon\} = 0} $$

* In distribution, weak convergence (this is the kind of convergence promised by CLT):


$$\mathsf{\mathbf{X_n} \xrightarrow{d} \mathbf{X} : \lim\limits_{n} \mathbb{P} ( \mathbf{X_n} \leq {x} ) = \mathbb{P} ( \mathbf{X} \leq {x} )} $$


Convergence _almost surely_ implies convergence _in probability_ which, in turn, implies convergence _in distribution_. Convergence _in distribution_ only implies convergence _in probability_ if the distribution is a point mass.

## Normality Assumptions in Time Series
To understand why the assumption of normality is important in modeling time-series, let us take the case of an **AR(1)** process, a linear first order [autoregressive process](https://en.wikipedia.org/wiki/Autoregressive_model). The following discussion can be extended to other common time-series structures as well. The **AR(1)** structure can be defined as:

$$\mathsf{Y_t = {\phi}Y_{t-1} + Z_t} \tag{2.1}$$

where $$\mathsf{\{Y_t\}}, t = 0, 1,.. $$ is a first order [Markov process](http://mathworld.wolfram.com/MarkovProcess.html) on sample space $$\mathbf{Y} \subseteq \mathbb{R} $$ with conditional (transition) density $$\mathsf{p(y_t \mid y_{t-1})} $$. $$\mathsf{\phi}$$ can take any _allowable_ value such that $$\mathsf{Y} \subseteq \mathbb{R} $$ when $$\mathsf{Y}_{t-1} \subseteq \mathbb{R} $$. $$\mathsf{Z_t}$$ is an _i.i.d_ sequence with mean $$\mathsf{\lambda}$$. More on this can be found at [Grunwald].

The normal **AR(1)** process with mean $$\mathsf{\mu}$$ is usually written in terms of a series of white noise variables $$\mathsf{\{E_t\}}$$:

$$\mathsf{Y_t - \mu = \phi(Y_{t-1} - \mu) + E_t} \tag{2.2}$$

where $$\mathsf{E_t \sim \mathcal{N}(0, \sigma^2)} $$ are _i.i.d_ and $$\mathsf{\mid \phi\mid < 1}$$.

The question is why would you choose to model your time-series as (2.2) over (2.1), even in the face of a lack of evidence of normal behaviour in your data. The reason is convenience.

A feature of normal AR(1) processes is that the marginal distribution is also normal. Thus,

$$\mathsf{Y_t \sim \mathcal{N}(\mu, \frac{\sigma^2}{1 - \phi^2})} \tag{2.3}$$

It is uncommon, in case of any other distribution, for the conditional and the marginal probabilities to have similar distributions. In fact, in the general case, they do not even possess relatively simple forms. The Normal distribution is a rare exception [Grunwald]. In addition, the parametric calculations corresponding to a particular time-series model using maximum likelihood estimators are simplified with the assumption of normality.

We will continue seeking the premise for the assumption of normality in time-series analysis in the next post, which will also elaborate on the extensions of Central Limit Theorem to dependent random variables. Until next time!


## References
[1] Grunwald, G. K., R. J. Hyndman, and L. M. Tedesco. "A unified view of linear AR (1) models." (1995). [Link](https://robjhyndman.com/papers/ar1.pdf)

[2] Asymptotic Distributions in Time Series, Statistics 910, Wharton School of the University of Pennsylvania. [Link](http://www-stat.wharton.upenn.edu/~stine/stat910/lectures/11_clt.pdf)

[3] Anna Mikusheva, course materials for 14.384 Time Series Analysis, Fall 2007. MIT OpenCourseWare,
Massachusetts Institute of Technology.

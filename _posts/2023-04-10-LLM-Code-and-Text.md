---
layout: "post"
title: "Large Language Models: Code vs. Text"
date: "2023-04-10 11:11"
desc: Why are LLMs better at code generation than general text generation?
comments: true
author: Sujith Jay Nair
tags: deep-learning large-language-models
permalink: /code-versus-text
---
Every technology hype-cycle is a Dickensian tale of two extremes.

> <blockquoted> It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of light, it was the season of darkness, it was the spring of hope, it was the winter of despair. 
<cite> Charles Dickens, A Tale of Two Cities </cite></blockquoted>

Large Language Models (LLMs) are the rage now, and we can see those extremes play out in the reception of products based on LLMs. For instance, Github Copilot has been a massive success within the programming community whereas Galactica was launched and shutdown in under 3 days by Meta and faced intense criticism. 

The general perception (as of early 2023) is that (auto-regressive) LLMs are better at generating code, but have had a mixed bag of results in use-cases involving generation of general text. Why is that?

Yann LeCun provides a possible explanation of this divergence:

<blockquote class="twitter-tweet" data-conversation="none" data-dnt="true"><p lang="en" dir="ltr">13. Why do LLMs appear much better at generating code than generating general text?<br>Because, unlike the real world, the universe that a program manipulates (the state of the variables) is limited, discrete, deterministic, and fully observable.<br>The real world is none of that.</p>&mdash; Yann LeCun (@ylecun) <a href="https://twitter.com/ylecun/status/1625127902890151943?ref_src=twsrc%5Etfw">February 13, 2023</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

> Why do LLMs appear much better at generating code than generating general text?<br>Because, unlike the real world, the universe that a program manipulates (the state of the variables) is limited, discrete, deterministic, and fully observable.<br>The real world is none of that.

I do NOT agree with this explanation. General text, same as code, does not contend with the entire universe. It is limited to the context of the text. An essay on hydrogen atoms and their chemical kinetics does not care about Nietzche's thoughts on the Antichrist. Also, if the contention that LLMs deal with a finite deterministic universe were true, code copilots would not hallucinate, would they?

<blockquote class="twitter-tweet" data-dnt="true"><p lang="en" dir="ltr">Copilot is great until it starts hallucinating methods that don&#39;t exist in the libraries being used, which is very often. Every time I autocomplete using Copilot, I need to check if the method exists and it makes sense. I am not sure how much of a time-saving this is.</p>&mdash; Delip Rao 🥭 (@deliprao) <a href="https://twitter.com/deliprao/status/1551725078005571587?ref_src=twsrc%5Etfw">July 26, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

> Copilot is great until it starts hallucinating methods that don't exist in the libraries being used, which is very often. Every time I autocomplete using Copilot, I need to check if the method exists and it makes sense. I am not sure how much of a time-saving this is.

My take is that the success of LLMs with code can partly be attributed to what happens after the generation of text. In code copilots, the compiler and tests provide verification of the correctness of generated code. There is no such equivalent mechanism available in scientific writing or any form of writing. The faster feedback loops with code buttresses the user experience of using code copilots despite the high chances of hallucinations. Tightening the feedback loop is the way to improve the usability of text generation tools for science and other use cases.

### Notes
1. Unlike general text, there are only a very limited number of correct completions in code. General text has a much wider universe of completions to offer, and thus more shots at offering a satisfactory completion. How does this affect my argument?

2. The notion that LLMs are better at generating code than generating general text can itself be debated. Can it be partly explained by the attitudes and expectations of those using these LLMs as aids (programmers versus scientists, for instance)?
---
layout: "post"
title: "A Staff Engineer's Guide to Inventing Work"
date: "2026-09-22 11:11"
desc: A how-to manual for engineer-led discovery in software platforms
comments: true
author: Sujith Jay Nair
tags: platforms product management
permalink: /inventing-work
---
Platform teams are engineering-led rather than product-led. There is almost never a product manager handing you a roadmap, no revenue line to follow, and no market to lose. This means that work does not exist unless an engineer invents it. The continuous struggle is to find ways to increase the value our platform provides to the users of the system. A big part of a staff engineer's job in a platform team is to figure out what the team should build next - I like to call that "inventing work". Thankfully, the signals that help us to invent work are already out there, and they arrive from four directions - from the systems, from the users, from your organization, and from the industry. What follows is a guide to reading each of them.

<!--break-->

## Signals the System Emits
### Crash-led Discovery
Crashes and their associated postmortems, when done right, are clear signals that tell you what to fix, or what to replace. It is rare for postmortems to point to a new thing to build, but sometimes that does happen if you pay close attention to how users were impacted by crashes, or how they made their processes work while your team fixed a long-running crash. Identifying patterns across postmortems is something teams rarely do as a practice because it is a sporadic source of patterns; make sure you are not missing the big picture.

Crash-led discovery has a major drawback: it biases the team towards the loudest and the most recent failures, not the largest opportunity. Also, it is a maximally lagging indicator.

### Cost
Cost, in terms of dollars, is an obvious one. The cloud bill makes up for your lack of a revenue north star. But don't stop there; go beyond optimizing the database query, or investigating how to cut inter-VPC traffic costs. Check the P/L for your business unit if it's available, or your team's vendor contracts & cloud bill line-items, or ask someone who has access or knowledge of the cost centers. For each cost center, understand how it benefits your team to "outsource" that function, and what it would mean to pull it into your team's scope. This investigation also works in the other direction: things in scope that should be farmed out to a vendor, a cloud offering, or another team. The core lesson here is: buy-versus-build is NOT a one-time decision; you are allowed to revisit it as scope, team membership, technology and markets shift.

### Your Own Toil
This is the other cost - invisible to many, sometimes including the ones who handle the toil work. Every team has toil, and it is almost never prioritized. But you already knew this one, so I won't spend more words to say that toil is an important signal that there is work waiting to be discovered. The trap: your toil is not your users' toil; fixing the former improves unit economics whereas fixing the latter improves user experience.

## Signals the Users Emit
### Continuous Discovery
I have argued in the past that captive users "do not have the best view of the ideal state of tooling", and that "over-reliance on user interviews is a bane to platform product management". Essentially, what I am saying is that if you ask people what they want, they will say faster horses. I continue to believe this is true, but that is no excuse not to talk to your users. Continuous discovery is having an ongoing conversation with your users:
- Talk to N users per week/month/quarter. Ask them versions of the following:
    - can you walk me through the most recent task you did that involved the platform?
    - what were your top three pains in using the platform?
    - what would it mean to you if we solved those pains?
    - who else has the same problem?
- Interrogate their pains. Understand that almost every real problem already has a hack. No hack means the pain is not acute enough.
- Push back on their suggested solutions. Understand why they want those solutions, and if those solutions are bounded by your current design.
- Document the pains. Index them by frequency of mentions.

In short, user interviews should stay committed to jointly understanding the problem space. Solution space design is a matter for another forum.

### Overloaded Use-cases
This is my favorite heuristic, and I have talked about it [over](/not-aws) and again in other places. There's a serendipitous property that some platforms possess: users press them into service for use-cases they were never designed to serve. You should spend time to understand why users would rather use your platform to solve their problem instead of alternatives (if any), even though it was never designed for solving that problem. Treat overloaded use-cases as prototypes your users built for you, and figure out which of those are worth assimilating. The litmus-check for assimilation is simple: who else among your users has the same problem?

### Partner-to-Prototype
Overloaded use-cases are discovered after the fact. Partner-to-prototype is the same thing arranged deliberately: your team and the users work together to prototype something on your platform that could solve their problem. A prototype isn't a promise that the feature will be part of the platform; it is simply a joint exploration. The litmus-check for assimilation remains the same as for overloaded use-cases: who else among your users has the same problem?

## Signals the Org Emits
### OKRs
This is yet another obvious one; I list it for completeness. Of course, if your team has set an OKR (or had it handed down), you have already invented this item of work. Congratulations! On to the next one!

### The Manager-Repetition Heuristic
This one's simple and sometimes effective: if you hear your manager (or their manager, or further up) talk about something twice in a week, there is likely an unaddressed concern behind it. This is a good reason to take notes in your 1:1s, or read those LLM-generated ones. This heuristic is, in my opinion, the weakest of the many ways to invent work. The reason: the higher up the hierarchy, the farther from the users, and the likelier you are to build on HiPPO (Highest Paid Person's Opinion).

### Migration Debris
Every major change to the platform needs a migration, and anyone who has led a critical migration knows that adoption has a fat tail - it looks like the famous curve from *Crossing the Chasm*. You will have your innovators, your early adopters, your early & late majority, and finally your laggards. The laggard teams that drag their feet or those who never onboard onto the latest offering are an important signal: they tell you why your offering is incomplete, and why there is more work to be done.

I have [previously argued](/not-aws) that internal platforms have to cater to a wider audience than just the median user. The debris of a migration points us to users that your "median" solution is not catering to.

## Signals the Industry Emits
### Descriptive Writing Leads to Prescriptive Writing
Ideation is hard, but it is your job to come up with fresh ideas on how to improve an existing system (and propose those improvements in a prescriptive form, say an RFC). My personal favorite way to come up with ideas is to describe existing systems (for your peers, for users, for new hires; you pick your audience). Write a design document for the system that already exists, and compare it with state-of-the-art systems that do a similar or adjacent job. This act of describing surfaces decisions that no longer make sense. This is writing-as-thinking at its best.

### Lag Is Your Arbitrage
There is genuine value in staying educated on industry trends - open-source releases, other companies' blogs, research papers & conference talks - but there is a sharper way to read them and to use them to invent work. I believe that any single computing domain swings between secular phases of bundling and unbundling. We bundled compute & storage in data warehouses, then split them in data lakes, and now we are bundling them again in lakehouse engines. The movement from monolith to microservices is now making way for modular monolith. Internal platforms have the same swing, in the same direction, but with a delay as ideas take time to percolate. That lag is not a bug; it lets you import both the reasoning behind the industry's convergence and the evidence for it - public postmortems, migration successes, comparative benchmarks, other companies' abandoned positions, etc. You get the evidence without paying to generate it, and you get to skip the positions the industry already abandoned. The failure case here is too much delay: you do not want to be in the straggler set of teams adopting the trend.

## Which Signal, When
Eleven signals is too many to run at once. I rank them on two axes: how much of the argument the signal hands me for free, and whether it is leading or lagging.

At one end sit the signals that arrive pre-argued. A postmortem already has an audience and a conclusion. A cost center is already denominated in dollars. An OKR tracks work that has already been invented. These are cheap to act on, but they lag, to varying degrees.

At the other end sit signals you have to construct an argument for. Lag arbitrage gives you the strongest reasoning and the weakest standing, because the evidence comes from outside your company. The manager-repetition heuristic gives you zero evidence, but it comes with some standing. Continuous discovery gives you user pains, but turning them into specifications is on you.

Overloaded use-cases sit in the middle, which is why they are my favorite. The signal is leading and the argument is already built and running in production. Partner-to-prototype buys the same evidence at the cost of building it yourself. Migration debris is the same trade one migration late: the laggards are a lagging signal about the migration you just ran, and a leading one for the next. Descriptive writing hands you no argument and no urgency, but it has the best odds of noticing decisions that have silently expired.

## A Closing Note
None of this is a shortage problem. The signals are always on and the list above is not exhaustive. The failure mode of an engineering-led platform team is not an empty backlog; it is a backlog assembled from the loudest signals - usually the crash, sometimes the skip-level. Inventing work is less about finding a signal than about being able to say why this one and not the other ten.
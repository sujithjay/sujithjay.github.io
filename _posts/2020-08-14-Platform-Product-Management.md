---
layout: "post"
title: "AWS Is NOT Your Ideal"
date: "2020-10-01 11:11"
desc: On platform product management
comments: true
author: Sujith Jay Nair
tags: product management
image: /public/notaws/Median.jpeg
permalink: /not-aws

---
Let me start with an assertion. Every platform engineering team [^1] in every organisation aspires to be like AWS [^2].

Every platform team wants to be like AWS, because like AWS, they provide infrastructure abstractions to users. AWS provides infrastructure via the abstractions of VMs and disks and write-capacity-units, while platform teams provide infrastructure using higher abstractions which solve service definitions, database or message queue provisioning, and service right-sizing [^3].


This similarity prompts leaders of platform engineering teams to model their teams as agnostic providers of universal, non-leaky (within SLO bounds), self-served abstractions for their engineering organisation. Platform teams structured as such detached units struggle to define cohesive roadmaps which provide increasing value to business. But how does your platform differ from AWS?

## Your Platform vs. The Platform

### The Middle Ground
As an agnostic service provider, AWS can afford to cater to median use-cases. The reason platform engineering teams exist is to bridge the gap between PaaS abstractions which work for the median use-case to your business' specific use-cases. AWS can afford to target the median (economy of scale etc.), but you cannot.

{% include image-caption.html file="/public/notaws/Median.jpeg" description="AWS can afford to stay within a single σ. You cannot." %}

Agnostic platform engineering teams which emulate AWS try to get away from this responsibility by proposing abstractions which target the median use-case. A tell-tale sign of this is when the lack in wide usability of internal abstractions is compensated for by extensive onboarding & repeated training. This is also a side-effect of the the relative valuation of engineering time vs. the time of another function [^4].

### Follow the Money
The dictum 'follow the money' works beautifully for customer-front products. When faced with a choice between two competing features to prioritise, a common tactical play is to make something which leads to more (immediate & long-term) revenue. The proxy for increased revenue could be increased acquisition conversion, better retention or improved user experience -- metrics which ensure increased revenue for the company over time. In short, revenue growth is the north star [^5].

Not so much in platform engineering. There is no revenue since your customers are internal, captive ones. Captive audiences are forced to use a solution by the force of dictum and lack of choice. The metrics used in platform products are proxies for usability and user satisfaction -- but there are no foolproof ways to measure it for captive audiences. For captive audiences, solutions can not compete and better solutions cannot win. Like a command economy, platform products are designed rather than evolved. Design takes priority over market economy. So why is design bad?

## Bad Design
For design to work, there has to be an objective function against which we can design. A specification is an objective function against which engineering teams design a solution. Since we do not have reliable metrics [^6] to rely on for platform engineering, how do we come up with specifications? And without rigorous specifications, new features created by the platform run a high risk of not solving worthwhile problems for the users.The current accepted methodology among platform engineering leaders to solve this paucity of specifications is to rely on user-interviews. This is, as mentioned before, an unreliable source since captive users do not have the best view of the ideal state of tooling and abstractions that could be available to them.

The only way to flip this situation is to let go of command-economy-style designed abstractions, and to let your platform self-organise along the principle of markets. How does that look in practice?

### Market, FTW
Camille Fournier mentions in [Product for Internal Platforms](https://medium.com/@skamille/product-for-internal-platforms-9205c3a08142) how her team partners with customer teams to develop prototypes for specific problems. These specific solutions are later honed and iterated on to become general solutions provided by your team. I would go a step further on this route, where possible. Partner to prototype with multiple teams facing related problems to develop multiple specific solutions. These specific solutions can be seen as competing candidates to solve a general problem. Bring in user-interviews at this point to gauge pain-points, and iterate individually on these specific solutions. This switches the economy of your team to a self-organised market. Once considerable thought and iteration has gone into each solution, it is time to assimilate. Assimilate the best solution(s) while migrating the rest to the chosen solution. As emphasised in [Product for Internal Platforms](https://medium.com/@skamille/product-for-internal-platforms-9205c3a08142), an early investment of time into migration strategies is essential for such a scheme to sustain.

In platforms designed with experimentation, you will find that innovation continues to thrive at the edges of the platform's domain while the stable core of the platform is subject to periodic rework or maintenance. The use-cases a platform supports grows in a controlled manner to address an ever-growing percent of the consumers, and does not stagnate after addressing just the median users.

### Overloaded Use-cases
Although agnostic platform engineering teams might only be catering to very specific median use-cases, the customer teams with specific cannot afford to be blocked and they cannot stop delivering their deliverables. These teams sometimes create their own solutions, and in such cases the above strategy of assimilation works wonders. You get a prototype for free on which the team can iterate on. However, this scenario is rarer in cases where it requires specific skills to build such solutions, such as in data platforms. One common pattern in such knowledge-constricted situations is that users find ways to overload the existing solutions with minor tweaks to fit their use-case. Look out for such overloaded use-cases within your platform, for they are excellent guides to unmet needs of the users. You can leverage them to advocate for newer features to explicitly support those use-cases.

### Listen To Them (Only At The Start!)
As a parting note, I will take a jab at user-interviews again. The above tactics work when you are trying to scale your platform from 1 to N. When taking a platform from 0 to 1, the only solution to creating specifications is to listen to the users. Give them exactly what they want. Listen to their exact demands. A propensity of platform product managers is to rely on this excessively at a much later stage in the product's lifecycle. User-interviews have their place in evolving products, but the over-reliance on the methodology is a bane to platform product management.

**P.S.** As I read back the above essay, the heavy influence of [Product for Internal Platforms](https://medium.com/@skamille/product-for-internal-platforms-9205c3a08142) is clear. I would like to say that was the intention: to reassert the ideas in it which resounded with me, while stating a few of my own.




### Footnotes
[^1]: To define a platform for the purposes of this post, I use Camille Fournier's words: A platform is the software side of infrastructure.
[^2]: I use AWS throughout this article as a stand-in for a generic cloud provider.
[^3]: Although I do not mention data abstractions provided by data platform teams specifically here, the arguments in this article hold just as true.
[^4]: The other function, in many cases, turns out to be another engineering team. eg., a team of backend engineers reliant on the tooling provided by the infrastructure team for the provisioning of servers.
[^5]: As anyone aware of product management for consumer products, this is gross reductionism; but let us take it at face value for the sake of the narrative I want to focus on.
[^6]: Metrics have an overloaded meaning here. To clarify, your team might have good observability metrics to understand the need to design better solutions to scale existing features, but no metrics to make the case for new features.

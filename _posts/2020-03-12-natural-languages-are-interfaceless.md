---
layout: "post"
title: "Natural Languages are Interfaceless"
date: "2020-04-20 11:11"
desc: On the lack of interfaces in a natural languages, and why humans might need it.
comments: true
author: Sujith Jay Nair
tags: philosophy language
image: /public/interfaceless/no-face.png
permalink: /interfaceless-languages
---

In [The Design of Everyday Things](https://www.goodreads.com/book/show/840.The_Design_of_Everyday_Things), Donald Norman talks about the temperature knobs on his refrigerator:

> <blockquoted> I used to own an ordinary, two-compartment refrigerator - nothing very fancy about it. The problem was that I couldn’t set the temperature properly. There were only two things to do: adjust the temperature of the freezer compartment and adjust the temperature of the fresh food compartment. And there were two controls, one labeled “freezer”, the other “refrigerator”. What’s the problem?
Oh, perhaps I’d better warn you. The two controls are not independent. The freezer control also affects the fresh food temperature, and the fresh food control also affects the freezer.</blockquoted>



> <blockquoted>In fact, there is only one thermostat and only one cooling mechanism. One control adjusts the thermostat setting, the other the relative proportion of cold air sent to each of the two compartments of the refrigerator.
It’s not hard to imagine why this would be a good design for a cheap fridge: it requires only one cooling mechanism and only one thermostat. Resources are saved by not duplicating components - at the cost of confused customers.</blockquoted>

Norman is talking about the lack of a (good) interface here: a layer to translate (and hide) the structure of the underlying mechanism to the users of the mechanism. [^1] The need to translate to the user arises in two scenario:
1. There is a divide between the want of the user, and the how the mechanism is structured. I like to call it the what-how divide. [^2]
2. Although the mechanism & the user's want are aligned, the mechanism is too convoluted for the user to use in a direct way. A facilitator is needed.

In both cases, a translation is needed, and the translator is termed an _interface_.

### Languages are Interfaceless
{% include image-caption.html file="/public/interfaceless/no-face.gif" description="(Inter)Faceless a.k.a No-Face" %}

(Natural) Languages are the quintessential human way of communication. Our advanced languages are arguably the lone differentiators of our species from our cousins in the primate family, and the larger animal kingdom. [^3]

We have been inventing, honing, assimilating, and discarding languages since the start of our existence as a species. But we do not develop languages with an intent for it to be translated. Languages are not meant by its inventors to be translated. Every language is developed as if it is the only language in existence, and everyone else understands it.

This is in spite of the fact that translations of literature and texts are a crucial medium of cross-pollinating ideas, technology, values, and ethics.

The very leap western civilisation made into modernity via the High Middle Ages & the Renaissance is attributable (along with other major correlated factors) to the exchange of ideas between classical Greek, Latin, and Arabic. I state a few stellar examples. The philosophical commentaries of [Abu 'Ali al-Husayn ibn Sina](https://en.wikipedia.org/wiki/Averroes) (written in Arabic) were based on the works of Aristotle (written in classical Greek), and in turn [Michael Scot's](https://en.wikipedia.org/wiki/Michael_Scot) Latin translation of ibn Sina's works reintroduced medieval Europe to Aristotle. [Muḥammad ibn Mūsā al-Khwārizmī](https://en.wikipedia.org/wiki/Muhammad_ibn_Musa_al-Khwarizmi) codified Indian numeral systems in Arabic, and Latin translations of his textbooks introduced the decimal positional number system to Europe.

The number of examples, and their sheer impact are so overwhelmingly in favour for translations (with no arguable downsides), it makes one wonder why do we not have languages which are conducive to translations. Why do natural languages not have interfaces?


### Languages with Interfaces?
The only reason for the non-existence of interfaces for languages is we do not know or understand what that means. It is also not how languages evolve. Organic evolution of languages do not have a fitness function which incorporates interfaceability. Even [constructed](https://en.wikipedia.org/wiki/Constructed_language), [auxiliary](https://en.wikipedia.org/wiki/International_auxiliary_language) languages do not design for it.

Constructed auxiliary languages, however, implicitly have a notion of interfaceability. I will use [Esperanto](https://en.wikipedia.org/wiki/Esperanto) as an illustrative example (partly because it is the most widely spoken constructed auxiliary language)[^4]. Constructed auxiliaries are designed not to be the primary language of a person, but an auxiliary language to help communication with a speaker of another language[^5]. Second, as a consequence, it provides systems for derivational word formation[^6]. These in conjunction mean: a constructed auxiliary is the closest we have to a language interface. One might go a step further and say that in constructed auxiliaries, the interface is the language[^7].

In general, for every auxiliary language, there exists an interface within the mind of the speaker which translates between their primary tongue & the auxiliary tongue.

### Interfaces are Dynamic
Almost every major language now possesses translation guides to almost every other major language. In cases where this is not true, we could use an auxiliary, third language to mediate the translation. Do such translation guides and dictionaries count as interfaces? This can be answered (in a non-intuitive, convoluted way) with a counter-question: Why do translations of literature between languages always require a medium (a human scholar or a machine-aided translation)? The shorter answer is no. Translation Guides are not Interfaces.

Interfaces are dynamic. They hide the evolution of source languages as long as they conform to the interface. Users do not need to understand the evolution of the source language. On the other hand, translation guides of every form are a static snapshot of a minuscule part of the source language captured into the target language; and this snapshot stays true for the subset of the source language for a given point in time, and may not hold for any time before or after.

The above discussion on dynamicity in interfaces uncovers an important necessary (but not sufficient?) feature of them: every interface has an associated Intermediate Representation (IR).

In the previous section, when I said that in constructed auxiliary languages the interface is the language, I implied that a constructed auxiliary language acts as an Intermediate Representation.


### Ongoing Discussion
This is an incomplete article, as it reflects my nebulous thoughts on the subject. Open questions remain:

- How does an Intermediate Representation look? Do they need to be a first-class language on their own?
- Can we have interfaces live outside of a mind? State-of-the-art Machine Language Translation does not, yet, fill those large shoes. How can we push it to be an interface?


### Notes
[^1]: [The Law of Leaky Abstractions.](https://www.joelonsoftware.com/2002/11/11/the-law-of-leaky-abstractions/)
[^2]: Declarative programming languages are based on this philosophy of separation of the what & the how.
[^3]: [Opposable thumbs.](https://www.ruf.rice.edu/~kemmer/Evol/opposablethumb.html)
[^4]: English is, by far, the most widely used auxiliary language, constructed or non-constructed. As a native of India, and a non-native speaker of Hindi, I believe Hindi is the second most-widely used auxiliary language.
[^5]: [A Language for Idealists.](https://paw.princeton.edu/article/language-idealists)
[^6]: Derivational word formation or [Morphological derivation](https://en.wikipedia.org/wiki/Morphological_derivation) in languages allows speakers to derive hundreds of other words by learning one word root.
[^7]: This is not true for any constructed auxiliary, and particularly Esperanto. The language evolves and loses conformity to its interface.

+++
toc = true
readTime = false
breadcrumbs = false
+++


## What is this?

This is an AI generated newsletter-style summary of what's going on at City Hall. City council meetings are sometimes important and often very boring. AI is a splendid tool for separating all that procedural jargon and finding the parts that residents might care to know about.

## Why bother following City Council?

I wanted to try using a different lens to follow local governance: something in between the laundry list meeting agenda and the more in-depth, topical reporting you might get from Racket or MinnPost about police union budgets (for example). What are the folks at the meeting actually talking about? I especially sought to foreground public comments.

## Why use AI?

What goes on at a typical city council meeting, anyway? Do they spend all their time plodding through license applications? Issuing grand proclamations?

There are a few ways you might try to find an answer.

You could go directly to the [LIMS website](https://lims.minneapolismn.gov). It's an excellent data portal, but there's just too much information to "browse". On top of that, the official minutes ([summary](https://lims.minneapolismn.gov/Download/CommitteeReport/3870/Regular%20Meeting%20of%20July%2018%202024.pdf)) and meeting summary ([sample](https://lims.minneapolismn.gov/MarkedAgenda/Council/4755)) are somehow both over-stuffed with procedure and very lacking in actual details. These documents are just not written with general audiences in mind, and that's OK.

You could watch the video. They're often several hours long and can be painfully boring. The boredom, jargon, and procedure disinceitivise public participation. Like a weed-out class, only the most committed are able to access this information. Each meeting stream typically receives [somewhere in the low hundreds of views](https://www.youtube.com/@cityofminneapolis/streams).

But we have journalism! You could follow a local publication and hope they report on the issues you care about. This has trade-offs too. Because of their business model (usually advertising) and resource constraints, human journalists are limited in the types of stories they can cover. Writing a 5 minute memo about a 3 hour meeting is expensive. AI is perfect for the job.

To be sure, AI is also poorly suited to doing things human journalists do well, like investigative reporting and evidence-based narrative development. AI can tell you what happened, but a journalist can help you understand what it means.

This is _not_ journalism.

## How does it work?

It's actually quite simple!

* I scraped the meeting list from [this page](https://lims.minneapolismn.gov/CityCouncil/Meetings).
* The city publishes YouTube videos with human-generated captions for all council meetings, which I downloaded.
* I feed the transcript, along with a fairly detailed prompt, to Claude.ai, An LLM like ChatGPT made by Anthropic.

## Can I use your data or code?

Yes. The data is public and available on [GitHub](https://github.com/subdavis/open-journal-mpls). It includes meeting data I've scraped from [LIMS](https://lims.minneapolismn.gov/) and the youtube captions I scraped. My code is also available on [GitHub](https://github.com/subdavis/open-journal-mpls/tree/main/archive).

## What else could this do?

If you have an idea for a project that might involve lots of open data and some questions you want to ask it, let me know. I hope to tune these reports (or even generate topic-based digests) to reflect the needs of the reader, and AI is able to do that much more economically. 

## I have comments or suggestions.

Wonderful, [please share them](https://docs.google.com/forms/d/e/1FAIpQLSdz6_e5PR5YMauD2l10KMbooyFvcIC6wl0JirllKRI7gm723g/viewform?usp=sf_link)!
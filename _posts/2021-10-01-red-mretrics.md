---
layout: post
title: Microservices and metrics
dem: Having a clear view of a microservice is important and metrics help us get there.
---

```
Having the right metrics in place is critical. For any microservice when things start to break having an overview of what broke is important. Because if you cannot see it you cannot fix it. Metrics is not only about having graphs and numbers but graphs that actually mean something and can give us a holistic view of what happened.
```

Designing proper metrics for a microservice or a system is a skill rarely possessed. Metrics is not only about the CPU, RAM, and thread count, but also about nuances like error codes, DB failures, rate limiting, etc.

Here comes the concept of **RED (Rate, Error, and Duration)** metrics. As an engineer you want to build a dashboard that contains the fundamentals and the business metrics, you don't want your product managers to be sad, do you?

Let's dig deeper into the **RED metrics**.

- **R for Rete** Rate metrics tells you about how many requests does the system process over some time, it is not only the number of API calls but also MQ messages or cron jobs or any external or internal process. This is important to estimate the scale of a system and how to handle a surge in the volume of requests the system receives. It can also determine the growth of any system as time passes.

- **E for Error** Error metrics is super important, it tells you how many and what type of errors the system has encountered over some time. It is not only useful for an engineer who is building the system but also the product folks who try to look at all the errors and try to understand what might have gone wrong with some of the processes designed. If not a business fault, it is easier to find which downstream broke and why? Having the right error metrics and code will save you crucial minutes in time of downtime. Having exhaustive error codes which are common across the organization particularly helps the on-call to figure out the bug when it's 2 in the morning. (Database errors, Rate limiting errors are the most common errors in a system and should not be skipped, they can be indicators of bad scaling policy or even a bad design practice that went unnoticed.)

- **D for Duration** having duration metrics will tell you how fast or slow is your system processing or reacting to a certain request. Duration will also tell you if there is a network fault or bottleneck between two systems. Providing SLA becomes easy when you have durations set up for rach API and the message that is being processed. The best practice of having duration metrics is to have latency buckets with 0.50, 0.90, and 0.99 percentile durations. This will tell you the median, the high, and the worst-case performers which will have you provide others with the right SLA. Durations not only show how much time it took to process a request but also how much time external systems took in that request like DNS, TLS, etc.

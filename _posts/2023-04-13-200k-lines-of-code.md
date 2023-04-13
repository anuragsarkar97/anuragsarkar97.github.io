---
layout: post
title: Journey from 100k lines of code to 20k lines of platform at AWS
dem: How we broke up our giant monolith into micro-platforms.
---

```
While microservices are cool to build and have, we didn't really have time for them. And hence, here we are.
```

<iframe src="https://giphy.com/embed/ghBpi4kaTpTgbut5Uj" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>


Where I was on the Network Communications and Services team, we were the source of truth for all deployments that would go across the whole networking system.
This would include
- Network topologies
- Network configurations
- Network security
- CI/CD for agents, modules, and OS.
- Network statistics and monitoring systems.

And yes, this was all a single system.

# Chapter 1 - Why

The pain and the need to break down the whole system into smaller pieces

- At that time, AWS was planning to onboard 3rd party companies to run their networking needs; this meant exponential growth in the types of systems we needed to manage, i.e., topologies, configurations, and most importantly, way too many deployments.
- We were adding engineers at that time and wanted a reliable way of building things with reduced friction.
- We are a Java shop, and we have a plan to start using open-source tools. The only problem was that very few people build networking tools in Java. To have access to all the open-source fun, we needed to have our systems written either in Python or Go.

(If your system runs cool and you don't need to break it into pieces, then do not.)

# Chapter 2 - How

At AWS, we always run short of time. With all the on-call load, present development effort, and research that we do, following the general practise of building microservices just didn't make sense.

We had to be smart about it.

1. We started by identifying things that really needed fixing. Because each machine requires a different configuration, the code was unique in that it scaled unlike anything else.
2. Elements that don't depend on each other Security has nothing to do with configuration systems, etc.
3. And development patterns: once an agent is defined, it rarely changes (few commits every quarter), and CI/CD patterns change often based on the client's requests.


One thing that worked out great for us in all this migration was our data. We keep everything in dynamodb and S3, so we really don't have to think about breaking the database and replicating it again.

The problems that we had to solve were internal communication and code standardisation.


## 2.1 - Communication

```
Ah, it's simple: use REST with SQS, Kafka, or RMQ (pick one).
```

But we were really inclined towards using some sort of RPC system. Why? Standadization. The last thing we wanted while building your system was 2 API doing similar things but with a different naming convention.

We picked Smitty (because Amazon uses it heavily) with SQS and Kafka (we will come back to this later).

## 2.2 Organising the mess

- We started out by writing the contracts between each service and how they would interact with each other. Consider how departments would obtain configuration data or how agents would obtain security tokens.
- We built out a single repository of all the contracts and let it be responsible for generating binding code for all the languages we wanted to support (Java, Python, Rust, Go).
- Having the contracts ready, we started porting out the simplest platforms first: the topologies and securities platforms.
- With moving out the Java codebase, we could now finally use open source tools like netflow, which we had already replicated in Java. that reduced about 7,000 lines of code and the headache of adding new features to it.

On all the other systems, we let it be in Java (we cloned the main repository and deleted what we didn't want).

This took us about 6 weeks to break down the whole system.

Now we are not fully done with what we initially intended to do, but it has given us a clear path for what we are going to do next and how we are going to optimise everything.


# Chapter - 3 Not everything is roses and sunshine.

There are a few disadvantages too; it's not all beautiful.

1. There is and always will be some redundancy here and there.
2. We have to build far better tools to get insight on whats happening.
3. We pay at least 20% more than we used to.
4. Debugging is now harder than it was. Sometimes we have to run the Python, Go, and Java servers together to understand what is happening.


<iframe src="https://giphy.com/embed/l3vRiLydJmh7X0Yx2" width="480" height="270" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>

# Final Notes

Ask yourself: Do you really want to go down this path? It is expensive, but it is cool.

Also, we were using Kafka for custom event ordering; more on that in the next blog.

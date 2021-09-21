---
layout: post
title: Logging Like a Pro
---

```
Logging is Hard especially when it comes to microservices. Sometimes logs do not give enough information and sometimes so much that it is redundant.
```

Let's look at the basics.

1. Configuration
2. Structure
3. Triage

## Configuration

```
Microservices are particularly difficult to log occur real-time systems. hitting the sweet spot of how frequently the systems send data to monitoring tools vs how much compute and memory overhead is there. Will it affect the performance of the system vs how quickly can I see my logs?
```

Every microservice has different criteria as to how it can be configured for optimal use as well as performance.
Let's take an example.
Gateway microservice handling over 100kreq/sec. A standard gateway microservice that does authentication and calling downstream services is the simplest use case we can choose. Now logging, in this case, is not particularly hard but when we look at the sheer scale the system operates we need to dig deeper into the consequences of logging data in the long run.
Aggregating and sending logs is a simple process - run a background task collects all the sysout data and as soon as the aggregation limit hits do an API call to a monitoring tool to record the data, repeat. This is fine when we talk about 10-100 req/sec and the logs are lightweight. When logs are less than 1 Kb in size and we can collect a lot of them it is almost realtime. (We will assume 1-2 sec delay is realtime for the developer)
Let's look at this particular use case where 100kreq/sec is the average load on the system. Let's assume the best-case scenario is running multiple nodes (Assume 25), so each node receives around 4kreq/sec. if we are generous with logging then we will log every request and every error assuming 2 logs for every request, the system is generating a little over 8k/sec. In terms of memory footprint, if every log is 2 Kb, the system is averaging 16Mb/sec. Now running a background task that keeps collecting and sending data every second can be a bit of a computational challenge if the background task is doing some processing on top of the log.
So now logging has become a multivariable problem, we are not only looking at the size of the log itself but also how frequently it is sent to the collector and how it stays in memory before it is actually sent.

To solve a problem at this scale we need to figure out the right balance between time, memory footprint, and compute overhead.
Ask, How much lag can the system have while sending logs? How many times shall the system send data to the collector system? How much do you need to log in to have a clear view of what broke when a system breaks?

Having lesser logs always reduces the overhead of a system but also reduces the visibility of a system and what happened inside. Having a lot of logs is good but terrible for a high-performance system. Sending out logs frequently is great but it consumes a lot of resources.

With high-performance systems, having lesser logs is always the right choice. Write code in a way where you can disable logs in the different settings of environments. In staging let all the logs flow to the collector meanwhile in the production system send only those are an absolute necessity for visibility.

## Structure

```
Having the right structure of a log across systems is always a good start for any organization. having rights tags on your logs, correct timestamps, IP address of your node maybe? Anything you think can help you debug an issue can be a good start while structuring your logs. For example, having a common request-id for all the downstream components for an API can help you pinpoint exactly what components broke. Having the right IP address can help you understand if any node is not working correctly and the right timestamps can help you figure out when exactly things broke.
```

Let's take an example,

An all Kafka(message queue) system receives a huge chunk of data for preprocessing and data cleaning for some machine learning systems. Now unline previous data this system is event-driven and mostly internal to the organization but plays an important role in the whole system's pipeline. It might process billions of data points so logging each becomes really pointless in a bigger scope. What a developer really needs is error monitoring. Now unlike the previous problem here logs become very critical to replay that event without a proper logging system it is almost impossible to replay the system if the data was volatile. So now you not only handle the error but also log all the details to replay that same data point. Error handling becomes crucial in a stage like this. Having the right structure now not only helps developers fix their systems but maybe product managers and data scientists to figure out potential issues. having the right structure can be used to build visualization which becomes an absolute necessity while building a large-scale data-driven system.

While choosing your structure is best if it is standardized in JSON/YAML form to make it simple to do field operations. Having only text data can only help you doing regex searches. JSON structures can help you do way more than just searching logs.

## Triage

```
Logging what is necessary and understanding its implications is what will separate your logs from all the noise in the world.
A simple example is never stored access tokens in logs. Well, it might help you debug a lot of problems very easily but any software audit and you will face a huge lawsuit against your organization.
Compliance is real even though your systems are internal and nobody probably cares, keep your logs in check.
```

Having set a standard rule for logging is a must in any organization be it a simple service or a real-time P0 service. Know what and what not to log. (Like passwords, secrets, and system keys). Don't do it. Compliance is now a real thing and the more compliant your systems are the lesser you will have to deal with these tech debts when the government comes up with new compliance schemes. Never log anything you think that others should see except you. So know what to keep and what to discard and when to discard.

# Conclusion

The best solution to log and catch the bug in any system is to plan early when developing a system. Document if you can (At least the important bits of the logs). Discuss it with the team and in reviews. Make it a part of code reviews and have correct log levels.

Having a central logging library in an organization can also save a lot of hassle when logging and monitoring. Furthermore, without logging, there is no monitoring, and troubleshooting individual issues can become complicated.

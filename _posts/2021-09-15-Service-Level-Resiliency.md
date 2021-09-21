---
layout: post
title: Service Level Resiliency
---

```
Resiliency is the ability of a system to gracefully handle and recover from failures. Detecting failures, and recovering quickly and efficiently, is necessary to maintain resilience.
The primary goal is to build robust services that can tolerate failures within their system, but also failures from components they depend on. When dealing with large scale systems it is near impossible to achieve 100% operational excellence, so the normal state of operation is partial failure. Running in a partial failure mode is a viable option for most of the services.
```

## What all to look at

1. Client facing (realtime vs interactive along with SLA?) services: Services exposing APIs which are used in customer interaction flow.

- This does not necessarily mean external services (that apps connect to), but any service that is causing the user to wait for its response. (e.g. Collections, pricing etc).
- Any background job impacts client wait time

2. Offline services: services which are not client facing, not real time and dont have strict SLA (can be off by “x” sec).

3. Upstream and Downstream services. Caller is considered upstream and callee is downstream, for example if service A is calling service B (A ⇒ B), Service A is upstream and service B is considered downstream service.

4. Brownout - A service is temporarily under stress which can exhibit increased API errors and/or latency, but it is able to serve some portion of its traffic.

5. Blackout - A complete and full downtime for a service, where 100% of the requests will fail for a complete service.

## Tenets

1. Determining whether the operation is suitable for retrying.
   You should retry only transient errors like intermittent network errors. There is no point in retrying the permanent failure operations like database primary key violation, invalid resource url etc.

   - If you can’t decide an exception as a transient error, then treat it as a permanent error and log them which will help us to analyse the list of errors offline and correct the error handling for transient errors.
   - When creating a service, consider implementing error codes which help clients to categorize retriable .and non-retriable errors, depending on the error code.
   - Make sure all the downstream services are idempotent before configuring retries. If the downstream service is not idempotent, either make it idempotent or implement duplicate checks at client side with the getter helper methods from downstream if available.

2. Determining the retry count and backoff interval.

   - As a general rule, apply exponential backoff for background tasks. And use immediate or fixed interval backoff for real-time or user interaction services. Choose the retry count and backoff value so that end-end latencies are under control (promised SLA).
   - If a service call includes multiple remote operations to perform within the upstream call, It might be expensive and complex enough to compensate for all other operations that were already successful when one fails. In this case it is suggested to have more retries for failed remote calls, or to have a larger back-off policy if the end-end latencies are acceptable, unless the other resources become scarce.
   - Make sure callee is idempotent (refer idempotent patterns here) when you configure retries (>1).
   - It is assumed that all the services are idempotent.
   - While publishing to message brokers like Kafka, idempotency can be achieved. (refer here.) If it is not possible to make the callee idempotent (e.g. Third Party Services), we can make the caller idempotent by asking for more apis (e.g. - get the state of an api call) and implement a state machine around the call.
   - Configure a higher retry count (?) for offline services where clients can afford E-E latencies but with guaranteed eventual completion of execution is more important. A smaller (probably not more than 3 retries, but again client promised SLA should not be broken) retry count for client facing services where we can’t afford higher latencies.
   - How to consider the scope of retry if a function requires multiple remote calls. It is easier to apply retry policy at the top level function instead of multiple levels if the end-end latencies are accepted, but this may trigger fewer unnecessary calls to successful ones also, this is more suitable for any background(offline) applications.
   - If applying the retry policy at the top level function is not an option due to an increase in the latency to the caller, then the scope for retry policy will be applied at multiple remote calls, this is more suitable for client facing and real time services

3. Resource Isolation.

   - Use different thread-pools with different limits (depending upon the downstream latency and number of calls you make to downstream) for different remote calls, so that errors with one remote endpoint won’t cause other threads to block.

4. Timeout for operation (Deadlines)

   - Combine retries with timeout, so that we still continue to retry “n” number of times but with an upper bound of time limit, which will help us.

5. Circuit breaker

   - After n retrials (there is a detailed section that talks about how to configure n) for transient errors, Configure a fallback function wherever applicable using CB. Configure CB for every RPC call and apply back pressure to your service callers (with the help of request queues and fallback functions).

6. Idempotency (An operation is idempotent if it will produce the same results when executed over and over again).

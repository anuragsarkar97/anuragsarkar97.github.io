---
title: Spring **Reactive**
layout: post
tags:
- java
- spring-boot
- reactive-java
- threads

---

Reactive Spring-Boot
-
The need of reactive spring-boot might not seem obvious and frankly it's not easy to begin with but trust me it is worth it.

**Definition**  - In plain terms reactive programming is about non-blocking applications that are asynchronous and event-driven and require a small number of threads to scale. A key aspect of that definition is the concept of backpressure which is a mechanism to ensure producers don’t overwhelm consumers. For example in a pipeline of reactive components that extends from the database to the HTTP socket when the HTTP client is slow the data repository slows down or stops until capacity frees up.
From a programming model perspective reactive programming involves a major shift from imperative style logic to a declarative composition of async logic. It is comparable to using *CompletableFuture* in Java 8 and composing follow-up actions via lambda expressions.


What it really means we won't have to bottleneck by a component in the code and slow everything behind it. we can still keep running only difference we won't be able to compute till it actually returns the data.

Adopting Reactive Programming has multiple benefits 
- It brings better performance to the backend systems.
- It offers better usage of hardware memory.
- It looks cool.

Now let's see how we can write our first Reactive Java Code 

what do you need to get started?

- Java8
- maven 
- Internet 😆


LET'S CODE

- Open up any editor and make it a maven project. (Or download it from <a href='start.spring.io/'>here</a>) 
- put the reactive spring dependencies to your POM.xml
``` xml
<!-- https://mvnrepository.com/artifact/org.springframework/spring-web-reactive -->
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-web-reactive</artifactId>
    <version>5.0.0.M4</version>
</dependency>

```
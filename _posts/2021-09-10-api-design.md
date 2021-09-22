---
layout: post
title: Scope of a Microservice
dem: Imagine you are going to rewrite a piece of a huge monolith system that has tens and thousands of lines of code
---

```
Imagine you are going to rewrite a piece of a huge monolith system that has tens and thousands of lines of code. You fork out the system and start commenting out things you don't need and you strip it down to that one business line. Let's call it to search? But now how do you make the most reliable and scalable search system which you just took out of the giant codebase? Let's talk.
```

When you start writing a microservice from a monolith you always have a choice to either keep the same code with some cosmetic changes or to rewrite the whole thing while not repeating the mistakes you did earlier. Where do you begin?

The first thing you need to talk about is the resource that you already have, namely time and skill. Do you have time and do you have the skill to build a large-scale microservice from scratch? If yes, ask the second question if it is worth rewriting the whole thing maybe because earlier the complex toolchains were not available as compared to the present times. If yes, choose a language that is well developed and has community and library support around it, maybe funded by a large organization. If you are writing a microservice it is essential to know the why's of the system. Do you need a fast compile time, do you need a lot of computational capacity? do you need a lot of network handling ? Do you need very good framework support which is easy to maintain?

Getting these answers right is the best thing you can do before even creating a git repo. (PERIOD)

Next, how do you want your systems to communicate with the world? It is through HTTP API or is it through well-defined RPC methods or nothing at all. Do your microservice even serve any traffic or is it event-driven.
knowing how your microservice can talk to the world is the first step to actually building it. Remember you really haven't started coding yet. you are still figuring out how your microservice should look like.

Next is your databases, now well it mostly depends on what your data is and your business logic, it is good to google that does the required database library exists for your language.

Now, how many databases should you really have per microservice? Really it depends on what data are you serving but it is generally either 0 or 1 or 2. Anything greater than that and you can break your microservice even further. Is it required, totally depends?

Next, you need to know what kind of servers your code runs best. These days it doesn't really matter. Silicon is super tight these days. So run anywhere you can. Keep in my that you need to have enough memory and CPU to actually serve traffic on it. It is a tricky thing to do especially when on a tight budget. If you underestimate that directly affect your clients and if you overestimate, you end up making Jeff Bezos rich.

Now you have actually set the rules to build your microservice. But before you begin putting a lot of effort into actually writing a technical document for the microservice. Developers will praise you after you are gone.

Technical documentation sounds boring but is a really important part of your career as a developer. You need to put as much effort as you put into actually crafting your code. People don't see the code much these days, they see the documentation. Shitty documentation is a shitty code.

Next comes Test. How do you test your code? Is it up to standards does it cover all the edge cases and the business use case? It is up to you to decide that you want to have test cases based on the business use case or plain or line coverage. It is up to you to decide, but make sure you document them well.

Now you can finally start crafting your code. But first, you need to talk about how are you going to monitor your code? Will you have error handlers, counters, histograms, timers? What pattern will you follow? How do you make sure that the on-call developer gets the gist of what went wrong when you were on a vacation. Figure those out. Once you have them handy push all the best code.

don't forget to give the team a run-through. Let people scrutinize the code. let people see it. It helps to get feedback and helps the team get a better idea about what is being built in the team. Who knows you might inspire someone to build something amazing too.

# Conclusion

Anyone can write code. That is not what you are paid for. You are paid to solve a problem in a way that will help you and the organization to run better. So do what other devs don't and be a legend while you do it.

Read Docs, talk to people whenever stuck, and code whenever you can.

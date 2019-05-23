---
title: Why *Web assembly* 
layout: post
tags:
- c++
- javascript
- webassembly
- html
- emscripten
---

WASM for WEB (PART I)
-
You might have seen the Google I/O '19 and also all the talks about webassembly and why it is so amazing or as I like to the future.

**Definition**  - WebAssembly (often shortened to Wasm) is a set of standards that define a portable (modular) binary format and a corresponding assembly-like programming language for executable program and environment-specific program interfaces into which it may be embedded and interact with. It was initially developed to improve JavaScript applications performance and to be used inside Web browsers but it isn't constrained to them and can be embedded anywhere else.

Javascript is pretty much exhausted in almost everyway and also in terms of performace. 
We need something that can provide native like performance in the browser. 
Well, you might have heard that it a c++/rust thing to begin with but it's not a 100% correct. You can also code in golang (development phase)
So there is a lot of development going around to bring native performance to the web and WASM is one of it. Most exciting thing about it is that is isn't that hard to integrate with any of your pet projects.

Adopting WASM has multiple benefits 
- It brings better performance to the web (especially for load times, and math-heavy stuff like games).
- It offers a good compile target for the web, so that people can choose which language they code their websites in.
- It is much faster to parse and compile because it is much closer to machine code (and it is compact). Much of the optimization is done once server-side, instead of every time client-side.
- It can be substantially faster to run, again because it's close to machine code, and because it has static types and is generally designed for speed.

Downsides (Tho mostly will be fixed in the upcoming updates)
- No DOM integration yet
- Slow integration with JS
- No threads yet
- No SIMD yet
- No garbage collector integration yet


Now let's see how we can build our first WASM website

what do you need to get started?

- emscripten binaries
- python 
- git 
- cmake (optional)
- choice of editor 
- choice of browser (Chrome please)



HOW-TO INSTALL 
-
- Install emscripten binaries
```
$ mkdir ~/tmp && cd ~/tmp
$ git clone https://github.com/juj/emsdk.git
$ cd emsdk
$ ./emsdk install --build=Release sdk-incoming-64bit binaryen-master-64bit
$ ./emsdk activate --build=Release sdk-incoming-64bit binaryen-master-64bit
``` 
This script will install and active emscripten system wide which will be compiler to all our c++/ rust code.

- Now this is in place we need to set a project directory right to make out lives easy. It is better to always keep your code in a different directory which has ```build/``` and ```gen/``` files beacuse we are going to generate a lot code right now.
Directory would look something like this. 
```
.
├── build
│   ├── main.wasm.map
│   └── main.wast // intermediate compiled files (your reference point)
├── build.sh
├── cpp
│   └── main.cpp // your access point to c++ 
├── package.json
├── server.js
├── tsconfig.json
└── web
    ├── gen
    │   ├── main.js // this is where the action happens 
    │   └── main.wasm
    └── index.html
```

Seems fairly obvious to begin with and to automate all this process we can have a bash file to do it all for us.
```
rm build/ -rf       # remove pre-build folder
mkdir build         # make a new build/ folder
mkdir web/gen       # make a new web/gen folder
cd build
# we compile main.cpp 
# -g will produce main.wast and main.wasm.map
# -s EXPORT_ALL=1 will export all fuctions in your c++ 
# -s MODULARIZE=1 -s EXPORT_NAME='assembly' will wrap the generated js file in a fuction 
# -o produces the main.js 
em++ ../cpp/main.cpp -g -s EXPORT_ALL=1 -s MODULARIZE=1 -s EXPORT_NAME='assembly'  -s -o main.js
mv main.js ../web/gen/
mv main.wasm ../web/gen/
```
Also add:

 ```source /Users/oyo/tmp/emsdk/emsdk_env.sh --build=Release > /dev/null``` 
 
 this your ```~\.bashrc```


LET'S CODE
-
This bash file will generate all the required files for you to finally connect **WASM to WEB**

Let's write a simple c++ code to make it web-accessible 
``` c++
#include <iostream>

unsigned short lfsr = 0xACE1u;
unsigned bit;

unsigned randomFunction() {
    // we'll write a random number generator 
    bit  = ((lfsr >> 0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 5) ) & 1;
    return lfsr =  (lfsr >> 1) | (bit << 15);
}

int main() {
    std::cout << "YAY web assembly" << std::endl;
    std::cout << randomFunction() << std::endl;
    return 0;
}
```
As we now have our c++ file in place we can use ```build.sh``` to get all out other files in place.

Let's start with our ```index.html``` 
``` html
<html>

<body>
    <h1>first web assembly code </h1>
    <script src='gen/main.js'></script>
    <script>
    assembly().then(function(Module) {
        console.log(Module.__Z14randomFunctionv());
    })
    </script>
</body>

</html>
```
Understanding the script tag is very important because the webassembly code cannot be executed until the website is completely initialized.
```assembly()``` function is the name given while ```EXPORT_NAME='value'``` was set. This function provides with a ```.then()``` like interface to process our c++ compiled code further.

now when you open your web console you can see random numbers. **YaY**
you now have a working prototype of WASM. 

In the next part we will be looking at how to integrate it with different web components.

Peace 😎
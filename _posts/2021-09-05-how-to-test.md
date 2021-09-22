---
layout: post
title: How to write a test
dem: There is a smart way and a boring way to test code. I never chose the smart way to write a test. I did what everyone else did. Dont be like me, write smart test and save yourself sometime to play FIFA.
---

```
There is a smart way and a boring way to test code. I never chose the smart way to write a test. I did what everyone else did. Dont be like me, write smart test and save yourself sometime to play FIFA.
```

Now like most of us you write your code and then write your test and by the time you start writing your test, you start to wonder what kind of a test should i write? What should be the data to test with? Suddenly it is overwhelming and the next second it is boring resulting is shitty tests that you know you could do better but just dont care.

# Smart tests

Write test before you wirte your code. Why you ask ? becuase then you will force yourself to write a code which will pass your test and not the other way around. Writing test before the code itself and generating the data before even you have written the code gives you a huge benifit while debugging. Having data beforehand can help you write way better business related test cases which serves 99% of th traffic.

Starting fresh with tests always help you maintain the highest of your standards as well as help you do better code coverage and helps you reduce code that was unnecesay in the first place.

Lets see and example.

let us write some test first

```go
import "testing"

func Test_simple(t *testing.T) {
	tests := []struct {
		input  int
		output int
	}{
		{
			1, 1,
		}, {
			-1, 1,
		},
	}

	for _, test := range tests {
		out := ToAbs(test.input)
		if out != test.output {
			t.Errorf("error output does not match")
		}
	}
}
```

now based on the test we just wrote let us write some code.
Now what it helps us achieve is when we start writing the code we write the code in a way that is passes the test cases. having a good testcase will solve most of the problems and the code follows.

So here we write out code .

```go
func ToAbs(a int) int {
	if a < 0 {
		return a * -1
	}
	return a
}

```

As you can see it doesnt look much different from what you would have written otherwise but the quality of the code is good because the test you wrote ealier were of good quality.

Now you might wonder what kind of a test you should write in the first place?

1. What is the best case scenario , i.e, when everything works.
2. What is the worst case scenario generally your input data is empty.
3. What happens when your downstream function breaks. So lets say your function calls 3 more functions internally. write 3 different test where each test consist of one failing downstream function call.

If you are able to suffice these conditions your code will go a long way. Not only that if will also help other developers who are contributing to the code base understand it better.

Now how much time should you really put into writing testcases ?

Given an example if you are going to take 1 hour to code that function, writing all the tests should not take more than 2 hours to write. Sounds a bit too much? Relax, I tought so but it reallt doesnt take so much of effort to write good test case. Make a habbit of making it a part of the feature release and you will never encur a tech debt.

# Conclusion

Writing test is simple dont overcomplicate it. Have solid data to test upon and keep the basics present, having quality tests over quantity. Finding the right balance of test is important so learn it.

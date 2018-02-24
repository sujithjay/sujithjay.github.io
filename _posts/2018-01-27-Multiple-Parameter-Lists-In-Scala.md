---
layout: post
comments: true
title: Multiple Parameter Lists in Scala
desc: A small tutorial on Currying in Scala
permalink: /2018/01/27/Multiple-Parameter-Lists-in-Scala/
---

**Note**: I wrote this article as part of a contribution to Scala Documentation. The original post can be found [here](http://docs.scala-lang.org/tour/multiple-parameter-lists.html).

Methods may define multiple parameter lists. When a method is called with a fewer number of parameter lists, then this will yield a function taking the missing parameter lists as its arguments. This is formally known as [currying](https://en.wikipedia.org/wiki/Currying).

<!--break-->
Here is an example, defined in [Traversable](/overviews/collections/trait-traversable.html) trait from Scala collections:

```scala
def foldLeft[B](z: B)(op: (B, A) => B): B
```

`foldLeft` applies a binary operator `op` to an initial value `z` and all elements of this traversable, going left to right. Shown below is an example of its usage.

Starting with an initial value of 0, `foldLeft` here applies the function `(m, n) => m + n` to each element in the List and the previous accumulated value.

```scala
val numbers = List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
val res = numbers.foldLeft(0)((m, n) => m + n)
print(res) // 55
```

Multiple parameter lists have a more verbose invocation syntax; and hence should be used sparingly. Suggested use cases include:

#### Single functional parameter
   In case of a single functional parameter, like `op` in the case of `foldLeft` above, multiple parameter lists allow a concise syntax to pass an anonymous function to the method. Without multiple parameter lists, the code would look like this:

```scala
numbers.foldLeft(0, {(m: Int, n: Int) => m + n})
```

   Note that the use of multiple parameter lists here also allows us to take advantage of Scala type inference to make the code more concise as shown below; which would not be possible in a non-curried definition.

```scala
numbers.foldLeft(0)(_ + _)
```

   Also, it allows us to fix the parameter `z` and pass around a partial function and reuse it as shown below:
```scala
val numbers = List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
val numberFunc = numbers.foldLeft(List[Int]())_

val squares = numberFunc((xs, x) => xs:+ x*x)
print(squares.toString()) // List(1, 4, 9, 16, 25, 36, 49, 64, 81, 100)

val cubes = numberFunc((xs, x) => xs:+ x*x*x)
print(cubes.toString())  // List(1, 8, 27, 64, 125, 216, 343, 512, 729, 1000)
```

#### Implicit parameters
   To specify certain parameters in a parameter list as `implicit`, multiple parameter lists should be used. An example of this is:

```scala
def execute(arg: Int)(implicit ec: ExecutionContext) = ???
```

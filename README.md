### A Better Lambda
[![PyPI version](https://badge.fury.io/py/lambdazen.svg)](https://badge.fury.io/py/lambdazen)
[![Build Status](https://travis-ci.org/brthornbury/lambdazen.svg?branch=master)](https://travis-ci.org/brthornbury/lambdazen)

**What is this?**

A better python lambda syntax for your anonymous function needs. 

Write `a = (x) > x` instead of `a = lambda x: x`. See below for syntax caveats.

Get started immediately: `pip install lambdazen`

```python
from lambdazen import zen
def otherfunc(*args):
    print sum(args)

@zen
def example():
    example.epic = (x, y, z) > otherfunc(x, y, z)

example.epic(1,2,3)
>>> 6
```

**Caveats**
 - better lambdas can only be defined in a function with the `@zen` attribute
 - any other code in this function will be executed, it's best to use the function as a container of lambdas

**How does it work**

[Read the story](https://github.com/brthornbury/lambdazen/blob/master/HowItWorks.md)

TLDR; Runtime in-memory source rewriting and recompilation


### A Better Lambda 

For a long time, I've had a distaste for the syntax of lambda expressions in python. 

```python
add1 = lambda value: value + 1
print add1(1)
>>> 2
```

Compared to syntaxes for the same effect in other languages (like c#), it seems clunky.
```c#
var add1 = (x) => x+1;
Console.WriteLine(add1(1));
>>> 2
```

I struck out to find a way to get a cleaner syntax in python. After a long wrestle, I've found a marginal but satisfying success.

```python
@zen
def _():
    _.add1 = (x) > x + 1

_.add1(1)
>>> 2
```

You might be wondering, what could the `_` function and `zen` attribute possibly be doing to make this work. I'll admit, `_` being needed is not my favorite thing, but it's necessary. 

But wait, before we dig into why it's necessary... let's look at a couple of the interesting options that looked promising for this, but ultimately failed. 

### Infix Operators

My first thoughts went back to c++ days and operator overloads. Research into these in python yielded some interesting results. There's not any native support for operator overloads, but somebody discovered a clever solution taking advantage of hooks into the existing operators `|, <<, >>` to create what they call [infix operators](http://code.activestate.com/recipes/384122-infix-operators/). 

```python
x=Infix(lambda x,y: x*y)
print 2 |x| 4
>>> 8
```

While infix operators are pretty cool, there's no way to get the unevaluated expression on either side of the operator. This leaves us without options for creating any kind of function object with regular looking syntax. 

### Compiled Bytecode rewriting

Python functions all have a [code object](https://late.am/post/2012/03/26/exploring-python-code-objects.html). The code object contains the python compiled bytecode that the interpreter executes. You can see the raw bytecode string using `func.__code__.co_code` or you can use `dis` for a human readable version.

```python
def func():
    return 1

print repr(func.__code__.co_code)
>>> 'd\x01\x00S'

import dis
dis.dis(func)
>>> 2           0 LOAD_CONST               1 (1)
>>>             3 RETURN_VALUE
```

Examining this I thought what if the code object could be changed, would the function then execute differently. As it turns out, code objects are immutable...

```python
def func():
    return 1

func.__code__.co_code = [c if index != 1 else chr(5) for index,c in enumerate(func.__code__.co_code)]
>>> Traceback (most recent call last):
>>>  File "<stdin>", line 1, in <module>
>>> TypeError: readonly attribute
```

But the whole code object can be replaced, which changes the behavior of the function.

```python
def func():
    return 1

def func2():
    return 2

func.__code__ = func2.__code__
print func()
>>> 2
```

At this point I realized it was possible to find patterns in the bytecode and replace them with different patterns, so the basic effect of changing python syntax can be achieved during python runtime. I realized though that this would take a deep understanding of the bytecode, similar to what a compiler might have for source code. 

While replacing the bytecode by [generating code objects](http://stackoverflow.com/questions/16064409/how-to-create-a-code-object-in-python) remains a viable option, I thought exploring uncompiled source rewriting might take less effort being able to take advantage of the python [compiler](https://docs.python.org/2/library/compiler.html) module.

### Zen (Source Rewriting)

Python provides a utility for fetching the raw source code of a function, by reading from the source file (so it doesn't work in the repl unfortunately).

```python
import inspect

def func():
    return 1

print inspect.getsource(func)
>>> 'def func():\n    return 1\n'
```

Using the [compiler](https://docs.python.org/2/library/compiler.html) module you can take advantage of the `parse` function to get an ast. However, for the initial version, I went the easier route of using a regular expression to find and replace the target syntactic pattern. It was enough to get this job done, and in the future we can use an ast to do more complicated source rewrites. 

Using a regular expression the solution is surprisingly just a few lines of python...

```python
def _replace_match(match):
    vars = match.groups(1)[0]
    return "= lambda {0}:".format(vars)

def zen(func):
    # Look for (x, y, ..., z) >
    lambda_syntax_regex = r'=\s*\(([^\)]*)\)\s*>'

    # Get source and replace our lambda syntax with official python lambdas
    source = inspect.getsource(func)
    source = re.sub(lambda_syntax_regex, _replace_match, source)

    # Remove the decorator from the function source, so we don't loop endlessly
    source = re.sub('@zen', '', source)

    # Execute recompiled source in the original scope of the function
    #   locals retains the original scope of the function
    locals = inspect.currentframe().f_back.f_locals
    a = compile(source, '<zen>', 'exec')
    exec(a, locals)
    new_function = locals[func.__name__]

    # Call the new function to bind the lambdas to the intended members on the new_function object
    new_function()

    return new_function
```

Now you can easily write code like this...

```python
def otherFunc(*args):
    print sum(args)

@zen
def lambdaContainer():
    lambdaContainer.func = (x, y, z) > otherFunc(x, y, z)

lambdaContainer.func(1,2,3)
>>> 6
```

Having to hide the new lambda expression under a function is non-ideal but necessary for the moment. Perhaps future research will show more usable patterns. 

Until then, enjoy...
A Better Lambda
~~~~~~~~~~~~~~~

|Build Status|

**What is this?**

A better python lambda syntax for your anonymous function needs.

Write ``a = (x) > x`` instead of ``a = lambda x: x``. See below for
syntax caveats.

Get started immediately: ``pip install lambdazen``

.. code:: python

    from lambdazen import zen
    def otherfunc(*args):
        print sum(args)

    @zen
    def example():
        example.epic = (x, y, z) > otherfunc(x, y, z)

    example.epic(1,2,3)
    >>> 6

**Caveats**

-  better lambdas can only be defined in a function with the ``@zen``
   attribute
-  any other code in this function will be executed, it’s best to use
   the function as a container of lambdas

**How does it work**

`Read the story`_

TLDR; Runtime in-memory source rewriting and recompilation

.. _Read the story: /HowItWorks.md

.. |Build Status| image:: https://travis-ci.org/brthornbury/lambdazen.svg?branch=master
   :target: https://travis-ci.org/brthornbury/lambdazen
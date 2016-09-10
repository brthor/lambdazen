#!/usr/bin/env python
import inspect
import re

def _replace_match(match):
    vars = match.groups(1)[0]
    return "= lambda {0}:".format(vars)

def _zen_decorator(func):
    # Look for (x, y, ..., z) >
    lambda_syntax_regex = r'=\s*\(([^\)]*)\)\s*>'

    source = inspect.getsource(func)
    source = re.sub(lambda_syntax_regex, _replace_match, source)
    source = re.sub('@zen', '', source)

    # Execute recompiled source in the original scope of the function
    #   func_globals retains the original scope of the function
    a = compile(source, '<zen>', 'exec')
    exec(a, func.func_globals)
    new_function = func.func_globals[func.__name__]

    # Call the new function to bind the function assignments
    new_function()

    return new_function

def zen(func):
    return _zen_decorator(func)






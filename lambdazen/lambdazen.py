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

    # remove attribute to prevent looping endlessly
    source = re.sub('\s*@zen\s*\n', '', source)

    # remove leading whitespace
    leading_whitespace_length = len(re.match('\s*', source).group())
    source = '\n'.join(
        [line[leading_whitespace_length:] if len(line) > leading_whitespace_length else line 
        for line in source.split('\n')])

    # Execute recompiled source in the original scope of the function
    #   locals retains the original scope of the function
    locals = inspect.currentframe().f_back.f_back.f_locals
    a = compile(source, '<zen>', 'exec')
    exec(a, locals)
    new_function = locals[func.__name__]

    # Call the new function to bind the function assignments
    new_function()

    return new_function

def zen(func):
    return _zen_decorator(func)






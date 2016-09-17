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

    # Gather the original scope of the function
    frame = inspect.currentframe().f_back.f_back
    globals, locals = frame.f_globals, frame.f_locals
    globals.update(locals)

    # Run the newly compiled source to define the new function
    recompiled_source = compile(source, '<zen>', 'exec')
    exec(recompiled_source, globals)

    # Execute the new function to bind the inner lambdas to the function object attributes
    new_function = globals[func.__name__]
    exec(new_function.__code__, globals)

    return new_function

def zen(func):
    return _zen_decorator(func)

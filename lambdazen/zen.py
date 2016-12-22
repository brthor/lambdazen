#!/usr/bin/env python
from lambdazen.rewriter import ZenFunctionRewriter


def zen(func):
    func_rewriter = ZenFunctionRewriter()
    return func_rewriter.rewrite(func)

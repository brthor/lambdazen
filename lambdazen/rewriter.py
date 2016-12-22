import ast
import inspect
import re

from lambdazen.ast_transformation import FunctionNodeVisitor
from lambdazen.recompiler import RewrittenFunctionRecompiler


class ZenFunctionRewriter(object):
    def __init__(self):
        self.function_node_visitor = FunctionNodeVisitor()
        self.rewritten_function_recompiler = RewrittenFunctionRecompiler()

    def rewrite(self, func):
        source = inspect.getsource(func)

        source = self._remove_leading_whitespace(source)
        source = self._remove_zen_decorator(source)

        code_ast = self._transform_source_ast(source)

        recompiled_func = self.rewritten_function_recompiler.execute(code_ast, func.__name__)
        return recompiled_func

    def _remove_leading_whitespace(self, source):
        leading_whitespace_length = len(re.match('\s*', source).group())
        source = '\n'.join(
            [line[leading_whitespace_length:] if len(line) > leading_whitespace_length else line
             for line in source.split('\n')])

        return source

    def _remove_zen_decorator(self, source):
        source = re.sub('\s*@zen\s*\n', '', source)
        return source

    def _transform_source_ast(self, source):
        code_ast = ast.parse(source)
        code_ast = self.function_node_visitor.visit(code_ast)

        return code_ast
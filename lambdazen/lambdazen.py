#!/usr/bin/env python
import inspect
import re
import compiler, ast, _ast

def _replace_match(match):
    vars = match.groups(1)[0]
    return "= lambda {0}:".format(vars)

def _is_multiline_lambda(function_body_node):
    return type(function_body_node) is _ast.Tuple or type(function_body_node) is _ast.List


def _transform_multiline_assignment_statements(statements):
    assignment_statements = [statement for statement in statements
                             if type(statement) is _ast.BinOp
                             and type(statement.op) is _ast.LShift
                             and type(statement.left) is _ast.Name]

    assignments = [ast.Assign(targets=[statement.left], value=statement.right, lineno=statement.lineno, col_offset=statement.col_offset)
            for statement in assignment_statements]

    for assignment in assignments:
        assignment.targets[0].ctx = ast.Store()

    return assignments


def _transform_multiline_return_statement(return_statement):
    return ast.Return(value=return_statement, lineno=return_statement.lineno, col_offset = return_statement.col_offset)


def _transform_function_arguments(left):
    names = []
    if type(left) is ast.Name:
        names = [left]
    else:
        names = left.elts

    arguments = ast.arguments(args=names, defaults=[])
    for argument in arguments.args:
        argument.ctx = ast.Param()

    return arguments

class FunctionNodeVisitor(ast.NodeTransformer):

    def visit_FunctionDef(self, node):
        """
        :type node: _ast.FunctionDef
        """
        children = node.body
        lambda_assign_children = [child for child in children
                                if type(child) == _ast.Assign
                                    and len(child.targets) == 1
                                    and type(child.targets[0]) is _ast.Attribute
                                    and type(child.targets[0].value) is _ast.Name
                                    and type(child.value) == _ast.Compare
                                    and (type(child.value.left) == _ast.Tuple or type(child.value.left) == _ast.Name)
                                    and all(map(lambda t: type(t) == _ast.Name, getattr(child.value.left, 'elts', [])))]

        for assign_type_child in lambda_assign_children:
            arguments = _transform_function_arguments(assign_type_child.value.left)
            function_body = assign_type_child.value.comparators[0]

            if _is_multiline_lambda(function_body):
                all_statements = function_body.elts

                return_statement = all_statements[-1]
                statements = all_statements[0:-1]

                statements = _transform_multiline_assignment_statements(statements)
                return_statement = _transform_multiline_return_statement(return_statement)

                all_transformed_statements = statements + [return_statement]
                functiondef_object = ast.FunctionDef(args = arguments,
                                                     body=all_transformed_statements,
                                                     lineno=assign_type_child.lineno,
                                                     name=assign_type_child.targets[0].attr,
                                                     col_offset=assign_type_child.col_offset,
                                                     decorator_list=[])

                children.insert(0, functiondef_object)
                assign_type_child.value = ast.Name(id=functiondef_object.name,
                                                   col_offset=functiondef_object.col_offset,
                                                   lineno=functiondef_object.lineno,
                                                   ctx=ast.Load())
            else:
                lambda_ast_transform = ast.Lambda(args=arguments,
                                                  body=function_body,
                                                  lineno=assign_type_child.lineno,
                                                  col_offset = assign_type_child.col_offset)
                assign_type_child.value = lambda_ast_transform

        return node

def _transform_ast(code_ast):
    code_ast = FunctionNodeVisitor().visit(code_ast)
    return code_ast

def _zen_decorator(func):
    source = inspect.getsource(func)

    # remove leading whitespace
    leading_whitespace_length = len(re.match('\s*', source).group())
    source = '\n'.join(
        [line[leading_whitespace_length:] if len(line) > leading_whitespace_length else line
         for line in source.split('\n')])

    # remove attribute to prevent looping endlessly
    source = re.sub('\s*@zen\s*\n', '', source)

    code_ast = ast.parse(source)
    code_ast = _transform_ast(code_ast)

    # Gather the original scope of the function
    frame = inspect.currentframe().f_back.f_back
    globals, locals = frame.f_globals, frame.f_locals
    globals.update(locals)

    # Run the newly compiled source to define the new function
    recompiled_source = compile(code_ast, '<zen>', 'exec')
    exec(recompiled_source, globals)

    new_function = globals[func.__name__]
    return new_function

def zen(func):
    return _zen_decorator(func)

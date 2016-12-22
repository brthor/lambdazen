import ast

import _ast


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

    other_statements = [statement for statement in statements if statement not in assignment_statements]

    assignments = [ast.Assign(targets=[statement.left], value=statement.right, lineno=statement.lineno,
                              col_offset=statement.col_offset)
                   for statement in assignment_statements]

    for assignment in assignments:
        assignment.targets[0].ctx = ast.Store()

    return other_statements + assignments


def _transform_multiline_return_statement(return_statement):
    return ast.Return(value=return_statement, lineno=return_statement.lineno, col_offset=return_statement.col_offset)


def _transform_function_arguments(left):
    if type(left) is ast.Name:
        names = [left]
    else:
        names = left.elts

    # Python3
    if hasattr(_ast, 'arg'):
        args = [_ast.arg(annotation=None, arg=name.id, col_offset=name.col_offset, lineno=name.lineno) for name in
                names]
        return ast.arguments(args=args, defaults=[], kwonlyargs=[], kw_defaults=[])

    # Python 2
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
                                  and type(child.value) == _ast.Compare
                                  and len(child.value.ops) == 1
                                  and type(child.value.ops[0]) in (_ast.Gt, _ast.In)
                                  and (type(child.value.left) == _ast.Tuple or type(child.value.left) == _ast.Name)
                                  and all(map(lambda t: type(t) == _ast.Name, getattr(child.value.left, 'elts', [])))]

        # Support single line lambdas outside of assigns
        other_children = [child for child in children if child not in lambda_assign_children]
        for child in other_children:
            CompareNodeVisitor().visit(child)

        for assign_type_child in lambda_assign_children:
            arguments = _transform_function_arguments(assign_type_child.value.left)
            function_body = assign_type_child.value.comparators[0]

            if _is_multiline_lambda(function_body):
                all_statements = function_body.elts

                return_statement = all_statements[-1]
                statements = all_statements[0:len(all_statements) - 1]

                statements = _transform_multiline_assignment_statements(statements)
                return_statement = _transform_multiline_return_statement(return_statement)

                assign_target = assign_type_child.targets[0]
                if type(assign_target) is _ast.Attribute:
                    function_name = assign_target.attr
                else:
                    function_name = assign_target.id

                all_transformed_statements = statements + [return_statement]
                functiondef_object = ast.FunctionDef(args=arguments,
                                                     body=all_transformed_statements,
                                                     lineno=assign_type_child.lineno,
                                                     name=function_name,
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
                                                  col_offset=assign_type_child.col_offset)
                assign_type_child.value = lambda_ast_transform

        return node


class CompareNodeVisitor(ast.NodeTransformer):
    def visit_Compare(self, node):
        # type: (_ast.CompareNode) -> ast.Lambda

        is_lambda_def = len(node.ops) == 1 \
                        and type(node.ops[0]) is _ast.Gt \
                        and (type(node.left) is _ast.Tuple or type(node.left) is _ast.Name) \
                        and all(map(lambda t: type(t) == _ast.Name, getattr(node.left, 'elts', [])))

        if not is_lambda_def:
            return node

        arguments = _transform_function_arguments(node.left)
        function_body = node.comparators[0]

        lambda_ast_transform = ast.Lambda(args=arguments,
                                          body=function_body,
                                          lineno=node.lineno,
                                          col_offset=node.col_offset)
        return lambda_ast_transform

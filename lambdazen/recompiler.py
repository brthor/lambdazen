import inspect


class RewrittenFunctionRecompiler(object):
    zen_decorator_name = 'zen'

    def execute(self, code_ast, function_name):
        scope = self._gather_original_scope_for_exec_in_dict()

        recompiled_source = compile(code_ast, '<zen>', 'exec')
        exec (recompiled_source, scope)

        new_function = scope[function_name]
        return new_function

    def _gather_original_scope_for_exec_in_dict(self):
        """
        It may seem surprising that this function collapses the local and global scope of the original function into a
        single scope, but unfortunately when `exec` is provided with local and global scope dictionaries, it treats the
        recompiled function as if it were a class function effectively inserting an argument into the function
        definition (self).

        When the scope is collapsed into a single dict, the correct behavior seems to be retained with respect to module,
        (as shown by tests).
        It is possible this will be an area of trouble in cases not yet covered by the tests.
        """
        zen_frame = self._find_zen_frame()
        zen_frame_globals, zen_frame_locals = zen_frame.f_globals, zen_frame.f_locals

        zen_frame_full_scope = dict(**zen_frame_globals)
        zen_frame_full_scope.update(zen_frame_locals)

        return zen_frame_full_scope

    def _find_zen_frame(self, current_frame=None):
        current_frame = current_frame or inspect.currentframe()
        current_frame_name = current_frame.f_code.co_name.replace('co_name:', '')
        current_frame_is_zen = current_frame_name.startswith(self.zen_decorator_name)

        return current_frame_is_zen and current_frame.f_back or self._find_zen_frame(current_frame.f_back)

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

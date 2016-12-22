import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from lambdazen import zen

module_var = "module_var"

class GivenAZenDecorator(unittest.TestCase):
    def test_It_supports_nested_lambdas(self):
        self.skipTest("TODO: nested lambdas not yet supported")

        @zen
        def lambdaContainer():
            l = (x) > ((y) > (y + x))
            self.assertTrue(l(1)(3) == 4)

        lambdaContainer()

    def test_It_creates_functions_from_alternate_lambda_syntax(self):

        @zen
        def lambdaContainer():
            lambdaContainer.func = (x) > x + 1

            lambdaContainer.x = (y) in y+1

        lambdaContainer()

        def emptyFunction():
            pass

        self.assertTrue(type(lambdaContainer.func) == type(emptyFunction))
        self.assertTrue(lambdaContainer.func(1) == 2)
        self.assertTrue(lambdaContainer.func(2) == 3)
        self.assertTrue(lambdaContainer.func(3) == 4)

    def test_It_creates_lists_of_single_line_lambdas(self):

        @zen
        def normalizeString(nS):
            transforms = [
                (s) > s.strip(),
                (s) > s.lower(),
                (s) > s.replace(' ', '_')]

            apply_all = (transforms_list, s) > (
                is_done << (len(transforms_list) == 0),
                current_transform << (transforms_list[0] if not is_done else None),
                remaining_transforms << (transforms_list[1:] if not is_done else None),
                current_transform(apply_all(remaining_transforms, s)) if not is_done else s)

            return apply_all(transforms, nS)

        self.assertTrue(normalizeString("Abraham Lincoln") == "abraham_lincoln")



    def test_It_creates_functions_from_nonbound_lambda_assigns(self):

        @zen
        def lambdaContainer():
            nonBound = (x) > x + 1
            nonBoundIn = (x) in x + 1

            self.assertTrue(nonBound(1) == 2)
            self.assertTrue(nonBoundIn(1) == 2)

        lambdaContainer()

    def test_It_creates_functions_that_can_use_local_scope(self):
        @zen
        def lambdaContainer(local_var):
            lambdaContainer.func = (y) > y + local_var

        lambdaContainer(2)
        self.assertTrue(lambdaContainer.func(2) == 4)

    def test_It_creates_functions_out_of_multiline_syntax(self):
        outer_var = 's'

        @zen
        def lambdaContainer():
            lambdaContainer.func = (x, y, z) > (
                s << x + y + z,
                s
            )

            lambdaContainer.func2 = (x, y, z) > [
                s << x + y + z,
                s
            ]

            lambdaContainer.outerFunc = () > (
                s << outer_var,
                s
            )

            lambdaContainer.moduleFunc = () > (
                s << module_var,
                s
            )

            lambdaContainer.combinedScopeFunc = (x) > (
                s << module_var + outer_var + x,
                s
            )

            lambdaContainer.singleLineTest = () > (
                1
            )

            lambdaContainer.multiLineInTest = (x) in (
                s << x + 1,
                s
            )

            lambdaContainer.singleLineInTest = (x) in (
                x + 1
            )

            nonBoundLambdaTest = () > (
                s << "yes",
                s)

            self.assertTrue(nonBoundLambdaTest() == "yes")

        lambdaContainer()

        self.assertTrue(lambdaContainer.func(1,2,3) == 6)
        self.assertTrue(lambdaContainer.func2(1, 2, 3) == 6)
        self.assertTrue(lambdaContainer.outerFunc() == outer_var)
        self.assertTrue(lambdaContainer.moduleFunc() == module_var)
        self.assertTrue(lambdaContainer.combinedScopeFunc("t") == (module_var + outer_var + "t"))
        self.assertTrue(lambdaContainer.singleLineTest() == 1)
        self.assertTrue(lambdaContainer.multiLineInTest(1) == 2)
        self.assertTrue(lambdaContainer.singleLineInTest(1) == 2)

    def test_It_creates_functions_with_multiple_arguments(self):
        
        @zen
        def lambdaContainer():
            lambdaContainer.func = (x, y, z) > x + y + z

        lambdaContainer()

        self.assertTrue(lambdaContainer.func(1,3,5) == 9)

    def test_It_creates_functions_with_no_arguments(self):
        @zen
        def lambdaContainer():
            lambdaContainer.func = () > "hello"
            lambdaContainer.func2 = () in "hello"

        lambdaContainer()

        self.assertTrue(lambdaContainer.func() == "hello")
        self.assertTrue(lambdaContainer.func2() == "hello")

    def test_It_creates_functions_that_call_other_functions(self):
        def otherfunc(*args):
            return sum(args)

        @zen
        def lambdaContainer():
            lambdaContainer.func = (x, y, z) > otherfunc(x,y,z)

        lambdaContainer()

        self.assertTrue(lambdaContainer.func(1,5,7) == 13)

    def test_It_creates_functions_that_call_other_functions_when_nested_in_another_function(self):

        def outer():
            def otherfunc(*args):
                return sum(args)

            @zen
            def lambdaContainer():
                lambdaContainer.func = (x, y, z) > otherfunc(x,y,z)

            lambdaContainer()

            self.assertTrue(lambdaContainer.func(1,5,7) == 13)

        outer()

    def test_It_creates_multiple_functions(self):
        @zen
        def lambdaContainer():
            lambdaContainer.func = () > "hello"
            lambdaContainer.func2 = (x) > x + 1
            lambdaContainer.func3 = (x) > x * 2

        lambdaContainer()

        self.assertTrue(lambdaContainer.func() == "hello")
        self.assertTrue(lambdaContainer.func2(1) == 2)
        self.assertTrue(lambdaContainer.func3(5) == 10)

    def test_It_creates_functions_that_use_values_outside_function_scope(self):
        outer_var = 5

        @zen
        def lambdaContainer():
            lambdaContainer.func = () > outer_var
            lambdaContainer.func2 = (x) > outer_var + x

        lambdaContainer()

        self.assertTrue(lambdaContainer.func() == 5)
        self.assertTrue(lambdaContainer.func2(5) == 10)

    def test_It_creates_functions_that_use_values_in_module_scope(self):
        outer_var = "s"

        @zen
        def lambdaContainer():
            lambdaContainer.func = () > module_var
            lambdaContainer.func2 = (x) > module_var + outer_var + x

        lambdaContainer()

        self.assertTrue(lambdaContainer.func() == "module_var")
        self.assertTrue(lambdaContainer.func2("t") == "module_varst")

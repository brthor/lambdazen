import unittest
from lambdazen import zen

module_var = "module_var"

class GivenAZenDecorator(unittest.TestCase):
    def test_It_creates_functions_from_alternate_lambda_syntax(self):

        @zen
        def lambdaContainer():
            lambdaContainer.func = (x) > x + 1

        def emptyFunction():
            pass

        self.assertTrue(type(lambdaContainer.func) == type(emptyFunction))
        self.assertTrue(lambdaContainer.func(1) == 2)
        self.assertTrue(lambdaContainer.func(2) == 3)
        self.assertTrue(lambdaContainer.func(3) == 4)

    def test_It_creates_functions_out_of_multiline_syntax(self):

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

        self.assertTrue(lambdaContainer.func(1,2,3) == 6)
        self.assertTrue(lambdaContainer.func2(1, 2, 3) == 6)

    def test_It_creates_functions_with_multiple_arguments(self):
        
        @zen
        def lambdaContainer():
            lambdaContainer.func = (x, y, z) > x + y + z

        self.assertTrue(lambdaContainer.func(1,3,5) == 9)

    def test_It_creates_functions_with_no_arguments(self):
        @zen
        def lambdaContainer():
            lambdaContainer.func = () > "hello"

        self.assertTrue(lambdaContainer.func() == "hello")

    def test_It_creates_functions_that_call_other_functions(self):
        def otherfunc(*args):
            return sum(args)

        @zen
        def lambdaContainer():
            lambdaContainer.func = (x, y, z) > otherfunc(x,y,z)

        self.assertTrue(lambdaContainer.func(1,5,7) == 13)

    def test_It_creates_functions_that_call_other_functions_when_nested_in_another_function(self):

        def outer():
            def otherfunc(*args):
                return sum(args)

            @zen
            def lambdaContainer():
                lambdaContainer.func = (x, y, z) > otherfunc(x,y,z)

            self.assertTrue(lambdaContainer.func(1,5,7) == 13)

        outer()

    def test_It_creates_multiple_functions(self):
        @zen
        def lambdaContainer():
            lambdaContainer.func = () > "hello"
            lambdaContainer.func2 = (x) > x + 1
            lambdaContainer.func3 = (x) > x * 2

        self.assertTrue(lambdaContainer.func() == "hello")
        self.assertTrue(lambdaContainer.func2(1) == 2)
        self.assertTrue(lambdaContainer.func3(5) == 10)

    def test_It_creates_functions_that_use_values_outside_function_scope(self):
        outer_var = 5

        @zen
        def lambdaContainer():
            lambdaContainer.func = () > outer_var
            lambdaContainer.func2 = (x) > outer_var + x

        self.assertTrue(lambdaContainer.func() == 5)
        self.assertTrue(lambdaContainer.func2(5) == 10)

    def test_It_creates_functions_that_use_values_in_module_scope(self):
        outer_var = "s"

        @zen
        def lambdaContainer():
            lambdaContainer.func = () > module_var
            lambdaContainer.func2 = (x) > module_var + outer_var + x

        self.assertTrue(lambdaContainer.func() == "module_var")
        self.assertTrue(lambdaContainer.func2("t") == "module_varst")




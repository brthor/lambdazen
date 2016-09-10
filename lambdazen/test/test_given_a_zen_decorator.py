import unittest
from lambdazen import zen

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

    def test_It_creates_functions_with_multiple_arguments(self):
        
        @zen
        def lambdaContainer():
            lambdaContainer.func = (x,y,z) > x + y + z

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
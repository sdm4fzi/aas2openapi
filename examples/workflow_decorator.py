import functools


class Middleware(object):
    def __init__(self, arg0):
        print("Inside decoratorClass.__init__()")
        self.arg0 = arg0

    def workflow(self, *args):
        def wrap(f):
            print("Inside wrap()")
            @functools.wraps(f)
            def wrapped_f(*args):
                print("Inside wrapped_f()")
                print("Decorator arguments:", *args)
                f(*args)
                print("After f(*args)")
                print("Decorator class arguments:", self.arg0)
            print("Returning wrapped_f")
            # TODO: the wrapped_f should also be used in the middleware to register the workflow in the API
            return wrapped_f
        return wrap
    
    def no_argument_worklow(self, *args):
        def wrap(f):
            print("Inside wrap()")
            @functools.wraps(f)
            def wrapped_f(*args):
                print("Inside wrapped_f()")
                print("Decorator arguments:", *args)
                f(*args)
                print("After f(*args)")
                print("Decorator class arguments:", self.arg0)
            return functools.partial(wrapped_f, *args)
        return wrap
    

middleware = Middleware("arg000")

# TODO: implement workflows like this -> function decorator, where the arguments, that shall be injected are provided
# as arguments to the decorator. The decorator will then inject the arguments into the function.

@middleware.workflow("hello", "world", 42)
def sayHello(a1, a2, a3, a4):
    print('sayHello arguments:', a1, a2, a3, a4)


print("After decoration")

print("Preparing to call sayHello()")
sayHello("say", "hello", "argument", "list")
print("after first sayHello() call")
sayHello("a", "different", "set of", "arguments")
print("after second sayHello() call")

@middleware.no_argument_worklow("hello", "world", 42)
def sayHello(a1, a2, a3, a4):
    print('sayHello arguments:', a1, a2, a3, a4)


print("After decoration")

print("Preparing to call sayHello()")
sayHello(43)
print("after first sayHello() call")
sayHello(41)
print("after second sayHello() call")

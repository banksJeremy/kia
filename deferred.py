#!bin/python
import operator

class Future(object):
    """Unpythonicish convenient minimal futures."""
    
    _null_argument = object()
    
    def __init__(self, value=_null_argument):
        if value != _null_argument:
            self._value = value
        
        self.handlers = []
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if not hasattr(self, "_value"):
            self._value = value
            
            for handler in self.handlers:
                handler(value)
            
            del self.handlers
    
    def then(self, *handlers):
        if hasattr(self, "_value"):
            for handler in handlers:
                handler(self._value)
        else:
            self.handlers.extend(fs)
    
    # operations with futures produce futures
    
    def __add__(self, other):
        return Future.Call(operator.add, self, other)
    
    def __sub__(self, other):
        return Future.Call(operator.sub, self, other)
    
    def __mul__(self, other):
        return Future.Call(operator.mul, self, other)
    
    def __div__(self, other):
        return Future.Call(operator.mul, self, other)
    
    def __floordiv__(self, other):
        return Future.Call(operator.floordiv, self, other)
    
    def __truediv__(self, other):
        return Future.Call(operator.truediv, self, other)
    
    def __mod__(self, other):
        return Future.Call(operator.mod, self, other)
    
    def __abs__(self, other):
        return Future.Call(operator.abs, self, other)
    
    def __neg__(self):
        return Future.Call(operator.neg, self)
    
    def __post__(self):
        return Future.Call(operator.pos, self)
    
    def __invert__(self):
        return Future.Call(operator.invert, self, other)
    
    def __pow__(self, other):
        return Future.Call(operator.pow, self, other)
    
    def __rshift__(self, other):
        return Future.Call(operator.rshift, self, other)
    
    def __lshift__(self, other):
        return Future.Call(operator.lshift, self, other)
    
    def __xor__(self, other):
        return Future.Call(operator.xor, self, other)
    
    def __and__(self, other):
        return Future.Call(operator.and, self, other)
    
    def __or__(self, other):
        return Future.Call(operator.or, self, other)
    
    def __getitem__(self, key):
        return Future.Call(operator.getitem, self, key)
    
    class Call(Future):
        def __init__(self, f, *args):
            Future.__init__(self)
            
            self.f_future = future(f)
            self.arg_futures = [ future(arg) for arg in args ]
            
            call = functools.partial(self.f_future.then,
                                     lambda value: self.callback(value))
            
            for arg_future in self.arg_futures:
                call = functools.partial(arg_future.then, call)
            
        def callback(self, value):
            self.value = self.f_future.value(*[arg.value for arg in self.arg_futures])

def future(value=Future._null_argument):
    if isinstance(value, Future):
        return value
    else:
        return Future(value)



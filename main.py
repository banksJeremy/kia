#!bin/python
import functools
import greenlet

class Generator(object):
    """A greenlet-based generator implementation.
    
    Use the @generator decorator on a function using the generate() function
    to yield values. .next() and .send() behave as the built-in. Non-generator
    functions called from generators can call generate() themselves, allowing
    things like generate_from(), which behaves like the proposed "yield from"
    keyword. """
    
    def __init__(self, f, *a, **kw):
        self.f = f
        self.a = a
        self.kw = kw
        
        self.greenlet = greenlet.greenlet(self.__switched_out_call)
        self.greenlet.switch() # will immidiately switch out
    
    def __iter__(self):
        return self
    
    def __switched_out_call(self):
        greenlet.getcurrent().parent.switch()
        self.f(*self.a, **self.kw)
    
    def next(self):
        return self.send(None)
    
    def send(self, value):
        result = self.greenlet.switch(value)
        
        if self.greenlet.dead:
            raise StopIteration()
        else:
            return result

def generator(f):
    return functools.partial(Generator, f)

def generate(value):
    return greenlet.getcurrent().parent.switch(value)

def generate_from(iterable):
    # Generates all of the values from a generator, returning the last value
    # passed into the generator.
    
    result = None
    
    for value in iterable:
        result = generate(value)
    
    return result

@generator
def oneTo(n):
    for x in range(1, n + 1):
        generate(x)

@generator
def oneTwo(n, m):
    generate_from(oneTo(n))
    generate_from(oneTo(m))
    generate_from([10, 20])

print list(oneTwo(10, 5))

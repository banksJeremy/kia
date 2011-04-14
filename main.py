#!bin/python
import functools
import greenlet

class Generator(object):
    def __init__(self, f, *a, **kw):
        self.greenlet = greenlet.greenlet(functools.partial(f, *a, **kw))
    
    def __iter__(self):
        return self
    
    def next(self):
        value = self.greenlet.switch()
        
        if self.greenlet.dead:
            raise StopIteration()
        else:
            return value

def generate(value):
    return greenlet.getcurrent().parent.switch(value)

def generator(f):
    return functools.partial(Generator, f)

@generator
def oneToTen():
    for x in range(1, 11):
        generate(x)

print list(oneToTen())

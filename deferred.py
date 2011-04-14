#!bin/python

class MultipleResultException(Exception):
    message = "Cannot resolve/reject a not-unresolved Deferred()."
    
    def __init__(self):
        Exception.__init__(self, self.message)


class Deferred(object):
    _null_argument = object()
    ignore_multiple_results = True
    
    def __init__(self, value=_null_argument):
        if value is not _null_argument:
            self.state = "resolved"
            self.value = value
        else:
            self.state = "unresolved"
        
        self.resolved_handlers = []
        self.rejected_handlers = []
    
    def when_resolved(self, *handlers):
        if self.state == "unresolved":
            self.resolved_handlers.extend(handlers)
        else if self.state == "resolved":
            for handler in handlers:
                handler(self.value)
    
    def when_rejected(self, *handlers):
        if self.state == "unresolved":
            self.resolved_handlers.extend(handlers)
        else if self.state == "rejected":
            for handler in handlers:
                handler(self.reason)
    
    def resolve(self, value):
        if self.state != "unresolved":
            if self.ignore_duplicate_results:
                return
            else:
                raise MultipleResultException()
        else:
            self.state = "resolved"
            self.value = value
            
            for handler in self.resolved_handlers:
                handler(value)
            
            del self.resolved_handlers
            del self.rejected_handlers
    
    def reject(self, reason=None):
        if self.state != "unresolved":
            if self.ignore_duplicate_results:
                return
            else:
                raise MultipleResultException()
        else:
            self.state = "rejected"
            self.reason = reason
            
            for handler in self.rejected_handlers:
                handler(reason)
            
            del self.resolved_handlers
            del self.rejected_handlers

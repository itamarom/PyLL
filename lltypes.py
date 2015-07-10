
class LLVar(object):

    @property
    def value(self):
        print "a"
        return self._value
        
    @value.setter
    def value(self, new_value):
        print "b"
        self._validate_type(new_value)
        self._value = new_value
     
    def _validate_type(self, new_value):
        raise NotImplementedError()

class LLPointer(LLVar):
    def __init__(self, value):
        self.value = value
        
    def _validate_type(self, value):
        assert(value is None or type(value).__name__ == self.obj_type.__name__)

class LLInt(LLVar):
    def __init__(self, value):
        value = int(value)
        self.value = value
        
    def _validate_type(self, value):
        assert(type(self).MIN <= value <= type(self).MAX)
        
class I32(LLInt):
    MIN = 0
    MAX = 2 ** 32
    
class I8(LLInt):
    MIN = 0
    MAX = 2 ** 8

def get_type(name):
    if name in TYPES:
        return TYPES[name]
        
    if name.endswith('*'):
        return type(name.replace("*", "Pointer"), (LLPointer, ), { 'obj_type': get_type(name[:-1])})

    raise LLTypeNotFound("Could not find type: '%s'" % name)
        
TYPES = {}
TYPES['i32'] = I32
TYPES['i8'] = I8
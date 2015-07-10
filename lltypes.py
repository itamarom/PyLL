class LLType(object):
    name = None
    size = None
        
    @classmethod
    def create(cls):
        return bytearray(cls.size)
        
class I32(LLType):
    name = 'i32'
    size = 4
        
class I8(LLType):
    name = 'i8'
    size = 1

def get_type(name):
    if name in TYPES:
        return TYPES[name]
    
    raise LLTypeNotFound("Could not find type: '%s'" % name)
        
TYPES = {}
TYPES['i32'] = I32
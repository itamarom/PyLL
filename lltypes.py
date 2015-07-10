class LLType(object):
    name = None
   
class LLPointerType(LLType):
    def __init__(self, obj):
        self.name = obj.name + "*"
        self.obj = obj

    @classmethod
    def intialize(cls, obj):
        return LLPointerType(obj)
    
class LLBufferType(LLType):
    size = None
        
    @classmethod
    def create(cls):
        return bytearray(cls.size)
        
class I32(LLBufferType):
    name = 'i32'
    size = 4
    
    @classmethod
    def intialize(cls, value):
        obj = cls.create()
        struct.pack_into('I', obj, 0, int(value))
        return obj
        
class I8(LLBufferType):
    name = 'i8'
    size = 1
    
    @classmethod
    def intialize(cls, value):
        obj = cls.create()
        struct.pack_into('b', obj, 0, int(value))
        return obj

def get_type(name):
    if name in TYPES:
        return TYPES[name]
    
    raise LLTypeNotFound("Could not find type: '%s'" % name)
        
TYPES = {}
TYPES['i32'] = I32
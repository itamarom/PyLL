class LLType(object):
    name = None
    size = None
        
    @classmethod
    def create(cls):
        return bytearray(cls.size)
        
class I32(LLType):
    name = 'i32'
    size = 4
    def __init__(self):

        LLType.__init__('i32', 4)

def get_type(name):
    if name in TYPES:
        return TYPES[name]
    
    raise LLTypeNotFound("Could not find type: '%s'" % name)
        
TYPES = {}
TYPES['i32'] = I32
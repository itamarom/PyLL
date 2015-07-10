class LLType(object):
    def __init__(self, name, size):
        self.name = name
        self.size = size
        
    def create(self):
        return bytearray(self.size)
        
        
class I32(LLType):
    def __init__(self):
        LLType.__init__('i32', 4)
        
def get_type(name):
    if name in TYPES:
        return TYPES[name]
    
    raise LLTypeNotFound("Could not find type: '%s'" % name)
        
TYPES = {}
TYPES['i32'] = I32
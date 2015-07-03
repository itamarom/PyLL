class Program(object):
    
    def __init__(self, unknown, globs, funcs, attribs):
        self.unknown = unknown
        self.globs = globs
        self.funcs = funcs
        self.attribs = attribs
        
        self.callstack = []
        self.current_inst = None
        
    def run(self, entry_point='main', args=None):
        self.current_inst = (self.funs[entry_point], 0, {})
        
        while True:
            self._exec_inst()
            
            
    def _exec_inst(self):
        raise NotImplementedError()
      
    
        
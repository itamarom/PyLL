class Program(object):
    
    def __init__(self, unknown, globs, funcs, attr):
        self.unknown = unknown
        self.globs = globs
        self.funcs = funcs
        self.attr = attr
        
        self.callstack = []
        self.current_instruction = None
        
    def run(self, entry_point='main', args=None):
        self.current_instruction = (self.functions[entry_point], 0)
        
        while True:
            self._exec_inst()
            
            
    def _exec_inst(self):
        raise NotImplementedError()
      
    
        
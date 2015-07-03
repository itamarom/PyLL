class Program(object):
    
    def __init__(self, unknown, globs, funcs, attribs):
        self.unknown = unknown
        self.globs = globs
        self.funcs = funcs
        self.attribs = attribs
        
        self.callstack = []
        self.current_inst = None
        
    def run(self, entry_point='main', args=None):
        self.current_inst = (self.funcs[entry_point], 0, {})
        
        while True:
            self._exec_inst()
            
            
    def _exec_inst(self):
        RESULT_OPCODE_PATTERN = r"%\w+\s*=\s*"
        func, op_index, scope = self.current_inst
        op_text = func['content'][op_index]
        
        if re.findall(RESULT_OPCODE_PATTERN, op_text) and
           op_text.find(re.findall(RESULT_OPCODE_PATTERN, op_text)[0]) == 0:
           
           dest, opcode = op_text.split('=', 1)
        
      
        self.current_inst = func, op_index+1, scope
    
        
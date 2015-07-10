import re
from opcodes import RESULT_OPCODES, OPCODES

class OpcodeNotSupported(Exception):
    def __init__(self, opcode_text):
        self.opcode_text = opcode_text
        Exception.__init__(self, 'Opcode not supported: "%s"' % opcode_text)

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
        op_text = func['content'][op_index].strip()
        
        if not op_text:
            self.current_inst = func, op_index+1, scope
            return
        
        if re.findall(RESULT_OPCODE_PATTERN, op_text) and \
            op_text.find(re.findall(RESULT_OPCODE_PATTERN, op_text)[0]) == 0:
            
            dest, opcode = map(str.strip, op_text.split('=', 1))
            opcode_name, params = opcode.split(' ', 1)
            
            if opcode_name in RESULT_OPCODES:
                RESULT_OPCODES[opcode_name](self, dest, params)
            else:
                raise OpcodeNotSupported(opcode)
                
        else:
            opcode_name, params = op_text.split(' ', 1)
            if opcode_name in OPCODES:
                OPCODES[opcode_name](self, params)
            else:
                raise OpcodeNotSupported(opcode)

        self.current_inst = func, op_index+1, scope
        

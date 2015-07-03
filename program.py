import re

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
            
            dest, opcode = op_text.split('=', 1)
            
            if opcode.startswith('alloca'):
                Opcodes.alloca(self, dest, opcode.split(' ', 1)[1])
            if opcode.startswith('call'):
                Opcodes.call(self, dest, opcode.split(' ', 1)[1])
            else:
                raise OpcodeNotSupported(op_text)
                
        else:
            if op_text.startswith('store'):
                Opcodes.call(pasten)
            else:
                raise OpcodeNotSupported(op_text)

        self.current_inst = func, op_index+1, scope
        
class Opcodes(object):

    @staticmethod
    def alloca(program, dest, operands):
        raise NotImplementedError()
        # %1 = alloca i32, align 4
        operands = operands.split(',')
        program.current_inst[2][dest] = '\x00' * TYPES[operands[0]].size

    @staticmethod
    def store(program, *args, **kwargs):
        # Implemented by Amit
        pass

    @staticmethod
    def call(program, *args, **kwargs):
        # Implemented by Gitlitz
        pass


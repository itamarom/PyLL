import re
from types import get_type
RESULT_OPCODES = {}
OPCODES = {}
    
class InvalidOpcodeArguments(Exception):
    def __init__(self, opcode_name, params, result_var=None):
        self.opcode_name = opcode_name
        self.params = params
        if result_var:
            Exception.__init__(self, 'Invalid args passed to opcode "%s": %s' % (opcode_name, str(params))
        else:
            Exception.__init__(self, 'Invalid args passed to opcode "%s": %s, resultvar=%s' % \
                                     (opcode_name, str(params), result_var)
    
def result_opcode(func):
    RESULT_OPCODES[func.__name__] = func
    return func

def opcode(func):
    OPCODES[func.__name__] = func
    return func

@result_opcode
def alloca(program, result_var, params):
    # TODO: Do something with align?
    ALLOCA_RE = r"(?P<type>[\w\d]+),\s*align\s+(?P<alignment>\d)"
    
    result = re.match(line)
    if not result:
        raise InvalidOpcodeArguments("alloca", params, result_var)
        
    values = result.groupdict()
    
    scope = program.current_inst[2]
    
    if dest in scope:
        # TODO: Maybe this should throw an exception?
        pass
    
    scope[dest] = get_type(operands[0]).create()
    program.inc_inst()
    print "ALLOCA dest: '%s', operands: '%s'" % (result_var, str(params))
    
@opcode
def store(program, params):
    # Implemented by Amit
    print "STORE", params
    
@result_opcode
def load(program, result_var, params):
    # Implemented by Amit
    print "LOAD dest: '%s', operands: '%s'" % (result_var, str(params))

@result_opcode
def call(program, result_var, params):
    # Implemented by Gitlitz0
    print "%s = CALL %s" % (result_var, params)

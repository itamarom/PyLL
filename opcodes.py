import re
from lltypes import get_type
import debug
RESULT_OPCODES = {}
OPCODES = {}

class InvalidOpcodeArguments(Exception):
    def __init__(self, opcode_name, params, result_var=None):
        self.opcode_name = opcode_name
        self.params = params
        if result_var:
            Exception.__init__(self, 'Invalid args passed to opcode "%s": %s' % (opcode_name, str(params)))
        else:
            Exception.__init__(self, 'Invalid args passed to opcode "%s": %s, resultvar=%s' % \
                                     (opcode_name, str(params), result_var))
    
def result_opcode(func):
    RESULT_OPCODES[func.__name__] = func
    return func

def opcode(func):
    OPCODES[func.__name__] = func
    return func

@result_opcode
@debug.log
def alloca(program, result_var, params):
    # TODO: Do something with align?
    ALLOCA_RE = r"(?P<type>[\w\d]+),\s*align\s+(?P<alignment>\d)"
    
    result = re.match(ALLOCA_RE, params)
    if not result:
        raise InvalidOpcodeArguments("alloca", params, result_var)
        
    values = result.groupdict()
    
    if result_var in program.state.scope:
        # TODO: Maybe this should throw an exception?
        pass
    
    program.state.scope[result_var] = get_type(values['type']).create()
    program.inc_inst()
    
@opcode
@debug.log
def store(program, params):
    # Implemented by Amit
    program.inc_inst()

@result_opcode
@debug.log
def load(program, result_var, params):
    # Implemented by Amit
    program.inc_inst()

@result_opcode
@debug.log
def call(program, result_var, params):
    # Implemented by Gitlitz0
    program.inc_inst()

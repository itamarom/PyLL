from lltypes import get_type
from utils import find_closing
from program import ProgramState
import debug
import re

RESULT_OPCODES = {}
OPCODES = {}

STORE_PATTERN = re.compile(r"(?P<src_type>\w*)\s+(?P<src>[%@]?\w+)\s*,\s*(?P<dest_type>\w*\*?)\s+(?P<dest>[%@]?\w+)\s*(,\s*align\s+(?P<alignment>\d+))?$")
ALLOCA_PATTERN = re.compile(r"(?P<type>[\w\d]+),\s*align\s+(?P<alignment>\d)")
CALL_PATTERN = re.compile(r"(?P<type>[\w\d]+)\s+(?P<params_type>\(.*\)\*\s+)?(?P<name>@\w+)\((?P<params>.*)\)")

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
    result = ALLOCA_PATTERN.match(params)
    
    if not result:
        raise InvalidOpcodeArguments("alloca", params, result_var)

    values = result.groupdict()
    
    if result_var in program.state.scope:
        # TODO: Maybe this should throw an exception?
        pass
    
    allocated = get_type(values['type'])()
    allocated = get_type(values['type'])()
    ptr = get_type(value['type'] + "*")()
    ptr.value = allocated
    
    program.state.scope[result_var] = ptr
    program.inc_inst()

@opcode
@debug.log
def store(program, params):
    # Implemented by Amit
    #result = STORE_PATTERN.match()
    #
    #if result is None:
    #    raise InvalidOpcodeArguments('store', params)
    #
    #values = result.groupdict()
    #
    #src = values['src']
    #if src.startswith('%') or src.startswith('@'):  # TODO: use var pattern
    #    pass

    program.inc_inst()

@result_opcode
@debug.log
def load(program, result_var, params):
    # Implemented by Amit
    program.inc_inst()
    
@result_opcode
@debug.log
def call(program, result_var, params):
    # call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([13 x i8]* @.str, i32 0, i32 0))
    result = CALL_PATTERN.match(params)
    
    if not result:
        raise InvalidOpcodeArguments("call", params, result_var)
        
    values = result.groupdict()
    
    func_type = values['type']
    func_params_type = values['params_type']
    func_name = values['name']
    func_params = values['params']
    
    if values['name']
    
    program.callstack.push(program.state)
    program.state = ProgramState()

from lltypes import get_type
import struct
from utils import find_closing
from program_state import ProgramState
import debug
import re

RESULT_OPCODES = {}
OPCODES = {}

STORE_PATTERN = re.compile(r"(?P<src_type>\w*)\s+(?P<src>[%@]?\w+)\s*,\s*(?P<dest_type>\w*)\*\s+(?P<dest>[%@]?\w+)\s*(?:,\s*align\s+(?P<alignment>\d+))?$")
INTEGER_VALUE = re.compile(r"\d+")
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

class InvalidLLValue(Exception):
    def __init__(self, value):
        self.value = value
        Exception.__init__(self, 'Could not parse value: {}'.format(value))

class FuncNotFoundError(Exception):
    def __init__(self, func_name):
        self.func_name = func_name
        Exception.__init__(self, 'Could not find function named "%s"' % func_name)

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

    allocated = get_type(values['type'])(None)
    ptr = get_type(values['type'] + "*")(None)
    ptr.value = allocated

    program.state.scope[result_var] = ptr
    program.inc_inst()

@opcode
@debug.log
def store(program, params):
    # Implemented by Amit
    result = store_pattern.match()

    if result is None:
        raise InvalidOpcodeArguments('store', params)

    values = result.groupdict()

    src = values['src']
    src_type = get_type(values['src_type'])
    try:
        src_var = program.get_var(src)  # TODO: validate type?
    except InvalidVarName:
        src_var = src_type(src)

    dest_type = get_type(values['dest_type'])
    dest_var = program.get_var(values['dest']).value

    if dest_type is src_type:
        dest_var.value = src_var.value
    elif issubclass(dest_type, LLInt) and issubclass(src_type, LLInt):
        dest_var.value = src_var.value  # TODO: deal with different sizes

    print("STORE", params)

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

    program.callstack.append(program.state)

    if values['name'] in program.funcs:
        program.state = ProgramState(program.funcs[values['name']], result_var=result_var)
    else:
        raise FuncNotFoundError(values['name'])

@opcode
@debug.log
def ret(program, params):
    # ret i32 0
    return_type, return_value = params.split()
    return_obj = get_type(return_type)(return_value)

    # TODO: Should we access value.value here?
    program.state.result_var.value = return_obj
    program.state = program.callstack.pop()

import re
import lltypes


RESULT_OPCODES = {}
OPCODES = {}

STORE_PATTERN = "(?P<src_type>\w*)\s+(?P<src>[%@]?\w+)\s*,\s*(?P<dest_type>\w*\*?)\s+(?P<dest>[%@]?\w+)\s*(,\s*align\s+(?P<alignment>\d+))?$"

store_pattern = re.compile(STORE_PATTERN)


def result_opcode(func):
    RESULT_OPCODES[func.__name__] = func
    return func


def opcode(func):
    OPCODES[func.__name__] = func
    return func


@result_opcode
def alloca(program, result_var, params):
    # raise NotImplementedError()
    # %1 = alloca i32, align 4
    # operands = operands.split(',')
    # program.current_inst[2][dest] = '\x00' * TYPES[operands[0]].size
    print("ALLOCA dest: '%s', operands: '%s'" % (result_var, str(params)))


@opcode
def store(program, params):
    # Implemented by Amit

    result = store_pattern.match()

    if result is None:
        raise InvalidOpcodeArguments('store', params)

    values = result.groupdict()

    src = values['src']
    if src.startswith('%') or src.startswith('@'):  #TODO: use var pattern
        pass

    print("STORE", params)


@result_opcode
def load(program, result_var, params):
    # Implemented by Amit
    print("LOAD dest: '%s', operands: '%s'" % (result_var, str(params)))


@result_opcode
def call(program, result_var, params):
    # Implemented by Gitlitz0
    print("%s = CALL %s" % (result_var, params))

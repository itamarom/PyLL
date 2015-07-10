import re
import argparse
from program import Program
import debug

PUBLIC_VAR_DEFINITION_PATTERN = r"@(?P<name>[\w\.]+)\s*=\s*(?P<props>[\w ]*)\[(?P<size>\d+)\s*x\s*(?P<unit>\w+)\]\s*(?P<value>.+),\s*align\s*(?P<alignment>\d+)$"
FUNC_DEFINITION_PATTERN = r"define\s+(?P<return_type>\w+)\s+@(?P<name>\w+)\((?P<params>[\w\d\s%,]+)?\)\s*(?P<attribs>#\d+)?\s*\{$"
ATTRIBS_DEFINITION_PATTERN = r"attributes\s(?P<name>#\d+)\s*=\s*\{\s*(?P<content>[\w\s\"\-=]+)\}\s*$"


unknown = {'target': {}}
globs = {}
funcs = {}
attribs = {}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('src', type=argparse.FileType('r'))
    parser.add_argument('--debug', action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    debug.IS_DEBUG = args.debug
    src = args.src

    public_var_definition = re.compile(PUBLIC_VAR_DEFINITION_PATTERN)
    func_definition = re.compile(FUNC_DEFINITION_PATTERN)
    attribs_definition = re.compile(ATTRIBS_DEFINITION_PATTERN)

    line = src.readline()
    while line:
        line = line.strip()

        if line.startswith(';') or len(line) == 0:
            line = src.readline()
            continue

        # public variables
        elif line.startswith('@'):
            result = public_var_definition.match(line)
            if result is None:
                raise Exception('FUCK')

            values = result.groupdict()

            globs[values['name']] = parse_llvm_str(values['value'])

        elif line.startswith('define'):
            # functions
            result = func_definition.match(line)
            if result is not None:
                values = result.groupdict()
                funcs[values['name']] = {'return_type': values['return_type'],
                                         'attribs': values['attribs'],
                                         'content': parse_func(src)}
            else:
                raise Exception('FUCK')

        elif line.startswith('attributes'):
            result = attribs_definition.match(line)
            if result is not None:
                values = result.groupdict()
                attribs[values['name']] = values['content']
            else:
                raise Exception('FUCK')

        elif line.startswith('target'):
            parts = line.split(' ')
            unknown['target'][parts[1]] = parts[3]

        else:
            print('ignoring: ' + line)

        line = src.readline()

    #print('unkonwn:')
    #print(unknown)
    #print('globs:')
    #print(globs)
    #print('funcs')
    #print(funcs)
    #print('attribs:')
    #print(attribs)

    prog = Program(unknown, globs, funcs, attribs)
    print "=============== RUNNING ==============="
    prog.run()


def parse_func(src):
    content = []

    line = src.readline()
    while line and not line.strip().startswith('}'):
        content.append(line)
        line = src.readline()

    return content


def parse_llvm_str(text):
    assert text.startswith('c"') and text.endswith('"')
    text = text[2:-1]

    p = r"[^\\]\\[0-9a-fA-F][0-9a-fA-F]"

    nums = re.findall(p, text)

    while nums:
        for n in nums:
            text = text.replace(n, n[0] + chr(int(n[-2:], 16)))
        nums = re.findall(p, text)

    if len(text) >= 4 and text[0] == '\\' and text[1] != '\\':
        text = chr(int(text[1:3], 16)) + text[3:]

    return text

if __name__ == "__main__":
    main()

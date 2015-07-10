        
class ProgramState(object):
    def __init__(self, func, op_index=0, scope=None, result_var=None):
        if scope is None:
            scope = {}
        self.func = func
        self.op_index = op_index
        self.scope = scope
        self.result_var = result_var

    @property
    def op_text(self):
        return self.func['content'][self.op_index].strip()
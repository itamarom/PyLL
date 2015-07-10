        
class ProgramState(object):
    def __init__(self, func, op_index=0, scope=None):
        if scope is None:
            scope = {}
        self.func = func
        self.op_index = op_index
        self.scope = scope
        
    def __iter__(self):
        return iter([self.func, self.op_index, self.scope])
        
    @property
    def op_text(self):
        return self.func['content'][self.op_index].strip()
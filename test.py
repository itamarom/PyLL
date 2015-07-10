import debug

debug.IS_DEBUG = True

@debug.log
def a(x):
    pass
    
a(5)

from utils.function_dispatcher import *

def func(a,b,c):
    print(a, b, c)

def main():
    dispatcher = function_dispatcher.open()
    dispatcher['hello'].add(func)
    dispatcher['hello'](1,2,3)

    function_dispatcher.close(dispatcher.name)







main()
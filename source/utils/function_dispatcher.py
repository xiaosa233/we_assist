from EventExecutor import *

class function_dispatcher_unit:

    def __init__(self):
        self.events = EventExecutor()

    def add(self, in_func):
        self.events.add_unique(in_func)
    
    def remove(self, in_func):
        self.events.remove(in_func)


    def __call__(self, *args, **kwargs):
        return self.events.broadcast(*args, **kwargs)


class function_dispatcher :
    g_dispatcher_map = {}
    def __init__(self, in_name):
        self.dispatchers = {}
        self.__name = in_name
        self.count = 1

    @staticmethod
    def open(name='default'):
        result = None
        if name in function_dispatcher.g_dispatcher_map :
            result = function_dispatcher.g_dispatcher_map[name]
            result.count += 1
        else :
            result = function_dispatcher(name)
            function_dispatcher.g_dispatcher_map[name] = result

        return result

    @staticmethod
    def weak_open(name='default'):
        if name in function_dispatcher.g_dispatcher_map :
            return function_dispatcher.g_dispatcher_map[name]
        else :
            #warning ,should not call here
            return function_dispatcher(name)

    @staticmethod
    def close(name) :
        if name in function_dispatcher.g_dispatcher_map:
            result = function_dispatcher.g_dispatcher_map[name]
            result.count -= 1
            if result.count == 0 :
                del function_dispatcher.g_dispatcher_map[name]


    def __getitem__(self, name):
        if name in self.dispatchers :
            return self.dispatchers[name]
        else  :
            result = function_dispatcher_unit()
            self.dispatchers[name] = result
            return result

    def remove(self, name) :
        if name in self.dispatchers :
            del self.dispatchers[name]

    @property
    def name(self):
        return self.__name

    @name.getter
    def name(self):
        return self.__name

__all__ = ['function_dispatcher']
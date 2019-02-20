
class EventExecutor:
    def __init__(self):
        self.funcs = []

    def add(self, func_obj):
        self.funcs.append(func_obj)

    def add_unique(self, func_obj):
        if func_obj not in self.funcs :
            self.funcs.append(func_obj)

    def remove(self, func_obj):
            self.funcs.remove(func_obj)

    def get_result(self):
        return self.result

    def broadcast(self, *args, **kwargs):
        result = None
        for func_obj in self.funcs :
            result = func_obj(*args, **kwargs)
        return result
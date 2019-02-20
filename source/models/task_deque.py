import threading
import collections



class task_unit:
    def __init__(self, func, *args, **key_args):
        self.v_func = func
        self.v_args = args
        self.v_key_args = key_args

    def __call__(self):
        return self.v_func(*self.v_args, **self.v_key_args)




class task_deque :
    def __init__(self):
        self.deque = collections.deque()
        self.mutex = threading.Lock()


    def push(self, in_task):
        self.mutex.acquire()
        self.deque.append(in_task)
        self.mutex.release()

    def push_with_param(self, *args, **kwargs):
        self.push( task_unit(*args, **kwargs))

    #run top task
    #return [is_empty , result]
    def run_top(self):
        top_task = None
        self.mutex.acquire()
        if len(self.deque) > 0 :
            top_task =  self.deque.popleft()
        self.mutex.release()
        if top_task :
            result = top_task()
            return (True, result)
        else :
            return (False, None)

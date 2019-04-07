import threading
import collections
import time


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


    def push(self, in_task, *args, **kwargs):
        self.mutex.acquire()
        self.deque.append(task_unit(in_task, *args, **kwargs) )
        self.mutex.release()

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


class async_task :
    def __init__(self):
        self.task_deque = task_deque()
        self.run_thread = None
        self.is_end = False
        self.is_clear = False

    def start(self):
        if self.run_thread is None :
            self.is_end = False
            self.is_clear = False
            self.run_thread = threading.Thread(target=self.run)
            self.run_thread.start()


    def stop(self, join_second = -1):
        join_param = join_second if join_second >= 0 else 99999
        self.is_clear = join_param > 0
        self.is_end = True
        if self.run_thread :
            join_param = join_second if join_second >= 0 else 99999
            self.run_thread.join(join_param)

        self.run_thread = None

    def run(self):
        next_sleep = 1.0
        while not self.is_end:
            #print('hwllo')
            next_sleep = 0.0 if self.task_deque.run_top()[0] else 1.0
            time.sleep(next_sleep)

        if self.is_clear :
            while self.task_deque.run_top()[0] :
                pass

    def add(self, func, *args, **kwargs):
        self.task_deque.push(func, *args, **kwargs)
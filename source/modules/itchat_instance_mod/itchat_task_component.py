import itchat_base_component
from models import global_accessor
import time
from models import task_deque
class itchat_task_component (itchat_base_component.itchat_base_component):


    def __init__(self, in_outer):
        super().__init__()
        self.outer = in_outer
        self.task_deque = task_deque.task_deque()
        self.tick_delta = 0.25


    def on_start(self):
        super().register()
        world = global_accessor.global_accessor.get_safe('world')
        if world is not None :
            self.tick_delta = 1.0 / world.get_run_frame()


    def tick(self, delta_time):
        should_run_time = self.tick_delta
        if delta_time > self.tick_delta :
            should_run_time -= delta_time - self.tick_delta

        if should_run_time < 0 :
            should_run_time = 0.00001

        start_run_time = time.time()
        now_time = start_run_time
        while now_time - start_run_time < should_run_time and self.task_deque.run_top()[0] :
            now_time = time.time()


    def add_task(self, in_task):
        self.task_deque.push(in_task)
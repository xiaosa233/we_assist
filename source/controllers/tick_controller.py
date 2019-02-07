from models.base import *
from utils.function_dispatcher import *
import base_controller
import threading
class tick_controller(base_controller.base_controller):
    def __init__(self):
        self.tick_objs = []
        self.pending_kill_idx = []
        self.pending_add_objs = []
        self.pending_mutex = threading.Lock()
        function_dispatcher.open()[base.g_base_register_name].add(self.on_base_register)
        function_dispatcher.open()[base.g_base_destroy_name].add(self.on_base_destroy)


    def on_base_register(self, base_obj):
        self.pending_mutex.acquire()
        idx = self.tick_objs.find(base_obj)
        if idx == -1 :
            if base_obj.is_tick and base_obj not in self.pending_add_objs:
                #add in
                self.pending_add_objs.append(base_obj)
        else :
            if not base_obj.is_tick and base_obj not in self.pending_kill_idx:
                #remove
                self.pending_kill_idx.append(idx)
        self.pending_mutex.release()

    def on_base_destroy(self, base_obj):
        #add to pending
        self.pending_mutex.acquire()
        idx = self.tick_objs.find(base_obj)
        if idx != -1 and base_obj not in self.pending_kill_idx:
            self.pending_kill_idx.append(idx)
        self.pending_mutex.release()

    def tick(self, delta_time):
        tick_obj_len = len(self.tick_objs)
        i = 0
        while i< tick_obj_len :
            self.tick_objs[i].tick(delta_time)

        #deal with pending
        self.pending_mutex.acquire()

        #remove pending kill objs
        self.pending_kill_idx.sort(reverse=True)
        for idx in self.pending_kill_idx :
            del self.tick_objs[idx]
        self.pending_kill_idx.clear()

        #add pending objs
        self.tick_objs.extend(self.pending_add_objs)
        self.pending_add_objs.clear()

        self.pending_mutex.release()
from models import base
import threading
from models import task_deque

class net_protocol_component(base.base) :

    event_name = { 'log' : 'ev_log',
                   'arrive' : 'ev_arrive',
                   'new_state' : 'ev_new_state',
                   'ask_state':'ev_now_state',
                   'asw_state' : 'ev_asw_state',
                   'ask_pid' : 'ev_ask_pid',
                   'asw_pid' : 'ev_asw_pid',
                   'close' : 'ev_close'}

    def __init__(self, controller):
        super().__init__()
        self.events = {}
        self.tasks = []
        self.controller = controller
        self.appending_mutex = threading.Lock()

    def initialize(self):
        super().register()


    def tick(self, delta_time):
        if len(self.tasks) > 0 :
            self.appending_mutex.acquire()
            now_works = self.tasks
            self.tasks = []
            self.appending_mutex.release()
            for it in now_works :
                it()


    '''
    key split with !
    '''
    def on_msg(self, tcp_base, data):
        #split message
        data = data.decode()
        data_array = data.split('`')

        for it in data_array:
            if len(it) > 0 :
                self.deal_msg(tcp_base, it)


    def deal_msg(self, tcp_base, data):
        key_index = data.find('!')
        #key _index should not be -1
        key = data[0:key_index]
        self.appending_mutex.acquire()
        self.tasks.append( task_deque.task_unit( net_protocol_component.broadcast_event, self.events.setdefault(key, []), tcp_base, data[key_index+1:]))
        self.appending_mutex.release()

    @staticmethod
    def broadcast_event(events, tcp_base, data):
        for it in events :
            it(tcp_base, data)


    def register_event(self, event_key, event_callback):
        self.events.setdefault(event_key, []).append(event_callback)


    def unregister_event(self, event_key, event_cb):
        if event_key in self.events and event_cb in self.events[event_key]:
            self.events[event_key].remove(event_cb)
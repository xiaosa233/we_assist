import base
import threading
import time
class input_manager(base.base) :
    def __init__(self):
        self.input_thread = None
        self.last_input = ''
        self.should_end = False
        self.after_input_call_back = None


    def initialize(self):
        if self.input_thread is None :
            self.input_thread = threading.Thread(target=input_manager.input_thread, args=(self,) )
            self.input_thread.start()

    def destroy(self):
        if self.input_thread is not None :
            self.input_thread.join()

    def get_last_input(self):
        result = self.last_input
        self.last_input = ''
        return result

    def input_impl(self):
        while not self.should_end :
            self.last_input = input()
            if self.after_input_call_back is not None :
                self.after_input_call_back()

    def set_should_end(self, value):
        self.should_end = value

    @staticmethod
    def input_thread(v_input_manager):
        v_input_manager.input_impl()
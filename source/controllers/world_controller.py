
import tick_controller
import input_manager
import async_controller
from utils import function_dispatcher
from models import global_accessor
from models import json_object
import config_controller
import time
import sys

class world_controller:
    
    def __init__(self) :
        self.v_tick_controller = tick_controller.tick_controller()
        self.v_async_controller = async_controller.async_controller()
        self.v_input_manager = input_manager.input_manager()
        self.should_end = False
        self.input_dispatcher = None
        self.test_mode = False
        self.run_frame = 40
        self.sys_argv = None
        global_accessor.global_accessor.set_value('world', self)
        global_accessor.global_accessor.set_value('async_controller', self.v_async_controller)



    def initialize(self, sys_argv):
        #initialize all things here
        json_test_mode = json_object.json_object.parse_with_file(config_controller.config_controller.get_save_dir() + 'world_config.json', 'test_mode')
        if json_test_mode is not None :
            self.set_test_mode(json_test_mode)

        self.input_dispatcher = function_dispatcher.function_dispatcher.open('input')
        self.input_dispatcher ['exit'].add(self.on_input_event_exit)
        self.v_tick_controller.initialize()
        self.v_input_manager.initialize()
        self.v_async_controller.initialize()


        if len(sys_argv) >= 2:
            global_accessor.global_accessor.set_value('cmd_qr', sys_argv[1])

    def loop(self, frame = 120):
        self.set_run_frame(frame)
        start_time = time.time()
        fix_delta_time = 1.0 / frame
        last_time = start_time - fix_delta_time
        count = 0

        while True :
            self.update(time.time() - last_time)
            if self.is_end():
                break

            last_time = time.time()
            count += 1
            end_time = count * fix_delta_time + start_time
            if end_time > last_time :
                time.sleep(end_time - last_time)


    def destroy(self):
        self.v_tick_controller.destroy()
        self.v_input_manager.destroy()
        self.v_async_controller.destroy()
        if self.input_dispatcher is not None :
            function_dispatcher.function_dispatcher.close(self.input_dispatcher.name)

    def update(self, delta_time):
        self.v_input_manager.deal_with_input()
        self.v_tick_controller.do_ticks(delta_time)

    def is_end(self):
        return self.should_end

    def on_input_event_exit(self):
        self.should_end = True

    def set_test_mode(self, in_mode):
        self.test_mode = in_mode

    def get_test_mode(self):
        return self.test_mode

    def set_run_frame(self, in_frame):
        self.run_frame = in_frame

    def get_run_frame(self):
        return self.run_frame

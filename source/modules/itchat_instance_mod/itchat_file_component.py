import itchat_base_component
import shutil
from models import json_object
from os import path
import os
import time
from models import ticker

class itchat_file_component(itchat_base_component.itchat_base_component) :

    def __init__(self, outer_controller):
        super().__init__()
        self.outer = outer_controller
        self.v_itchat = outer_controller.get_itchat()
        self.is_login = False
        self.is_movepkl = False
        self.start_time = 0.0
        self.move_file_run_times = 0.0

    def on_start(self):
        super().register()


    def tick(self, delta_time):
        if not self.is_login :
            return

        if not self.is_movepkl :
            if self.move_file_and_record( self.move_file_run_times > 10.0) :
                self.is_movepkl = True
            self.move_file_run_times += delta_time

        if self.is_movepkl :
            self.set_is_tick(False)
            self.notify_tickable()


    def move_file_and_record(self, force_do = False):
        result = False

        if self.v_itchat.get_itchat_name() != self.v_itchat.get_instance_name():
            src_path = self.outer.get_save_data_dir() + self.v_itchat.get_instance_name() + '/' + self.v_itchat.get_instance_name() + '.pkl'
            src_path = self.outer.get_save_data_dir() + self.v_itchat.get_instance_name() + '/' + self.v_itchat.get_instance_name() + '.pkl'
            dist_dir = self.outer.get_itchat_data_dir()
            dist_path = self.outer.get_itchat_data_dir() + self.v_itchat.get_itchat_name() + '.pkl'

            if path.exists(src_path):

                #check if src_path is the last file
                try:
                    last_modify_time = path.getctime(src_path)
                    if force_do or abs(self.start_time - last_modify_time) < 5.0 :
                        if not path.exists(dist_dir):
                            os.makedirs(dist_dir)

                        shutil.copy(src_path, dist_path)
                        # record last module
                        json_object.json_object.write_with_file(self.v_itchat.get_itchat_name(),
                                                                self.outer.get_save_data_dir() + 'itchat_default.json',
                                                                'last_login_name')
                        result = True

                except Exception as e :
                    pass
        else :
            result = True

        return result


    def on_login(self):
        self.is_login = True
        self.start_time = time.time()
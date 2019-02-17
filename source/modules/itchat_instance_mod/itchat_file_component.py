import itchat_base_component
import shutil
from models import json_object
from os import path
import os

class itchat_file_component(itchat_base_component.itchat_base_component) :

    def __init__(self, outer_controller):
        super().__init__()
        self.outer = outer_controller
        self.v_itchat = outer_controller.get_itchat()

    def on_login(self):
        if self.v_itchat.get_itchat_name() != self.v_itchat.get_instance_name() :
            src_path = self.outer.get_save_data_dir() + self.v_itchat.get_instance_name() + '/' + self.v_itchat.get_instance_name() +  '.pkl'
            dist_dir = self.outer.get_itchat_data_dir()
            dist_path = self.outer.get_itchat_data_dir() + self.v_itchat.get_itchat_name() + '.pkl'

            if not path.exists(src_path):
                return

            if not path.exists(dist_dir):
                os.makedirs(dist_dir)
            shutil.copy(src_path, dist_path)

            #record last module
            json_object.json_object.write_with_file(self.v_itchat.get_itchat_name(), self.outer.get_save_data_dir() + 'itchat_default.json', 'last_login_name')
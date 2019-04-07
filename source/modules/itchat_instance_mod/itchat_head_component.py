import itchat_base_component
from models import json_object
from models import task_deque
from utils.func_library import func_library
from models import monitor_variable
from controllers import log_controller
import img_handler
from os import path
import os
import shutil

class itchat_head_component(itchat_base_component.itchat_base_component) :
    def __init__(self, in_outer) :
        super().__init__()
        self.outer = in_outer
        self.last_head_index = 0
        self.task_component = None
        self.v_itchat = self.outer.get_itchat()
        self.img_cache = {}

    def on_login(self):
        self.add_task(self.on_login_main_thread)

    def on_login_main_thread(self):
        self.last_head_index = json_object.json_object.parse_with_file(self.get_cache_json(), 'last_head_index')
        if self.last_head_index is None:
            self.last_head_index = 0

        self.read_last_imgs()
        self.update_head_image()

    def on_start(self):
        self.task_component = self.outer.get_component('itchat_task_component')


    def on_close(self):
        json_object.json_object.write_with_file(self.last_head_index, self.get_cache_json(), 'last_head_index')


    def update_head_image(self):
        log_controller.log_controller.g_log('begin to update head imgs ')
        friend_infos = self.v_itchat.get_friend_infos()
        self.change_index()
        for item in friend_infos :
            self.add_task( self.update_head_image_impl, item, self.last_head_index)
        self.add_task(self.on_after_update_head)



    def read_last_imgs(self):
        # initialize img cache
        last_dir = self.get_head_dir(self.last_head_index)

        if not path.exists(last_dir) :
            return

        friend_infos = self.v_itchat.get_friend_infos()
        last_dir_files = os.listdir(last_dir)

        exists_filse = {}
        for it in last_dir_files :
            exists_filse[it] = False

        for item in friend_infos:
            now_name = self.outer.get_friendly_name(item)
            item_path = last_dir + now_name + '.png'
            if path.exists(item_path):
                self.img_cache[item['UserName']] = monitor_variable.monitor_variable(img_handler.img_handler(item_path) )
                exists_filse[now_name + '.png'] = True

        to_remove_key = []
        for key, value in exists_filse.items():
            if not value :
                to_remove_key.append(key)

        for it in to_remove_key :
            os.remove( last_dir + it)

        next_index = 1- self.last_head_index
        # remove now imgs
        now_dir = self.get_head_dir( next_index)
        if path.exists(now_dir) :
            shutil.rmtree(now_dir)

    def on_after_update_head(self):
        log_controller.log_controller.g_log('end update head imgs')


    # diff img, it should run in main thread
    def update_head_image_impl(self, friend_info, last_index):
        head_dir = self.get_head_dir(last_index)
        img_path = head_dir + func_library.get_windows_valid_path(self.outer.get_friendly_name(friend_info) ) + '.png'
        self.v_itchat.get_head_img(img_path,friend_info['UserName'])
        if friend_info['UserName'] not in self.img_cache :
            self.img_cache[friend_info['UserName'] ] = monitor_variable.monitor_variable( img_handler.img_handler(img_path) )
        else :
            now_it = self.img_cache[ friend_info['UserName'] ]
            if now_it.set_value( img_handler.img_handler(img_path) ) :
                msg = self.outer.get_friendly_name(friend_info) + ' 修改了头像 ，即将给你发送修改前和修改后的头像'
                log_controller.log_controller.g_log(msg)
                log_controller.log_controller.g_log('修改前 ：'+now_it.get_last_value().get_src_path()+'修改后：'+now_it.get_value().get_src_path())
                self.outer.send_msg_impl(msg, self.outer.filehelper_name)
                self.outer.send_image_impl(now_it.get_last_value().get_src_path())
                self.outer.send_image_impl(now_it.get_value().get_src_path())

    def add_task(self, in_task, *args, **kwargs):
        if self.task_component :
            self.task_component.add_task(in_task, *args, **kwargs)
        else :
            in_task()

    def change_index(self):
        self.last_head_index = 1- self.last_head_index
        json_object.json_object.write_with_file(self.last_head_index, self.get_cache_json(), 'last_head_index')


    def get_cache_json(self) :
        return self.outer.get_itchat_data_dir() + 'cache.json'

    def get_head_dir(self, index):
        return self.outer.get_itchat_data_dir() + 'head_imgs/' + str(index) + '/'
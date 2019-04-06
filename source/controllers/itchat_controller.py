from modules.itchat_instance_mod import itchat_instance
from modules.itchat_instance_mod import offline_itchat_instance
from config_controller import *
from log_controller import *
import base_controller
import friend_info
from utils import json_coder
from utils.func_library import *
import time
import random
import itchat_file_component
import itchat_cache_component
import itchat_task_component
import itchat_head_component
import itchat_upload_component
import itchat_input_component
import itchat_record_component
from models import json_object
from models import global_accessor
from models import task_deque
from models import ticker
from utils import function_dispatcher

class itchat_controller (base_controller.base_controller):

    filehelper_name = 'filehelper'

    def __init__(self) :
        super().__init__()
        self.v_itchat = None
        self.save_data_json = json_coder.json_coder()
        self.save_data_json.set_path( self.get_save_data_dir() + "objects/itchat_controller.json" )
        self.is_logging = False
        self.friend_info_ticker = ticker.ticker(60.0)
        self.head_ticker = ticker.ticker(60 * 10.0)
        self.update_head_img_index = 0 # use for switch path when get head imgs
        self.components = []
        self.cache_component = None
        self.task_component = None
        self.head_component = None
        self.upload_component = None
        
# public ------------
    def start(self) :
        super().register()
        world = global_accessor.global_accessor.get_safe('world')
        is_test = False
        if world is not None :
            is_test = world.get_test_mode()

        self.function_dispatcher = function_dispatcher.function_dispatcher.open('input')
        self.function_dispatcher['test'].add(self.on_test)

        if not is_test :
            self.v_itchat = itchat_instance.itchat_instance(self.get_default_login_name())
        else :
            self.v_itchat = offline_itchat_instance.offline_itchat_instance(self.get_default_login_name())
        #register callback
        '''
        on_receive_callback :itchat_instance , msg
        on_login_callback :itchat_instance
        on_logout_callback : itchat_instance
        on_newfriend_arrive_call_back : itchat_instance, msg
        '''
        self.v_itchat.on_receive_callback = self.on_receive
        self.v_itchat.on_login_callback = self.on_login
        self.v_itchat.on_logout_callback = self.on_logout
        self.v_itchat.on_newfriend_arrive_callback = self.on_newfriend_arrive

        self.components.append( itchat_file_component.itchat_file_component(self))
        self.cache_component = itchat_cache_component.itchat_cache_component(self)
        self.task_component = itchat_task_component.itchat_task_component(self)
        self.components.append( self.cache_component)
        self.components.append( self.task_component)
        self.head_component =  itchat_head_component.itchat_head_component(self)
        self.components.append(  self.head_component )
        self.upload_component = itchat_upload_component.itchat_upload_component(self)
        self.components.append(  self.upload_component )
        self.components.append( itchat_input_component.itchat_input_component(self))
        self.components.append( itchat_record_component.itchat_record_component(self))


        self.v_itchat.login_and_run(self.get_save_data_dir() + self.v_itchat.get_instance_name() + '/')
        for it in self.components :
            it.on_start()

    def close(self) :
        msg = self.v_itchat.instance_name + " logout"
        log_controller.g_log(msg)
        self.v_itchat.send_msg(msg, self.filehelper_name)


        for it in self.components:
            it.on_close()
        self.v_itchat.logout()


    def get_itchat(self):
        return self.v_itchat


    def tick(self, delta_time):
        if self.is_logging :
            if self.friend_info_ticker.tick(delta_time):
                print('time : ', time.time(), 'update friend info')
                self.update_friend_infos()
            if self.head_ticker.tick(delta_time):
                print('time : ', time.time() ,'update head imgs')
                self.update_head_image()

    def on_test(self):
        pass


    def update_friend_infos(self) :
        if not self.is_logging:
            return

        if self.cache_component is not None :
            self.cache_component.update_friend_infos(True)
    def update_head_image(self):
        if not self.is_logging:
            return
        if self.head_component:
            self.head_component.update_head_image()

    def send_msg(self, msg, username = None):
        if username is None :
            username = self.filehelper_name
        if self.task_component :
            self.task_component.add_task( task_deque.task_unit(self.send_msg_impl, msg, username) )

    def send_file(self, msg, username=None):
        if username is None:
            username = self.filehelper_name
        if self.task_component:
            self.task_component.add_task(task_deque.task_unit(self.send_file_impl, msg, username))

    def send_image(self, msg, username=None):
        if username is None:
            username = self.filehelper_name
        if self.task_component:
            self.task_component.add_task(task_deque.task_unit(self.send_image_impl, msg, username))

    def send_msg_impl(self, msg, username):
        self.v_itchat.send_msg_check(msg, username)


    def send_image_impl(self, img_path, username = None):
        if username is None :
            username = self.filehelper_name

        final_path = img_path
        if self.upload_component:
            final_path = self.upload_component.request_send(img_path)

        self.v_itchat.send_img( final_path, username)

    def send_file_impl(self, file_path, username = None):
        if username is None :
            username = self.filehelper_name

        final_path = file_path
        if self.upload_component:
            final_path = self.upload_component.request_send(file_path)

        self.v_itchat.send_file( final_path, username)




    def get_is_logging(self):
        return self.is_logging

    def get_component(self, component_name):

        for it in self.components :
            if type(it).__name__ == component_name :
                return it
        return None




# private ------------
    def get_friendly_name(self, wechat_friend_infos_item) :
        response_name = wechat_friend_infos_item['RemarkName']
        if response_name == '':
            response_name = wechat_friend_infos_item['NickName']
        return response_name


    def on_receive(self, in_itchat_instance, msg) :
        for it in self.components:
            it.on_receive(msg)

    def on_login(self, in_itchat_instance) :

        msg = 'we_assist loging : ' + self.v_itchat.get_itchat_name()
        log_controller.g_log(msg)
        self.is_logging = True

        self.send_msg(msg)

        for it in self.components:
            it.on_login()
        return
        #check friend imgs
        self.check_friend_head_imgs()


    def on_logout(self, in_itchat_instance) :
        for it in self.components:
            it.on_logout()
         

    def on_newfriend_arrive(self, in_itchat_instance, msg) :
        pass

    @staticmethod
    def get_save_data_dir() :
        return config_controller.get_save_dir() + "itchat_data/"

    @staticmethod
    def get_default_login_name():
        result = json_object.json_object.parse_with_file(itchat_controller.get_save_data_dir() + 'itchat_default.json', 'last_login_name')
        if result is None :
            result = 'default_name'
        return result

    def get_itchat_data_dir(self):
        return itchat_controller.get_save_data_dir() + self.v_itchat.get_itchat_name() + '/'

    def show_helper(self) :
        return '1:获取所有微信好有的个性签名\n2:获取所有好友头像\n'
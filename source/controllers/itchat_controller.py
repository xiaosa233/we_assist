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
import itchat_state_component
from models import json_object
from models import global_accessor
from models import task_deque
from models import ticker
from utils import function_dispatcher

import sys

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
        self.arrive_ticker = ticker.ticker(20.0)
        self.arrive_ticker.tick(15) # make it first time tick at 5sec
        self.alarm_clock_ticker = ticker.ticker(1.0) # for alarm clock

        #patch to test why I can not success to re logging
        self.log_relogging_ticker = ticker.ticker(60*3)

        self.update_head_img_index = 0 # use for switch path when get head imgs
        self.cache_component = None
        self.task_component = None
        self.head_component = None
        self.upload_component = None
        self.net_controller = None
        
# public ------------
    def start(self) :
        super().register()
        world = global_accessor.global_accessor.get_safe('world')
        is_test = False
        if world is not None :
            is_test = world.get_test_mode()

        self.function_dispatcher = function_dispatcher.function_dispatcher.open('input')
        function_dispatcher.function_dispatcher.open()['itchat_exception'].add(self.on_itchat_exception)

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
        self.components.append(itchat_state_component.itchat_state_component(self))

        cmd_qr=global_accessor.global_accessor.get_safe('cmd_qr')
        cmd_qr = cmd_qr if cmd_qr else 1

        self.v_itchat.login_and_run(self.get_save_data_dir() + self.v_itchat.get_instance_name() + '/', cmd_qr)
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

    def get_net_controller(self):
        if self.net_controller is None :
            self.net_controller = global_accessor.global_accessor.get_safe('net_controller')
        return self.net_controller

    def on_itchat_exception(self):
        print('itchat exception at time ', func_library.timestamp_to_datetime(time.time()))
        self.is_logging = False

    def tick(self, delta_time):
        if self.is_logging :
            if self.arrive_ticker.tick(delta_time) and self.get_net_controller():
                #pass
                print('send arrive time at : ', func_library.timestamp_to_datetime(time.time()))
                self.get_net_controller().send_arrive()
            if self.alarm_clock_ticker.tick(delta_time) :
                #say good night to me
                time_struct = time.localtime(time.time())
                if time_struct.tm_hour == 23 and time_struct.tm_min == 0 and time_struct.tm_sec == 0 :
                    self.send_msg('准备休息了哦~~')
                elif time_struct.tm_hour == 23 and time_struct.tm_min == 30 and time_struct.tm_sec == 0 :
                    self.send_msg('晚安~~')

            if self.friend_info_ticker.tick(delta_time):
                log_controller.g_log('time : ' + func_library.timestamp_to_datetime(time.time()) +'update friend info')
                self.update_friend_infos()
            if self.head_ticker.tick(delta_time):
                log_controller.g_log('time : ' + func_library.timestamp_to_datetime(time.time()) + 'update head imgs')
                self.update_head_image()
        else :
            if self.log_relogging_ticker.tick(delta_time) :
                print( 'Failed to logging : ', func_library.timestamp_to_datetime(time.time()))
                self.function_dispatcher['exit']()
                sys.exit(0)


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
            self.task_component.add_priority_task(5, self.send_msg_impl, msg, username)

    def send_file(self, msg, username=None):
        if username is None:
            username = self.filehelper_name
        if self.task_component:
            self.task_component.add_priority_task(5, self.send_file_impl, msg, username)

    def send_image(self, msg, username=None):
        if username is None:
            username = self.filehelper_name
        if self.task_component:
            self.task_component.add_priority_task(5, self.send_image_impl, msg, username)

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
        self.log_relogging_ticker.reset(self.log_relogging_ticker.get_tick_time())
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

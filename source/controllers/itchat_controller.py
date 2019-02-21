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
from models import json_object
from models import global_accessor
from models import task_deque
from models import ticker

class itchat_controller (base_controller.base_controller):

    filehelper_name = 'filehelper'

    def __init__(self) :
        super().__init__()
        self.v_itchat = None

        self.v_friend_infos = {} # map , user_name to friend_info
        self.save_data_json = json_coder.json_coder()
        self.save_data_json.set_path( self.get_save_data_dir() + "objects/itchat_controller.json" )
        self.is_logging = False
        self.ticker = ticker.ticker(3.0)

        self.update_head_img_index = 0 # use for switch path when get head imgs

        self.components = []
        self.cache_component = None
        self.task_component = None
        
# public ------------
    def start(self) :
        super().register()
        world = global_accessor.global_accessor.get_safe('world')
        is_test = False
        if world is not None :
            is_test = world.get_test_mode()

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


        self.v_itchat.login_and_run(self.get_save_data_dir() + self.v_itchat.get_instance_name() + '/')
        for it in self.components :
            it.on_start()

    def close(self) :
        #self.write_json_file()
        for it in self.components:
            it.on_close()
        self.v_itchat.logout()


    def get_itchat(self):
        return self.v_itchat


    def tick(self, delta_time):
        if self.is_logging and self.ticker.tick(delta_time):
            print('time : ', time.time(), 'update friend info')
            self.update_friend_infos()


    def update_friend_infos(self) :
        if not self.is_logging:
            return

        if self.cache_component is not None :
            self.cache_component.update_friend_infos(True)

    def send_msg(self, username, msg):
        if self.task_component :
            self.task_component.add_task( task_deque.task_unit(self.v_itchat.send_msg_check, username, msg) )


    def update_friend_head_imgs(self) :

        friend_infos = self.v_itchat.instance.get_friends(update=False)
        last_index = self.update_head_img_index
        self.update_head_img_index = 1 - last_index
        for item in friend_infos :
            img_a = self.get_head_img_path(str(self.update_head_img_index), item)
            self.v_itchat.get_head_img(item['UserName'], img_a)
            img_b = self.get_head_img_path(str(last_index), item)

            #check if img size is different
            if func_library.is_img_size_different(img_a, img_b) :
                msg = self.get_friendly_name(item) + ' 修改了头像 ，即将给你发送修改前和修改后的头像'
                log_controller.g_log(msg)
                self.v_itchat.send_msg(itchat_controller.filehelper_name, msg)
                self.v_itchat.send_img(itchat_controller.filehelper_name, img_b)
                self.v_itchat.send_img(itchat_controller.filehelper_name, img_a)
        





# private ------------
    def get_friendly_name(self, wechat_friend_infos_item) :
        response_name = wechat_friend_infos_item['RemarkName']
        if response_name == '':
            response_name = wechat_friend_infos_item['NickName']
        return response_name

    def get_head_img_path(self, middle_dir_name, wechat_friend_infos_item) :
        file_name = wechat_friend_infos_item['UserName']
        return self.get_save_data_dir() + "head_imgs/" + middle_dir_name + "/" + file_name +".png"

    def on_receive_all_signature(self) :
        friend_infos = self.v_itchat.instance.get_friends(update=True)
        response_msg = ''
        for info_it in friend_infos :
            response_name = info_it['RemarkName']
            if response_name == '':
                response_name = info_it['NickName']

            response_msg += response_name + ' : ' + info_it['Signature'] + '\n'
        
        return response_msg
            

            

    def on_receive(self, in_itchat_instance, msg) :
        if msg['ToUserName'] == itchat_controller.filehelper_name :
            reply = ''
            if msg['Content'] == '帮助' :
                reply = self.show_helper()
            elif msg['Content'] == '1' :
                # get all signature
                reply = self.on_receive_all_signature()

            if reply != '':
                self.v_itchat.send_msg_check(itchat_controller.filehelper_name, reply)



    def on_login(self, in_itchat_instance) :

        msg = self.v_itchat.get_itchat_name() + " login"
        log_controller.g_log(msg)
        self.is_logging = True

        for it in self.components:
            it.on_login()
        return
        #check friend imgs
        self.check_friend_head_imgs()

    def check_friend_head_imgs(self) :
        if 'friendly_name_map' not in self.save_data_json.json_data :
            return 

        friendly_name_map = self.save_data_json.json_data['friendly_name_map']
        friend_infos = self.v_itchat.instance.get_friends(update=False)
        last_index = self.update_head_img_index
        self.update_head_img_index = 1 - self.update_head_img_index
        for item in friend_infos :
            friendly_name = self.get_friendly_name(item)
            if(friendly_name not in friendly_name_map) :
                continue 

            img_a = self.get_head_img_path(str(self.update_head_img_index), item)
            self.v_itchat.get_head_img(item['UserName'], img_a)
            img_b = self.get_head_img_path(str(last_index), item)
            #replace img_b
            img_b = os.path.dirname(img_b) + '/' + friendly_name_map[friendly_name] + '.png'

            #check if img size is different
            if func_library.is_img_size_different(img_a, img_b) :
                msg = friendly_name + ' 修改了头像 ，即将给你发送修改前和修改后的头像'
                log_controller.g_log(msg)
                self.v_itchat.send_msg(itchat_controller.filehelper_name, msg)
                self.v_itchat.send_img(itchat_controller.filehelper_name, img_b)
                self.v_itchat.send_img(itchat_controller.filehelper_name, img_a)

    def get_all_friend_head_imgs(self) :
        
        friend_infos = self.v_itchat.instance.get_friends(update=False)
        for item in friend_infos :
            img_path = self.get_head_img_path('all_head_imgs', item)
            img_path = os.path.dirname(img_path) + '/' + func_library.get_windows_valid_path(self.get_friendly_name(item)) + '.png'
            self.v_itchat.get_head_img(item['UserName'], img_path)

            msg = self.get_friendly_name(item) + ' 的头像：'
            log_controller.g_log(msg + img_path)
            time.sleep(random.random() )


    def on_logout(self, in_itchat_instance) :
        msg = self.v_itchat.instance_name + " logout"
        log_controller.g_log(msg)

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
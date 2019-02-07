from modules.itchat_instance_mod import *
from config_controller import *
from log_controller import *
from models import friend_info
from utils import json_coder
from utils.func_library import *
import time
import random

class itchat_controller :

    filehelper_name = 'filehelper'

    def __init__(self) :
        self.v_itchat = itchat_instance.itchat_instance()
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

        #add friends info 
        self.v_friend_infos = {} # map , user_name to friend_info
        self.save_data_json = json_coder.json_coder()
        self.save_data_json.set_path( self.get_save_data_dir() + "objects/itchat_controller.json" )
        self.is_logging = False

        self.update_head_img_index = 0 # use for switch path when get head imgs
        
# public ------------
    def start(self) : 
        self.v_itchat.login_and_run(self.get_save_data_dir())

    def close(self) :
        self.write_json_file()
        self.v_itchat.logout()

    def update_friend_infos(self) :
        if not self.is_logging:
            return
        friend_infos = self.v_itchat.instance.get_friends(update=True)

        response_msg = ''
        for info_it in friend_infos :
            #print(info_it['UserName'], '  ', info_it['NickName'], '  ', info_it['Signature'], )
            if info_it['UserName'] not in self.v_friend_infos :
                self.v_friend_infos[ info_it['UserName']] = friend_info.friend_info( info_it['UserName'], info_it['NickName'], info_it['Signature'])
            else :
                now_it = self.v_friend_infos[ info_it['UserName']]
                response_name = self.get_friendly_name(info_it)

                if now_it.monitor_nickname.set_value( info_it['NickName']) :
                    tmp_msg = response_name + ' 修改了昵称 : ' + now_it.monitor_nickname.get_last_value() + " --> " + now_it.monitor_nickname.get_value()
                    response_msg += tmp_msg + "\n"
                    log_controller.g_log(tmp_msg)
                if now_it.monitor_signature.set_value( info_it['Signature']) :
                    tmp_msg = response_name + ' 修改了个性签名 : ' + now_it.monitor_signature.get_last_value() + " --> " + now_it.monitor_signature.get_value()
                    response_msg += tmp_msg + "\n"
                    log_controller.g_log(tmp_msg)
        if response_msg != '' :
            #send to filehelper 
            self.v_itchat.send_msg_check(itchat_controller.filehelper_name, response_msg)
            self.write_json_file()

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
        msg = self.v_itchat.instance_name + " login"
        log_controller.g_log(msg)
        self.is_logging = True

        #load json_data
        self.read_json_file()
        self.update_friend_infos()

        #remove key which not in friend_infos 
        friend_infos = self.v_itchat.instance.get_friends(update = False)
        friend_info_keys = { it['UserName'] : 1 for it in friend_infos }

        to_remove_keys = []
        for key in self.v_friend_infos :
            if key not in friend_info_keys :
                to_remove_keys.append(key)

        for it in to_remove_keys :
            del self.v_friend_infos[it]

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
         

    def on_newfriend_arrive(self, in_itchat_instance, msg) :
        pass

    def get_save_data_dir(self) :
        return config_controller.get_save_dir() + "data/"

    def show_helper(self) :
        return '1:获取所有微信好有的个性签名\n2:获取所有好友头像\n'

    def read_json_file(self) :
        json_data = self.save_data_json.parse_file()
        if len(json_data) > 0 :
            self.json_data_to_friend_infos(json_data['friend_infos'])
            self.update_head_img_index = json_data['update_head_img_index']

    def write_json_file(self) :
        json_data = {}
        json_data['update_head_img_index'] = self.update_head_img_index #the last json_files dir 
        json_data['friend_infos'] = self.friend_infos_to_json_data()  
        friend_infos = self.v_itchat.instance.get_friends(update=False)
        json_data['friendly_name_map'] = self.get_friendly_name_map(friend_infos)
        self.save_data_json.write_file(json_data)

    def friend_infos_to_json_data(self) :
        json_data = {}

        #user_name every_time is different ,so we can not user the same username
        friend_infos = self.v_itchat.instance.get_friends(update=False)
        for it in friend_infos :
            json_data[ self.get_friendly_name(it)] = {'nickname' : it['NickName'], 'signature' : it['Signature']}
        return json_data

    def json_data_to_friend_infos(self, json_data) :
        if json_data == None :
            return 
        friend_infos = self.v_itchat.instance.get_friends(update=False)
        name_map_key = self.get_friendly_name_map(friend_infos)

        for (key, value) in json_data.items():
            if key in name_map_key:
                self.v_friend_infos[name_map_key[key] ] = friend_info.friend_info( name_map_key[key], value['nickname'], value['signature'])

    def get_friendly_name_map(self, friend_infos) :
        #create_map 
        invalid_key = [] # if there are two same friendly name send_msgthen we ignore it
        name_map_key = {}
        for it in friend_infos :
            friendly_name = self.get_friendly_name(it)
            if friendly_name in invalid_key :
                continue
            if friendly_name not in name_map_key :
                name_map_key[friendly_name] = it['UserName']
            else :
                del name_map_key[friendly_name]
                invalid_key.append(friendly_name)

        return name_map_key


    def test_func(self):
        self.v_itchat.send_msg(itchat_controller.filehelper_name, 'test')

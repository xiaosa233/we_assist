from modules.itchat_instance import *
from config_controller import *
from log_controller import *
from models import friend_info
from utils import json_coder

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
        self.friend_infos_json = json_coder.json_coder()
        self.friend_infos_json.set_path( self.get_save_data_dir() + "objects/friend_infos.json" )
        self.is_logging = False
        
# public ------------
    def start(self) : 
        #load json_data
        self.read_json_file()
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
                response_name = info_it['RemarkName']
                if response_name == '':
                    response_name = info_it['NickName']

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

# private ------------

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
            
            self.v_itchat.send_msg_check(itchat_controller.filehelper_name, reply)

    def on_login(self, in_itchat_instance) :
        msg = self.v_itchat.instance_name + " login"
        log_controller.g_log(msg)
        self.is_logging = True
        self.update_friend_infos()
        

        #remove key which not in friend_infos 
        friend_infos = self.v_itchat.instance.get_friends(update = False)

        to_remove_keys = []
        for key in self.v_friend_infos :
            if key not in friend_infos :
                to_remove_keys.append(key)

        for it in to_remove_keys :
            del self.v_friend_infos[it]

          
    def on_logout(self, in_itchat_instance) :
        msg = self.v_itchat.instance_name + " logout"
        log_controller.g_log(msg)
         

    def on_newfriend_arrive(self, in_itchat_instance, msg) :
        pass

    def get_save_data_dir(self) :
        return config_controller.get_save_dir() + "data/"

    def show_helper(self) :
        return '1:获取所有微信好有的个性签名\n'

    def read_json_file(self) :
        self.json_data_to_friend_infos(self.friend_infos_json.parse_file())

    def write_json_file(self) :
        self.friend_infos_json.write_file( self.friend_infos_to_json_data() )

    def friend_infos_to_json_data(self) :
        json_data = {}
        for (key, value) in self.v_friend_infos.items() :
            json_data[key] = value.get_json_data()
        return json_data

    def json_data_to_friend_infos(self, json_data) :
        if json_data == None :
            return 
        for (key, value) in json_data.items():
            self.v_friend_infos[key] = friend_info.friend_info( value['user_name'], value['nickname'], value['signature'])


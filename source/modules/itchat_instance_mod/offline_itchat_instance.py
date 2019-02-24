import threading
import itchat_instance
import time
import random
import os
from utils import function_dispatcher
from controllers import config_controller
import shutil

'''
this class on use for debug and test
'''

class offline_itchat_instance:
    '''
    for itchat instance
    '''
    def __init__(self, instance_name = 'default_name'):
        super().__init__()
        self.instance_name = instance_name
        self.itchat_name = ''
        self.run_thread = None

        self.on_receive_callback = None
        self.on_login_callback = None
        self.on_logout_callback = None
        self.on_newfriend_arrive_callback = None
        self.func_dispatcher = None

    def login_and_run(self, storage_dir) :
        self.func_dispatcher = function_dispatcher.function_dispatcher.open()
        if self.run_thread is None :
            self.run_thread = threading.Thread(target=offline_itchat_instance.itchat_run, args=(self, storage_dir) )
            self.run_thread.start()

    def logout(self, is_keep_hotload = True) :
        function_dispatcher.function_dispatcher.close( self.func_dispatcher.name)
        if not is_keep_hotload :
            self.instance.logout()
            self.run_thread.join(2)
        else :
            itchat_instance.ns_itchat_instance.terminate_thread(self.run_thread)


    def login_callback(self):
        friend_info = self.get_friend_infos(True)
        self.itchat_name = friend_info[0]['NickName']
        if self.on_login_callback :
            self.on_login_callback(self)

    def logout_callback(self):
        if self.on_logout_callback :
            self.on_logout_callback(self)

    def send_msg(self, msg, to_username):
        print('offline_itchat send msg ,user_name : ', to_username, 'msg : ', msg)

    def send_msg_check(self, msg, to_username) :
        max_words = 800
        if(len(msg) <= max_words) :
            self.send_msg(msg, to_username)
        else :
            msg_len = len(msg)
            while( msg_len > 0) :
                tosend_msg = msg[: max_words if msg_len >= max_words else msg_len]
                self.send_msg(tosend_msg, to_username)
                time.sleep(random.random() * 2 + 1) # 防封号
                msg = msg[max_words if msg_len >= max_words else msg_len:]
                msg_len = len(msg)

    def send_img(self, pic_dir, to_username) :
        print('offline_itchat send img : ', to_username, pic_dir)

    def get_head_img(self, pic_path, user_name) :
        test_dir = self.get_test_dir() + self.get_itchat_name() + '/head_imgs/'
        result = os.listdir(test_dir)
        dir_len = len(result)
        target_file = test_dir + result[random.randint(0, dir_len-1)]

        #copy file
        pic_dir = os.path.dirname(pic_path)
        if not os.path.exists(pic_dir ) :
            os.mkdir(pic_dir)
        shutil.copy(target_file, pic_path)

    def get_test_dir(self):
        return config_controller.config_controller.get_project_dir() + 'test_dir/'


    def get_friend_infos(self, update = False):
        result = self.func_dispatcher['get_friend_infos'](self)
        if result is None :
            #add default
            result = [{'UserName': '@f340e2867f146249bd94707b520e0c8ec9ecdd21e264ae8ec8cd111e292b849f', 'City': '',
            'DisplayName': '', 'PYQuanPin': '', 'RemarkPYInitial': '', 'Province': '', 'KeyWord': '', 'RemarkName': '', 'PYInitial': '', 'EncryChatRoomId': '',
            'Alias': '', 'Signature': '', 'NickName': '小伍', 'RemarkPYQuanPin': '',
            'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=1941491314&username=@f340e2867f146249bd94707b520e0c8ec9ecdd21e264ae8ec8cd111e292b849f&skey=@crypt_5f5822ec_3e78232cfbf02d257f337fe07afd8559',
            'UniFriend': 0, 'Sex': 1, 'AppAccountFlag': 0, 'VerifyFlag': 0, 'ChatRoomId': 0, 'HideInputBarFlag': 0, 'AttrStatus': 0, 'SnsFlag': 48, 'MemberCount': 0, 'OwnerUin': 0,
            'ContactFlag': 0, 'Uin': 2843835563, 'StarFriend': 0, 'Statues': 0, 'WebWxPluginSwitch': 0, 'HeadImgFlag': 1}]
        return result

    def get_itchat_name(self):
        return self.itchat_name

    def get_instance_name(self):
        return self.instance_name

    @staticmethod
    def itchat_run(value_itchat_instance, storage_dir):

        storage_path = storage_dir + value_itchat_instance.instance_name + '.pkl'
        '''
        make dir
        '''
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

        with open(storage_path, 'w') as f :
            f.write(value_itchat_instance.instance_name)

        print('offline itchat loggin : ', value_itchat_instance.instance_name)
        value_itchat_instance.login_callback()

        while True :
            value_itchat_instance.func_dispatcher['offline_itchat_run'](value_itchat_instance)
            time.sleep(1)
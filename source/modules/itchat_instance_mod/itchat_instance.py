import itchat
import os
import threading
import time
import random
import ctypes
from models import base

class ns_itchat_instance:
    @staticmethod
    def terminate_thread(thread):
        if not thread.isAlive():
            return

        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(thread.ident), exc)
        if res == 0:
            raise ValueError("nonexistent thread id")
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")


class itchat_instance:
    '''
    for itchat instance
    '''
    def __init__(self, instance_name = 'default_name'):
        super().__init__()
        self.instance_name = instance_name
        self.itchat_name = ''
        self.run_thread = None
        self.instance = itchat.new_instance()

        self.on_receive_callback = None
        self.on_login_callback = None
        self.on_logout_callback = None
        self.on_newfriend_arrive_callback = None

    '''
    storage_dir is dir/ 
    '''
    def login_and_run(self, storage_dir) :
        if self.run_thread is None :
            self.run_thread = threading.Thread(target=itchat_instance.itchat_run, args=(self, storage_dir) )
            self.run_thread.start()

    def logout(self, is_keep_hotload = True) :
        if not is_keep_hotload :
            self.instance.logout()
            self.run_thread.join(2)
        else :
            ns_itchat_instance.terminate_thread(self.run_thread)


    def login_callback(self):
        friend_info = self.get_friend_infos(True)
        self.itchat_name = friend_info[0]['NickName']
        if self.on_login_callback :
            self.on_login_callback(self)

    def logout_callback(self):
        if self.on_logout_callback :
            self.on_logout_callback(self)

    def send_msg(self, msg, toUserName):
        try:
            self.instance.send(msg=msg, toUserName=toUserName)
        except Exception as e:
            print(e)

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
        try :
            self.instance.send_image(pic_dir, to_username)
        except Exception as e :
            print(e)

    def get_head_img(self,pic_path, user_name) :
        itchat_instance.mkdir(os.path.dirname(pic_path))
        try :
            self.instance.get_head_img(userName = user_name, picDir = pic_path)
            return True 
        except Exception as e :
            print(e)
            return False

    def get_friend_infos(self, update = False):
        return self.instance.get_friends(update=update)

    def get_itchat_name(self):
        return self.itchat_name

    def get_instance_name(self):
        return self.instance_name

    def search_friends(self, userName):
        return self.instance.search_friends(userName=userName)

    def search_chatrooms(self, userName):
        return self.instance.search_chatrooms(userName=userName)

    @staticmethod
    def itchat_run(value_itchat_instance, storage_dir):

        storage_path = storage_dir + value_itchat_instance.instance_name + '.pkl'
        '''
        make dir
        '''
        itchat_instance.mkdir(os.path.dirname(storage_path))

        value_itchat_instance.instance.auto_login(enableCmdQR=False, hotReload=True, statusStorageDir=storage_path,
                                 loginCallback=value_itchat_instance.login_callback, exitCallback=value_itchat_instance.logout_callback)

        @value_itchat_instance.instance.msg_register([itchat.content.TEXT, itchat.content.MAP,
                                                      itchat.content.CARD, itchat.content.NOTE, itchat.content.SHARING,
                                                      itchat.content.PICTURE, itchat.content.RECORDING, itchat.content.ATTACHMENT,
                                                      itchat.content.VIDEO],isFriendChat=True, isGroupChat=True, isMpChat=True)
        def receive(msg):
            if value_itchat_instance.on_receive_callback :
                return value_itchat_instance.on_receive_callback(value_itchat_instance, msg)
            else :
                return None

        @value_itchat_instance.instance.msg_register(itchat.content.FRIENDS)
        def add_friend_info(msg):
            if value_itchat_instance.on_newfriend_arrive_callback :
                value_itchat_instance.on_newfriend_arrive_callback(value_itchat_instance, msg)

        value_itchat_instance.instance.run()



    @staticmethod
    def mkdir(dir) :
        '''
        make dir
        '''
        if not os.path.exists( dir) :
            os.makedirs(dir)
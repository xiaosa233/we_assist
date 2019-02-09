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


class itchat_instance(base.base):
    '''
    for itchat instance
    '''
    def __init__(self, instance_name = 'default_name'):
        super().__init__()
        self.instance_name = instance_name
        self.instance = itchat.new_instance()
        self.run_thread = None      

        self.on_receive_callback = None
        self.on_login_callback = None
        self.on_logout_callback = None
        self.on_newfriend_arrive_callback = None

    def initialize(self):
        self.register()

    def tick(self, delta_time):
        #deal with message
        pass

    '''
    storage_dir is dir/ 
    '''
    def login_and_run(self, storage_dir) :
        if self.run_thread is None :
            storage_path = storage_dir+self.instance_name+'.pkl'
            '''
            make dir
            '''
            itchat_instance.mkdir(os.path.dirname(storage_path))

            self.instance.auto_login(enableCmdQR=True, hotReload= True, statusStorageDir=storage_path,loginCallback=self.login_callback,exitCallback=self.logout_callback)
            self.run_thread = threading.Thread(target=itchat_instance.itchat_run, args=(self, ) )
            self.run_thread.start()

    def logout(self, is_keep_hotload = True) :
        if not is_keep_hotload :
            self.instance.logout()
            self.run_thread.join(2)
        else :
            ns_itchat_instance.terminate_thread(self.run_thread)


    def login_callback(self):
        if self.on_login_callback :
            self.on_login_callback(self)

    def logout_callback(self):
        if self.on_logout_callback :
            self.on_logout_callback(self)

    def send_msg(self, toUserName, msg):
        try:
            self.instance.send(msg=msg, toUserName=toUserName)
        except Exception as e:
            print(e)

    def send_msg_check(self, to_username, msg) :
        max_words = 800
        if(len(msg) <= max_words) :
            self.send_msg(to_username, msg)
        else :
            msg_len = len(msg)
            while( msg_len > 0) :
                tosend_msg = msg[: max_words if msg_len >= max_words else msg_len]
                self.send_msg(to_username, tosend_msg)
                time.sleep(random.random() * 2 + 1) # 防封号
                msg = msg[max_words if msg_len >= max_words else msg_len:]
                msg_len = len(msg)

    def send_img(self, to_username, pic_dir) :
        try :
            self.instance.send_image(pic_dir, to_username)
        except Exception as e :
            print(e)

    def get_head_img(self,user_name, pic_dir) :
        itchat_instance.mkdir(os.path.dirname(pic_dir))
        try :
            self.instance.get_head_img(userName = user_name, picDir = pic_dir)
            return True 
        except Exception as e :
            print(e)
            return False

    @staticmethod
    def itchat_run(value_itchat_instance):
        @value_itchat_instance.instance.msg_register(itchat.content.TEXT)
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
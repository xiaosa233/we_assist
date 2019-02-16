import threading
import itchat_instance
import time
import random
import os
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

    def login_and_run(self, storage_dir) :
        if self.run_thread is None :
            self.run_thread = threading.Thread(target=offline_itchat_instance.itchat_run, args=(self, storage_dir) )
            self.run_thread.start()

    def logout(self, is_keep_hotload = True) :
        if not is_keep_hotload :
            self.instance.logout()
            self.run_thread.join(2)
        else :
            itchat_instance.ns_itchat_instance.terminate_thread(self.run_thread)


    def login_callback(self):
        self.itchat_name = 'xiaojian'
        if self.on_login_callback :
            self.on_login_callback(self)

    def logout_callback(self):
        if self.on_logout_callback :
            self.on_logout_callback(self)

    def send_msg(self, to_username, msg):
        print('offline_itchat send msg : ', to_username, msg)

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
        print('offline_itchat send img : ', to_username, pic_dir)

    def get_head_img(self, user_name, pic_dir) :
        print('offline_itchat get head img : ', user_name, pic_dir)

    def get_friend_infos(self, update = False):
        return {}

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
            time.sleep(1)
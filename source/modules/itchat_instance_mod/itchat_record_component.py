import itchat_base_component
import collections
import re
import record_object
from log_controller import log_controller
from models import task_deque
import time

import shutil

import os

class itchat_record_component (itchat_base_component.itchat_base_component) :
    def __init__(self, outer):
        super().__init__()
        self.outer = outer
        self.v_itchat = self.outer.get_itchat()
        self.msg_history = collections.deque()
        self.my_user_name = 'none'
        self.message_out_time = 60 * 2 + 1
        self.task_component = None

    def on_start(self):
        super().register()
        self.task_component = self.outer.get_component('itchat_task_component')


    def on_close(self):
        #remove old files
        tmp_dir = self.get_recv_dir()
        if os.path.exists(tmp_dir) :
            shutil.rmtree(tmp_dir)

    def on_login(self):
        friend_infos = self.v_itchat.get_friend_infos()
        self.my_user_name = friend_infos[0]['UserName']

    def on_receive(self, msg):
        print(msg)
        if msg['ToUserName'] != self.my_user_name:
            return

        if self.task_component :
            self.task_component.add_task(task_deque.task_unit(self.on_receive_impl, msg))
        else :
            log_controller.g_log('warning: in itchat_record_component, itchat_task_component is None')

    def on_receive_impl(self, msg):
        if msg['Type'] == 'Text' or msg['Type']=='Recording' or msg['Type'] == 'Attachment'\
                or msg['Type']=='Video' or msg['Type']=='Picture':
            self.msg_history.append( record_object.record_object(msg, self.get_recv_dir() ))
        elif msg['Type'] == 'Note' :
            if re.search(r"\<\!\[CDATA\[.*撤回了一条消息\]\]\>", msg['Content']) :
                self.on_revoke_msg(msg)


    def tick(self, delta_time):
        #remove outer 2min message
        out_time = time.time() - self.message_out_time
        now_len = len(self.msg_history)
        while len(self.msg_history) > 0 and self.msg_history[0].get_create_time() < out_time :
            self.msg_history.pop()

        after_len = len(self.msg_history)
        if after_len > now_len :
               print(' pop element number = ', after_len - now_len)

    def on_revoke_msg(self, msg):
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)

        record_object = None
        for it in self.msg_history:
            if it.get_key() == old_msg_id:
                record_object = it
                break

        if record_object :
            if record_object.is_text():
                self.msg_history.remove(record_object)
                revoke_msg = record_object.get_revoke_msg(self.outer)
                log_controller.g_log(revoke_msg)
                self.outer.send_msg(revoke_msg)
            else :
                record_object.asyn_revoke(self.outer, self.on_revoke_file_downloaded)

    def on_revoke_file_downloaded(self, revoke_msg, file_path, is_picture):
        log_controller.g_log(revoke_msg)
        self.outer.send_msg(revoke_msg)

        if not os.path.exists(file_path) :
            return

        if is_picture :
            self.outer.send_image(file_path)
        else :
            self.outer.send_file(file_path)

    def get_recv_dir(self):
        return self.outer.get_itchat_data_dir() + 'rec/'
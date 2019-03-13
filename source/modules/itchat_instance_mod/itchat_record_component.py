import itchat_base_component
import collections
import re
import record_object
from log_controller import log_controller
import time
class itchat_record_component (itchat_base_component.itchat_base_component) :
    def __init__(self, outer):
        super().__init__()
        self.outer = outer
        self.v_itchat = self.outer.get_itchat()
        self.msg_history = collections.deque()
        self.my_user_name = 'none'
        self.message_out_time = 60 * 2 + 1

    def on_start(self):
        super().register()

    def on_login(self):
        friend_infos = self.v_itchat.get_friend_infos()
        self.my_user_name = friend_infos[0]['UserName']

    def on_receive(self, msg):
        print(msg)
        if msg['ToUserName'] != self.my_user_name:
            return

        if msg['Type'] == 'Text':
            #new message, assemble c
            self.msg_history.append( self.create_record_object(msg))
        elif msg['Type'] == 'Note' :
            if re.search(r"\<\!\[CDATA\[.*撤回了一条消息\]\]\>", msg['Content']) :
                self.on_revoke_msg(msg)


    def create_record_object(self, msg):
        group_name = ''
        is_group_msg = False
        from_name = ''
        if 'ActualNickName' in msg :
            group_name = msg['User']['NickName']
            is_group_msg = True
            from_name = msg['ActualNickName']
        else :
            from_name = self.v_itchat.search_friends(msg['FromUserName'])
            if from_name :
                from_name = self.outer.get_friendly_name(from_name)
            else :
                from_name = 'xx错误'

        result_object = None
        if is_group_msg :
            result_object = record_object.group_record_object(msg['MsgId'], from_name, msg['Text'], msg['CreateTime'],
                                                              group_name)
        else :
            result_object = record_object.record_object(msg['MsgId'], from_name, msg['Text'], msg['CreateTime'])

        return result_object

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
        for it in self.msg_history :
            if it.get_key() == old_msg_id :
                record_object = it
                break


        if record_object :
            self.msg_history.remove(record_object)
            revoke_msg = record_object.get_revoke_msg()
            log_controller.g_log(revoke_msg)
            self.outer.send_msg(revoke_msg)
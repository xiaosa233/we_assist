from utils import func_library
import os
from os import path

class record_object:
    def __init__(self, msg, receive_dir):
        self.msg = msg
        self.receive_dir = receive_dir
        if not path.exists( self.receive_dir):
            os.makedirs( self.receive_dir)

    def get_create_time(self):
        return self.msg['CreateTime']

    def get_key(self):
        return self.msg['MsgId']

    def is_text(self):
        return self.msg['Type'] == 'Text'

    def get_revoke_msg(self, itchat_controller):
        reply_msg = ''
        try :
            group_name = ''
            is_group_msg = False
            from_name = ''
            if 'ActualNickName' in self.msg :
                group_name = self.msg['User']['NickName']
                is_group_msg = True
                from_name = self.msg['ActualNickName']
            else :
                from_name = itchat_controller.get_itchat().search_friends(self.msg['FromUserName'])
                if from_name :
                    from_name = itchat_controller.get_friendly_name(from_name)
                else :
                    from_name = 'xx错误'
            create_time = func_library.func_library.timestamp_to_datetime(self.msg['CreateTime'])

            if self.msg['Type'] == 'Text' :
                if is_group_msg :
                    reply_msg = '消息撤回' + create_time + ': ' + from_name + ' 在群里 ' + group_name + ' ' + self.msg['Text']
                else :
                    reply_msg = '消息撤回' + create_time + ': ' + from_name + ' ' + self.msg['Text']
            else :
                if is_group_msg :
                    reply_msg = '消息撤回' + create_time + ': ' + from_name + ' 在群里 ' + group_name + ' 撤回了文件或者图片'
                else :
                    reply_msg = '消息撤回' + create_time + ': ' + from_name + ' 撤回了文件或者图片'

        except Exception as e :
            reply_msg = str(e)

        return reply_msg

    def asyn_revoke(self, itchat_controller, aysn_callback):
        reply_msg = ''
        try :
            reply_msg = self.get_revoke_msg(itchat_controller)

            if self.msg['Type'] == 'Recording' or self.msg['Type'] == 'Attachment' \
                    or self.msg['Type'] == 'Video' or self.msg['Type']=='Picture':
                file_path = self.receive_dir + self.msg['FileName']
                self.msg['Text'](file_path)
                aysn_callback(reply_msg, file_path, self.msg['Type'] == 'Picture')
        except Exception as e :
            reply_msg = str(e)
            aysn_callback(reply_msg, "", False)


import itchat_base_component
from utils.function_dispatcher import function_dispatcher
from controllers.log_controller import log_controller
from utils.func_library import func_library
class itchat_input_component(itchat_base_component.itchat_base_component) :
    def __init__(self, outer):
        super().__init__()
        self.outer = outer
        self.v_itchat = self.outer.get_itchat()

    def on_receive(self, msg):
        if msg['ToUserName'] == self.outer.filehelper_name and msg['Type'] == 'Text' :
            #debug
            print('receive from 文件助手 : ', msg['TEXT'])

            if msg['Text'] == '帮助' :
                self.outer.send_msg( self.get_helper() )
            elif msg['Text'] == '1' or msg['Text'] == '个性签名' :
                self.get_all_signature()

    def get_all_signature(self):
        friend_infos = self.v_itchat.get_friend_infos()
        msg = ''
        for it in friend_infos :
            msg += self.outer.get_friendly_name(it) + ' : ' + it['Signature'] + '\n'
        self.outer.send_msg(msg)

    def get_helper(self):
        return '1.[个性签名]获取好友个性签名\n没什么，hhh\n=====\n发送数字或者指令执行相关功能'
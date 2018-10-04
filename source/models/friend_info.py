from modules.monitor_variable import * 

class friend_info :

    def __init__(self, user_name="", nickname = "", signature="", headimgurl="") :
        self.user_name = user_name
        self.monitor_nickname = monitor_variable.monitor_variable(nickname)
        self.monitor_signature = monitor_variable.monitor_variable(signature)
        self.monitor_headimgurl = monitor_variable.monitor_variable(headimgurl)
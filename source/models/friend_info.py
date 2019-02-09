import monitor_variable

class friend_info :

    def __init__(self, user_name="", nickname = "", signature="") :
        self.user_name = user_name
        self.monitor_nickname = monitor_variable.monitor_variable(nickname)
        self.monitor_signature = monitor_variable.monitor_variable(signature)
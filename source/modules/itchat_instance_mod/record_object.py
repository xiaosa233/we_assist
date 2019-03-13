class record_object:
    def __init__(self, in_key, from_name, msg, in_create_time):
        self.key = in_key
        self.from_name = from_name
        self.create_time = in_create_time
        self.msg = msg

    def reset(self):
        pass

    def get_create_time(self):
        return self.create_time

    def get_key(self):
        return self.key

    def get_revoke_msg(self):
        return self.from_name + ' 撤回了消息 :' + self.msg


class group_record_object(record_object) :
    def __init__(self, in_key, from_name, msg, in_create_time, group_name):
        super().__init__(in_key, from_name, msg, in_create_time)
        self.group_name = group_name

    def get_revoke_msg(self):
        return self.from_name + ' 在群里 ' + self.group_name + ' 撤回了消息 :' + self.msg

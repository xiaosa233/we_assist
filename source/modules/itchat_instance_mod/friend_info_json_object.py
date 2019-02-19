from models import json_object
import friend_info

class friend_info_json_object(json_object.json_object):
    def __init__(self, key_func):
        super().__init__()
        self.key_func = key_func


    def value_to_json(self, value):
        json_data = {}

        # user_name every_time is different ,so we can not user the same username
        friend_infos = value
        for it in friend_infos:
            #print( 'test ', self.key_func(it))
            json_data[self.key_func(it)] = {'nickname': it['NickName'], 'signature': it['Signature']}

        self.set_json_data(json_data)


    def json_to_value(self, friend_infos):
        json_data = super().json_to_value()
        if json_data is None :
            return {}
        result = {}
        for it in friend_infos :
            key = self.key_func(it)
            if key in json_data :
                json_item = json_data[key]
                result[ it['UserName']] = friend_info.friend_info( it['UserName'], json_item['nickname'], json_item['signature'])

        return result
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


    def json_to_value(self, name_map_key):
        json_data = super().json_to_value()
        result = {}
        if json_data is None :
            return result
        for (key, value) in json_data.items():
            if key in name_map_key:
                result[name_map_key[key] ] = friend_info.friend_info( name_map_key[key], value['nickname'], value['signature'])

        return result
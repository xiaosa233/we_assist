from models import json_object


class friend_info_json_object(json_object.json_object):
    def __init__(self, in_json_coder, in_json_key):
        super().__init__(in_json_coder, in_json_key)

    def value_to_json(self, value):
        pass


    def json_to_value(self):
        pass
from utils import json_coder


class json_object :
    def __init__(self, in_json_coder, in_json_key = None):
        self.v_json_coder = in_json_coder
        self.json_key = in_json_key

    def is_key_none(self):
        return self.json_key is None

    # virtual
    def value_to_json(self, value):
        if not self.is_key_none():
            self.v_json_coder.json_data[self.json_key] = value
        else:
            self.v_json_coder.json_data = value

    # virtual
    def json_to_value(self):
        if not self.is_key_none() :
            return self.v_json_coder.get_json_data()[self.json_key]
        else :
            return self.v_json_coder.get_json_data()

    def write_file(self):
        self.v_json_coder.write_file()


    def udpate_value_to_file(self, value):
        self.value_to_json(value)
        self.write_file()
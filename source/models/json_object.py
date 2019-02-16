from utils import json_coder


class json_object :
    def __init__(self):
        self.v_json_coder = None
        self.json_key = None

    def open_file(self, json_file, in_json_key = None):
        self.v_json_coder = json_coder.json_coder()
        self.v_json_coder.set_path(json_file)
        self.v_json_coder.parse_file()
        self.json_key = in_json_key

    def set_json_coder(self, in_json_coder, in_json_key):
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
            if self.json_key in self.v_json_coder.get_json_data():
                return self.v_json_coder.get_json_data()[self.json_key]
            else:
                return None
        else :
            return self.v_json_coder.get_json_data()

    def write_file(self):
        self.v_json_coder.write_file()


    def update_value_to_file(self, value):
        self.value_to_json(value)
        self.write_file()

    @staticmethod
    def parse_with_file(json_file, json_key = None) :
        value = json_object()
        value.open_file(json_file, json_key)
        return value.json_to_value()

    @staticmethod
    def write_with_file(in_value, json_file, json_key = None):
        v_json_object = json_object()
        v_json_object.open_file(json_file, json_key)
        v_json_object.update_value_to_file(in_value)
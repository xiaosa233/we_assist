
import json
import os

class json_coder:
    def __init__(self):
        self.json_data = {}
        self.json_file_path = ''

    def set_path(self, file_path) :
        self.json_file_path = file_path

    def get_json_data(self):
        return self.json_data

    def set_json_data(self, in_json_data):
        self.json_data = in_json_data

    def parse_file(self):
        work_file_path = self.json_file_path

        json_data = {}
        if os.path.isfile(work_file_path) and os.path.exists(work_file_path) :
            with open(work_file_path, 'r', encoding='utf-8') as f :
                try :
                    json_data = json.load(f)
                except Exception as e :
                    print(e)
        self.json_data = json_data
        return self.json_data

    def parse_str(self, json_str):
        self.json_data =  json.load(json_str)
        return self.json_data

    def reset(self):
        self.json_data = {}
        self.json_file_path = ''

    def write_file(self):
        work_file_path = self.json_file_path
        json_coder.mkdir( os.path.dirname(work_file_path))
        with open(work_file_path, 'w', encoding='utf-8') as f :
            f.write(json.dumps(self.json_data ))

    @staticmethod
    def mkdir(dir) :
        '''
        make dir
        '''
        if not os.path.exists( dir) :
            os.makedirs(dir)

    @staticmethod
    def parse_with_file(file_path):
        value = json_coder()
        value.set_path(file_path)
        return value.parse_file()

    @staticmethod
    def parse_with_string(json_str):
        value = json_coder()
        return value.parse_str(json_str)

    @staticmethod
    def write_file(json_data, file_path):
        value = json_coder()
        value.set_path(file_path)
        value.set_json_data(json_data)
        value.write_file()
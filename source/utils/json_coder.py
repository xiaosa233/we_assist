
import json
import os

class json_coder:
    def __init__(self):
        self.json_data = {}
        self.json_file_path = ''

    def set_path(self, file_path) :
        self.json_file_path = file_path

    def parse_file(self, file_path = ''):
        work_file_path = self.json_file_path
        if os.path.isfile(file_path):
            work_file_path = file_path

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
        self.json_file_path = ''

    def write_file(self, json_data, file_path = ''):
        work_file_path = self.json_file_path
        if os.path.isfile(file_path):
            work_file_path = file_path

        json_coder.mkdir( os.path.dirname(work_file_path))
        with open(work_file_path, 'w', encoding='utf-8') as f :
            f.write(json.dumps(json_data ))

        self.json_data = json_data

    @staticmethod
    def mkdir(dir) :
        '''
        make dir
        '''
        if not os.path.exists( dir) :
            os.makedirs(dir)

import json
import os

class json_coder:
    def __init__(self, in_map):
        self.json_data_ref = in_map
        self.json_file_path = ''

    def set_path(file_path) :
        self.json_file_path = file_path

    def parse_file(self, file_path = ''):
        work_file_path = self.json_file_path
        if os.path.isfile(file_path):
            work_file_path = file_path

        if os.path.isfile(work_file_path) and os.path.exists(work_file_path) :
            with open(work_file_path, 'r', encoding='utf-8') as f :
                file_data = json.load(f)
                for key in file_data :
                    self.json_data_ref[key] = file_data[key]
        else :
            self.json_data_ref.clear()
        return self.json_data_ref

    def parse_str(self, json_str):
        str_data = json.load(json_str)
        for key in str_data :
            self.json_data_ref[key] = str_data
        return self.json_data_ref

    def reset(self, in_map):
        self.json_data_ref = in_map
        self.json_file_path = ''

    def write_file(self, file_path = ''):
        work_file_path = self.json_file_path
        if os.path.isfile(file_path):
            work_file_path = file_path

        json_coder.mkdir( os.path.dirname(work_file_path))
        with open(work_file_path, 'r', encoding='utf-8') as f :
            f.write(json.dump(self.json_data_ref))


    @staticmethod
    def mkdir(dir) :
        '''
        make dir
        '''
        if not os.path.exists( dir) :
            os.makedirs(dir)
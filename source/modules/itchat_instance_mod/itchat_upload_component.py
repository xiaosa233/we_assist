import itchat_base_component
import shutil
import tempfile
import os
import random
'''
因为itchat 不能上传带中文路径的文件或者图片
所有通过这个component 进行修复
'''
class itchat_upload_component(itchat_base_component.itchat_base_component):
    def __init__(self, outer):
        super().__init__()
        self.outer = outer


    def request_send(self, to_send_path):
        result_path = to_send_path
        if self.is_contain_chinese(to_send_path) :
            #copy file to tmp files and rename it
            result_path = self.generate_tmp_path(to_send_path)
            print('file random', to_send_path, ' -> ', result_path)
            shutil.copy(to_send_path, result_path)

        return result_path

    def on_close(self):
        #remove old files
        tmp_dir = self.get_tmp_dir()
        if os.path.exists(tmp_dir) :
            shutil.rmtree(tmp_dir)


    def generate_tmp_path(self, file_path):
        tmp_dir = self.get_tmp_dir()
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        extension = os.path.splitext(file_path)[1]

        new_filename = ''
        while True :
            new_filename = self.generate_random_filename(file_path)
            if not os.path.exists(tmp_dir + new_filename + extension) :
                break

        return tmp_dir + new_filename + extension

    '''
    generate file to 16-char file with number and characters
    '''
    def generate_random_filename(self, text):
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
        length = len(base_str) - 1
        for i in range(16):
            random_str += base_str[random.randint(0, length)]
        return random_str

    def get_tmp_dir(self):
        return tempfile.gettempdir() + '/itchat/'


    @staticmethod
    def is_contain_chinese(text):
        for char in text :
            if '\u4e00' <= char <= '\u9fff' :
                return True
        return False


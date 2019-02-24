from PIL import Image
from os import path


class func_library :



    @staticmethod
    def get_windows_valid_path(file_name) :
        invalid_chars = ['/','\\',':','*','?','"','<','>','|']
        new_path = ''
        for char in file_name :
            if char not in invalid_chars :
                new_path += char
        if new_path == '' :
            new_path = 'impossable'
        return new_path





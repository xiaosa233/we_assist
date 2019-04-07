from PIL import Image
from os import path
from datetime import datetime

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

    @staticmethod
    def timestamp_to_datetime(timestamp):
        # if you encounter a "year is out of range" error the timestamp
        # may be in milliseconds, try `ts /= 1000` in that case
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')




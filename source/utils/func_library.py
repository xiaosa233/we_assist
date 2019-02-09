from PIL import Image
from os import path



class func_library :

    @staticmethod
    def is_img_size_different(img_path_a, img_path_b) :
        if path.exists(img_path_a) and path.exists(img_path_b) :
            try :
                img_a = Image.open(img_path_a)
                img_b = Image.open(img_path_b)
                result = not(img_a.size[0] == img_b.size[0] and img_a.size[1] == img_b.size[1])
                img_a.close()
                img_b.close()
                return result
            except Exception as e :
                pass

        
        return False

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



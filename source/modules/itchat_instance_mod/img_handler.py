from os import path
from PIL import Image
class img_handler :
    def __init__(self, in_path):
        self.src_path = in_path


    def __eq__(self, other):
        return not self.is_img_different(self.src_path, other.src_path)

    def get_src_path(self):
        return self.src_path


    @staticmethod
    def get_file_size_in_kb(path_a):
        a_size = path.getsize(path_a)
        return int(a_size / 1024.0)


    @staticmethod
    def is_img_different(img_path_a, img_path_b) :
        if path.exists(img_path_a) and path.exists(img_path_b) :
            if img_path_a == img_path_b :
                return False
            try :
                if abs(img_handler.get_file_size_in_kb(img_path_a) - img_handler.get_file_size_in_kb(img_path_b) ) < 1:
                    return True

                img_a = Image.open(img_path_a)
                img_b = Image.open(img_path_b)
                result = not(img_a.size[0] == img_b.size[0] and img_a.size[1] == img_b.size[1])
                img_a.close()
                img_b.close()
                return result
            except Exception as e :
                pass


        return False
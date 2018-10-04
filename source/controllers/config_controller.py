import os
import os.path as path


class config_controller :

    @staticmethod 
    def get_project_dir() :
        current_path = os.path.realpath(__file__)
        controllers_dir = path.dirname(current_path)
        source_dir = path.dirname(controllers_dir)
        return path.dirname(source_dir) + "/"

    @staticmethod 
    def get_save_dir() :
        return config_controller.get_project_dir() + "save/"
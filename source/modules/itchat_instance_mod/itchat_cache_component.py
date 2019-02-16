import itchat_base_component
from utils import json_coder
import friend_info_json_object

class itchat_cache_component(itchat_base_component.itchat_base_component) :

    def __init__(self, outer_controller):
        super().__init__()
        self.outer = outer_controller
        self.v_itchat = outer_controller.get_itchat()
        self.friend_info = {}
        self.json_friend_info = None

    def on_login(self):
        #todo 拿到微信的名称，同步json 变量
        itchat_name = self.v_itchat.get_itchat_name()
        self.friend_info.set_value( self.v_itchat.get_friend_infos())
        save_data_json = json_coder.json_coder()
        save_data_json.set_path( self.get_save_data_dir() + "itchat.json" )
        self.json_friend_info = friend_info_json_object(save_data_json, 'friend_info')




    def update_friend_info(self):

        pass
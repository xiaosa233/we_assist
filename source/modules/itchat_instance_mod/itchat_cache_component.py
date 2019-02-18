import itchat_base_component
from utils import json_coder
import friend_info_json_object
import friend_info
import json_object
from controllers import log_controller


class itchat_cache_component(itchat_base_component.itchat_base_component) :

    def __init__(self, outer_controller):
        super().__init__()
        self.outer = outer_controller
        self.v_itchat = outer_controller.get_itchat()
        self.v_friend_infos = {}
        self.json_friend_info = None
        self.json_friend_map = None

    def on_login(self):
        # load json_data
        self.init_json_file()
        self.update_friend_infos()

        # remove key which not in friend_infos
        friend_infos = self.v_itchat.get_friend_infos(update=False)
        friend_info_keys = {it['UserName']: 1 for it in friend_infos}

        to_remove_keys = []
        for key in self.v_friend_infos:
            if key not in friend_info_keys:
                to_remove_keys.append(key)

        for it in to_remove_keys:
            del self.v_friend_infos[it]

    def on_close(self):
        self.udpate_data_to_json( self.v_itchat.get_friend_infos() )

    def update_friend_infos(self, update = False):
        friend_infos = self.v_itchat.get_friend_infos(update)
        print(friend_infos)
        response_msg = ''
        for info_it in friend_infos:
            # print(info_it['UserName'], '  ', info_it['NickName'], '  ', info_it['Signature'], )
            if info_it['UserName'] not in self.v_friend_infos:
                self.v_friend_infos[info_it['UserName']] = friend_info.friend_info(info_it['UserName'],
                                                                                   info_it['NickName'],
                                                                                   info_it['Signature'])
            else:
                now_it = self.v_friend_infos[info_it['UserName']]
                response_name = self.outer.get_friendly_name(info_it)

                if now_it.monitor_nickname.set_value(info_it['NickName']):
                    tmp_msg = response_name + ' 修改了昵称 : ' + now_it.monitor_nickname.get_last_value() + " --> " + now_it.monitor_nickname.get_value()
                    response_msg += tmp_msg + "\n"
                    log_controller.g_log(tmp_msg)
                if now_it.monitor_signature.set_value(info_it['Signature']):
                    tmp_msg = response_name + ' 修改了个性签名 : ' + now_it.monitor_signature.get_last_value() + " --> " + now_it.monitor_signature.get_value()
                    response_msg += tmp_msg + "\n"
                    log_controller.g_log(tmp_msg)
        if response_msg != '':
            # send to filehelper
            self.udpate_data_to_json(friend_infos)
            self.v_itchat.send_msg_check(self.outer.filehelper_name, response_msg)

    def init_json_file(self):
        self.json_friend_info = friend_info_json_object.friend_info_json_object(self.outer.get_friendly_name)
        self.json_friend_map = json_object.json_object()
        v_json_coder = json_coder.json_coder()
        v_json_coder.set_path(self.get_cache_json())
        v_json_coder.parse_file()
        self.json_friend_info.set_json_coder(v_json_coder, 'friend_infos')
        self.json_friend_map.set_json_coder(v_json_coder, 'friendly_name_map')

        friend_infos = self.v_itchat.get_friend_infos()
        name_map_key = self.get_friendly_name_map(friend_infos)

        self.v_friend_infos = self.json_friend_info.json_to_value(name_map_key)

    def udpate_data_to_json(self, friend_infos):
        self.json_friend_info.value_to_json(friend_infos)
        self.json_friend_map.value_to_json(self.get_friendly_name_map(friend_infos))
        self.json_friend_map.write_file()

    def get_friendly_name_map(self, friend_infos):
        # create_map
        invalid_key = []  # if there are two same friendly name send_msgthen we ignore it
        name_map_key = {}
        for it in friend_infos:
            friendly_name = self.outer.get_friendly_name(it)
            if friendly_name in invalid_key:
                continue
            if friendly_name not in name_map_key:
                name_map_key[friendly_name] = it['UserName']
            else:
                del name_map_key[friendly_name]
                invalid_key.append(friendly_name)

        return name_map_key


    def get_cache_json(self) :
        return self.outer.get_itchat_data_dir() + 'cache.json'
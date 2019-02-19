import import_source
from utils import function_dispatcher
from models import ticker
from models import json_object
from controllers import config_controller
import time
import random


class test_case :

    def __init__(self):

        self.pre_time = 0.0
        self.ticker = ticker.ticker(5.0)
        self.last_test_mode = False
        self.json_test_mode = None
        self.friend_info = self.get_default_friend_infos()

        self.function_dispatcher = function_dispatcher.function_dispatcher.open()
        self.function_dispatcher['get_friend_infos'].add(self.on_get_friend_infos)
        self.function_dispatcher['offline_itchat_run'].add(self.on_itchat_run)


    def close(self):
        self.function_dispatcher['get_friend_infos'].remove(self.on_get_friend_infos)
        self.function_dispatcher['offline_itchat_run'].remove(self.on_itchat_run)
        function_dispatcher.function_dispatcher.close( self.function_dispatcher.name)

        if self.json_test_mode is not None and self.json_test_mode.json_to_value() != self.last_test_mode:
            self.json_test_mode.update_value_to_file(self.last_test_mode)

    def run(self):
        self.set_test_mode()
        self.pre_time = time.time()


    def set_test_mode(self) :
        self.json_test_mode = json_object.json_object()
        self.json_test_mode.open_file(config_controller.config_controller.get_save_dir() + 'world_config.json', 'test_mode')
        self.last_test_mode = self.json_test_mode.json_to_value()
        if not self.last_test_mode :
            self.json_test_mode.update_value_to_file(True)

    def on_itchat_run(self, itchat_instance):
        last_time = self.pre_time
        self.pre_time = time.time()
        last_delta_time = self.pre_time - last_time

        if self.ticker.tick(last_delta_time) :
            #change some thing
            len_info = len(self.friend_info)
            if len_info > 1:
                index = random.randint(1, len_info-1)
                self.friend_info[index]['Signature'] = self.get_random_signature()
                print('name:', self.friend_info[index]['NickName'], ':', self.friend_info[index]['Signature'])

    def on_get_friend_infos(self, itchat_instance):
        return self.friend_info

    def get_random_signature(self):
        first_map = ['高兴的', '沮丧的', '兴奋的', '快乐的', '惊喜的']
        second_map = ['airpod', '森林', '佩弦', '小键', '嘻嘻嘻', '遥控器']
        first_index = random.randint(0, len(first_map)-1)
        second_index = random.randint(0, len(second_map)-1)
        return first_map[first_index] + second_map[second_index]


    def get_default_friend_infos(self):
        return [{'UserName': '@4933804bb6f5a30c2e89fea37c5253b1a2de09d7c163d16993d5655343259aab', 'City': '', 'DisplayName': '', 'PYQuanPin': '', 'RemarkPYInitial': '', 'Province': '', 'KeyWord': '', 'RemarkName': '', 'PYInitial': '', 'EncryChatRoomId': '', 'Alias': '', 'Signature': '', 'NickName': '小伍', 'RemarkPYQuanPin': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=121349541&username=@4933804bb6f5a30c2e89fea37c5253b1a2de09d7c163d16993d5655343259aab&skey=@crypt_5f5822ec_2afe08911953ef1cdeea2973bb6666c0', 'UniFriend': 0, 'Sex': 1, 'AppAccountFlag': 0, 'VerifyFlag': 0, 'ChatRoomId': 0, 'HideInputBarFlag': 0, 'AttrStatus': 0, 'SnsFlag': 48, 'MemberCount': 0, 'OwnerUin': 0, 'ContactFlag': 0, 'Uin': 2843835563, 'StarFriend': 0, 'Statues': 0, 'WebWxPluginSwitch': 0, 'HeadImgFlag': 1}, {'Uin': 0, 'UserName': '@8f3715093a512ccbb88e28fabdd7c46017757528c4ee9fb2147a0a0ee0ccb1cc', 'NickName': '网购小帮手〖不懂可回复帮助〗', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=670190327&username=@8f3715093a512ccbb88e28fabdd7c46017757528c4ee9fb2147a0a0ee0ccb1cc&skey=@crypt_5f5822ec_2afe08911953ef1cdeea2973bb6666c0', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 2, 'Signature': '淘宝天猫任何商品可查内部优惠券+现金返利', 'VerifyFlag': 0, 'OwnerUin': 0, 'PYInitial': 'WGXBSBDKHFBZ', 'PYQuanPin': 'wanggouxiaobangshoubudongkehuifubangzhu', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'AttrStatus': 233509, 'Province': '广东', 'City': '广州', 'Alias': '', 'SnsFlag': 1, 'UniFriend': 0, 'DisplayName': '', 'ChatRoomId': 0, 'KeyWord': '', 'EncryChatRoomId': '', 'IsOwner': 0}, {'Uin': 0, 'UserName': '@14c8d62550933543bfba39e5e658c84af5fa385e1d0088e0612b76b7eefa559c', 'NickName': '志龙', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=670202400&username=@14c8d62550933543bfba39e5e658c84af5fa385e1d0088e0612b76b7eefa559c&skey=@crypt_5f5822ec_2afe08911953ef1cdeea2973bb6666c0', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '志龙', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '现在过得每一天，都是余生中最年轻的一天。', 'VerifyFlag': 0, 'OwnerUin': 0, 'PYInitial': 'ZL', 'PYQuanPin': 'zhilong', 'RemarkPYInitial': 'ZL', 'RemarkPYQuanPin': 'zhilong', 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'AttrStatus': 234277, 'Province': '广东', 'City': '深圳', 'Alias': '', 'SnsFlag': 49, 'UniFriend': 0, 'DisplayName': '', 'ChatRoomId': 0, 'KeyWord': '', 'EncryChatRoomId': '', 'IsOwner': 0}, {'Uin': 0, 'UserName': '@15fd22233ad1fb7e1de536217cacab66a95ec49b50fe0519e7f96087a625c32d', 'NickName': 'song', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=668190374&username=@15fd22233ad1fb7e1de536217cacab66a95ec49b50fe0519e7f96087a625c32d&skey=@crypt_5f5822ec_2afe08911953ef1cdeea2973bb6666c0', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '自律', 'VerifyFlag': 0, 'OwnerUin': 0, 'PYInitial': 'SONG', 'PYQuanPin': 'song', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'AttrStatus': 98749, 'Province': '广东', 'City': '肇庆', 'Alias': '', 'SnsFlag': 17, 'UniFriend': 0, 'DisplayName': '', 'ChatRoomId': 0, 'KeyWord': '', 'EncryChatRoomId': '', 'IsOwner': 0}, {'Uin': 0, 'UserName': '@31ff7fe85b89d602b49a67c09c024fb5dd54d8eb32a25df8108a3aa6318e0773', 'NickName': '小键', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=670200392&username=@31ff7fe85b89d602b49a67c09c024fb5dd54d8eb32a25df8108a3aa6318e0773&skey=@crypt_5f5822ec_2afe08911953ef1cdeea2973bb6666c0', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '小键', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '不要看了', 'VerifyFlag': 0, 'OwnerUin': 0, 'PYInitial': 'XJ', 'PYQuanPin': 'xiaojian', 'RemarkPYInitial': 'XJ', 'RemarkPYQuanPin': 'xiaojian', 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'AttrStatus': 119293, 'Province': '广东', 'City': '深圳', 'Alias': '', 'SnsFlag': 145, 'UniFriend': 0, 'DisplayName': '', 'ChatRoomId': 0, 'KeyWord': '', 'EncryChatRoomId': '', 'IsOwner': 0}]





value = test_case()
value.run()


#run here
import main

value.close()

from controllers import * 
from modules.scheduler_mod import *
import time

from datetime import datetime
class world_controller:
    
    def __init__(self) :
        self.v_itchat_controller = itchat_controller.itchat_controller()
        self.scheduler = scheduler.scheduler()


    def start(self) :
        log_controller.log_controller.g_log("we_assist begin start")
        self.v_itchat_controller.start()
        
        #scheduler task to update
        text_delta_time = 60 * 1
        self.scheduler.enqueue(time.time() + text_delta_time, self.on_update_text_msg, None, -1, text_delta_time) #6min

        img_delta_time = 60 * 5
        self.scheduler.enqueue(time.time() + img_delta_time, self.on_update_img_msg, None, -1, img_delta_time) #6min
        self.scheduler.start()
        
    def close(self) :
        self.v_itchat_controller.close()
        self.scheduler.stop()
        log_controller.log_controller.g_log("we_assist stop")

    def on_update_text_msg(self) :
        msg = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' : update text infos'
        log_controller.log_controller.g_log(msg)
        self.v_itchat_controller.update_friend_infos()

    def on_update_img_msg(self):
        msg = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' : update img infos'
        log_controller.log_controller.g_log(msg)
        self.v_itchat_controller.update_friend_head_imgs()
from controllers import * 
from modules.scheduler import *
import time

class world_controller:
    
    def __init__(self) :
        self.v_itchat_controller = itchat_controller.itchat_controller()
        self.scheduler = scheduler.scheduler()


    def start(self) :
        log_controller.log_controller.g_log("we_assist begin start")
        self.v_itchat_controller.start()
        
        #scheduler task to update
        delta_time = 60*3
        self.scheduler.enqueue(time.time() + delta_time, self.on_update, None, -1, delta_time) #6min
        self.scheduler.start()
        
    def close(self) :
        self.v_itchat_controller.close()
        self.scheduler.stop()
        log_controller.log_controller.g_log("we_assist stop")

    def on_update(self) :
        msg = time.time() + ' : update infos'
        log_controller.g_log(msg)
        self.v_itchat_controller.update_friend_infos()
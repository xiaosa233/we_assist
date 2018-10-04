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
        self.scheduler.enqueue(time.time() + 10 * 60, self.v_itchat_controller.update_friend_infos, None, -1, 10 * 60) #6min
        self.scheduler.start()
        
    def close(self) :
        self.v_itchat_controller.close()
        self.scheduler.stop()
        log_controller.log_controller.g_log("we_assist stop")
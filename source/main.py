from controllers import itchat_world_controller
from enum import IntEnum
import time
import os
import sys

class cmd_header(IntEnum):
    exit = 0
    get_all_imgs = 1

def show_cmd_helper() :
    help_str = " \n" + str(int(cmd_header.exit)) + " : exit"
    help_str += " \n" + str(int(cmd_header.get_all_imgs)) + ' : get all head imgs'
    return help_str


def main() :
    run_frame = 40 # 10hz to run
    fix_delta_time = 1.0 / run_frame

    #initialize world controller
    v_world_controller = itchat_world_controller.itchat_world_controller()
    v_world_controller.initialize(sys.argv)

    pre_time = time.time()
    delta_time = fix_delta_time


    while True :

        #print('delta', delta_time)

        v_world_controller.update(delta_time)
        if v_world_controller.is_end() :
            break

        now_time = time.time()
        delta_time = now_time - pre_time
        pre_time = now_time

        if delta_time < fix_delta_time:
            #print('sleep : ', fix_delta_time - delta_time)
            time.sleep(fix_delta_time - delta_time)
            delta_time = fix_delta_time

    v_world_controller.destroy()

main()
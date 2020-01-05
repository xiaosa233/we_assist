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
    #initialize world controller
    v_world_controller = itchat_world_controller.itchat_world_controller()
    v_world_controller.initialize(sys.argv)
    v_world_controller.loop(run_frame)
    print(' end loop!!!')
    v_world_controller.destroy()


main()

os._exit(0)

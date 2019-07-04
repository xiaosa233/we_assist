

'''
1) monitor the process
2) wake up the process
'''

import wakeup_work_controller
import sys
def main() :
    world = wakeup_work_controller.wakeup_world_controller()
    world.initialize(sys.argv)
    world.loop(0.1)
    world.destroy()


main()


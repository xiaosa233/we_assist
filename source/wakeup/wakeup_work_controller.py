from controllers import world_controller


class wakeup_world_controller(world_controller.world_controller) :


    def update(self, delta_time):
        print('delta_time = ', delta_time)

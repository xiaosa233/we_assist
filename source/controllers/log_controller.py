from models import global_accessor
class log_controller :
    v_g_log = None

    def __init__(self, log_category = "global") :
        self.log_category = log_category
        self.net_controller = None

    def get_net_controller(self):
        if self.net_controller is None :
            self.net_controller = global_accessor.global_accessor.get_safe('net_controller')

        return self.net_controller
        

    def log(self, msg) :
        if self.get_net_controller() :
            self.get_net_controller().sendout_log( self.get_log_prefix() + msg)
        log_controller.log_impl(self.get_log_prefix() + msg)

    def get_log_prefix(self) :
        return self.log_category + " : "

    @staticmethod
    def get_g_log() :
        if log_controller.v_g_log == None :
            log_controller.v_g_log = log_controller()
        return log_controller.v_g_log

    @staticmethod
    def log_impl(msg) :
        print(msg)

    @staticmethod
    def g_log(msg) :
        log_controller.get_g_log().log(msg)
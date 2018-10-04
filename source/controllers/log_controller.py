
class log_controller :
    v_g_log = None

    def __init__(self, log_category = "global") :
        self.log_category = log_category
        

    def log(self, msg) :
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
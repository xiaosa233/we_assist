class global_accessor :
    g_inst = None


    def __init__(self):
        self.map = {}


    def get_safe_impl(self, key):
        if key in self.map :
            return self.map[key]
        else :
            return None

    def set_value_impl(self, key, value):
        self.map[key] = value

    def remove_key_impl(self, key):
        if key in self.map:
            del self.map[key]

    @staticmethod
    def _inst():
        if global_accessor.g_inst is None :
            global_accessor.g_inst = global_accessor()
        return global_accessor.g_inst

    @staticmethod
    def get_safe(key):
        return global_accessor._inst().get_safe_impl(key)

    @staticmethod
    def set_value(key, value):
        global_accessor._inst().set_value_impl(key, value)

    @staticmethod
    def remove_key(key):
        global_accessor._inst().remove_key_impl(key)


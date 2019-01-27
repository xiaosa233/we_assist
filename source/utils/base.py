import function_dispatcher
class base :
    def __init__(self):
        self.v_is_tick = False
        function_dispatcher.open()['base_creation'](self)
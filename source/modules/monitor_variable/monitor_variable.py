

class ns_monitor_variable :

    #return True if they are not equal
    @staticmethod
    def default_compare (value, last_value) :
        if type(value) is type(last_value) :
            return value != last_value
        else :
            return False

class monitor_variable :
    
    def __init__(self, value = None) :
        self.value = value 
        self.last_value = None

    # return True if new value is not equal with value
    def set_value(self, in_value, compare_func = ns_monitor_variable.default_compare) :
        self.last_value = self.value
        self.value = in_value
        return compare_func(self.value, self.last_value)

    def get_value(self):
        return self.value 

    def get_last_value(self) :
        return self.last_value
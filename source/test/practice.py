class base(object):
    def __init__(self):
        print('base')


class widget (base) :
    def __init__(self):
        print('widget')


v = widget()
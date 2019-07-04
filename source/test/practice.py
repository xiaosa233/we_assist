from multiprocessing import Process
import time

def f(name):
    print('hello', name)
    time.sleep(3)
    print('ok')


class tcp_server :
    def __init__(self, ip, port, connected_cb, error_cb, msg_cb):
        self.ip = ip
        self.port = port
        self.connected_cb = connected_cb
        self.error_cb = error_cb
        self.msg_cb = msg_cb


if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()

    print('i am main over')
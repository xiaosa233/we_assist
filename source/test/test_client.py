import import_source
from modules.io_mod import tcp_client
import time




class test_client_main:
    def work(self):
        self.test_client = tcp_client.tcp_client('127.0.0.1', 23332, connected_cb=self.on_connected, error_cb=self.on_error, msg_cb =self.on_msg)
        self.is_connected = False
        self.test_client.connect()
        self.count = 0

        while True :
            self.tick()
            time.sleep(1)

    def tick(self):
        if self.is_connected :
            self.count += 1
            self.test_client.send(('hello' + str(self.count) ).encode())

    def on_error(self, exception):
        self.is_connected = False
        print('error !', str(exception))

    def on_connected(self):
        print(' connected !!!')
        self.is_connected = True

    def on_msg(self):
        pass


def main() :

    inst = test_client_main()
    inst.work()

main()
import import_source
from modules.io_mod import tcp_client
import time
import sys




class test_client_main:
    def work(self, argv):
        ip = '127.0.0.1'
        if len(argv) > 1:
            ip = argv[1]
        self.test_client = tcp_client.tcp_client(ip, 23332, connected_cb=self.on_connected, error_cb=self.on_error, msg_cb =self.on_msg)
        self.is_connected = False
        self.test_client.connect()
        self.count = 0

        while True :
            self.tick()
            time.sleep(1)

    def tick(self):
        if self.is_connected :
            self.count += 1
            #self.test_client.send(('hello' + str(self.count) ).encode())

    def on_error(self, tcp_base, exception):
        self.is_connected = False
        print('error !', str(exception))

    def on_connected(self, tcp_base):
        print(' connected !!!')
        self.is_connected = True

    def on_msg(self, tcp_base, data):
        msg = data.decode()
        msg_array = msg.split('`')

        for it in msg_array:
            if len(it) > 0:
                key_index = it.find('!')
                key = it[0:key_index]
                content = it[key_index+1:]
                print('key : ', key, ' content : ', content)


def main() :

    inst = test_client_main()
    inst.work(sys.argv)

main()
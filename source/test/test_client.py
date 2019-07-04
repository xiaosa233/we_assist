import import_source
from modules.io_mod import tcp_client
import time



def tick():
    pass


def on_connected():
    print('connected !!')


def main() :
    test_client = tcp_client.tcp_client('127.0.0.1', 23332, connected_cb=on_connected)
    test_client.connect()


    while True :
        tick()
        time.sleep(0.03)


main()
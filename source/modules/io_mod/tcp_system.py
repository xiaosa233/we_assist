import threading
import time
from models import task_deque
import asyncio

class tcp_system :
    inst = None
    def __init__(self):
        self.run_thread = None
        self.should_stop = False
        self.clients = {'1'} # make it as set
        self.task_deque = task_deque.task_deque()


    def add_client(self, in_client):
        self.clients.add(in_client)
        self.connected_client(in_client)

    def remove_client(self, in_client):
        self.clients.remove(in_client)

    def run(self):
        if not self.run_thread :
            self.should_stop = False
            self.run_thread = threading.Thread(target = self.loop)
            self.run_thread.start()


    def stop(self):
        self.should_stop = True
        if self.run_thread :
            self.run_thread.join()
            self.run_thread = None


    def update(self, delta_time):
        while self.task_deque.run_top()[0] :
            pass

    def loop(self):
        run_frame = 40
        start_time = time.time()
        fix_delta_time = 1.0 / run_frame
        last_time = start_time - fix_delta_time
        count = 0

        while not self.should_stop:
            self.update(time.time() - last_time)
            last_time = time.time()
            count += 1
            end_time = count * fix_delta_time + start_time
            if end_time > last_time:
                time.sleep(end_time - last_time)

    def connected_client(self, client):
        asyncio.run(self.connect_impl(client))


    def on_client_connected_cb(self, client):
        self.task_deque.push(client.on_connected_cb)


    def on_client_error_cb(self, client):
        self.task_deque.push(client.on_error_cb)
        if client.is_connected:
            self.task_deque.push(self.connected_client, client)



    async def connect_impl(self, client):
        try :
            client.reader, client.writer = await asyncio.open_connection(client.ip, client.port)
            self.on_client_connected_cb(client)
        except Exception as e :
            self.on_client_error_cb(client)


    @staticmethod
    def static_get():
        if not tcp_system.inst:
            tcp_system.inst = tcp_system()
        return tcp_system.inst
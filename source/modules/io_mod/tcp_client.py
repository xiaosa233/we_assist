import tcp_client_base
import threading

from models import loop_object
from enum import Enum

import asyncio
import time


class eclient_state(Enum):
    unvalid = 0
    connecting = 1
    work = 2

class tcp_client(tcp_client_base.tcp_client_base):
    def __init__(self, ip, port, connected_cb = None , error_cb = None, msg_cb = None):
        super().__init__()
        self.ip = ip
        self.port = port
        self.connected_cb = connected_cb
        self.error_cb = error_cb
        self.msg_cb = msg_cb
        self.is_connected = False
        self.run_thread = None
        self.client_state = eclient_state.unvalid

    def connect(self):
        self.is_connected = True
        if self.run_thread is None :
            self.client_state = eclient_state.connecting
            self.run_thread  = threading.Thread(target=self.client_loop_thread)
            self.run_thread.run()

    def close(self):
        self.is_connected = False
        if self.run_thread:
            self.client_state = eclient_state.unvalid
            self.run_thread.join()
            self.run_thread = None


    def client_loop_thread(self):
        asyncio.run(self.client_loop())

    async def client_loop(self):
        last_time = time.time()

        while self.is_connected :
            new_time = time.time()
            await self.client_tick(new_time - last_time)
            last_time = new_time

    async def client_tick(self, delta):
        if self.client_state == eclient_state.connecting :
            #connected
            try:
                self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)
                self.on_connected_cb()
                self.client_state = eclient_state.work
            except Exception as e:
                self.on_error_cb(e)

        elif self.client_state == eclient_state.work :
            await super().work() #super.work



    #virtual
    def on_msg(self, data):
        print(data.decode())
        if self.msg_cb:
            self.msg_cb() #new msg

    #virtual
    def on_read_error(self, exception):
        self.on_error_cb(exception)
        if self.client_state == eclient_state.work:
            self.client_state = eclient_state.connecting #make it reconnect


    def close(self):
        self.is_connected = False

    def on_connected_cb(self):
        if self.connected_cb :
            self.connected_cb()

    def on_error_cb(self, exception):
        if self.error_cb :
            self.error_cb(exception)

        #reconnected
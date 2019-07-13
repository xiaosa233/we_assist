import asyncio
import threading
import time


class tcp_client_base :
    g_limit = 64 * 1024
    def __init__(self):
        self.reader = None
        self.writer = None
        self.run_thread = None
        self.is_connected = True


    # virtual
    def on_msg(self, data):
        pass

    # virtual
    def on_read_error(self, exception):
        pass

    #virtual
    async def client_tick(self, delta):
        pass

    def start_work(self):
        self.is_connected = True
        if self.run_thread is None:
            self.run_thread = threading.Thread(target=self.loop_thread)
            self.run_thread.start()

    #virtual
    def close(self):
        self.is_connected = False
        if self.run_thread:
            self.run_thread.join()
            self.run_thread = None


    def loop_thread(self):
        asyncio.run(self.loop())


    async def loop(self):
        last_time = time.time()

        while self.is_connected:
            new_time = time.time()
            await self.client_tick(new_time - last_time)
            last_time = new_time

    async def work(self, delta):
        is_read_ok = True
        try :
            data = await self.reader.read(tcp_client_base.g_limit) #default limit size is 64KB
        except Exception as e :
            #remote connection is closed
            self.on_read_error(e)
            is_read_ok = False

        if is_read_ok:
            self.on_msg(data)

    def send(self, data):
        if self.writer :
            self.writer.write(data)

import asyncio
import threading

class tcp_client_base :
    def __init__(self):
        self.reader = None
        self.writer = None
        self.run_thread = None
        self.should_end = False


    def start_work(self):
        if self.run_thread is None :
            self.should_end = False
            self.run_thread = threading.Thread(target = self.run)
            self.run_thread.start()

    def stop_work(self):
        if self.run_thread :
            self.should_end = True
            self.run_thread.join()
            self.run_thread = None

    # virtual
    def on_msg(self, data):
        pass

    def run(self):
        #asyncio.run(self.start_work_impl())
        self.start_work_impl()

    async def start_work_impl(self):
        #while not self.should_end:
        print(' begin recv ')
        data = await self.reader.read()
        print('recev')
        self.on_msg(data)

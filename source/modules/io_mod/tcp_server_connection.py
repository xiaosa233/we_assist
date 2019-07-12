import tcp_client_base
import threading

class tcp_server_connection(tcp_client_base.tcp_client_base):
    def __init__(self, reader, writer):
        super().__init__()
        self.reader = reader
        self.writer = writer
        self.run_thread = None


    def start_work(self):
        if self.run_thread is None :
            self.run_thread = threading.Thread(target=self.loop)
            self.run_thread.run()

    async def loop(self):
        data = await self.reader.reader(100) #FUCK WARNINGS.
        print(data.decode())
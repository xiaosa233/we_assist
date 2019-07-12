import asyncio
import threading
import tcp_server_connection
class tcp_server :
    def __init__(self, ip, port, connected_cb = None, error_cb=None, msg_cb=None):
        self.ip = ip
        self.port = port
        self.connected_cb = connected_cb
        self.error_cb = error_cb
        self.msg_cb = msg_cb
        self.limit = 64 * 1024 #64KB

        self.server = None
        self.loop = None
        self.server_thread = None


    def start(self):
        if not self.server_thread :
            self.server_thread = threading.Thread(target=self.server_loop)
            self.server_thread.start()
            
    def stop(self):
        if self.server_thread :
            if self.server :
                self.loop.stop()
                self.server.close()
            
            self.server_thread.join()
            self.server_thread = None


    def server_loop(self):
        self.start_impl()

    def start_impl(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        coro = asyncio.start_server(self.on_connected_cb, self.ip, self.port, loop=self.loop,limit=self.limit)
        self.server = self.loop.run_until_complete(coro)
        self.loop.run_forever()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.run_until_complete(self.loop.shutdown_asyncgens())
        self.loop.close()
        self.loop = None
        self.server = None


    async def on_connected_cb(self, reader, writer):
        self.tmp = tcp_server_connection.tcp_server_connection(reader, writer)
        print('new connection')
        message = 'hello world'
        writer.write(message.encode())
        await writer.drain()
        print('send messgae : ', message)
        self.tmp.start_work()
        pass








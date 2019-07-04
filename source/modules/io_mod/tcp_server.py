import asyncio

class tcp_server :
    def __init__(self, ip, port, connected_cb = None, error_cb=None, msg_cb=None):
        self.ip = ip
        self.port = port
        self.connected_cb = connected_cb
        self.error_cb = error_cb
        self.msg_cb = msg_cb
        self.limit = 64 * 1024 #64KB

        self.server = None


    def start(self):
        asyncio.run(self.start_impl())
        asyncio.run(self.serve_forever())

        '''
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self.on_connected_cb, self.ip, self.port, loop=loop,limit=self.limit)
        self.server = loop.run_until_complete(coro)
        print('run complete')
        coro = asyncio.start_server(self.on_connected_cb, self.ip, self.port + 1, loop=loop,limit=self.limit)
        self.server = loop.run_until_complete(coro)
        print('run complete')


        loop.run_forever()
        '''


    async def start_impl(self):
        self.server = await asyncio.start_server(self.on_connected_cb, self.ip, self.port,limit=self.limit)
        #async with self.server:
        await self.server.serve_forever()

    async def serve_forever(self):
        pass

    def stop(self):
        pass

    async def on_connected_cb(self, reader, writer):
        print('new connection')
        pass








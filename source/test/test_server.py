import import_source
from modules.io_mod import tcp_server
from modules.io_mod import tcp_server_connection
import time




class test_server_main:

    def work(self):
        self.test_server = tcp_server.tcp_server('0.0.0.0', 23332, connected_cb=self.on_connection, error_cb=self.on_error, msg_cb=self.on_msg)
        self.test_server.start()
        print('start server')
        self.count = 1
        while True:
            self.tick()
            time.sleep(1)

        test_server.stop()


    def on_connection(self, tcp_connection):
        print('new connection !!')

    def on_error(self, tcp_connection, exception):
        print('server error : ' + str(exception))

    def on_msg(self, tcp_connection, data):
        print('server recv :', data.decode())

    def tick(self):
        self.count += 1
        self.test_server.broadcast(('server send to : hello' + str(self.count)).encode() )

def main() :
    inst = test_server_main()
    inst.work()

def test2() :
    import asyncio

    async def handle_echo(reader, writer):
        print('in!!')
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))

        print("Send: %r" % message)
        writer.write(data)
        await writer.drain()

        print("Close the client socket")
        writer.close()

    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_echo, '0.0.0.0', 23332, loop=loop)
    server = loop.run_until_complete(coro)


    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

main()
#test2()
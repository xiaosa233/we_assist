import import_source
from modules.io_mod import tcp_server
import time


def tick():
    pass



def main() :
    test_server = tcp_server.tcp_server('0.0.0.0', 23332)
    test_server.start()
    print('start server')
    
    time.sleep(2)
    test_server.stop()
    print('stop!')
    test_server = tcp_server.tcp_server('0.0.0.0', 23332)
    print('restart!')
    


    while True :
        tick()
        time.sleep(0.03)


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
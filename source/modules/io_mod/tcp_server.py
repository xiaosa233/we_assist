import asyncio
import threading
import tcp_server_connection
from controllers import log_controller
class tcp_server :
    def __init__(self, ip, port, connected_cb = None, error_cb=None, msg_cb=None):
        self.ip = ip
        self.port = port
        self.connected_cb = connected_cb
        self.error_cb = error_cb
        self.msg_cb = msg_cb

        self.server = None
        self.loop = None
        self.server_thread = None
        self.tcp_connections = []


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

    def clear_data(self):
        self.loop = None
        self.server = None
        self.tcp_connections.clear()


    def server_loop(self):
        self.start_impl()

    def start_impl(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        coro = asyncio.start_server(self.on_connected_cb, self.ip, self.port, loop=self.loop)
        self.server = self.loop.run_until_complete(coro)
        self.loop.run_forever()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.run_until_complete(self.loop.shutdown_asyncgens())
        self.loop.close()

        self.clear_data()

    def broadcast(self, data):
        for connection in self.tcp_connections :
            connection.send(data)


    async def on_connected_cb(self, reader, writer):
        tmp = tcp_server_connection.tcp_server_connection(self, reader, writer)
        self.tcp_connections.append(tmp)

        if self.connected_cb :
            self.connected_cb(tmp)

        asyncio.get_event_loop().create_task( tmp.recv_once() )

    def close_connection(self, tcp_connection):
        self.tcp_connections.remove(tcp_connection)


    def on_msg(self, tcp_connection, data):
        if self.msg_cb :
            self.msg_cb(tcp_connection, data)

    def on_read_error(self, tcp_connection, exception):
        if exception.errno == 10054 or exception.errno == 10053: #force to close
            self.tcp_connections.remove(tcp_connection)
        else :
            log_controller.log_controller.g_log('unknow exception : ' + str(exception))

        if self.error_cb :
            self.error_cb(tcp_connection, exception)





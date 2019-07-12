import asyncio
import threading



class tcp_client_base :
    def __init__(self):
        self.reader = None
        self.writer = None


    # virtual
    def on_msg(self, data):
        pass

    # virtual
    def on_read_error(self, exception):
        pass

    async def work(self):
        #while not self.should_end:
        print(' begin recv ')
        is_read_ok = True
        try :
            data = await self.reader.read(1024 * 64) #default limit size is 64KB
        except Exception as e :
            #remote connection is closed
            self.on_read_error(e)
            is_read_ok = False

        print('recev')
        if is_read_ok:
            self.on_msg(data)

    def send(self, data):
        if self.writer :
            self.writer.write(data)

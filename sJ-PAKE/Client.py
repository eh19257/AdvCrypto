# Acts as a network wrapper for the party class

import socket
import datetime

class sJ_PAKE_Client():
    def __init__(self, host, port):
        self.socket = (host, port)
        return
    
    def Connect_to_Server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(self.socket)
            print("{0} - Connected to Server!".format(datetime.datetime.now().strftime("%H:%M:%S")))
        except:
            print("No Server found on {0}:{1} :(".format(self.socket[0], self.socket[1]))
        
        #data = sock.recv(1024)
        #print(data)
        return

foo = sJ_PAKE_Client("127.0.0.1", 6666)
foo.Connect_to_Server()
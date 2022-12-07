from socketserver import *
import datetime
from collections import defaultdict
from Party import Party
from Curve25519 import Curve25519
import json

class sJ_PAKE_Server():

    def __init__(self, host, port):
        
        # Each entry is of the form label:pw
        # The label acts like a username
        self.client_db = {}
        self.server_socket = (host, port)

        self.G = Curve25519()

        self.protocol = Party(self.G, self.G.GetGenerator(), self.G.F(42069), self.G.F(98765432345678), True)
        return
    
    def StartServer(self):
        #server = socketserver.TCPServer(self.server_socket, RequestHandler)
        server = StatefulTCP(self.server_socket, RequestHandler, self.protocol)
        print("{2} - Listening on socket {0}:{1} ...".format(self.server_socket[0], self.server_socket[1], datetime.datetime.now().strftime("%H:%M:%S")))
        server.serve_forever()
        return


# Stateful Request Handler for managing 3 consectutive messages from the same IP
class RequestHandler(StreamRequestHandler):
    def __init__(self, request, client_address, server: BaseServer) -> None:
        
        
        self.CurrentStage = None

        super().__init__(request, client_address, server)

    # OVERRIDE - Gets the current stage of the client
    def setup(self) -> None:
        # Get and locally set the current stage of the client
        self.CurrentStage = self.server.GetCurrentStageOfConnection(self.client_address[0])

        return super().setup()

    # OVERRIDE - actually handles the request
    def handle(self):
        print("{0} is on stage {1}".format(self.client_address, self.CurrentStage))

        if  (self.CurrentStage == 1):
            asdf
        elif (self.CurrentStage == 2):
            asdf
        elif (self.CurrentStage == 3):
            asdf
        else:
            raise Exception("Somehow you convinced the server that it's on stage {0}. How the hell did you do that?".format(self.CurrentStage))

        return
    
    # OVERRIDE - Updates the current stage of the client
    def finish(self) -> None:
        # Update the stage for this client on the server side
        if (self.CurrentStage == 3):
            self.server.SetCurrentStageOfConnection(self.client_address[0], None)
        
        return super().finish()
    
    # Unpacks the byte data from the recv stream
    def UnpackData(self, buf):
        return json.loads(buf.encode("utf-8"))
    
    # Packs dict into byte string
    def PackData(self, dict):
        return json.dumps(dict, indent=4).encode()



# Stateful TCP Server Implementation
class StatefulTCP(TCPServer):

    def __init__(self, server_address, RequestHandlerClass, protocol, bind_and_activate: bool = ...) -> None:
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

        self.protocol = protocol
        self.currentConnections = defaultdict(lambda: None)
        print("{0} - Server Initilised".format(datetime.datetime.now().strftime("%H:%M:%S")))
    

    def process_request(self, request, client_address) -> None:
        
        if (self.currentConnections[client_address[0]] == None):
            self.currentConnections[client_address[0]] = 1
        else:
            # In theory, this should never go above 3 (Fingers crossed - looks like it's working nicely)
            self.currentConnections[client_address[0]] += 1
        

        return super().process_request(request, client_address)


    # Gets the current stage of the protocol that the parameterised IP is in
    def GetCurrentStageOfConnection(self, addr):
        return self.currentConnections[addr]

    # Setter for the current stage of the protocol for the parameterised IP
    def SetCurrentStageOfConnection(self, addr, val):
        self.currentConnections[addr] = val
        return


foo = sJ_PAKE_Server("127.0.0.1", 6666)
foo.StartServer()

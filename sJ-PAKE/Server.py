from socketserver import *
import datetime
import time
from collections import defaultdict
from Party import Party
from Curve25519 import Curve25519
import json
import argparse
from argparse import RawTextHelpFormatter
import hashlib

VERBOSE = False


class sJ_PAKE_Server():

    def __init__(self, host, port, hash):
        
        # Each entry is of the form label:pw
        # The label acts like a username
        self.server_socket = (host, port)

        self.G = Curve25519()

        self.protocol = Party(self.G, self.G.GetGenerator(), "MAIN_SERVER", "1337_H4x0_123!", hash, True)
        return
    
    def StartServer(self):
        #server = socketserver.TCPServer(self.server_socket, RequestHandler)
        server = StatefulTCP(self.server_socket, RequestHandler, self.protocol)
        print("{2} - Listening on socket {0}:{1} ...".format(self.server_socket[0], self.server_socket[1], datetime.datetime.now().strftime("%H:%M:%S")))
        try:
            server.serve_forever()
        except:
            print("{0} - Server has been killed".format(datetime.datetime.now().strftime("%H:%M:%S")))
            server.shutdown()
        return


# Stateful Request Handler for managing 3 consectutive messages from the same IP
class RequestHandler(StreamRequestHandler):
    def __init__(self, request, client_address, server: BaseServer) -> None:
        self.CurrentState = None
        super().__init__(request, client_address, server)


    # OVERRIDE - actually handles the request
    def handle(self):
        self.Verbose("Client request incoming. Starting exchange...")

        self.Verbose("============== STAGE 1 ==============")
        # Load in their result of STAGE 1
        input = self.UnpackData(self.rfile.readline())

        print(input["l"])
        # We have to workout who we are actually talking to
        if input["l"] in self.server.client_db:
            self.server.protocol.Change_pw(self.server.client_db[input["l"]])
        # Look at label and try to find the coresponding client
        else:
            # send kill signal
            self.wfile.write(b'\x00\x00\x00\x00\x00\x00\x00\x00')

            self.server.close_request(self.request)
            return

        # prepare result from STAGE 1
        output = self.server.protocol.Stage1()

        self.Verbose("Received:\n{0}\nSending over:\n{1}".format(input, output))

        self.Verbose("========== STAGE 1 COMPLETE ==========\n")

        self.Verbose("============== STAGE 2 ==============")

        # Compute STAGE 2
        stage2_result = self.server.protocol.Stage2(input)

        # Send out your result of STAGE 1 and STAGE 2
        self.wfile.write(self.PackData(output) + self.PackData(stage2_result))

        # Load in their result from STAGE 2
        input = self.UnpackData(self.rfile.readline())

        # Handles Failed checks in stage 2
        if (input == b'\x00\x00\x00\x00\x00\x00\x00\x00'):
            print("Other party has their X_2 == 1! This is not allowed")
            self.server.close_request(self.request)
            return
        
        elif (input == b'\x00\x00\x00\x00\x00\x00\x00\x01'):
            print("Other party doesn't have their x_1!")
            self.server.close_request(self.request)
            return
        
        elif (input == b'\x00\x00\x00\x00\x00\x00\x00\x02'):
            print("Other party doesn't have their x_1!")
            self.server.close_request(self.request)
            return
        
        self.Verbose("Received:\n{0}\nSending over:\n{1}".format(input, stage2_result))

        self.Verbose("========== STAGE 2 COMPLETE ==========\n")

        self.Verbose("============== STAGE 3 ==============")
        # Compute STAGE 3
        self.server.protocol.Stage3(input)
        
        self.Verbose("Key = {0}".format(self.server.protocol.key))

        self.Verbose("========== STAGE 3 COMPLETE ==========\n")

        print("{1} - Final shared secret key K is: {0}".format(self.server.protocol.K, datetime.datetime.now().strftime("%H:%M:%S")))

        return

    
    def finish(self) -> None:

        print("\n\n========== Connection Separated with {0}:{1} ==========".format(self.client_address[0], self.client_address[1]))
        return super().finish()


   # Unpacks the byte data from the recv stream
    def UnpackData(self, buf):
        buf = json.loads(buf.decode("utf-8"))
        out = {}
        
        for b in buf:
            out[b] = self.server.protocol.G.F(buf[b]) 
        return out
    
    # Packs dict into byte string
    def PackData(self, dict):
        out = {}
        for d in dict:
            out[d] = int(dict[d])
        return (json.dumps(out) + '\n').encode()

    # Prints out more info
    def Verbose(self, str):
        if (VERBOSE):
            print((("{0} - ").format(datetime.datetime.now().strftime("%H:%M:%S") ) + str))


# Stateful TCP Server Implementation
class StatefulTCP(TCPServer):

    def __init__(self, server_address, RequestHandlerClass, protocol, bind_and_activate: bool = ...) -> None:
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

        # sJ-PAKE protocol
        self.protocol = protocol

        # A "Database" of all the clients on the system and therefore the ones that the server can authenticate 
        self.client_db = {
            "ceo" : "InsanelySecretPassword",
            "user_01" : "p4ssw0rd_01!",
            "root" : "root",
            "admin" : "admin",
            "guest" : "N0St&stLFruhUNapH0mU!r&P2oTHespUKEph_s7U!*phamlMudlCl*ridrUstLfa"
        }

        # Encodes all the usernames and passwords to numbers
        tmp = {}
        for e in self.client_db:
            #
            tmp[self.protocol.G.F(int.from_bytes(e.encode(), "big"))] = self.protocol.G.F(int.from_bytes(self.client_db[e].encode(), "big"))
            #print(k)
        
        self.client_db = tmp


        print("{0} - Server Initilised".format(datetime.datetime.now().strftime("%H:%M:%S")))
   

def ParseArgs():
    help_desc = '''
  ________________
< sJ-PAKE SERVER >
 ----------------
        \\   ^__^
         \\  (oo)\\_______
            (__)\\       )\\/\\
                ||----w |
                ||     ||
    
    This is the server part of the networked sJ-PAKE implementation
    '''

    parser = argparse.ArgumentParser(
                    prog = 'Server.py',
                    description = help_desc,
                    epilog = 'Enjoy :)',
                    formatter_class=RawTextHelpFormatter)
    
    parser.add_argument('-v', '--verbose',
                    action='store_true',
                    help="Will produce a more detailed output.")
    
    parser.add_argument("HOST",
                        help="IPv4 address that the server will bind to.")
    parser.add_argument("PORT", 
                        help="Port that the server listens on.",
                        type=int)

    hashes = parser.add_mutually_exclusive_group()
    hashes.add_argument("--sha256",
                        help="SHA256 hash algorithm, used for 256 bit keys.",
                        action='store_true')
    hashes.add_argument("--sha512",
                        help="SHA512 hash algorithm, used for 512 bit keys.",
                        action='store_true')

    args = parser.parse_args()

    return args


def main():
    args = ParseArgs()

    VERBOSE = args.verbose

    hash = hashlib.sha256
    if (args.sha512):
        hash = hashlib.sha512
    
    foo = sJ_PAKE_Server(args.HOST, args.PORT, hash)
    foo.StartServer()

main()

#foo = sJ_PAKE_Server("127.0.0.1", 5678)
#foo.StartServer()

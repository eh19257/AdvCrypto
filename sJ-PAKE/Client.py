# Acts as a network wrapper for the party class

import socket
import datetime
from Curve25519 import Curve25519
from Party import Party
import json
import argparse
from argparse import RawTextHelpFormatter
import hashlib

VERBOSE = True


class sJ_PAKE_Client():
    def __init__(self, host, port, label, pw, hash):
        self.socket = (host, port)
        self.state = 1

        self.G = Curve25519()
        self.g = self.G.GetGenerator()

        self.protocol = Party(self.G, self.g, label, pw, hash)
        return
    
    def Connect_to_Server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #try:
        try:
            sock.connect(self.socket)
            print("{0} - Connected to Server!".format(datetime.datetime.now().strftime("%H:%M:%S")))
            try:
                self.Handle_Exchange(sock)
            except:
                print("")
        except:
            print("{2} - No Server found on {0}:{1} :(".format(self.socket[0], self.socket[1], datetime.datetime.now().strftime("%H:%M:%S")))
        
        return

    def Handle_Exchange(self, sock):
        
        self.Verbose("============== STAGE 1 ==============")
        # Compute STAGE 1
        out = self.PackData(self.protocol.Stage1())

        # Send result of STAGE 1 to server
        sock.send(out)
       
        # Read in result of STAGE 1 and 2
        raw_input = sock.recv(1024)
        if (raw_input == b'\x00\x00\x00\x00\x00\x00\x00\x00'):
            print("{0} - Server can't find your username and therefore password in it's database".format(datetime.datetime.now().strftime("%H:%M:%S")))
            
            print("========== EXITING ==========")
            sock.close()
            return
        
        #if (raw_input[len(raw_input)-8-1: -1] == b'\x00\x00\x00\x00\x00\x00\x00\x00'):
        #    print("")
        stage2_chunk = raw_input[len(raw_input)-8-1: -1]
        # Handles Failed checks in stage 2
        if (stage2_chunk == b'\x00\x00\x00\x00\x00\x00\x00\x00'):
            print("Other party has their X_2 == 1! This is not allowed")
            print("========== EXITING ==========")
            sock.close()
            return
        
        elif (stage2_chunk == b'\x00\x00\x00\x00\x00\x00\x00\x01'):
            print("Other party doesn't have their x_1!")
            print("========== EXITING ==========")
            sock.close()
            return
        
        elif (stage2_chunk == b'\x00\x00\x00\x00\x00\x00\x00\x02'):
            print("Other party doesn't have their x_1!")
            print("========== EXITING ==========")
            sock.close()
            return
        
        # Recieving the input (made up of STAGE1 and STAGE2)
        pre_input = raw_input.decode("utf-8").split('\n')
        input = [self.UnpackData(pre_input[0].encode()), self.UnpackData(pre_input[1].encode())]

        self.Verbose("Received:\n{0}\nSending over:\n{1}".format(input[0], out))

        self.Verbose("========== STAGE 1 COMPLETE ==========\n")

        self.Verbose("============== STAGE 2 ==============")

        # Compute STAGE 2
        output = self.protocol.Stage2(input[0])

        self.Verbose("Received:\n{0}\nSending over:\n{1}".format(input[1], output))

        # Send result of STAGE 2 to server
        sock.send(self.PackData(output))

        self.Verbose("========== STAGE 2 COMPLETE ==========\n")


        self.Verbose("============== STAGE 3 ==============")

        # Compute STAGE 3
        self.protocol.Stage3(input[1])

        self.Verbose("Key = {0}".format(self.protocol.key))
        self.Verbose("========== STAGE 3 COMPLETE ==========\n")


        print("{1} - Final shared secret key K is: {0}".format(self.protocol.K, datetime.datetime.now().strftime("%H:%M:%S")))

        return

     
    # Unpacks the byte data from the recv stream
    def UnpackData(self, buf):
        buf = json.loads(buf.decode("utf-8"))
        out = {}
        
        for b in buf:
            out[b] = self.protocol.G.F(buf[b]) 
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



def ParseArgs():
    help_desc = '''
 ________________
< sJ-PAKE CLIENT >
 ----------------
        \\   ^__^
         \\  (oo)\\_______
            (__)\\       )\\/\\
                ||----w |
                ||     ||    
    
    This is the client part of the networked sJ-PAKE implementation.
    '''

    parser = argparse.ArgumentParser(
                    prog = 'Server.py',
                    description = help_desc,
                    epilog = 'Enjoy :)',
                    formatter_class=RawTextHelpFormatter)
  
    parser.add_argument("HOST", 
                        help="IPv4 address of the server we will be connecting to.")
    parser.add_argument("PORT",
                        help="Port that the server listens on.",
                        type=int)

    parser.add_argument("USERNAME",
                        help="Username/label of the some user.")
    parser.add_argument("PASSWORD",
                        help="Password with the associated user.")

    parser.add_argument('-v', '--verbose',
                    action='store_true',
                    help="Will produce a more detailed output.")

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
    
    foo = sJ_PAKE_Client(args.HOST, args.PORT, args.USERNAME, args.PASSWORD, hash)
    #foo = sJ_PAKE_Client(args.host, args.port, "ceo", "InsanelySecretPassword")
    foo.Connect_to_Server()


main()
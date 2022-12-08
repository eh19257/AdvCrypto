# sJ-PAKE

The sJ-PAKE protocol is a slimmed down version of the J-PAKE procotol; both of these use some low-entropy password that is secret and shared between both parties so that they can authenticate and share some secret key with one another. The protocol relies on the security of a Diffie-Hellman exchange, non-interactive zero knowledge proofs and the group that is used to implement them. In my implementation, I used Schnorr-like zero-knowledge proofs for the NIZK proofs and Curve25519 as the group.

In order for an adversary to decrypt some messages, they need to know the password, $x_2$ and $x_4$. To mitigate an adversary decrypting previous messages, we delete $x_2$ and $x_4$ as soon as they have been used - pushing towards perfect forwad secrecy. This implementation could be paired with a ratchet in order to give the protocol post-compromised security.

The implementation of sJ-PAKE was done in such a way that abstracts away key elements of the protocol for example the group, this was done so that it is easy to replace the group in the future when ECCs become completely broken by Quantum Computers. For a similar reason, the hash functions can be very easily replaced; changing hash functions can also be done to change the length of the final keys. My implementation makes use of sha256 and sha512 for 256 and 512 bit keys respectively - other hash functions could be used for varying lengths.

## Small Notes
A single client is identified by their label/username which is inputted as as string and they're authenticated by the server using the password that both party's share.
The protocol use TCP.


## Requirements
The program requires `sage` to be installed along with `python 3.10.6`. All python modules that the program uses should be included with the default version of python 3.10.6 however below is a list of them just incase there are any issues.

* socket
* datetime
* json
* socketserver
* collections
* hashlib
* sage.all
* argparse

## How to run

The protocol can be run in 2 modes: as an offline exchange or over the network - the latter is a lot more fleshed out.

### Offline exchange
To run the offline program, simply enter `python3 OfflineExchange.py` into a bash terminal. This will simulate an exchange between a server and a client both with the shared password `SuperSecretSharedPassword`.

### Online exchange
To run the networked exchange you will need to first run the server using `python3 Server.py -v HOST PORT` and then follow up by running the the client in a different terminal with `python3 Client.py -v HOST PORT USERNAME PASSWORD `. Whichever port is used needs to be opened - if this cannot be done then this program can be run in a vagrant machine. There is a help menu for both `Server.py` and `Client.py` and this can be accessed by using the `--help` flag.

Both `Client.py` and `Server.py` can have their final hash functions changed in order to output a different key length, this can be done by adding either `--sha256` or `--sha512` as a flag (default to sha256 without either).

The `-v` or `--verbose` flag can be used to print more information about the exchange.

`Client.py` requires some logins and a list full list of logins in the system can be found below. These passwords are hardcoded into `Server.py` on line 142, this is done for demonstration purposes and shouldn't be done in reality.

| Username |                             Password                             |
| :------: | :--------------------------------------------------------------: |
|   ceo    |                      InsanelySecretPassword                      |
| user_01  |                           p4ssw0rd_01!                           |
|   root   |                               root                               |
|  admin   |                              admin                               |
|  guest   | N0St&stLFruhUNapH0mU!r&P2oTHespUKEph_s7U!*phamlMudlCl*ridrUstLfa |


## Running Examples
To run a server on localhost:5678 with a 256 bit key and verbosing: ```python3 Server.py -v --sha256 127.0.0.1 5678```</br>
To run user_01 on localhost:5678 with a 256 bit key and verbosing: ```python3 Client.py -v --sha256 127.0.0.1 5678 user_01 p4ssw0rd_01!```</br>
To run in offline mode: ```python3 OfflineExchange.py```
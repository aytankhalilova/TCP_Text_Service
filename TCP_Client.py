import socket
import json
import argparse
import os
import sys
import TCP_Server

INTERFACE = '127.0.0.1'
PORT = 1060
BUFFSIZE = 2048
GAP = "*"

class TcpClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self, mode, source_file, key_or_json_file):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        print('Socket name of client:', sock.getsockname())
        size_of_srcfile = os.path.getsize(source_file)
        size_of_kjfile = os.path.getsize(key_or_json_file)
        print('Sending mode, source file and {} file size to TCP_Server:'.format("json" if mode=="change_text" else "key"))
        sock.send(f"{mode}{GAP}{size_of_srcfile}{GAP}{size_of_kjfile}".encode())
        with open(source_file, "r") as f:
            data_of_srcfile = f.read()
            print(data_of_srcfile)
            print("Sending source file as bytes to server:")
            sock.sendall(bytes(data_of_srcfile.encode()))
            print((data_of_srcfile.encode()))
            f.close()
        with open(key_or_json_file, "r") as f:
            data_of_kjfile = f.read() if mode == "encode_decode" else json.dumps(f)
            print(f'Sending {"json" if mode=="change_text" else "key"} file as  bytes to server:')
            sock.sendall(bytes(data_of_kjfile.encode()))
            f.close()

        print('Receiving conclusion from TCP_Server:')
        received = sock.recv(size_of_srcfile).decode()
        print('Server replied with:', str(received))
        sock.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices={'change_text', 'encode_decode'})
    parser.add_argument('srcfile')
    parser.add_argument('kjfile')
    args = parser.parse_args()
    print("-------------------")
    TcpClient(INTERFACE, PORT).connect(args.mode, args.srcfile, args.kjfile)


if __name__ == '__main__':
    main()

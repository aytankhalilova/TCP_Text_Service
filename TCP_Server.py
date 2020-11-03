import socket
import json

INTERFACE = '127.0.0.1'
PORT = 1060
BUFFSIZE = 2048
GAP = "*"


class TcpServer:
    def __init__(self, interface, port):
        self.interface = interface
        self.port = port

    def bind(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.interface, self.port))
        sock.listen(1)
        print('Listening at', sock.getsockname())

        while True:
            sc, sockname = sock.accept()
            print('We have accepted connection from ', sockname)
            print('Receiving mode, file size and json/key file size:')
            received = sc.recv(BUFFSIZE).decode()
            mode, size_of_file, size_of_key_or_json = received.split(GAP)
            size_of_file = int(size_of_file)
            size_of_key_or_json = int(size_of_key_or_json)

            print('Received source file data :')
            data_of_srcfile = sc.recv(size_of_file).decode()

            print("Received {} data: ".format('json' if mode == 'change_text' else 'key'))
            data_of_kjfile = sc.recv(size_of_key_or_json).decode()
            if mode=="change_text":
                data_of_kjfile = json.loads(data_of_kjfile)

            conclusion = ""
            if str(mode) == "change_text":
                conclusion = self.change_text(data_of_srcfile, data_of_kjfile)
            else:
                conclusion = self.encode_decode(data_of_srcfile, data_of_kjfile)
                print(conclusion)


            print('Sending conclusion to the client:')
            sc.sendall(bytes(conclusion.encode()))
            sc.close()
            print("Session closed.")

    def change_text(self, source_file, json_file):
        for i in json_file:
            source_file = source_file.replace(i, json_file[i])
        return source_file


    def encode_decode(self, source_file, key_file):
        return "".join(chr(ord(source_file[j]) ^ ord(key_file[j%len(key_file)])) for (j) in range(len(source_file)))

def main():
    TcpServer(INTERFACE, PORT).bind()

if __name__ == '__main__':
    main()


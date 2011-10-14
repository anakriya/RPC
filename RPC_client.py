import serialization
import socket

HOST = '127.0.0.1'    # The remote host
PORT = 50007              # The same port as used by the server

def connectToServer(host, port, data):
    HOST = host
    PORT = port
    print data
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    s.send(serialization.serializable(data))
    data = s.recv(1024)
    s.close()
    print 'Received: ', serialization.deserializable(data)

connectToServer('127.0.0.1',50007, "hello world!!!")

if __name__ == '__main__':
    pass
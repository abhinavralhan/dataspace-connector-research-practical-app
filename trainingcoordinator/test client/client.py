import socket
from ports import ports
from edge_node import edgeNodeProvider, edgeNodeConsumer

HOST = '127.0.0.1'
PORT = 65432


def clientProviders():
    edgeNodeProvider(ports.edgeNode1)
    edgeNodeProvider(ports.edgeNode2)
    edgeNodeProvider(ports.edgeNode3)


def clientConsumers():
    edgeNodeConsumer(ports.edgeNode1)
    edgeNodeConsumer(ports.edgeNode2)
    edgeNodeConsumer(ports.edgeNode3)


if __name__ == '__main__':
    clientProviders()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)
        print(repr(data))
        clientConsumers()

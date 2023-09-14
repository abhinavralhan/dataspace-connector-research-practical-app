from training_coordinator import training_coordinator
import socket
import time
from ports import ports


HOST = '127.0.0.1'
PORT = 4000

if __name__ == '__main__':
    while True:
        time.sleep(60)
        try:
            training_coordinator.trainingCoordinator(ports.trainingCoordinator)
        except:
            print("trainingCoordinator failed")

    '''with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", PORT))
        while True:
            s.listen()
            print('Training Coordinator Online')
            connect, addr = s.accept()
            with connect:
                print("client connected")
                training_coordinator.trainingCoordinator(ports.trainingCoordinator)
                connect.sendall(b'Aggregated data available')'''

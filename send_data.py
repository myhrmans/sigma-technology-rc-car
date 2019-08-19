from socket import *
import time
class Transport(object):
    def __init__(self):
        self.address = ('10.0.0.2', 5005)
        self.client_socket = socket(AF_INET, SOCK_DGRAM) #Set Up the Socket
        self.client_socket.settimeout(1) #only wait 1 second for a resonse

    def send_data(self, data):
        self.client_socket.sendto(data.encode('utf-8'), self.address) #send command to arduino
        try:
            rec_data, addr = self.client_socket.recvfrom(2048) #Read response from arduino
            print(rec_data) #Print the response from Arduino
        except:
            pass

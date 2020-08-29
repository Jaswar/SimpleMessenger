import socket
import pickle

class ClientSocket(object):

    __HOST = 'YOUR SERVERS PUBLIC IP ADDRESS'
    __PORT = 6889

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.logged_in = False

    def connect(self):
        self.s.connect((self.__HOST, self.__PORT))
        self.connected = True

    def send_to_host(self, type, data):
        to_send = [type, data]
        to_send = pickle.dumps(to_send)
        self.s.send(to_send)

    def check_login(self, login, password):
        data = [login, password]
        self.send_to_host('login', data)

    def strtobool(self, string):
        return string in ['True', 'true', '1']

    def receive(self):
        data = self.s.recv(1024)
        type, data = pickle.loads(data)
        if type == 'login':
            success = self.strtobool(data[0])
            return success
        elif type == 'msg':
            return data[0]

import socket
import pickle
import _thread

class Server(object):

    HOST = ''
    PORT = 6890

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))
        self.logins_filepath = 'logins.txt'

        self.messages = []

        self.logins = {}
        self.load_logins()

    def load_logins(self):
        file = open(self.logins_filepath).read().splitlines()
        for i, line in enumerate(file):
            file[i] = line.split(',')
        for (log, pwd) in file:
            self.logins[log] = pwd

    def handle_connection(self, conn, addr):
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
            except:
                break
            type, data = pickle.loads(data)
            if type == 'login':
                log, pwd = data
                success = False
                if log in self.logins and self.logins[log] == pwd:
                    success = True
                self.send_to_client(conn, 'login', [str(success)])
            elif type == 'msg':
                login, message = data
                self.messages.append([login, message])
                self.send_to_client(conn, 'msg', [self.messages])
            elif type == 'get_msg':
                self.send_to_client(conn, 'msg', [self.messages])

    def send_to_client(self, conn, type, data):
        to_send = [type, data]
        to_send = pickle.dumps(to_send)
        conn.sendall(to_send)

    def run(self):
        self.s.listen(5)
        while True:
            conn, addr = self.s.accept()
            _thread.start_new_thread(self.handle_connection, (conn, addr))


if __name__ == '__main__':
    server = Server()
    server.run()


from client_socket import ClientSocket
from windows.login_window import LoginWindow
from windows.message_window import MessageWindow

class Client(object):

    def __init__(self):
        self.socket = ClientSocket()
        self.login = None

    def run(self):
        self.login_window = LoginWindow(self.socket)
        self.login_window.show()
        if self.socket.logged_in:
            self.login = self.login_window.log
            self.message_window = MessageWindow(self.socket, self.login)
            self.message_window.show()


if __name__ == '__main__':
    client = Client()
    client.run()


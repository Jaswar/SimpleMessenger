import tkinter as tk
from hashlib import sha256
import tkinter.messagebox


class LoginWindow(object):

    def __init__(self, socket):
        self.root = tk.Tk()
        self.socket = socket
        self.root.geometry('260x100')
        self.root.title('Login')
        self.log = None


        self.login_label = tk.Label(self.root, text='Login:', font=('TkDefaultFont', 12))
        self.login_label.place(x=10, y=10)

        self.login_entry = tk.Entry(self.root, font=('TkDefaultFont', 12))
        self.login_entry.place(x=100, y=10, width=150)

        self.password_label = tk.Label(self.root, text='Password:', font=('TkDefaultFont', 12))
        self.password_label.place(x=10, y=35)

        self.password_entry = tk.Entry(self.root, show='*', font=('TkDefaultFont', 12))
        self.password_entry.place(x=100, y=35, width=150)

        self.login_button = tk.Button(self.root, command=self.login, text='Login', font=('TkDefaultFont', 12))
        self.login_button.place(x=175, y=60, width=75)

        self.root.bind('<Return>', self.on_enter)

    def on_enter(self, event):
        self.login()

    def login(self):
        login = self.login_entry.get()
        password = sha256(self.password_entry.get().encode('utf-8')).hexdigest()
        success = clear_boxes = False
        try:
            if not self.socket.connected:
                self.socket.connect()
            self.socket.check_login(login, password)
            success = self.socket.receive()
            if not success:
                clear_boxes = True
        except WindowsError as we:
            if we.errno == 10065:
                tk.messagebox.showinfo('No internet access', 'Could not connect to the internet. Please ensure that '
                                                             'you have internet access and try again later.')
            elif we.errno == 10061:
                tk.messagebox.showinfo('Could not access server', 'Connection with the server could not be made. '
                                                                  'Please try again later.')
            elif we.errno == 10060:
                tk.messagebox.showinfo('Request timeout', 'The server did not respond. Please try again later.')
            else:
                tk.messagebox.showinfo('Error', str(we))

        if clear_boxes:
            tk.messagebox.showinfo('Incorrect login or password', 'Your login or password is incorrect.')
            self.login_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')

        if success:
            self.socket.logged_in = True
            self.log = self.login_entry.get()
            self.root.destroy()

    def show(self):
        self.root.mainloop()



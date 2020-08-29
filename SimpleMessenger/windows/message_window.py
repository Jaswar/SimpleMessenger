import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class MessageWindow(object):

    def __init__(self, socket, login):
        self.root = tk.Tk()
        self.login = login
        self.socket = socket
        self.root.geometry('500x500')
        self.root.title('Conversation')

        self.new_msg_entry = tk.Entry(self.root, font=('TkDefaultFont', 12))
        self.new_msg_entry.place(x=5, y=450, width=490, height=45)

        self.msg_entry = ScrolledText(self.root, font=('TkDefaultFont', 12))
        self.msg_entry.place(x=5, y=5, width=490, height=440)
        self.msg_entry.config(state=tk.DISABLED)

        self.msg_entry.tag_configure('tag-right', justify='right')
        self.msg_entry.tag_configure('tag-left', justify='left')

        self.root.bind('<Return>', self.on_enter)
        self.msg_entry.bind('<<Modified>>', self.scroll_down)

        to_send = []
        self.socket.send_to_host('get_msg', [to_send])
        messages = self.socket.receive()
        self.draw_messages(messages)

    def scroll_down(self, event):
        self.msg_entry.see(tk.END)
        self.msg_entry.edit_modified(0)

    def draw_messages(self, messages):
        self.msg_entry.config(state=tk.NORMAL)
        self.msg_entry.delete('1.0', tk.END)
        for i, (login, message) in enumerate(reversed(messages)):
            if 440 >= (i + 1) * 12:
                if self.login == login:
                    self.msg_entry.insert('1.0', f'{message}\n', 'tag-right')
                else:
                    self.msg_entry.insert('1.0', f'{login}: {message}\n', 'tag-left')
        self.msg_entry.config(state=tk.DISABLED)

    def on_enter(self, event):
        to_send = self.new_msg_entry.get()
        self.socket.send_to_host('msg', [self.login, to_send])
        self.new_msg_entry.delete(0, 'end')

        messages = self.socket.receive()
        self.draw_messages(messages)

    def show(self):
        while True:
            to_send = []
            self.socket.send_to_host('get_msg', [to_send])
            messages = self.socket.receive()
            self.draw_messages(messages)
            self.root.update()
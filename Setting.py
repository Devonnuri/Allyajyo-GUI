from tkinter import *
from configparser import ConfigParser


class Setting:
    def __init__(self):
        self.root = Tk()
        self.frame = Frame(self.root)
        self.labelFlagFormat = Label(self.frame, text="플래그 포맷: ")
        self.entryFlagFormat = Entry(self.frame)

        self.root.iconbitmap(default='logo.ico')
        self.root.title("설정 - 알랴죠")
        self.root.resizable(width=False, height=False)
        self.root.minsize(width=300, height=300)

        self.frame.grid(row=0, column=0, sticky=N+S+E+W)
        self.labelFlagFormat.config(font=["나눔고딕", 15])
        self.labelFlagFormat.grid(row=0, column=0)
        self.entryFlagFormat.config(font=["나눔고딕", 15])
        self.entryFlagFormat.grid(row=0, column=1, sticky=N+S+E+W)
        self.entryFlagFormat.insert(END, self.get_setting("flagFormat"))

        self.buttonSave = Button(self.root, text="저장", command=self.save_settings)
        self.buttonSave.config(font=["나눔고딕", 15])
        self.buttonSave.grid(row=3, column=0, pady=(200, 0))

    def show(self):
        self.root.mainloop()

    def save_settings(self):
        self.set_setting("flagFormat", self.entryFlagFormat.get())
        self.root.destroy()

    @staticmethod
    def get_setting(key):
        config = ConfigParser()
        config.read("allyajyo.ini")
        return config.get('Setting', key)

    @staticmethod
    def set_setting(key, value):
        config = ConfigParser()
        config.read("allyajyo.ini")
        config.set("Setting", key, value)
        with open("allyajyo.ini", "w") as f:
            config.write(f)

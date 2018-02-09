from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import *

import os
from configparser import ConfigParser


class HexViewer:
    def __init__(self):
        self.filename = ""
        self.filedata = []
        self.filesize = 0
        self.buffersize = 16  # Byte count that will be displayed in a line
        self.isOpened = False

        # GUI Components
        self.root = Tk()
        self.menuRoot = Menu(self.root)
        self.menuFile = Menu(self.menuRoot)
        self.menuTool = Menu(self.menuRoot)

        self.root.iconbitmap(default='logo.ico')
        self.root.title("Hex Viewer - 알랴죠")
        self.root.config(menu=self.menuRoot)
        self.root.resizable(width=False, height=False)
        self.root.minsize(width=700, height=500)

        self.menuRoot.add_cascade(label="파일", menu=self.menuFile)
        self.menuRoot.add_cascade(label="도구", menu=self.menuTool)
        self.menuFile.add_command(label="열기...", command=self.open_filedialog)
        self.menuTool.add_command(label="플래그 찾기", command=self.find_flag)

        self.labelHelp = Label(self.root, text="\n\n\n[파일] > [열기...]를 눌러 바이너리를 분석하세요!")
        self.labelHelp.config(font=["나눔고딕", 20])
        self.labelHelp.pack()

        self.frameViewer = Frame(self.root)
        self.frameInfo = Frame(self.root)

        self.scrollBar = Scrollbar(self.frameViewer)
        self.listboxAddress = Listbox(self.frameViewer, yscrollcommand=self.scrollBar.set)
        self.listboxHex = Listbox(self.frameViewer, yscrollcommand=self.scrollBar.set)
        self.listboxString = Listbox(self.frameViewer, yscrollcommand=self.scrollBar.set)

        self.labelFilename = Label(self.frameInfo)
        self.labelFilesize = Label(self.frameInfo)
        self.labelFiletype = Label(self.frameInfo)

    def show(self):
        self.root.mainloop()

    def open_filedialog(self):
        self.root.fileName = askopenfilename(title="Hex Viewer로 분석할 파일을 선택해주세요!")
        self.labelHelp.destroy()
        self.open_file(self.root.fileName)
        self.view_code()

    def open_file(self, filename):
        self.filename = filename
        print(filename)
        with open(self.filename, "rb") as f:
            self.filedata = f.read()

        self.filesize = os.path.getsize(self.filename)

    def view_code(self):
        for i in range(0, self.filesize, self.buffersize):
            self.listboxAddress.insert(END, "%010X" % i)
            byte = " "
            for j in range(int(self.buffersize/4)):
                for k in range(int(self.buffersize/4)):
                    if (i + j*4 + k) < self.filesize:
                        byte += "%02X " % self.filedata[i + j*4 + k]
                byte += ' '
            self.listboxHex.insert(END, byte)
            string = " "
            for j in range(self.buffersize):
                if (i + j) < self.filesize:
                    if 0x20 <= self.filedata[i + j] <= 0x7E:
                        string += chr(self.filedata[i + j])
                    else:
                        string += '.'
            self.listboxString.insert(END, string)

        self.listboxAddress.configure(justify=RIGHT)
        self.listboxAddress.config(font=["Consolas", 10], width=12)
        self.listboxHex.config(font=["Consolas", 10], width=int(self.buffersize*2+self.buffersize+self.buffersize/4))
        self.listboxString.config(font=["Consolas", 10], width=self.buffersize+2)
        self.labelFilename.config(font=["나눔고딕", 10])
        self.labelFiletype.config(font=["나눔고딕", 10])
        self.labelFilesize.config(font=["나눔고딕", 10])

        self.scrollBar['command'] = self.on_scroll
        self.listboxAddress['yscrollcommand'] = self.on_textscroll
        self.listboxHex['yscrollcommand'] = self.on_textscroll
        self.listboxString['yscrollcommand'] = self.on_textscroll

        self.listboxAddress.pack(side=LEFT, fill=BOTH)
        self.listboxHex.pack(side=LEFT, fill=BOTH)
        self.listboxString.pack(side=LEFT, fill=BOTH)
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.frameViewer.pack(side=LEFT, fill=BOTH)

        self.labelFilename["text"] = "파일이름:\n"+self.filename
        self.labelFiletype["text"] = "파일형식:\n"+self.get_filetype()
        self.labelFilesize["text"] = "파일크기:\n"+str(self.filesize)+" 바이트"

        self.labelFilename.pack(fill=X)
        self.labelFiletype.pack(fill=X)
        self.labelFilesize.pack(fill=X)
        self.frameInfo.pack(side=LEFT, fill=BOTH)

        self.isOpened = True

    def on_scroll(self, *args):
        self.listboxAddress.yview(*args)
        self.listboxHex.yview(*args)
        self.listboxString.yview(*args)

    def on_textscroll(self, *args):
        self.scrollBar.set(*args)
        self.on_scroll('moveto', args[0])

    def find_flag(self):
        keyword = self.get_setting("flagFormat").split("*", 1)[0]
        if self.isOpened:
            for i in range(0, len(self.filedata)):
                is_flagfound = False
                weight = 0
                startpoint = 0
                # var startpoint saves the index of data where the flag-like strings start
                for j in range(0, len(keyword)):
                    if j == 0:
                        startpoint = i
                    if not chr(self.filedata[i + weight]).upper() == keyword[j].upper():    # ignore case
                        break
                    weight += 1
                    if j == len(keyword) - 1:
                        is_flagfound = True
                if is_flagfound is not False:
                    flaglike = ""
                    for j in range(startpoint, self.filesize):
                        if 0x20 <= self.filedata[j] <= 0x7E:
                            flaglike += chr(self.filedata[j])
                        else:
                            break
                    showinfo("플래그 발견!", flaglike)

    def get_filetype(self):
        if self.is_hexheader("89 50 4E 47 0D 0A 1A 0A"):
            return "image/png"
        if self.is_hexheader("FF D8 FF DB") or self.is_hexheader("FF D8 FF E0") or self.is_hexheader("FF D8 FF E1"):
            return "image/jpg"
        if self.is_hexheader("42 4D"):
            return "image/bmp"
        if self.is_hexheader("4D 5A"):
            return "Windows Executable"
        return "알수 없음"

    def is_hexheader(self, string):
        return self.is_arraymatch(self.filedata, self.convert_tohexarr(string))

    @staticmethod
    def convert_tohexarr(string):
        hexlist = string.split(" ")
        return list(map(lambda x: int(x, 16), hexlist))

    @staticmethod
    def is_arraymatch(longarr, shortarr):
        for i, e in enumerate(shortarr):
            if not longarr[i] == e:
                return False
        return True

    @staticmethod
    def get_setting(key):
        config = ConfigParser()
        config.read("allyajyo.ini")
        return config.get('Setting', key)

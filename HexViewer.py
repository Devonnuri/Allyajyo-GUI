from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
import re

import os
from configparser import ConfigParser


class HexViewer:
    def __init__(self):
        self.filename = ""
        self.filedata = []
        self.filesize = 0
        self.buffersize = 16  # Byte count that will be displayed in a line
        self.isOpened = False

        self.filesignature = [
            ["image/png", "89 50 4E 47 0D 0A 1A 0A"],
            ["image/jpg", "FF D8 FF DB"],
            ["image/jpg", "FF D8 FF E0"],
            ["image/jpg", "FF D8 FF E1"],
            ["image/bmp", "42 4D"],
            ["image/x-icon", "00 00 01 00"],
            ["image/gif", "47 49 46 38 37 61"],
            ["image/gif", "47 49 46 38 39 61"],
            ["image/tiff(Little Endian)", "49 49 2A 00"],
            ["image/tiff(Big Endian)", "4D 4D 00 2A"],
            ["image/bpg", "42 50 47 FB"],
            ["Windows Executable", "4D 5A"],
            ["Compressed File(often tar, Lempel-Ziv-Welch)", "1F 9D"],
            ["Compressed File(often tar, LZH)", "1F A0"],
            ["Compressed File(Bzip2)", "42 5A 68"],
            ["Compressed File(based-on zip)", "50 4B 03 04"],
            ["Compressed File(based-on zip, empty)", "50 4B 05 06"],
            ["Compressed File(RAR 1.50)", "52 61 72 21 1A 07 00"],
            ["Compressed File(RAR 5.0)", "52 61 72 21 1A 07 01 00"],
            ["Executable and Linkable Format(ELF)", "7F 45 4C 46"],
            ["Java Class File, Mach-O Fat Binary", "CA FE BA BE"],
        ]

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
        self.labelFileOverlap = Label(self.frameInfo)

        self.buttonFindFlag = Button(self.frameInfo, text="플래그 찾기", command=lambda: self.find_flag())
        self.buttonFindFlag.config(font=["나눔고딕", 13])

    def show(self):
        self.root.mainloop()

    def open_filedialog(self):
        self.root.fileName = askopenfilename(title="Hex Viewer로 분석할 파일을 선택해주세요!")
        self.labelHelp.destroy()
        self.open_file(self.root.fileName)
        self.view_code()

    def open_file(self, filename):
        self.filename = filename
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
        self.labelFilename.config(font=["나눔고딕", 10], wraplength=200)
        self.labelFiletype.config(font=["나눔고딕", 10], wraplength=200)
        self.labelFilesize.config(font=["나눔고딕", 10], wraplength=200)
        self.labelFileOverlap.config(font=["나눔고딕", 9], fg="red", wraplength=200)

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
        self.labelFilesize["text"] = "파일크기:\n"+str(self.filesize)+" 바이트\n"
        self.labelFileOverlap["text"] = self.get_overlapped()

        self.labelFilename.pack(fill=X)
        self.labelFiletype.pack(fill=X)
        self.labelFilesize.pack(fill=X)
        self.labelFileOverlap.pack(fill=X)
        self.buttonFindFlag.pack(fill=X)
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
        pattern = re.compile(self.get_setting("flagFormat"), re.IGNORECASE)
        result = pattern.findall(str([chr(e) for e in self.filedata if 0x20 <= e <= 0x7E]))
        if len(result) == 0:    # When the result is empty
            showinfo("Hex Viewer - 알랴죠", "Flag가 발견되지 않았습니다.")
        else:
            showinfo("Hex Viewer - 알랴죠", "Flag가 발견되었습니다!\n\n"+"\n".join(result))

    def get_filetype(self):
        for entry in self.filesignature:
            if self.is_arraymatch(self.filedata, self.convert_tohexarr(entry[1])):
                return entry[0]
        return "알 수 없음"
    
    def get_overlapped(self):
        result = ""
        count = 0

        for entry in self.filesignature:
            match = self.get_arraymatch(self.filedata, self.convert_tohexarr(entry[1]))
            poslist = list(map(lambda x: "0x%010X" % x, match))
            if len(poslist) > 0:
                result += f"{entry[0]}({len(match)}개) {str(poslist)}\n"
                count += len(match)
        
        if count > 1:
            return "중복된 파일 헤더가 발견되었습니다.\n" + result
        else:
            return ""

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
    def get_arraymatch(longarr, shortarr):
        index = 0
        lastpos = 0
        startpos = []
        for i, e in enumerate(longarr):
            if e == shortarr[index]:
                index += 1
            else:
                lastpos = i
                index = 0

            if index+1 > len(shortarr):
                index = 0
                startpos.append(lastpos)
        return sorted(startpos)

    @staticmethod
    def get_setting(key):
        config = ConfigParser()
        config.read("allyajyo.ini")
        return config.get('Setting', key)

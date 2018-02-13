from tkinter import *
import os.path

from HexViewer import HexViewer
from Setting import Setting
from WebCrawler import WebCrawler

root = Tk()
root.title("알랴죠")
root.iconbitmap(default='logo.ico')
root.resizable(width=False, height=False)
root.minsize(width=400, height=540)

labelTitle = Label(root, text="알랴죠")
labelTitle.config(font=["나눔고딕", 25])
labelTitle.pack(fill=X)

labelSubtitle = Label(root, text="궁극의 CTF 플래그 탐색기", anchor="c")
labelSubtitle.config(font=["나눔고딕", 13])
labelSubtitle.pack(fill=X)

buttonHexViewer = Button(root, text="Hex Viewer", command=lambda: HexViewer().show())
buttonHexViewer.config(font=["나눔고딕", 15])
buttonHexViewer.pack(fill=X)

buttonHexViewer = Button(root, text="웹 크롤러", command=lambda: WebCrawler().show())
buttonHexViewer.config(font=["나눔고딕", 15])
buttonHexViewer.pack(fill=X)

buttonHexViewer = Button(root, text="Cryptography", command=lambda: WebCrawler().show())
buttonHexViewer.config(font=["나눔고딕", 15])
buttonHexViewer.pack(fill=X)

buttonSetting = Button(root, text="설정", command=lambda: Setting().show())
buttonSetting.config(font=["나눔고딕", 15])
buttonSetting.pack(fill=X)

if not os.path.exists("allyajyo.ini"):
    with open("allyajyo.ini", "w") as f:
        f.write("[Setting]\n"
                "flagFormat=Flag{.*}\n")

root.mainloop()
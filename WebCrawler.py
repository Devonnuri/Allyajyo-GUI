from tkinter import *
from tkinter.simpledialog import *
from bs4 import BeautifulSoup
import requests


class WebCrawler:
    def __init__(self):
        self.url = ""

        # GUI Components
        self.root = Tk()
        self.root.iconbitmap(default='logo.ico')
        self.root.title("설정 - 알랴죠")
        self.root.resizable(width=False, height=False)
        self.root.minsize(width=700, height=500)

        self.labelURL = Label(self.root, text="아래 URL 열기를 눌러주세요!")
        self.labelURL.config(font=["나눔고딕", 10])
        self.labelURL.pack(fill=X)

        self.buttonOpenURL = Button(self.root, text="URL 열기", command=lambda: self.openurl())
        self.buttonOpenURL.config(font=["나눔고딕", 13])
        self.buttonOpenURL.pack(fill=X)

        self.textSource = Text(self.root)
        self.textSource.config(font=["Consolas", 10], state=DISABLED, height=30, width=100)
        self.textSource.pack(side=LEFT, fill=BOTH)

        self.scrollbar = Scrollbar(self.root, command=self.textSource.yview)
        self.textSource["yscrollcommand"] = self.scrollbar.set
        self.scrollbar.pack(side=RIGHT, fill=Y)

    def show(self):
        self.root.mainloop()

    def openurl(self):
        self.url = askstring("알랴죠 - 웹크롤러", "크롤링할 웹페이지의 URL을 입력해주세요")
        self.labelURL["text"] = self.url
        self.crawl(self.url)

    def crawl(self, url):
        html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                        'Chrome/63.0.3239.132 Safari/537.36'}).text
        soap = BeautifulSoup(html, "html.parser")

        self.textSource["state"] = NORMAL
        self.textSource.insert(END, ''.join([ch for ch in list(soap.prettify()) if ord(ch) in range(65536)]))
        self.textSource["state"] = DISABLED

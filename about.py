from tkinter import Toplevel, Text, INSERT, END, DISABLED
import HyperlinkManager
import webbrowser
from functools import partial


class About:
    def __init__(self):
        self.rootpath = 'F:\\PROJECT\\Python\\TestcaseGenerator\\'
        self.openAbout()

    def openAbout(self):
        self.about = Toplevel()
        
        w = 501
        h = 170
        ws = self.about.winfo_screenwidth()
        hs = self.about.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.about.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.about.resizable(0, 0)
        self.about.title('About Testcase Generator')
        self.about.attributes("-toolwindow", 1)
        self.about.protocol("WM_DELETE_WINDOW", self.closeAboutWindow)
        self.about.grab_set()
        self.about.iconbitmap(self.rootpath + 'appdata\\asset\\favicon.ico')
        txt = Text(self.about, padx=10, pady=10, font=("Consolas", 10), wrap='word')
        self.hyperlink = HyperlinkManager.HyperlinkManager(txt)
        txt.tag_configure('bold', font='Consolas 11 bold')
        txt.insert(INSERT, 'Testcase Generator ', 'bold')
        txt.insert(END, "is a handy tool for preparing the input and output dataset for programming competition. ")
        txt.insert(END, 'Input generator is implemented using CodeForces testlib.h library for C++. ')
        txt.insert(END, "This tool is specially helpful for the problem author and tester of a programming competition.")
        txt.insert(END, '\n\n')
        txt.insert(END, 'Developed by ')
        txt.insert(END, 'Md Moniruzzaman', 'bold')
        txt.insert(END, ' <skmnrcse@gmail.com>\n')
        txt.insert(END, 'Facebook', self.hyperlink.add(partial(webbrowser.open, "https://www.facebook.com/skmnrcse/")))
        txt.insert(END, ' ')
        txt.insert(END, 'LinkedIn', self.hyperlink.add(partial(webbrowser.open, "https://www.linkedin.com/in/skmonir/")))
        txt.insert(END, ' ')
        txt.insert(END, 'Github Repo', self.hyperlink.add(partial(webbrowser.open, "https://www.github.com/skmonir/")))
        txt.pack()
        txt.config(state=DISABLED)

    def closeAboutWindow(self):
        self.about.grab_release()
        self.about.destroy()


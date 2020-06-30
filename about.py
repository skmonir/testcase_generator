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
        h = 240
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
        txt.tag_configure('header', font='Consolas 15 bold')
        txt.insert(INSERT, '             Testcase Generator\n', 'header')
        txt.insert(INSERT, '                            version: 1.0\n')
        txt.insert(END, '\nTestcase Generator ', 'bold')
        txt.insert(END, "is a handy tool for preparing the input and output dataset for programming competition. ")
        txt.insert(END, 'Input generator is implemented using ')
        txt.insert(END, 'CodeForces', self.hyperlink.add(partial(webbrowser.open, "https://www.codeforces.com/")))
        txt.insert(END, ' testlib.h library for C++. ')
        txt.insert(END, "This tool is specially helpful for the problem author and tester of a programming competition.")
        txt.insert(END, '\n\n')
        txt.insert(END, 'Github Repository', self.hyperlink.add(partial(webbrowser.open, "https://github.com/skmonir/testcase_generator/")))
        txt.insert(END, '\n\n')
        txt.insert(END, 'Developed by ')
        txt.insert(END, 'Md Moniruzzaman', 'bold')
        txt.insert(END, ' <skmnrcse@gmail.com>\n')
        txt.insert(END, 'Facebook', self.hyperlink.add(partial(webbrowser.open, "https://www.facebook.com/skmnrcse/")))
        txt.insert(END, ' ')
        txt.insert(END, 'LinkedIn', self.hyperlink.add(partial(webbrowser.open, "https://www.linkedin.com/in/skmonir/")))
        txt.insert(END, ' ')
        txt.insert(END, 'Github', self.hyperlink.add(partial(webbrowser.open, "https://www.github.com/skmonir/")))
        txt.pack()
        txt.config(state=DISABLED)

    def closeAboutWindow(self):
        self.about.grab_release()
        self.about.destroy()


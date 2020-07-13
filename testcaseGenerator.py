from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from mttkinter import *

import os
from os.path import isfile, join

import about
import inputGenerator
import outputGenerator

class MainWindow:
    def __init__(self):
        self.rootpath = 'F:\\PROJECT\\Python\\TestcaseGenerator\\'
        # self.root = mtTkinter.Tk()
        self.root = ThemedTk(theme="breeze")
        self.initFiles()
        self.initMainWindowUI()
        self.style = ttk.Style()
        # print(self.style.theme_names())
        # self.style.theme_use('xpnative')

    def run(self):
        self.root.mainloop()


    def initFiles(self):
        files = [
            'out_input.dir', 'out_output.dir', 'out_exe.dir', 'empty.tgen',
            'in_input.dir', 'in_exe.dir','script.tgen', 'tgenValidation.log'
        ]

        for file in files:
            filePath = self.rootpath + 'appdata\\files\\' + file
            if not isfile(filePath):
                f = open(filePath, 'w+')
                f.close()

    def initMainWindowUI(self):
        self.root.title('Testcase Generator 1.0')
        # self.root.iconbitmap('favicon.ico')
        self.root.iconbitmap(self.rootpath + 'appdata\\asset\\favicon.ico')

        w = 655 # width for the Tk root
        h = 610 # height for the Tk root

        # get screen width and height
        ws = self.root.winfo_screenwidth() # width of the screen
        hs = self.root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.resizable(0, 0)

        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # settings_menu = Menu(menubar, tearoff=0)
        # menubar.add_cascade(label="Format", menu=settings_menu)
        # settings_menu.add_command(label="Input File")
        # settings_menu.add_separator()
        # settings_menu.add_command(label="Output File")

        about_menu = Menu(menubar)
        menubar.add_cascade(label="About", command=self.openAbout)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack()

        self.inputGeneratorTab = inputGenerator.InputGenerator(self.tabs)
        self.outputGeneratorTab = outputGenerator.OutputGenerator(self.root, self.tabs)
        self.tabs.add(self.inputGeneratorTab.app, text="Input Generator")
        self.tabs.add(self.outputGeneratorTab.app, text="Output Generator")

    def openAbout(self):
        self.about = about.About()


def main():
    mainWindow = MainWindow()
    mainWindow.run()

if __name__ == "__main__":
    main()
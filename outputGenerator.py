import subprocess
import pathlib
import os
from os import listdir
from os.path import isfile, join
import concurrent.futures
import time

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.scrolledtext as ScrolledText
from tkinter import messagebox


class OutputGenerator:
    def __init__(self, root, notebook):
        self.root = root
        self.app = ttk.Frame(notebook, width=655, height=610)
        self.app.pack(fill="both", expand=1)

        self.rootpath = 'F:\\PROJECT\\Python\\TestcaseGenerator\\'

        self.inputDirText = StringVar()
        self.outputDirText = StringVar()
        self.exeFileText = StringVar()
        self.errorLog = StringVar()

        self.initUI()
        self.populateField()

    def initUI(self):
        inputDirBtn = ttk.Button(self.app, text="Select Input Directory", width=25,  command=self.selectInputDir)
        inputDirBtn.grid(row=0, column=0, padx=10)
        inputDirEntry = ttk.Entry(self.app, width=55, textvariable=self.inputDirText, state="readonly")
        inputDirEntry.grid(row = 0, column=1, padx=5, pady=10, ipady=1)

        outputDirBtn = ttk.Button(self.app, text="Select Output Directory", width=25, command=self.selectOutputDir)
        outputDirBtn.grid(row=1, column=0, padx=10, pady=0)
        outputDirEntry = ttk.Entry(self.app, width=55, textvariable=self.outputDirText, state="readonly")
        outputDirEntry.grid(row = 1, column=1, padx=5, pady=10, ipady=1)

        exeFileBtn = ttk.Button(self.app, text="Select Executable File", width=25, command=self.selectExeFile)
        exeFileBtn.grid(row=2, column=0, padx=10, pady=10)
        exeFileEntry = ttk.Entry(self.app, width=55, textvariable=self.exeFileText, state="readonly")
        exeFileEntry.grid(row = 2, column=1, padx=5, pady=10, ipady=1)

        self.generateOutputBtn = ttk.Button(self.app, text="Generate Output", width=15, command=self.generateOutputBtnClicked)
        self.generateOutputBtn.grid(row=3, column=0, columnspan=2, padx=50, pady=10)
        
        self.logs = ScrolledText.ScrolledText(self.app, height=19, width=85)
        self.logs.grid(row=4, column=0, columnspan=2, rowspan=6, pady=10, padx=10, ipady=5)
        self.logs.config(state=DISABLED)
        self.logs.tag_config('success', foreground='green')
        self.logs.tag_config('failure', foreground='red')

    def selectInputDir(self):
        directory = filedialog.askdirectory(title="Select The Directory Where Input Files Are Located")
        if len(directory) > 0:
            self.inputDirText.set(directory)
            self.updateFieldData('input.inf', directory)

    def selectOutputDir(self):
        directory = filedialog.askdirectory(title="Select The Directory Where Output Files Will Be Saved")
        if len(directory) > 0:
            self.outputDirText.set(directory)
            self.updateFieldData('output.inf', directory)

    def selectExeFile(self):
        filename = filedialog.askopenfilename(
                title="Select The Executable(.exe) File of Your Source Code", 
                filetypes=(("exe files", "*.exe"), ("all files", "*.exe*"))
            )
        if len(filename) > 0:
            self.exeFileText.set(filename)
            self.updateFieldData('exe.inf', filename)

    def writeLog(self, logText):
        if len(logText) > 0 and logText[0] == 'C':
            self.logs.insert(END, logText + '\n', 'success')
        elif len(logText) > 0 and logText[0] == 'F':
            self.logs.insert(END, logText + '\n', 'failure')
        else:
            self.logs.insert(END, logText + '\n')

    def updateFieldData(self, field, value):
        file_name = self.rootpath + 'appdata\\files\\' + field
        with open(file_name, 'w+') as inf:
            inf.write(value)

    def populateField(self):
        path = self.rootpath + 'appdata\\files\\'
        
        with open(path + 'input.inf', 'r') as inf:
            self.inputDirText.set(inf.read())
        with open(path + 'output.inf', 'r') as inf:
            self.outputDirText.set(inf.read())
        with open(path + 'exe.inf', 'r') as inf:
            self.exeFileText.set(inf.read())

    def generateOutputBtnClicked(self):
        inputDirPath = self.inputDirText.get()
        outputDirPath = self.outputDirText.get()
        exeFilePath = self.exeFileText.get()

        if not inputDirPath:
            self.logs.config(state=DISABLED)
            messagebox.showerror("ERROR!","Please Select The Input Directory.")
        elif not outputDirPath:
            self.logs.config(state=DISABLED)
            messagebox.showerror("ERROR!","Please Select The Output Directory.")
        elif not exeFilePath:
            self.logs.config(state=DISABLED)
            messagebox.showerror("ERROR!","Please Select Executable(.exe) of Your Solution.")
        else:
            self.logs.config(state=NORMAL)
            self.openLoadingWindow(inputDirPath, outputDirPath, exeFilePath)
            
    
    def openLoadingWindow(self, inputDirPath, outputDirPath, exeFilePath):
        self.loadingWindow = Toplevel()
        w = 492
        h = 140
        ws = self.loadingWindow.winfo_screenwidth()
        hs = self.loadingWindow.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.loadingWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.loadingWindow.resizable(0, 0)
        self.loadingWindow.title('Short Notice!')
        self.loadingWindow.attributes("-toolwindow", 1)
        self.loadingWindow.protocol("WM_DELETE_WINDOW", self.closeLoadingWindow)
        self.loadingWindow.grab_set()
        txt = Text(self.loadingWindow, padx=10, pady=10, height=3, width=64, font=("Consolas", 10))
        txt.insert(INSERT, "As we're going to perform CPU intensive IO bound task, the main window ")
        txt.insert(END, "will freeze to prevent the UI interactions. Don't panic! Everything ")
        txt.insert(END, "will be right back after the process ends.")
        txt.grid(row = 0, column = 0, padx = 10, pady = 10)
        txt.config(state=DISABLED)
        Btn = ttk.Button(self.loadingWindow, text="Continue", width=25, command=lambda: self.collectOutputFiles(inputDirPath, outputDirPath, exeFilePath))
        Btn.grid(row=1, column=0, padx=10, pady=10)
        self.generateOutputBtn.config(text="Generating...")

    def closeLoadingWindow(self):
        self.loadingWindow.grab_release()
        self.loadingWindow.destroy()
        self.generateOutputBtn.config(text="Generate Output")

    def collectOutputFiles(self, inputDirPath, outputDirPath, exeFilePath):
        self.loadingWindow.withdraw()
        self.writeLog('Process Started.')
        self.writeLog('')

        allInputFiles = [f for f in listdir(inputDirPath) if isfile(join(inputDirPath, f))]

        in_files = []
        out_files = []

        for inputFile in allInputFiles:
            input_file_name = inputDirPath + '/' + inputFile
            output_file_name = outputDirPath + '/'  + inputFile.replace("in", "out")
            
            in_files.append(input_file_name)
            out_files.append(output_file_name)

        n = len(in_files)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            logs = [executor.submit(self.writeOutputFile, in_files[i], out_files[i], exeFilePath) for i in range(n)]

            for log in concurrent.futures.as_completed(logs):
                self.writeLog(log.result())

        self.writeLog('')
        self.writeLog('Process Finished.')
        self.writeLog('#####################################################################################')
        self.logs.config(state=DISABLED)
        self.closeLoadingWindow()


    def writeOutputFile(self, input_file_name, output_file_name, exeFilePath):
        with open(input_file_name, 'rb', 0) as inf, open(output_file_name, 'w') as outf:
            proc = subprocess.Popen(exeFilePath, shell=True, stdin=inf, stdout=outf, stderr=subprocess.PIPE, text=True)
            try:
                proc.communicate()
                if proc.returncode != 0:
                    return f'Failed File: {output_file_name}'
                else:
                    return f'Created File: {output_file_name}'
            except subprocess.TimeoutExpired:
                proc.kill()
                print('Time Limit Exceeded')
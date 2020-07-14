import math
import subprocess
import pathlib
import random
import os
from os import listdir
from os.path import isfile, join, isdir
import concurrent.futures

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.scrolledtext as ScrolledText



class InputGenerator:
    def __init__(self, notebook):
        self.app = ttk.Frame(notebook, width=655, height=610)
        self.app.pack(fill="both", expand=1)

        self.rootpath = '.\\'
        
        self.inputDirText = StringVar()
        self.exeFileText = StringVar()
        self.errorLog = StringVar()

        self.numOfFilesSnArray = [str(i) for i in range(1, 101)]
        self.testPerFileOptions = [str(i) for i in range(1, 101)]
        self.testPerFileOptions.insert(0, 'N\A')
        
        self.scriptDict = {
            "Line" : "<line>",
            "Space" : "<space>",
            "Integer Variable" : "<$n[min_value:max_value]>",
            "Integer Array" : "<int_array[size:min_value:max_value:isDistinct:end_with]>",
            "Integer Pair" : "<int_pair[size:min_value:max_value:isSecondGreaterEqual]>",
            "Integer Permutation" : "<int_permutation[size:indexing]>",
            "String(s)" : "<string[number_of_string:min_size:max_size:max_total_size:charset]>",
            "Tree" : "<tree[vertices]>",
            "Weighted Tree" : "<weighted_tree[vertices:min_value:max_value]>",
            "Rooted Tree" : "<rooted_tree[vertices]>",
            "Connected Graph" : "<connected_graph[vertices:edges]>",
            "Weighted Connected Graph" : "<weighted_connected_graph[vertices:edges:min_value:max_value]>",
            "Integer Matrix" : "<int_matrix[row:column:min_value:max_value]>",
            "Character Matrix" : "<char_matrix[row:column:charset]>"
        }

        self.availableScript = [key for key in self.scriptDict.keys()]
        self.availableScript.insert(0, 'Line')

        self.generateMethod = StringVar()
        self.fileMode = StringVar()
        self.numberOfFiles = StringVar()
        self.numberOfTest = StringVar()
        self.filePref = StringVar()
        self.fileSuff = StringVar()
        self.fileSn = StringVar()
        self.selectedScript = StringVar()
        self.selectedScript.set(self.availableScript[0])
        self.logs = []

        self.initUI()
        self.initVariables()
        self.populateField()


    def initUI(self):
        numberOfFilesLabel = ttk.Label(self.app, text="No. of File", font='Consolas 10 bold', borderwidth=2, relief="groove", anchor="center")
        numberOfFilesLabel.grid(row = 0, column = 0, padx = 10, ipadx = 5, ipady = 5, sticky="E")
        numberOfFilesComboBox = ttk.Combobox(self.app, width=8, values=self.numOfFilesSnArray, font='Consolas 10 bold', textvariable = self.numberOfFiles)
        numberOfFilesComboBox.grid(row = 0, column=1, padx=10, pady=5, ipadx=5, ipady=1)

        fileWritingModeLabel = ttk.Label(self.app, text=" File Mode ", font='Consolas 10 bold', borderwidth=2, relief="groove", anchor="center")
        fileWritingModeLabel.grid(row = 0, column = 2, padx = 5, ipadx = 5, ipady = 5, sticky="E")
        fileWritingModeComboBox = ttk.Combobox(self.app, width=8, values=["Write", "Append"], font='Consolas 10 bold', textvariable = self.fileMode)
        fileWritingModeComboBox.grid(row = 0, column=3, padx=10, pady=5, ipadx=5, ipady=1)

        numberOfTCLabel = ttk.Label(self.app, text=" Test/File ", font='Consolas 10 bold', borderwidth=2, relief="groove", anchor="center")
        numberOfTCLabel.grid(row = 0, column = 4, padx = 5, ipadx = 5, ipady = 5)
        numberOfTCComboBox = ttk.Combobox(self.app, width=8, values=self.testPerFileOptions, font='Consolas 10 bold', textvariable = self.numberOfTest)
        numberOfTCComboBox.grid(row = 0, column=5, padx=10, pady=5, ipadx=5, ipady=1, sticky="E")

        fileNamePrefLabel = ttk.Label(self.app, text="File Prefix", font='Consolas 10 bold', borderwidth=2, relief="groove", anchor="center")
        fileNamePrefLabel.grid(row = 1, column = 0, padx = 10, ipadx = 5, ipady = 5)
        fileNamePrefEntry = ttk.Entry(self.app, width=10, font='Consolas 10 bold', textvariable = self.filePref)
        fileNamePrefEntry.grid(row = 1, column=1, padx=10, pady=5, ipadx=5, ipady=1)

        serialFromLabel = ttk.Label(self.app, text="Serial From", font='Consolas 10 bold', borderwidth=2, relief="groove", anchor="center")
        serialFromLabel.grid(row = 1, column = 2, padx = 5, ipadx = 5, ipady = 5)
        serialFromComboBox = ttk.Combobox(self.app, width=8, values=self.numOfFilesSnArray, font='Consolas 10 bold', textvariable = self.fileSn)
        serialFromComboBox.grid(row = 1, column=3, padx=10, pady=5, ipadx=5, ipady=1, sticky="E")

        fileNameSuffLabel = ttk.Label(self.app, text="File Suffix", font='Consolas 10 bold', borderwidth=2, relief="groove", anchor="center")
        fileNameSuffLabel.grid(row = 1, column = 4, padx = 5, ipadx = 5, ipady = 5)
        fileNameSuffEntry = ttk.Entry(self.app, width=10, font='Consolas 10 bold', textvariable = self.fileSuff)
        fileNameSuffEntry.grid(row = 1, column=5, padx=10, pady=5, ipadx=5, ipady=1, sticky="w")

        inputDirBtn = ttk.Button(self.app, text="Select Input Directory", width=25,  command=self.selectInputDir)
        inputDirBtn.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
        inputDirEntry = ttk.Entry(self.app, width=56, textvariable=self.inputDirText, state="readonly")
        inputDirEntry.grid(row = 2, column=2, padx=5, pady=5, ipady=1, columnspan=4)

        generatingMethodRadioButton_1 = ttk.Radiobutton(self.app, text='Run Generator Script Exe', variable=self.generateMethod, value='exe', command=self.generateMethodChanged)
        generatingMethodRadioButton_1.grid(row = 3, column = 0, pady = 5, columnspan=2)
        generatingMethodRadioButton_2 = ttk.Radiobutton(self.app, text='Write TGen Script in CLI', variable=self.generateMethod, value='cli', command=self.generateMethodChanged)
        generatingMethodRadioButton_2.grid(row = 3, column = 2, pady = 5, columnspan=2)

        self.exeFileBtn = ttk.Button(self.app, text="Select Script Executable", width=25, command=self.selectExeFile)
        self.exeFileBtn.grid(row=4, column=0, pady=5, columnspan=2)
        self.exeFileEntry = ttk.Entry(self.app, width=56, textvariable=self.exeFileText, state="readonly")
        self.exeFileEntry.grid(row = 4, column=2, padx=5, pady=5, ipady=1, columnspan=4)

        self.scriptOptions = ttk.OptionMenu(self.app, self.selectedScript, *self.availableScript)
        self.scriptOptions.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.insertScriptBtn = ttk.Button(self.app, text="Insert Script", command=self.insertScriptIntoCli)
        self.insertScriptBtn.grid(row=4, column=2, padx=5, pady=10)

        self.notepad = Text(self.app, height=13, width=50, font='Consolas 11', bg = "#1E1E1E", fg="white", insertbackground="white")
        self.notepad.grid(row=5, column=0, padx=5, pady=10, ipadx=10, ipady = 10, rowspan = 5, columnspan=6, sticky = N + E + S + W)

        self.generateInputBtn = ttk.Button(self.app, text="Generate Input", width=15, command=self.generateInputBtnClicked)
        self.generateInputBtn.grid(row=10, column=0, columnspan=3, padx=20, pady=10)

        self.viewLogBtn = ttk.Button(self.app, text="View Log", width=15, command=self.openLogWindow)
        self.viewLogBtn.grid(row=10, column=3, columnspan=3, padx=20, pady=10)
        

    def initVariables(self):
        self.numberOfFiles.set('1')
        self.numberOfTest.set('N\A')
        self.fileMode.set('Write')
        self.filePref.set('input')
        self.fileSn.set('1')
        self.fileSuff.set('.txt')
        self.generateMethod.set('exe')
        self.generateMethodChanged()
        self.viewLogBtn["state"] = "disabled"

        self.populateTgenScriptConsole()

    
    def updateFieldData(self, field, value):
        file_name = self.rootpath + 'appdata\\files\\' + field
        with open(file_name, 'w+') as inf:
            inf.write(value)

    def populateField(self):
        path = self.rootpath + 'appdata\\files\\'

        with open(path + 'in_input.dir', 'r') as inf:
            directory = (inf.read()).strip()
            if isdir(directory):
                self.inputDirText.set(directory)
        
        with open(path + 'in_exe.dir', 'r') as inf:
            directory = (inf.read()).strip()
            if isfile(directory):
                self.exeFileText.set(directory)


    def selectInputDir(self):
        directory = filedialog.askdirectory(title="Select The Directory Where Input Files Will Be Saved")
        if len(directory) > 0:
            self.inputDirText.set(directory)
            self.updateFieldData('in_input.dir', directory)


    def selectExeFile(self):
        filename = filedialog.askopenfilename(
                title="Select The Executable(.exe) File of Your Script", 
                filetypes=(("exe files", "*.exe"), ("all files", "*.exe*"))
            )
        if len(filename) > 0:
            self.exeFileText.set(filename)
            self.updateFieldData('in_exe.dir', filename)


    def generateMethodChanged(self):
        if self.generateMethod.get() == 'cli':
            self.notepad['fg'] = 'white'
            self.notepad['state'] = 'normal'
            self.scriptOptions.grid()
            self.insertScriptBtn.grid()
            self.exeFileBtn.grid_remove()
            self.exeFileEntry.grid_remove()
        else:
            self.notepad['fg'] = 'gray'
            self.notepad['state'] = 'disabled'
            self.exeFileBtn.grid()
            self.exeFileEntry.grid()
            self.scriptOptions.grid_remove()
            self.insertScriptBtn.grid_remove()


    def insertScriptIntoCli(self):
        self.notepad.insert(INSERT, self.scriptDict[self.selectedScript.get()])


    def validateFields(self):
        testPerFile = self.numberOfTest.get()
        numberOfFiles = self.numberOfFiles.get()
        fileMode = self.fileMode.get()
        filePref = self.filePref.get()
        fileSn = self.fileSn.get()
        fileSuff = self.fileSuff.get()
        inputDirText = self.inputDirText.get()
        generateMethod = self.generateMethod.get()
        exeFileText = self.exeFileText.get()
        script = self.notepad.get("1.0", "end").strip()

        msg = ''
        if not numberOfFiles:
            msg = 'Number of files can not be empty'
        elif not numberOfFiles.isdigit():
            msg = 'Number of files must be a number'
        elif not fileMode:
            msg = 'File Mode can not be empty'
        elif fileMode != 'Append' and fileMode != 'Write':
            msg = "File mode must be either 'Append' or 'Write'"
        elif not fileSn:
            msg = 'File serial from can not be empty'
        elif not fileSn.isdigit():
            msg = 'File serial must be a number'
        elif not fileSuff:
            msg = 'File name suffix can not be empty'
        elif not inputDirText:
            msg = 'Input directory can not be empty'
        elif generateMethod == 'cli' and len(script) == 0:
            msg = 'Tgen script can not be empty'
        elif generateMethod != 'cli' and len(exeFileText) == 0:
            msg = 'Generator executable(.exe) can not be empty'
        elif generateMethod == 'cli' and (not testPerFile):
            msg = 'Number of test per file can not be empty'
        elif generateMethod == 'cli' and testPerFile != 'N\A' and (not testPerFile.isdigit()):
            msg = 'Number of test per file must be a in the option list'
        # elif not filePref:
        #     msg = 'File name prefix can not be empty'
        
        return msg
        

    def populateTgenScriptConsole(self):
        self.notepad['state'] = 'normal'
        self.notepad.delete('1.0', END)

        with open(self.rootpath + 'appdata\\files\\script.tgen', 'r') as script:
            for line in script:
                line = line.strip()
                if line == 'END':
                    break
                self.notepad.insert(END, line + '\n')
        
        self.notepad['state'] = 'disabled'


    def generateInputBtnClicked(self):
        validationMsg = self.validateFields()

        if len(validationMsg) > 0:
            messagebox.showerror("ERROR!", validationMsg)
        else:
            if self.generateMethod.get() == 'cli':
                self.prepareTgenScript()

            validationMsg = self.validateTgenScript()
            
            if validationMsg == "OK":
                self.openLoadingWindow()
            else:
                messagebox.showerror("ERROR!", validationMsg)

    
    def prepareTgenScript(self):
        script = self.notepad.get("1.0", "end").strip().splitlines()
        with open(self.rootpath + 'appdata\\files\\script.tgen', 'w+') as file:
            for line in script:
                file.write(line.strip() + '\n')
            file.write('END')

    
    def validateTgenScript(self):
        cmd = self.rootpath + 'appdata\\bin\\validator.exe'
        inp = self.rootpath + 'appdata\\files\\script.tgen'
        out = self.rootpath + 'appdata\\files\\tgenValidation.log'
        
        self.writeFile(cmd, inp, out, 'w')

        validationMsg = ''
        with open(self.rootpath + 'appdata\\files\\tgenValidation.log', 'r') as file:
            for line in file:
                validationMsg = line.strip()
                break
        return validationMsg
    

    def openLoadingWindow(self):
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
        Btn = ttk.Button(self.loadingWindow, text="Continue", width=25, command=self.generateInput)
        Btn.grid(row=1, column=0, padx=10, pady=10)
        self.generateInputBtn.config(text="Generating...")


    def closeLoadingWindow(self):
        self.loadingWindow.grab_release()
        self.loadingWindow.destroy()
        self.generateInputBtn.config(text="Generate Input")


    def generateInput(self):
        self.closeLoadingWindow()

        testPerFile = 0
        if (self.numberOfTest.get() != 'N\A'):
            testPerFile = int(self.numberOfTest.get())
        numberOfFiles = int(self.numberOfFiles.get())
        fileMode = 'w'
        filePref = self.filePref.get()
        fileSn = int(self.fileSn.get())
        fileSuff = self.fileSuff.get()
        inputDirText = self.inputDirText.get()
        generateMethod = self.generateMethod.get()
        exeFileText = self.exeFileText.get()
        if self.fileMode.get() == 'Append':
            fileMode = 'a'

        self.logs.append('##################################_Process Started_###################################\n')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            if generateMethod == 'cli':
                paramId = random.randint(12345, 12345678987654321)
                for i in range(numberOfFiles):
                    paramId = paramId + 1
                    cmd = self.rootpath + 'appdata\\bin\\generator.exe' + ' ' + str(testPerFile) + ' ' + str(paramId)
                    scriptPath = self.rootpath + 'appdata\\files\\script.tgen'
                    input_file_path = inputDirText + '/' + filePref + str(fileSn) + fileSuff
                    fileSn = fileSn + 1
                    self.logs.append(executor.submit(self.writeFile, cmd, scriptPath, input_file_path, fileMode).result())
            else:
                for i in range(numberOfFiles):
                    cmd = exeFileText + ' 1 ' + str(i)
                    scriptPath = self.rootpath + 'appdata\\files\\empty.tgen'
                    input_file_path = inputDirText + '/' + filePref + str(fileSn) + fileSuff
                    fileSn = fileSn + 1
                    self.logs.append(executor.submit(self.writeFile, cmd, scriptPath, input_file_path, fileMode).result())

            self.logs.append('\n##################################_Process Finished_##################################\n\n')
            os.startfile(inputDirText)
            self.viewLogBtn["state"] = "normal"


    def writeFile(self, cmd, inputFilePath, outputFilePath, fileMode):
        with open(inputFilePath, 'rb', 0) as inf, open(outputFilePath, fileMode) as outf:
            proc = subprocess.Popen(cmd, shell=True, stdin=inf, stdout=outf, stderr=subprocess.PIPE, text=True)
            try:
                proc.communicate()
                if proc.returncode != 0:
                    return f'Failed File: ' + self.getFileName(outputFilePath)
                else:
                    return f'Created File: ' + self.getFileName(outputFilePath)
            except subprocess.TimeoutExpired:
                proc.kill()
    
    def openLogWindow(self):
        self.logWindow = Toplevel()
        w = 650
        h = 340
        ws = self.logWindow.winfo_screenwidth()
        hs = self.logWindow.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.logWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.logWindow.resizable(0, 0)
        self.logWindow.title('Input Generator Logs!')
        self.logWindow.attributes("-toolwindow", 1)
        self.logWindow.protocol("WM_DELETE_WINDOW", self.closeLogWindow)
        self.logWindow.grab_set()

        inputGeneratorLogs = ScrolledText.ScrolledText(self.logWindow, height=19, width=85)
        inputGeneratorLogs.grid(row=0, column=0, columnspan=2, rowspan=6, pady=10, padx=10, ipady=5)
        inputGeneratorLogs.tag_config('success', foreground='green')
        inputGeneratorLogs.tag_config('failure', foreground='red')

        for logText in self.logs:
            if len(logText) > 0 and logText[0] == 'C':
                inputGeneratorLogs.insert(END, logText + '\n', 'success')
            elif len(logText) > 0 and logText[0] == 'F':
                inputGeneratorLogs.insert(END, logText + '\n', 'failure')
            else:
                inputGeneratorLogs.insert(END, logText + '\n')

        inputGeneratorLogs.config(state=DISABLED)


    def closeLogWindow(self):
        self.logWindow.grab_release()
        self.logWindow.destroy()

    def getFileName(self, filePath):
        if isfile(filePath):
            return os.path.basename(filePath)
        else:
            return 'Error in file name'
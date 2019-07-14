#############################################
#                                           #
#    AitorPyOS by AITOR ROSELL TORRALBA     #
#                                           #
#############################################


#############
#Import Zone#
#############

import getpass #This is for the password field
import time #This is for wait time
import sys
from os import system, name #This is needed for the clear function
import os
from subprocess import call #This is also needed for the clear function
from msvcrt import getch #This is for the text editor
import pickle 
import os.path
import math
import random

########################


###########
#Functions#
###########

def importFile(path):
    if os.path.isfile(path):
        file = open(path, "r") 
        result = file.read()
        head, tail = os.path.split(path)
        file.close()
        print("File loaded")
        return [True,result,tail]
    else:
        print("Such file does not exists")
        return [False]

def exportFile(file):
    temp = dir()
    temp += ".content['"+file+"']"
    temp2 = dir()+".findId('"+file+"')"
    temp2 = eval(temp2)
    if temp2 != -1:
        temp = eval(temp)
        path = temp.fullname()
        if temp.fileType != "Dir":
            if os.path.isfile(path):
                if input("Such file aleardy exist. Overwrite? y/n: ") == "y":
                    os.remove(path)
                    print("File Overwritting mode ON")
                else:
                    print("procedure cancelled")
                    return False
            file = open(path, "w+") 
            file.write(temp.content)
            file.close()
            print("File Exported")
            return True
        else:
            print("Directories are not exportable")
            return False
    else:
        print("Such file does not exists")
        return False

def saveToDisk():
    disk = DiskObject()
    filehandler = open("disk", 'wb') 
    pickle.dump(disk, filehandler)

def loadDisk():
    global systema
    global pwd
    global clipboard
    filehandler = open("disk", 'rb') 
    disk = pickle.load(filehandler)
    systema = disk.systema
    pwd = disk.pwd
    clipboard = disk.clipboard
    print("Disk loaded")

def move(order, target):#function to move copy paste cut etc
    temp = dir()
    if order == "copy":
        try:
            target = temp+".copy('"+target+"')"
            returnVal = eval(target)
        except:
            returnVal = False
            print("Error")
    elif order == "cut":
        try:
            target = temp+".cut('"+target+"')"
            returnVal = eval(target)
        except:
            returnVal = False
            print("Error")
    elif order == "paste":
        try:
            target = temp+".paste()"
            returnVal = eval(target)
        except:
            returnVal = False
            print("Error")
    else:
       returnVal = False
       print("Error")

    if returnVal != False and (order == "copy" or order == "cut"):
        global clipboard
        clipboard = returnVal
    else:
        return

def runScript(scriptString, params = []):#function to exec but whit safety
    try:
        if params != []:
            sys.argv = params
        exec(scriptString)
    except SyntaxError as err:
        print("Syntax error")
        print(err)
    except Exception as err:
        print("Exception error")
        print(err)
    except:
        print("Error")

#This function is to clear the CMD
def clear(): 
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 

#This 2 functions is to create the objects
def mkDirFunc(name, location):
    return MkDir(name, location)

def mkFileFunc(name, location):
    return MkFile(name, location)

#This function generates the directory string based on pwd for later evaluation
def dir():
    cmmnd = "systema"
    for x in pwd:
        cmmnd += ".content['"+x+"']"
    return cmmnd

#This function is to edit the text
def editText(text, otext):
    possition = 0
    while True:
        clear()
        print(text[:possition]+"|"+text[possition:])
        text2 = getch()
        if (ord(text2) == 224):
            key = ord(getch())
            if key == 75 and possition-1 != -1:
                possition = possition- 1
            elif key == 77 and possition+1 != len(text)+1:
                possition = possition+ 1
            elif key == 83:
                test = text
                text = test[:possition] + test[possition+1:]
              
        elif ord(text2) == 27:
            break
        elif ord(text2) == 8:
            test = text
            if possition != 0:
                text = test[:possition-1] + test[possition:]
                possition = possition-1
        elif ord(text2) == 13:
            test = text
            text = test[:possition] + "\n" + test[possition:]
            possition = possition+1
        elif ord(text2) == 9:
            test = text
            text = test[:possition] + "\t" + test[possition:]
            possition = possition+1
        else:
            test = text
            text2 = text2.decode("utf-8") 
            text = test[:possition] + text2 + test[possition:]
            possition = possition+1
    while True:
        res = input("Do you want to save the changes? y/n: ")
        if res == "y":
            return text
        elif res == "n":
            return otext
        else:
            continue

#####################################################


#########
#Classes#
#########

#This is the class for creating a file
class DiskObject:
    def __init__(self):
        self.systema = systema
        self.pwd = pwd
        self.clipboard = clipboard

class MkFile:
    def __init__(self,name,location):#the init function
        self.fileType = name[1]
        self.directory = location
        self.name = name[0]
        self.content = ""
    def edit(self):#This is for calling the text editor
        self.content = editText(self.content, self.content)
    def fullname(self):#This returns the full name, so name + filetype 
        return self.name+"."+self.fileType

#This is the class for creating a directory
class MkDir:
    def __init__(self,name,location):#the init function
        self.directory = location
        self.name = name
        self.content = {}
        self.fileType = "Dir"
    def fullname(self):#this return the name is kinda redundant to be honest
        return self.name
    def ls(self):#This is for listing the contents of the directory
        temp = self.content.keys()
        if not self.content:#This happens when its empty
            print("<empty>")
        else:#This happens when there is stuff inside
            for x in temp:
                y = self.content[x]
                print(x+"\t\t\t"+"type:"+y.fileType)
    def findId(self,name):#this is a somewhat not su useful function, before it had his sense but now it does not, but is legacy
        if name in self.content.keys():
            result = 1
        else:
            result = -1
        return result
    def rename(self,name, newname):#function for renaming dirs and files
        if self.findId(name) != -1:# if exists
            if self.content[name].fileType == "Dir":#if its a dir
                if not self.content[name].content: # if is not empty
                    print("The names of directories that are not empty cannot be changed")
                else:#if its empty
                    self.content[name].name = newname
                    self.content[newname] = self.content[name]
                    del self.content[name]
            else:#if its a file
                newname = newname.split(".")
                if len(newname) < 2:#this is a check to add the old if no filetype is provided
                    newname[1] = name.split(".")[1]
                newfullnamae = newname[0]+"."+newname[1]
                self.content[name].name = newname[0]
                self.content[name].fileType = newname[1]
                self.content[newfullnamae] = self.content[name]
                del self.content[name]
    def cut(self,name):
        if self.findId(name) != -1:# if exists
            if self.content[name].fileType == "Dir":#if its a dir
                print("directories cannot be cut")
                return False
            else:#if its a file
                returnVal = self.content[name]
                del self.content[name]
                return returnVal
    def copy(self,name):
        if self.findId(name) != -1:# if exists
            if self.content[name].fileType == "Dir":#if its a dir
                print("directories cannot be copied")
                return False
            else:#if its a file
                returnVal = self.content[name]
                return returnVal
    def paste(self):
        content = clipboard
        if self.findId(content.fullname()) == -1:# if it does not exists
            content.directory = self.directory+[self.name]
            self.content[content.fullname()] = content
            print("File succesfully pasted")            
            return True
        else:
            print("a file whit that name aleardy exists")
            return False
    def mkDir(self,name):#this is for creating a new directory inside this directory
        if self.findId(name) == -1:# if there is no directory whit this name here do this
            tempDir = mkDirFunc(name,self.directory+[self.name])
            self.content[name] = tempDir
        else:# if there is a directory whit this name here do this
            print("That directory aleardy exists")
    def mkFile(self,name):#this is for creating a file inside this directory
        name = name.split(".")
        if len(name) < 2:#this is a check to add the .txt if no filetype is provided
            name[1] = "txt"
        fullnamae = name[0]+"."+name[1]
        if self.findId(fullnamae) == -1:#if there is no file whit this name here do this
            tempFile = mkFileFunc(name,self.directory+[self.name])
            self.content[fullnamae] = tempFile
        else:#else if there is a file whit this name do this
            print("That file aleardy exists")
    def rm(self,name):#this is the function to remove a file or directory from this directory
        if self.findId(name) != -1:# if there is a file/directory whit this name do this
            self.content.pop(name)
        else:#else if there is a file directory whitout this name do this
            if self.content[self.findId(name)].fileType == "Dir":
                print("That directory does not exists")
            else:
                print("That file does not exist")

#########################################


##########################
#Setup of the file system#
##########################

clipboard = {}
systema = MkDir("./",[])#create the root directory
systema.mkDir("C:")# create the C disk
systema.content["C:"].mkDir("home")#create the home directory in C:
systema.content["C:"].content["home"].mkDir("root")#create the root user directory in home
systema.content["C:"].content["home"].content["root"].mkFile("ejemplo.txt")#create a example file in the root user directory
systema.content["C:"].content["home"].content["root"].content["ejemplo.txt"].content = "Este es un texto de prueba\nEsta es la linea 2\nEsta es la linea 3\nEsta es la ultima linea"#change the contents of that file

##########################################


##########
#START OS#
##########

time.sleep(2)
print("Booting the AitorPyOS 0.1")
time.sleep(2)
print(" . ")
time.sleep(2)
print(" .. ")
time.sleep(2)
print(" ... ")
time.sleep(3)
print("AitorPyOs Succesfully Loaded!")
time.sleep(1)
print("Please log in")
time.sleep(1)

while True: #This is the log-in part
    user = input("User: ")
    if user != "root":
        print("Incorrect user")
        time.sleep(1)
        continue
    else:
        time.sleep(1)
        password = getpass.getpass("Password: ")
        if password != "root":
            print("Incorrect password")
            time.sleep(1)
            continue
        else:
            time.sleep(1)
            break

#welcome messages
print("Welcome "+user)
pwd = ["C:","home",user]

if os.path.isfile('disk'):
    if input("disk detected! load? y/n: ") == "y":
        print("loading disk...")
        time.sleep(2)
        loadDisk()
        time.sleep(1)
#This is the command loop
while True:
    c = input("$> ")# get the input of the command
    b = c#save the whole command for things
    c = c.split(" ")#split the commands in to a list separated by spaces
    a = c[0] # save the first command in to a var for ease of my writting
    b = b[len(a)+1:] #remove the first command for things from the whole string
    if a == "shutdown": # shutdown command
        if input("Do you want to save changes to disk y/n: ") == "y":
            saveToDisk()
            print("saving to disk...")
            time.sleep(2)
        print("shutting down system...")
        time.sleep(1)
        break
    elif a == "pwd":#tell me current directory command
        print("/".join(pwd))
    elif a == "ls":#list contents of current directory command
        temp = dir()
        temp += ".ls()"
        exec(temp)
    elif a == "mkdir":#create a new directory command
        temp = dir()
        temp += ".mkDir('"+c[1]+"')"
        exec(temp)
    elif a == "edit":#edit a file command
        temp = dir()
        temp += ".content['"+c[1]+"'].edit()"
        exec(temp)
    elif a == "rename":#rename a file
        temp = dir()
        temp += ".rename('"+c[1]+"','"+c[2]+"')"  
        exec(temp)
    elif a == "mkfile":#create a new file command
        temp = dir()
        temp += ".mkFile('"+c[1]+"')"
        exec(temp)
    elif a == "rm":#remove file / directory command
        temp = dir()
        temp += ".rm('"+c[1]+"')"
        exec(temp)
    elif a == "cd":# change directory command
        if c[1] == "..":
            pwd.pop(len(pwd)-1)
        else:
            pwd += c[1].split("/")
    elif a == "mv":# move command
        if len(c) == 3:
            move(c[1],c[2])
        elif len(c) == 2 and c[1] == "paste":
            move(c[1],clipboard)
        else:
            print("error")
    elif a == "exec":# exec python code command
        runScript(b)
    elif a == "export":# exports a file to the outside
        exportFile(c[1])
    elif a == "import":# imports a file from the outside
        temporal = importFile(b)
        if temporal[0]:
            temporal2 = dir()+".findId('"+temporal[2]+"')"
            if temporal2 != -1:
                print(temporal[2])
                exec(dir()+".mkFile('"+temporal[2]+"')")
                print("importing file step 1...")
                global importGlobal
                importGlobal = temporal[1]
                time.sleep(1)
                exec(dir()+".content['"+temporal[2]+"'].content = importGlobal")
                print("importing file step 2...")
                time.sleep(1)
                print("File imported succesfully!")
            else:
                print("a file whit the same name aleardy exists")
        else:
            print("a error has occurred")
    elif a == "math":# exec python code command but whit print and for math
        runScript("print("+b+")")
    elif a == "run":#run a script file
        temp = dir()
        temp += ".content['"+c[1]+"'].content"
        runScript(eval(temp))
    elif a[-3:] == ".py": # to execute scripts just by putting the name as long as they are .py
        temp = dir()
        temp += ".content['"+a+"'].content"
        runScript(eval(temp),c[1:])
    else:# unknown command
        print("Unknown command")

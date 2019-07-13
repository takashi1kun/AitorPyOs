import getpass
import time
from os import system, name 
from subprocess import call 
from msvcrt import getch
#classes

# define our clear function 
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 
  
def mkDirFunc(name, location):
    return MkDir(name, location)
def mkFileFunc(name, location):
    return MkFile(name, location)
def editText2(text, otext):
    index = 0
    xPossition = 0
    yPossition = len(text)-1
    while True:
        index = 0
        clear()
        for x in text:
            if index != yPossition:
                print(x)
            else:
                print(x[:xPossition]+"|"+x[xPossition:])
            index += 1
        text2 = getch()
        if (ord(text2) == 224):
            key = ord(getch())
            if key == 72 and yPossition-1!=-1:
                yPossition = yPossition- 1
            elif key == 80 and yPossition+1!=len(text):
                yPossition = yPossition+ 1
            elif key == 75 and xPossition-1 != -1:
                xPossition = xPossition- 1
            elif key == 77 and xPossition+1 != len(text[yPossition])+1:
                xPossition = xPossition+ 1
            elif key == 83:
                test = text[yPossition]
                if xPossition != len(text)-1:
                    text[yPossition] = test[:xPossition] + test[xPossition+1:]
                else:
                    test2 = text[yPossition+1]
                    text.pop(yPossition+1)
                    text[yPossition] += test2
        elif ord(text2) == 27:
            break
        elif ord(text2) == 8:
            test = text[yPossition]
            if xPossition != 0:
                text[yPossition] = test[:xPossition-1] + test[xPossition:]
                xPossition = xPossition-1
            else:
                text.pop(yPossition)
                xPossition = len(text[yPossition-1])
                text[yPossition-1] += test
                yPossition -= 1    
        elif ord(text2) == 13:
            test = text[yPossition]
            text[yPossition] = test[xPossition:]
            text.insert(yPossition, test[:xPossition])
        else:
            test = text[yPossition]
            text2 = text2.decode("utf-8") 
            text[yPossition] = test[:xPossition] + text2.lower() + test[xPossition:]
            xPossition = xPossition+1
    while True:
        res = input("Do you want to save the changes? y/n: ")
        if res == "y":
            return text
        elif res == "n":
            return otext
        else:
            continue

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
class MkFile:
    def __init__(self,name,location):
        self.fileType = name[1]
        self.directory = location
        self.name = name[0]
        self.content = ""
    def edit(self):
        self.content = editText(self.content, self.content)
    def fullname(self):
        return self.name+"."+self.fileType
class MkDir:
    def __init__(self,name,location):
        self.directory = location
        self.name = name
        self.content = {}
        self.fileType = "Dir"
    def fullname(self):
        return self.name
    def ls(self):
        temp = self.content.keys()
        if not self.content:
            print("<empty>")
        else:
            for x in temp:
                y = self.content[x]
                print(x+"\t\t\t"+"type:"+y.fileType)
    def findId(self,name):
        if name in self.content.keys():
            result = 1
        else:
            result = -1
        return result
    def mkDir(self,name):
        if self.findId(name) == -1:
            tempDir = mkDirFunc(name,self.directory+[self.name])
            self.content[name] = tempDir
        else:
            print("That directory aleardy exists")
    def mkFile(self,name):
        name = name.split(".")
        if len(name) < 2:
            name[1] = "txt"
        fullnamae = name[0]+"."+name[1]
        if self.findId(fullnamae) == -1:
            tempFile = mkFileFunc(name,self.directory+[self.name])
            self.content[fullnamae] = tempFile
        else:
            print("That file aleardy exists")
    def rm(self,name):
        if self.findId(name) != -1:
            self.content.pop(name)
        else:
            if self.content[self.findId(name)].fileType == "Dir":
                print("That directory does not exists")
            else:
                print("That file does not exist")

#test
systema = MkDir("./",[])
systema.mkDir("C:")
systema.content["C:"].mkDir("home")
systema.content["C:"].content["home"].mkDir("root")
systema.content["C:"].content["home"].content["root"].mkFile("ejemplo.txt")
#systema.content["C:"].content["home"].content["root"].content["ejemplo.txt"].content = ["Este es un texto de prueba", "Esta es la linea 2", "Esta es la linea 3", "Esta es la ultima linea"]
systema.content["C:"].content["home"].content["root"].content["ejemplo.txt"].content = "Este es un texto de prueba\nEsta es la linea 2\nEsta es la linea 3\nEsta es la ultima linea"
def dir():
    cmmnd = "systema"
    for x in pwd:
        cmmnd += ".content['"+x+"']"
    return cmmnd

#START OS
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
while True:
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
print("Welcome "+user)
pwd = ["C:","home",user]
while True:
    c = input("$> ").split(" ")
    a = c[0]
    if a == "shutdown":
        print("shutting down system...")
        time.sleep(1)
        break
    elif a == "pwd":
        print("/".join(pwd))
    elif a == "ls":
        temp = dir()
        temp += ".ls()"
        exec(temp)
    elif a == "mkdir":
        temp = dir()
        temp += ".mkDir('"+c[1]+"')"
        exec(temp)
    elif a == "edit":
        temp = dir()
        temp += ".content['"+c[1]+"'].edit()"
        exec(temp)
    elif a == "mkfile":
        temp = dir()
        temp += ".mkFile('"+c[1]+"')"
        exec(temp)
    elif a == "rm":
        temp = dir()
        temp += ".rm('"+c[1]+"')"
        exec(temp)
    elif a == "cd":
        if c[1] == "..":
            pwd.pop(len(pwd)-1)
        else:
            pwd += c[1].split("/")
    elif a == "exec":
        exec(input("$> exec "))
    elif a == "run":
        temp = dir()
        temp += ".content['"+c[1]+"'].content"
        exec(eval(temp))
    else:
        print("Unknown command")
import tkinter as tk
import json
import os
import shutil
import webbrowser
import http.server
import socketserver
import ttkbootstrap as ttk
from tkinter import filedialog

from model import GenNEforUsr
from spider.ChineseUniversityMooc import getMooc
from spider.HaoDaXue import getHDX
from spider.bilibili import getBiliBili
from spider.iCourse import getIcourse


def openGraph(curWindow, name):
    # current_directory = os.path.dirname(__file__)
    # html_file_path = os.path.join(current_directory, '..', 'usr', name, 'graph.html')
    shutil.copy("../usr/" + name + "/graph.html", "graph.html")
    shutil.copy("../usr/" + name + "/node_edge_usr.json", "node_edge_usr.json")

    allSet = set()
    with open("../model/node_edge.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    for node in data["nodes"]:
        allSet.add(node["label"])
    with open("node_edge_usr.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    for node in data["nodes"]:
        if not node["label"] in allSet:
            kw = node["label"]
            getBiliBili(kw, 1)
            getBiliBili(kw, 2)
            getBiliBili(kw, 3)
            getBiliBili(kw, 4)
            getBiliBili(kw, 5)
            getMooc(kw)
            getHDX(kw)
            getIcourse(kw)

    with open('graph.html', 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用replace()方法将旧关键词替换为新关键词
    new_content = content.replace('USERNAME', '\"' + name + '\"')

    with open('graph.html', 'w', encoding='utf-8') as file:
        file.write(new_content)

    html_file_path = 'graph.html'
    handler = http.server.SimpleHTTPRequestHandler
    port = 8000
    curWindow.destroy()
    with socketserver.TCPServer(("", port), handler) as httpd:
        fileUrl = f"http://localhost:{port}/{html_file_path}"
        webbrowser.open(fileUrl)
        httpd.serve_forever()



def select(name, curWindow):
    filePath = filedialog.askopenfilename()
    shutil.copy(filePath, "../usr/" + name + "/")
    openGraph(curWindow, name)


def askAndOpen(usr):
    window2 = ttk.Window(
        title="自定义知识图谱文件",
        themename="darkly",
        size=(650, 700),
        position=(1000, 300),
        minsize=(0, 0),
        maxsize=(1920, 1080),
        resizable=None,
        alpha=1.0,
    )
    window2.wm_attributes('-topmost', 1)
    askLabel = tk.Label(window2, text='是否有新的知识图谱文件导入？')
    askLabel.grid(row=0, column=0, columnspan=2, padx=0, pady=200)
    yesButton = tk.Button(window2, text='是', width=10, command=lambda name=usr, curWindow=window2:select(name, curWindow))
    yesButton.grid(row=1, column=0, sticky='w', padx=80, pady=30)
    noButton = tk.Button(window2, text='否', width=10, command=lambda name=usr, curWindow=window2:openGraph(curWindow, name))
    noButton.grid(row=1, column=1, sticky='e', padx=30, pady=30)
    window2.mainloop()


def logIn():
    name = nameVar.get()
    password = passwordVar.get()
    d = dict()
    if os.path.exists('usrPwd.json'):
        with open("usrPwd.json", "r", encoding="utf-8") as file:
            for line in file.readlines():
                line = line.strip()
                if len(line) == 0:
                    continue
                data = json.loads(line)
                d.update(data)
    if d.get(name) is None:
        resultLabel["text"] = "用户不存在，请注册！"
        nameEntry.delete(0, len(name))
        passwordEntry.delete(0, len(password))
        register()
    elif d.get(name) != password:
        resultLabel["text"] = "密码错误，请重新输入！"
        passwordEntry.delete(0, len(password))
    else:
        resultLabel["text"] = "登录成功！欢迎" + name + "!"
        window.after(2000, lambda usr=name : askAndOpen(usr))
        window.after(3000, window.destroy)


ifAll = 0
ifArch = 0
ifApp = 0
ifMath = 0
ifCode = 0


def register():
    def click1(event):
        global ifArch
        if ifArch == 0:
            ifArch = 1
        else:
            ifArch = 0

    def click2(event):
        global ifApp
        if ifApp == 0:
            ifApp = 1
        else:
            ifApp = 0

    def click3(event):
        global ifMath
        if ifMath == 0:
            ifMath = 1
        else:
            ifMath = 0

    def click4(event):
        global ifCode
        if ifCode == 0:
            ifCode = 1
        else:
            ifCode = 0

    def clickAll():
        c1.select()
        c2.select()
        c3.select()
        c4.select()
        global ifAll, ifArch, ifApp, ifMath, ifCode
        ifAll = 1
        ifArch = 1
        ifApp = 1
        ifMath = 1
        ifCode = 1

    def doReg():
        name = str(nameEntry1.get()).strip()
        password = str(passwordEntry1.get()).strip()
        if len(name) == 0:
            resultLabel1["text"] = "账号名不能为空！"
            nameEntry1.delete(0, len(name))
            passwordEntry1.delete(0, len(name))
            return
        if len(password) == 0:
            resultLabel1["text"] = "密码不能为空！"
            nameEntry1.delete(0, len(name))
            passwordEntry1.delete(0, len(name))
            return
        path = '../usr/' + name
        if os.path.exists(path):
            resultLabel["text"] = "用户已注册，请登陆！"
            window1.destroy()
            return
        file = open("usrPwd.json", "a", encoding="utf-8")
        file.write('\n{\"' + name + '\":\"' + password + '\"}')
        file.close()
        os.mkdir(path)
        shutil.copy("../model/graph.html", "../usr/" + name + "/graph.html")
        global ifAll, ifArch, ifApp, ifMath, ifCode
        GenNEforUsr.genNodeEdgeForUsr(ifAll, ifArch, ifApp, ifMath, ifCode, path)
        nameEntry1.delete(0, len(name))
        passwordEntry1.delete(0, len(password))
        resultLabel["text"] = "注册成功，请重新登陆！"
        window1.destroy()

    window1 = ttk.Window(
        title="注册",
        themename="darkly",
        size=(650, 700),
        position=(1000, 300),
        minsize=(0, 0),
        maxsize=(1920, 1080),
        resizable=None,
        alpha=1.0,
    )
    # window1 = ttk.Window(themename="darkly")
    # style1 = ttk.Style("darkly")
    # window1.title('注册')
    # window1.geometry('500x500')
    nameLabel1 = tk.Label(window1, text='账号：')
    nameLabel1.grid(row=0, column=0, padx=0, pady=30)
    passwordLabel1 = tk.Label(window1, text='密码：')
    passwordLabel1.grid(row=1, column=0)
    nameEntry1 = tk.Entry(window1)
    nameEntry1.grid(row=0, column=1, padx=0, pady=20)
    passwordEntry1 = tk.Entry(window1)
    passwordEntry1.grid(row=1, column=1, padx=0, pady=20)
    radioLabel = tk.Label(window1, text='请选择您的学习偏好：')
    radioLabel.grid(row=2, column=0, columnspan=2, padx=0, pady=20)
    c1 = tk.Checkbutton(window1, text='体系结构')
    c1.grid(row=3, column=0, padx=0, pady=20)
    c1.bind('<Button-1>', click1)
    c2 = tk.Checkbutton(window1, text='应用工程')
    c2.grid(row=4, column=0, padx=0, pady=20)
    c2.bind('<Button-1>', click2)
    c3 = tk.Checkbutton(window1, text='数理逻辑')
    c3.grid(row=3, column=1)
    c3.bind('<Button-1>', click3)
    c4 = tk.Checkbutton(window1, text='编程语言')
    c4.grid(row=4, column=1)
    c4.bind('<Button-1>', click4)
    cAll = tk.Checkbutton(window1, text='我全都要！（全选）', command=clickAll)
    cAll.grid(row=5, column=0, columnspan=2, padx=0, pady=20)
    logInButton1 = tk.Button(window1, text='注册', width=10, command=doReg)
    logInButton1.grid(row=6, column=0, sticky='w', padx=80, pady=30)
    quitButton1 = tk.Button(window1, text='退出', width=10, command=window1.destroy)
    quitButton1.grid(row=6, column=1, sticky='e', padx=30, pady=30)
    resultLabel1 = tk.Label(window1, text='')
    resultLabel1.grid(row=7, column=0, columnspan=2)
    window1.mainloop()


window = ttk.Window(
        title="登录",
        themename="darkly",
        size=(700,400),
        position=(1000,500),
        minsize=(0,0),
        maxsize=(1920,1080),
        resizable=None,
        alpha=1.0,
        )
# root.place_window_center()    #让显现出的窗口居中
# root.resizable(False,False)   #让窗口不可更改大小
# root.wm_attributes('-topmost', 1)#让窗口位置其它窗口之上

# style = Style(theme='darkly')
# window = ttk.Window(themename="darkly")
# window.title('登录')
# window.geometry('500x300')

nameLabel = ttk.Label(window, text='账号：')
nameLabel.grid(row=0, column=0, padx=0, pady=30)
passwordLabel = ttk.Label(window, text='密码：')
passwordLabel.grid(row=1, column=0)

nameVar = tk.StringVar()
passwordVar = tk.StringVar()

nameEntry = ttk.Entry(window, textvariable=nameVar)
nameEntry.grid(row=0, column=1, padx=0, pady=20)
passwordEntry = ttk.Entry(window, textvariable=passwordVar, show='*')
passwordEntry.grid(row=1, column=1, padx=0, pady=20)

logInButton = ttk.Button(window, text='登录', width=10, command=logIn, style='success.TButton')
logInButton.grid(row=3, column=0, sticky='w', padx=80, pady=30)
quitButton = ttk.Button(window, text='退出', width=10, command=window.quit, style='success.TButton')
quitButton.grid(row=3, column=1, sticky='e', padx=30, pady=30)

resultLabel = ttk.Label(window, text='')
resultLabel.grid(row=4, column=0, columnspan=2)

registerButton = ttk.Button(window, text='注册', width=10, command=register, style='success.Outline.TButton')
registerButton.grid(row=5, column=0, columnspan=2)

window.mainloop()

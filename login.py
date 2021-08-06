import json
import random
import main
import otp as onetimepassword

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox as msg

range = random.randint(1000, 9999)


def newpass():
    def setPass():
        if txt2.get() == txt3.get():
            with open('users.json', 'r') as file:
                jo = json.load(file)

            username = jo['user1']['username']
            gmail = jo['user1']['gmail']
            password = txt2.get()

            data = {'user1': {'username': username, 'password': password, 'gmail': gmail}}

            with open('users.json', 'w') as file:
                json.dump(data, file)

            root.destroy()
            login()

        else:
            msg.showwarning('Security Error', message='Your both password should identical.')

    root = tk.Tk()
    root.geometry("1280x720")
    root.resizable(True, False)
    root.title("Login Page")
    root.config(bg='#262523')

    frame1 = tk.Frame(root, bd=12, relief='groove', bg="#00aeff")
    frame1.place(relx=0.28, rely=0.12, relwidth=0.50, relheight=0.78)

    h1 = tk.Label(frame1, bd=8, relief='groove', text='Password Change', fg='black', bg="#3ece48", width=29, height=1,
                  font=('times', 25, ' bold '))
    h1.place(x=11, y=5)

    lb2 = tk.Label(frame1, text="Enter Password", fg="black", bg="#00aeff", font=('times', 18, ' bold '))
    lb2.place(x=130, y=180)

    txt2 = tk.Entry(frame1, bd=5, relief=SUNKEN, width=40, fg="black", show='*', font=('times new roman', 15, ' bold '))
    txt2.place(x=130, y=220)

    lb3 = tk.Label(frame1, text="Re-Enter Password", fg="black", bg="#00aeff", font=('times', 18, ' bold '))
    lb3.place(x=130, y=270)

    txt3 = tk.Entry(frame1, bd=5, relief=SUNKEN, width=40, fg="black", show='*', font=('times new roman', 15, ' bold '))
    txt3.place(x=130, y=310)

    clearButton = tk.Button(frame1, text="Confirm", command=setPass, bd=5, relief="groove", fg="black", bg='red',
                           width=15, height=1, activebackground='white', font=('times', 15, ' bold '))
    clearButton.place(x=130, y=400)


def passReset():
    
    def login2():
        root.destroy()
        login()

    def send():
        with open('users.json', 'r') as file:
            json_object = json.load(file)

        name = json_object['user1']['username']
        gmail = json_object['user1']['gmail']

        onetimepassword.send_mail(gmail, range, name)
        clock.config(text='Send Successfully.', bg='#3ece48')

    def submit():
        otp = int(txt1.get())
        if otp == range:
            root.destroy()
            newpass()

        else:
            msg.showwarning('Error', message='You have enter wrong OTP.')

    root = tk.Tk()
    root.geometry("1280x720")
    root.resizable(True, False)
    root.title("Login Page")
    root.config(bg='#262523')

    frame1 = tk.Frame(root, bd=12, relief='groove', bg="#00aeff")
    frame1.place(relx=0.28, rely=0.12, relwidth=0.50, relheight=0.78)

    h1 = tk.Label(frame1, bd=8, relief='groove', text='OTP Verification', fg='black', bg="#3ece48", width=29, height=1,
                  font=('times', 25, ' bold '))
    h1.place(x=11, y=5)

    lb1 = tk.Label(frame1, text="Your OTP only send on your register gmail.", fg="black", bg="#00aeff",
                   font=('times', 17, ' bold '))
    lb1.place(x=130, y=105)

    gm = tk.Label(frame1, fg="black", bg="#00aeff", font=('times', 15, ' bold '))
    gm.place(x=130, y=145)

    try:
        with open('users.json', 'r') as file:
            json_object = json.load(file)

        gmail = json_object['user1']['gmail']
        gm.config(text=gmail, bg='#3ece48')

    except:
        pass

    lb2 = tk.Label(frame1, text='Enter OTP(4 digit) : ', fg="black", bg="#00aeff", font=('times', 17, ' bold '))
    lb2.place(x=220, y=290)

    txt1 = tk.Entry(frame1, bd=5, relief=SUNKEN, width=20, fg="black", font=('times new roman', 15, ' bold '))
    txt1.place(x=220, y=330)

    Button1 = tk.Button(frame1, text="Send", command=send, bd=5, relief="groove", fg="black", bg='red',
                        width=8, height=1, activebackground='yellow', font=('times', 14, ' bold '))
    Button1.place(x=130, y=200)

    clock = tk.Label(frame1, text='', fg="black", bg="#00aeff", width=20, height=1, font=('times', 16, ' bold '))
    clock.place(x=250, y=205)

    clearButton = tk.Button(frame1, text="Submit", command=submit, bd=5, relief="groove", fg="black", bg='red',
                            width=15, height=1, activebackground='white', font=('times', 15, ' bold '))
    clearButton.place(x=130, y=400)

    Button = tk.Button(frame1, text="Exit", command=login2, bd=5, relief="groove", fg="black", bg='red',
                       width=15, height=1, activebackground='white', font=('times', 15, ' bold '))
    Button.place(x=340, y=400)


def register():
    def signup():
        username = str(txt1.get())
        password = str(txt2.get())
        gmail = str(txt4.get())

        if username != '' and password != '' and gmail != '' and txt3.get() != '':
            data = {'user1': {'username': username, 'password': password, 'gmail': gmail}}

            with open('users.json', 'w') as file:
                json.dump(data, file)

            if password != txt3.get():
                msg.showwarning('Password not match', message='Your passwords are not identical.')
            else:
                sign.destroy()
                login()
        else:
            msg.showwarning('Error', message='Try to fill all entry to register.')

    sign = tk.Tk()
    sign.geometry("1280x720")
    sign.resizable(True, False)
    sign.title("Login Page")
    sign.config(bg='#262523')

    frame1 = tk.Frame(sign, bd=12, relief='groove', bg="#00aeff")
    frame1.place(relx=0.28, rely=0.12, relwidth=0.50, relheight=0.78)

    h1 = tk.Label(frame1, bd=8, relief='groove', text='Sign Up Page', fg='black', bg="#3ece48", width=29, height=1,
                  font=('times', 25, ' bold '))
    h1.place(x=11, y=5)

    lb1 = tk.Label(frame1, text="Enter Username", fg="black", bg="#00aeff", font=('times', 18, ' bold '))
    lb1.place(x=130, y=80)

    txt1 = tk.Entry(frame1, bd=5, relief=SUNKEN, width=40, fg="black", font=('times new roman', 15, ' bold '))
    txt1.place(x=130, y=120)

    lb2 = tk.Label(frame1, text="Enter Password", fg="black", bg="#00aeff", font=('times', 18, ' bold '))
    lb2.place(x=130, y=180)

    txt2 = tk.Entry(frame1, bd=5, relief=SUNKEN, width=40, fg="black", show='*', font=('times new roman', 15, ' bold '))
    txt2.place(x=130, y=220)

    lb3 = tk.Label(frame1, text="Re-Enter Password", fg="black", bg="#00aeff", font=('times', 18, ' bold '))
    lb3.place(x=130, y=270)

    txt3 = tk.Entry(frame1, bd=5, relief=SUNKEN, width=40, fg="black", show='*', font=('times new roman', 15, ' bold '))
    txt3.place(x=130, y=310)

    lb4 = tk.Label(frame1, text="Enter Gmail", fg="black", bg="#00aeff", font=('times', 18, ' bold '))
    lb4.place(x=130, y=360)

    txt4 = tk.Entry(frame1, bd=5, relief=SUNKEN, width=40, fg="black", font=('times new roman', 15, ' bold '))
    txt4.place(x=130, y=400)

    clearButton = tk.Button(frame1, text="Submit", command=signup, bd=5, relief="groove", fg="black", bg='#f44336',
                            width=15, height=1, activebackground='white', font=('times', 15, ' bold '))
    clearButton.place(x=130, y=460)


def get_otp():

    def login1():
        root.destroy()
        login()

    def send():
        with open('users.json', 'r') as file:
            json_object = json.load(file)

        name = json_object['user1']['username']
        gmail = json_object['user1']['gmail']

        onetimepassword.send_mail(gmail, range, name)
        clock.config(text='Send Successfully.', bg='#3ece48')

    def submit():
        otp = int(txt1.get())
        if otp == range:
            root.destroy()
            register()

        else:
            msg.showwarning('Error', message='You have enter wrong OTP.')

    root = tk.Tk()
    root.geometry("1280x720")
    root.resizable(True, False)
    root.title("Login Page")
    root.config(bg='#262523')

    frame1 = tk.Frame(root, bd=12, relief='groove', bg="#00aeff")
    frame1.place(relx=0.28, rely=0.12, relwidth=0.50, relheight=0.78)

    h1 = tk.Label(frame1, bd=8, relief='groove', text='OTP Verification', fg='black', bg="#3ece48", width=29, height=1,
                  font=('times', 25, ' bold '))
    h1.place(x=11, y=5)

    lb1 = tk.Label(frame1, text="Your OTP only send on your register gmail.", fg="black", bg="#00aeff",
                   font=('times', 17, ' bold '))
    lb1.place(x=130, y=105)

    gm = tk.Label(frame1, fg="black", bg="#00aeff", font=('times', 15, ' bold '))
    gm.place(x=130, y=145)

    with open('users.json', 'r') as file:
        json_object = json.load(file)

    gmail = json_object['user1']['gmail']
    gm.config(text=gmail, bg='#3ece48')

    lb2 = tk.Label(frame1, text='Enter OTP(4 digit) : ', fg="black", bg="#00aeff", font=('times', 17, ' bold '))
    lb2.place(x=220, y=290)

    txt1 = tk.Entry(frame1, bd=5, relief=SUNKEN, width=20, fg="black", font=('times new roman', 15, ' bold '))
    txt1.place(x=220, y=330)

    Button1 = tk.Button(frame1, text="Send", command=send, bd=5, relief="groove", fg="black", bg='red',
                        width=8, height=1, activebackground='yellow', font=('times', 14, ' bold '))
    Button1.place(x=130, y=200)

    clock = tk.Label(frame1, text='', fg="black", bg="#00aeff", width=20, height=1, font=('times', 16, ' bold '))
    clock.place(x=250, y=205)

    clearButton = tk.Button(frame1, text="Submit", command=submit, bd=5, relief="groove", fg="black", bg='red',
                            width=15, height=1, activebackground='white', font=('times', 15, ' bold '))
    clearButton.place(x=130, y=400)

    Button = tk.Button(frame1, text="Exit", command=login1, bd=5, relief="groove", fg="black", bg='red',
                       width=15, height=1, activebackground='white', font=('times', 15, ' bold '))
    Button.place(x=340, y=400)


def login():
    def reset():
        try:
            with open('users.json', 'r') as file:
                json_object = json.load(file)

            gmail = json_object['user1']['gmail']
            root.destroy()
            passReset()

        except:
            msg.showwarning("Error", message='No user registration till now')

    def sign():
        try:
            with open('users.json', 'r') as file:
                json_ob = json.load(file)

            if json_ob is not None:
                OTP = random.randint(1000, 9999)
                a = msg.askyesno("Conformation Message", message='Do want to new Registration?')
                if a:
                    root.destroy()
                    get_otp()

                else:
                    pass

            else:
                root.destroy()
                register()
        except:
            root.destroy()
            register()

    def nextPage():
        try:
            with open('users.json', 'r') as file:
                json_object = json.load(file)

            print(json_object['user1']['username'])
            if txt1.get() == json_object['user1']['username'] and txt2.get() == json_object['user1']['password']:
                root.destroy()
                main.secondPage()

            else:
                msg.showwarning('Security Issue', message='your username or password is incorrect')
                username = json_object['user1']['username']
                txt1.delete(0, 'end')
                txt1.insert(0, username)
                txt2.delete(0, 'end')
        except:
            msg.showwarning('error', message='Enter valid username or password')

    root = tk.Tk()
    root.geometry("1280x720")
    root.resizable(True, False)
    root.title("Login Page")
    root.config(bg='#262523')

    frame1 = tk.Frame(root, bd=12, relief='groove', bg="#00aeff")
    frame1.place(relx=0.28, rely=0.12, relwidth=0.50, relheight=0.78)

    h1 = tk.Label(frame1, bd=8, relief='groove', text='Login Page', fg='black', bg="#3ece48", width=29, height=1,
                  font=('times', 25, ' bold '))
    h1.place(x=11, y=5)

    bg = Image.open('logo.png')
    image = bg.resize((100, 100), Image.ANTIALIAS)
    bg = ImageTk.PhotoImage(image)
    my = Label(frame1, image=bg)
    my.place(x=260, y=80)

    lb1 = tk.Label(frame1, text="Enter Username", fg="black", bg="#00aeff", font=('times', 20, ' bold '))
    lb1.place(x=130, y=205)

    txt1 = tk.Entry(frame1, bd=5, relief=SUNKEN, width=40, fg="black", font=('times new roman', 15, ' bold '))
    txt1.place(x=130, y=250)

    try:
        with open('users.json', 'r') as file:
            json_object = json.load(file)

        username = json_object['user1']['username']
        txt1.delete(0, 'end')
        txt1.insert(0, username)

    except:
        pass

    lb2 = tk.Label(frame1, text="Enter Password", fg="black", bg="#00aeff", font=('times', 20, ' bold '))
    lb2.place(x=130, y=295)

    txt2 = tk.Entry(frame1, bd=5, relief=SUNKEN, width=40, fg="black", show='*', font=('times new roman', 15, ' bold '))
    txt2.place(x=130, y=340)

    clearButton = tk.Button(frame1, text="Login", command=nextPage, bd=5, relief="groove", fg="black", bg='red',
                            width=15, height=1, activebackground='white', font=('times', 15, ' bold '))
    clearButton.place(x=130, y=400)

    Button = tk.Button(frame1, text="Sign Up", command=sign, bd=5, relief="groove", fg="black", bg='red',
                       width=15, height=1, activebackground='white', font=('times', 15, ' bold '))
    Button.place(x=340, y=400)

    Button1 = tk.Button(frame1, text="Forgot Password", command=reset, bd=5, relief="groove", fg="black", bg='red',
                        width=15, height=1, activebackground='white', font=('times', 15, ' bold '))
    Button1.place(x=130, y=470)

    exit = tk.Button(frame1, text="Exit", command=root.destroy, bd=5, relief="groove", fg="black", bg='red',
                     width=15, height=1, activebackground='white', font=('times', 15, ' bold '))
    exit.place(x=340, y=470)

    root.mainloop()


login()

#################################################### END ###################################################################

################################# USED LIBRARY ######################################
import os
import tkinter as tk
from tkinter import *
import pandas as pd
from tkinter import messagebox as msz
import datetime
import time
import cv2
import csv

import face_recognition
import imutils
import database
import numpy as np
import pyttsx3


def secondPage():
    ################################ Check CSV ##########################################

    def check_csv(attendance):
        assure_path_exists("Attendance/")
        date = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y')
        col_names = ['Id', 'Name', 'Date', 'Time']
        exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")

        if exists:
            df = pd.read_csv("Attendance\Attendance_" + date + ".csv")
            print(df["Id"].values)
            print(int(attendance[0]) not in df['Id'].values)
            if int(attendance[0]) not in df['Id'].values:
                with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
                    writer = csv.writer(csvFile1)
                    writer.writerow(attendance)
                csvFile1.close()
            else:
                print("repeated entry")
        else:
            with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(col_names)
                writer.writerow(attendance)
            csvFile1.close()
        writeText()

    ################################ Get frame ##########################################

    def get_frame(fvs):
        check, frame = fvs.read()
        if frame is None:
            raise Exception('Frame not found')
        frame = cv2.flip(frame, 1)
        frame = imutils.resize(frame, width=600, height=600)
        return frame

    ################################ Take Image from webcam ###############################

    def captureImage():
        speak('your web cam is ready to take image.')
        check_haarcasecadefile()
        face_detect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        fvs = cv2.VideoCapture(0)
        time.sleep(2.0)

        TIME = 5
        t = time.time()
        while True:
            frame = get_frame(fvs)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = face_detect.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            curr = time.time() - t

            if curr < TIME:
                for x, y, w, h in face:
                    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            if curr > TIME:
                break
            cv2.putText(frame, str(int(TIME - curr) + 1), (250, 255), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4)
            cv2.imshow("Setup", frame)
            cv2.waitKey(1)

        cv2.destroyAllWindows()
        return frame

    ################################ Encoded Face ################################################

    def get_encoded_face():
        encoded = {}
        for dirpath, dname, fname in os.walk("./Images"):
            for f in fname:
                if f.endswith('.jpg') or f.endswith('.png'):
                    face = face_recognition.load_image_file("Images/" + f)
                    encoding = face_recognition.face_encodings(face)[0]
                    encoded[f.split('.')[0] + '.' + f.split('.')[1]] = encoding
        return encoded

    ################################ Classify Face ################################################

    def classify_face(image):
        faces = get_encoded_face()
        faces_encoded = list(faces.values())
        known_face_name = list(faces.keys())

        img = cv2.imread(image)
        face_location = face_recognition.face_locations(img)
        unknown_face_encoding = face_recognition.face_encodings(img, face_location)

        face_name = []
        face_id = []

        for face_encoding in unknown_face_encoding:
            name = "unknown"
            matches = face_recognition.compare_faces(faces_encoded, face_encoding)

            face_distance = face_recognition.face_distance(faces_encoded, face_encoding)
            best_match = np.argmin(face_distance)

            if matches[best_match]:
                name = known_face_name[best_match]

            face_name.append(name)

            for (top, right, bottom, left), name in zip(face_location, face_name):
                cv2.rectangle(img, (left - 20, top - 20), (right + 20, bottom + 20), (255, 0, 0), 2)
                cv2.rectangle(img, (left - 20, bottom - 15), (right + 20, bottom + 20), (255, 0, 0), cv2.FILLED)
                cv2.putText(img, name, (left - 20, bottom + 15), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

        while True:
            cv2.imshow("Detected face images", img)
            cv2.waitKey(3000)
            return face_name

    ################################ Face Detection ###############################################

    def faceRecognition():
        frame = captureImage()
        cv2.imwrite("check.jpg", frame)
        c_face = classify_face('check.jpg')
        cv2.destroyAllWindows()

        for i in c_face:
            Time = time.strftime('%H:%M:%S')
            check_csv([i.split('.')[1], i.split('.')[0], day + "-" + month + "-" + year, Time])

    ################################ Button Save Data ######################################

    def saveData():
        id = txt1.get()
        name = txt2.get()

        if id != '' and name != '':
            database.insert(id, name)
            print(database.view())
            message2.configure(text="Registered Successfully..", fg='black', bg='#3ece48')
            countId()
        else:
            msz.showwarning(title='Human Error', message='Please enter data ( Student roll no and name )')

    ################################ Button Take Image ##################################

    def takeImage():
        id = txt1.get()
        name = txt2.get()

        if id != '' and name != '':
            assure_path_exists("Images/")
            frame = captureImage()
            name = name.title()

            path = 'Images/' + name + '.' + str(id) + '.' + 'jpg'
            cv2.imwrite(path, frame)

            message1.configure(text="  Image Capture for ID : " + str(txt1.get()), fg='black', bg='#3ece48')
        else:
            msz.showwarning(title='Human Error', message='Please enter data ( Student roll no and name )')

    ################################ count ID ###########################################

    def countId():
        assure_path_exists("Images/")
        id = os.listdir("Images/")
        message.configure(text='Total Registrations till now  : ' + str(len(id)))

    ################################ check directories and create #######################

    def assure_path_exists(path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    ################################ CLOCK TIME #########################################

    def tick():
        time_string = time.strftime('%H:%M:%S')
        clock.config(text=time_string)
        clock.after(500, tick)

    ################################ Reset Massages #####################################

    def resetMassages():
        if txt1.get() == '' and txt2.get() == '':
            message1.configure(text="  (1) Take Images  ", bg="#f44336", fg="black")
            message2.configure(text="  (2) Save Profile  ", bg="#f44336", fg="black")
        else:
            print("Not null")

    ################################ Clear Entry ########################################
    def clear():
        txt1.delete(0, 'end')
        txt2.delete(0, 'end')
        resetMassages()

    ################################ HaarCaseCade File ##################################

    def check_haarcasecadefile():
        exists = os.path.isfile("haarcascade_frontalface_default.xml")
        if exists:
            pass
        else:
            msz._show(title='Some file missing', message='Please contact us for help...')
            window.destroy()

    ################################ DATE AND TIME ######################################

    def date():
        x = datetime.datetime.now()
        day = str(x.day)
        month = x.strftime("%b")
        year = str(x.year)
        return day, month, year

    day, month, year = date()

    ################################ write on textarea #################################

    def writeText():
        try:
            date = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y')
            df = pd.read_csv("Attendance\Attendance_" + date + ".csv")
            textarea.delete(1.0, 'end')
            textarea.insert(END, f'\n ====================================================')
            textarea.insert(END, f'\n Roll NO.\t    Name\t\t\tDate\t  Time')
            textarea.insert(END, f'\n ====================================================')

            for i in range(df.shape[0]):
                data = df.iloc[i]
                textarea.insert(END, f'\n{data[0]}\t    {data[1]}\t\t\t{data[2]}\t  {data[3]}')
        except:
            print("csv file not created")

    ################################ View registration #################################

    def viewRegistration():
        textarea.delete(1.0, 'end')
        textarea.insert(END, f'\n ====================================================')
        textarea.insert(END, f'\n Roll NO.\t    Name')
        textarea.insert(END, f'\n ====================================================')
        rows = database.view()
        for i in rows:
            textarea.insert(END, f'\n{i[0]}\t    {i[1]}')

    ################################ Speak Function ####################################

    def speak(text):
        engine.say(text)
        engine.runAndWait()

    def onIt(e):
        help.config(bg='yellow')

    def onIt1(e):
        help1.config(bg='yellow')

    def outIt(e):
        help.config(bg='#3ece48')

    def outIt1(e):
        help1.config(bg='#3ece48')

    def intro():
        speak("For new registration, first you have to take a picture, and then click save profile button.")

    def instruct():
        speak("For take attendance, click on yellow color take attendance button and you will able to see attendance on text area.")

    ################################ FRONT-END ##########################################

    # window1.destroy()

    engine = pyttsx3.init()
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[0].id)
    voiceRate = 160
    engine.setProperty('rate', voiceRate)

    window = tk.Tk()
    window.geometry("1280x720")
    window.resizable(True, False)
    window.title("ATTENDANCE SYSTEM")
    window.config(background='#262523')

    frame1 = tk.Frame(window, bd=12, relief='groove', bg="#00aeff")
    frame1.place(relx=0.10, rely=0.17, relwidth=0.39, relheight=0.80)

    frame2 = tk.Frame(window, bd=12, relief='groove', bg="#00aeff")
    frame2.place(relx=0.50, rely=0.17, relwidth=0.39, relheight=0.80)

    h1 = tk.Label(window, text="Face Recognition Based Attendance System", fg="white", bg="#262523", width=55, height=1,
                  font=('times', 29, ' bold '))
    h1.place(x=10, y=10)

    frame3 = tk.Frame(window, bg="#c4c6ce")
    frame3.place(relx=0.51, rely=0.09, relwidth=0.09, relheight=0.07)

    frame4 = tk.Frame(window, bg="#c4c6ce")
    frame4.place(relx=0.35, rely=0.09, relwidth=0.16, relheight=0.07)

    date = tk.Label(frame4, text=day + "-" + month + "-" + year + "  |  ", fg="orange", bg="#262523", width=55,
                    height=1,
                    font=('times', 22, ' bold '))
    date.pack(fill='both', expand=1)

    clock = tk.Label(frame3, fg="orange", bg="#262523", width=55, height=1, font=('times', 22, ' bold '))
    clock.pack(fill='both', expand=1)
    tick()

    head1 = tk.Label(frame2, width=28, bd=10, relief="groove", text="For New Registrations", fg="black", bg="#3ece48",
                     font=('times', 17, ' bold '))
    head1.grid(row=0, column=0, pady=3, padx=3)

    head2 = tk.Label(frame1, width=28, bd=10, relief="groove", text="For Already Registered", fg="black", bg="#3ece48",
                     font=('times', 17, ' bold '))
    head2.grid(row=0, column=0, pady=3, padx=3)

    help = tk.Button(frame2, text='?', command=intro, activebackground='red', bg="#3ece48", width=3, bd=10,
                     relief="groove", fg='black',
                     font=('times', 12, ' bold '))
    help.place(x=420, y=2)
    help.bind('<Enter>', func=onIt)
    help.bind('<Leave>', func=outIt)

    help1 = tk.Button(frame1, text='?', command=instruct, activebackground='red', bg="#3ece48", width=3, bd=10,
                     relief="groove", fg='black',
                     font=('times', 12, ' bold '))
    help1.place(x=420, y=2)
    help1.bind('<Enter>', func=onIt1)
    help1.bind('<Leave>', func=outIt1)

    lb1 = tk.Label(frame2, text="Enter Roll Number", fg="black", bg="#00aeff", font=('times', 17, ' bold '))
    lb1.place(x=25, y=65)

    txt1 = tk.Entry(frame2, bd=5, relief=SUNKEN, width=40, fg="black", font=('times new roman', 15, ' bold '))
    txt1.place(x=30, y=100)

    clearButton = tk.Button(frame2, text="Clear", command=clear, bd=5, relief="groove", fg="black", bg='red',
                            width=16, height=1, activebackground='white', font=('times', 15, ' bold '))
    clearButton.place(x=28, y=420)

    roll = tk.Button(frame2, text="Roll List", command=viewRegistration, bd=5, relief="groove", fg="black",
                     bg='red',
                     width=16, height=1, activebackground='white', font=('times', 15, ' bold '))
    roll.place(x=240, y=420)

    lbl2 = tk.Label(frame2, text="Enter Name", fg="black", bg="#00aeff", font=('times', 17, ' bold '))
    lbl2.place(x=25, y=140)

    txt2 = tk.Entry(frame2, width=40, bd=5, relief=SUNKEN, fg="black", font=('times', 15, ' bold '))
    txt2.place(x=30, y=173)

    message1 = tk.Label(frame2, bd=5, relief='groove', text="  (1) Take Images  ", bg="#f44336", width=32, fg="black",
                        height=1,
                        activebackground="yellow", font=('times', 15, ' bold '))
    message1.place(x=35, y=237)

    message2 = tk.Label(frame2, bd=5, relief='groove', text="  (2) Save Profile  ", bg="#f44336", width=32, fg="black",
                        height=1,
                        activebackground="yellow", font=('times', 15, ' bold '))
    message2.place(x=35, y=266)

    takeImg = tk.Button(frame2, text='Take Images', command=takeImage, bd=5, relief='groove', fg="white", bg="blue",
                        width=16, height=1, activebackground="white", font=('times', 16, ' bold '))
    takeImg.place(x=28, y=340)

    trainImg = tk.Button(frame2, text="Save Profile", command=saveData, fg='white', bd=5, relief="groove", bg='blue',
                         width=16, height=1, activebackground='white', font=('times', 16, ' bold '))
    trainImg.place(x=240, y=340)

    message = tk.Label(frame2, text='', bg='#00aeff', width=35, fg='black', height=1,
                       activebackground='yellow', font=('times', 16, ' bold '))
    message.place(x=7, y=490)
    countId()

    trackImage = tk.Button(frame1, text='Take Attendance', command=faceRecognition, bd=5, relief='groove', fg='black',
                           bg='yellow', width=37, height=1, activebackground='white', font=('times', 16, ' bold'))
    trackImage.place(x=8, y=60)

    ################################## Screen to show attendance #####################################

    screen = LabelFrame(frame1, bd=5, relief=GROOVE)
    screen.place(x=5, y=125, width=465, height=360)
    bill_title = Label(screen, text='Attendance', font='arial 15 bold', bd=7, relief=GROOVE).pack(fill=X)
    scrol_y = Scrollbar(screen, orient=VERTICAL)
    textarea = Text(screen, yscrollcommand=scrol_y.set)
    scrol_y.pack(side=RIGHT, fill=Y)
    scrol_y.config(command=textarea.yview)
    textarea.pack(fill=BOTH, expand=1)

    ############################################## Quit Button ######################################

    quitWindow = tk.Button(frame1, text='Exit', command=window.destroy, bd=6, relief='groove', fg='black', bg='red',
                           width=37, height=1, activebackground='white', font=('times', 16, 'bold'))
    quitWindow.place(x=8, y=500)

    # speak("Hello, This is a program to take, attendance using face recognition.")

    writeText()

    ############################################ MAin loop ##########################################

    window.mainloop()

    ########################################### End ################################################

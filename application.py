import numpy as np
import pandas as pd
import cv2
import datetime 
import time
import tkinter as tk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
from tkinter import ttk
import os
from PIL import Image
import csv

global key
key = ''

#Время
ts = time.time()
#Дата
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

#Словраь с месяцами года
mont={'01':'Январь',
      '02':'Февраль',
      '03':'Март',
      '04':'Апрель',
      '05':'Мая',
      '06':'Июнь',
      '07':'Июль',
      '08':'Август',
      '09':'Сентябрь',
      '10':'Октябрь',
      '11':'Ноябрь',
      '12':'Декабрь'
      }

#Главное окно приложения и его свойства
app_window = tk.Tk()
app_window.geometry("1920x1080")
app_window.title("Система контроля посещаемости")
app_window.configure(background="peru")

#Функция для проверки наличия XML-файла обученного классификатора
def checking_haarcascade_file():
    if os.path.isfile("haarcascade_frontalface_default.xml"):
        pass
    else:
        mess._show(title="XML-файл обученного классификатора не найден",message="Добавьте обученный классификатор")
        app_window.destroy()

#Проверка наличий существующего пути к директории
def file_path_exists(path):
    dir = os.path.dirname(path)
    if os.path.exists(dir) == False:
        os.makedirs(dir)

#Функция для получения изображений и их названий
def get_images_and_labels(path):
    image_paths = [os.path.join(path,f) for f in os.listdir(path)]
    faces = []
    ids = []
    for i in image_paths:
        pil_image = Image.open(i).convert('L')
        image_array = np.array(pil_image,'uint8')
        face_id = int(os.path.split(i)[-1].split(".")[1])
        faces.append(image_array)
        ids.append(face_id)
    return faces, ids

#Функция, реализующая обучение
def training():
    checking_haarcascade_file()
    file_path_exists('Training_image_label/')
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    haar_cascade_file = 'haarcascade_frontalface_default.xml'
    face_detector = cv2.CascadeClassifier(haar_cascade_file)
    faces,ids = get_images_and_labels('Training_image')

    try:
        recognizer.train(faces,np.array(ids))
    except:
        mess._show(title='Пользователь не зарегистрирован!', message="Зарегистрируйте пользователя")
        return
    
    recognizer.save("Training_image_label/trainer.yml")
    result = "Профиль студента успешно сохранен"
    message1.configure(text=result)
    message.configure(text='Общее количество регистраций: ' + str(ids[0]))

#Функция, создающая набор данных студента
def make_student_dataset():
    checking_haarcascade_file()
    columns = ['Number',' ','ID',' ', 'Name']
    file_path_exists("Student_details/")
    file_path_exists("Training_image/")
    number = 0
    if os.path.isfile("Student_details\Student_details.csv"):

        with open("Student_details\Student_details.csv", 'r') as csv_file1:
            reader1 = csv.reader(csv_file1)
            for i in reader1:
                number += 1
        number = (number // 2)
        csv_file1.close()
    else:
        with open("Student_details\Student_details.csv", 'a+') as csv_file1:
            writer = csv.writer(csv_file1)
            writer.writerow(columns)
            number = 1
        csv_file1.close()
    Id = (txt.get())
    name = (txt2.get())

    if ((name.isalpha()) or (' ' in name)):
        camera = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        while (True):
            ret, img = camera.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                cv2.imwrite("Training_image\ " + name + "." + str(number) + "." + Id + '.' + str(sampleNum) + ".jpg",
                             gray[y:y + h, x:x + w])
                cv2.imshow('Taking Images', img)

            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 100:
                break
        camera.release()
        cv2.destroyAllWindows()
        result = "Сделан набор данных для ID : " + Id
        row = [number, '', Id, '', name]
        with open('Student_details\Student_details.csv', 'a+') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(row)
        csv_file.close()
        message1.configure(text=result)

    else:
        if (name.isalpha() == False):
            result = "Введите имя корректно"
            message.configure(text=result)

#Функция, отвечающая за время
def tick():
    time_str = time.strftime('%H:%M:%S')
    clock.config(text=time_str)
    clock.after(200,tick)

#Функция очистки формы
def clear():
    txt.delete(0, 'end')
    result = "1)Сделайте набор данных студента ---> 2)Сохраните профиль"
    message1.configure(text=result)

#Функция очистки формы
def clear2():
    txt2.delete(0, 'end')
    res = "1)Сделайте набор данных студента ---> 2)Сохраните профиль"
    message1.configure(text=res)

#Функция, реализующая распознавание
def recognition():
    checking_haarcascade_file()
    file_path_exists("Attendance/")
    file_path_exists("Student_details/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("Training_image_label/trainer.yml")
    if exists3:
        recognizer.read("Training_image_label/trainer.yml")
    else:
        mess._show(title='Нет соответствующих данных', message='Добавьте профиль студентов')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    camera = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("Student_details/Student_details.csv")
    if exists1:
        df = pd.read_csv("Student_details/Student_details.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        camera.release()
        cv2.destroyAllWindows()
        app_window.destroy()
    while True:
        ret, im = camera.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['Number'] == serial]['Name'].values
                ID = df.loc[df['Number'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    camera.release()
    cv2.destroyAllWindows()

#Функция сохранения пароля
def save_password():
    file_path_exists('Training_image_label/')
    if os.path.isfile("Training_image_label\passwordd.txt"):
        tf = open("Training_image_label\password.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Пароль не найден', 'Придумайте новый пароль', show='*')
        if new_pas == None:
            mess._show(title='Пароль не введен', message='Пароль не введен, попробуйте снова')
        else:
            tf = open("Training_image_label\password.txt", "w")
            tf.write(new_pas)
            mess._show(title='Пароль зарегистрирован', message='Новый пароль был успешно зарегистрирован')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("Training_image_label\password.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Ошибка', message='Подтвердите новый пароль снова')
            return
    else:
        mess._show(title='Неверный пароль', message='Введите корректно пароль')
        return
    mess._show(title='Пароль был изменен', message='Пароль был успешно изменен')
    master.destroy()

#Функция смены пароля
def change_password():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Изменение пароля")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Старый пароль',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   Новый пароль', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Новый пароль', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Отмена", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Сохранить", command=save_password, fg="black", bg="#3ece48", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

def psw():
    file_path_exists("Training_image_label/")
    exists1 = os.path.isfile("Training_image_label\password.txt")
    if exists1:
        tf = open("Training_image_label\password.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Старый пароль не найден', 'Создайте пароль администратора', show='*')
        if new_pas == None:
            mess._show(title='Пароль не был введен', message='Пароль не введен! Попробуйте снова')
        else:
            tf = open("Training_image_label\password.txt", "w")
            tf.write(new_pas)
            mess._show(title='Пароль зарегистрирован', message='Новый пароль был успешно зарегистрирован')
            return
    password = tsd.askstring('Пароль', 'Введите пароль', show='*')
    if (password == key):
        training()
    elif (password == None):
        pass
    else:
        mess._show(title='Неправильный пароль', message='Был введен неверный пароль')

frame1 = tk.Frame(app_window, bg="tan")
frame1.place(relx=0.6, rely=0.17, relwidth=0.38, relheight=0.80)

frame2 = tk.Frame(app_window, bg="tan")
frame2.place(relx=0.02, rely=0.17, relwidth=0.39, relheight=0.80)

message3 = tk.Label(app_window, text="Система контроля посещаемости" ,fg="white",bg="saddlebrown" ,width=80 ,height=1,font=('times', 29, ' bold '))
message3.place(x=-80, y=0)

frame3 = tk.Frame(app_window, bg="#F0FFFF")
frame3.place(relx=0.80, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(app_window, bg="#c4c6ce")
frame4.place(relx=0.64, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year+"  |  ", fg="black",bg="peru" ,width=55 ,height=1,font=('Arial', 22, ' bold '))
datef.pack(fill='both',expand=1)

clock = tk.Label(frame3,fg="black",bg="peru" ,width=55 ,height=1,font=('Arial', 22, ' bold '))
clock.pack(fill='both',expand=1)
tick()

head2 = tk.Label(frame2, text="                       Для новых регистраций студентов                       ", fg="white",bg="saddlebrown" ,font=('times', 17, ' bold ') )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                       Для зарегистрированных студентов                       ", fg="white",bg="saddlebrown" ,font=('times', 17, ' bold ') )
head1.place(x=0,y=0)

lbl = tk.Label(frame2, text="Введите ID",width=20  ,height=1  ,fg="black"  ,bg="tan" ,font=('times', 17, ' bold ') )
lbl.place(x=50, y=55)

txt = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold '))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="Введите имя и фамилию",width=20  ,fg="black"  ,bg="tan" ,font=('times', 17, ' bold '))
lbl2.place(x=50, y=140)

txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold ')  )
txt2.place(x=30, y=173)

message1 = tk.Label(frame2, text="Сделайте набор данных, затем сохраните профиль" ,bg="tan" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="" ,bg="tan" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
message.place(x=7, y=550)

lbl3 = tk.Label(frame1, text="Присутствующие студенты",width=20  ,fg="black"  ,bg="tan"  ,height=1 ,font=('times', 17, ' bold '))
lbl3.place(x=100, y=115)

res=0
exists = os.path.isfile("Student_details\Student_details.csv")
if exists:
    with open("Student_details\Student_details.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Зарегистрированных студентов  : '+ str(res))

menubar = tk.Menu(app_window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='Сменить пароль', command = change_password)
filemenu.add_command(label='Выход',command = app_window.destroy)
menubar.add_cascade(label='Help',font=('times', 29, ' bold '),menu=filemenu)

tv= ttk.Treeview(frame1,height =17,columns = ('name','date','time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(40,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='Имя и фамилия')
tv.heading('date',text ='Дата')
tv.heading('time',text ='Время')

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

clearButton = tk.Button(frame2, text="Очистить", command=clear  ,fg="white"  ,bg="saddlebrown"  ,width=11 ,activebackground = "white" ,font=('times', 11, ' bold '))
clearButton.place(x=400, y=86)
clearButton2 = tk.Button(frame2, text="Очистить", command=clear2  ,fg="white"  ,bg="saddlebrown"  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton2.place(x=400, y=172)    
takeImg = tk.Button(frame2, text="Сделать набор данных", command=make_student_dataset  ,fg="white"  ,bg="saddlebrown"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
takeImg.place(x=60, y=400)
trainImg = tk.Button(frame2, text="Сохранить профиль", command=psw ,fg="white"  ,bg="saddlebrown"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trainImg.place(x=60, y=480)
trackImg = tk.Button(frame1, text="Отметить студентов на занятии", command=recognition  ,fg="white"  ,bg="saddlebrown"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trackImg.place(x=40,y=50)
quitWindow = tk.Button(frame1, text="Выход", command=app_window.destroy  ,fg="white"  ,bg="saddlebrown"  ,width=15 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=330, y=555)

app_window.configure(menu=menubar)
app_window.mainloop()
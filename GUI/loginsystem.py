from tkinter import *
from tkmacosx import *
from tkinter import ttk

from PIL import ImageTk

from tkinter import messagebox

import pymysql


class Login:

    def __init__(self, root):
        self.root = root
        self.username = None
        self.img = None
        self.password = None
        self.entrySlots = None
        self.infoLabel = Label()

        self.root.title("Smart Medicine Dispenser Login System")

        self.root.geometry("1200x700+50+0")

        self.root.resizable(False, False)

        self.img = ImageTk.PhotoImage(file="Logins/mainframe.jpg")

        self.login_page()


    def clear_info_label(self):
        if len(self.infoLabel.place_info()):
            self.infoLabel.place_forget()

    def set_info_label(self, frame, text, x, y, fg='red', bg='white'):
        self.infoLabel = Label(frame, text=text, font=('optima', 14), fg=fg,
                           bg=bg)
        self.infoLabel.place(x=x, y=y)

    def login_page(self):
        loginFrame = Frame(self.root, bg="white")
        loginFrame.place(x=0, y=0, height=700, width=1200)

        img = Label(loginFrame, image=self.img).place(x=0, y=0, width=1200, height=700)

        self.entrySlots = Frame(loginFrame, bg='white')
        self.entrySlots.place(x=680, y=130, height=450, width=420)
        title = Label(self.entrySlots, text="SMART MEDICINE DISPENSER", font=('impact', 32, 'bold'), fg='black',
                      bg='white')
        title.place(x=35, y=20)

        slot1 = Label(self.entrySlots, text="Username/Email", font=('optima', 24, 'bold'), fg='orangered', bg='white')
        slot1.place(x=55, y=110)

        slot2 = Label(self.entrySlots, text="Password", font=('optima', 24, 'bold'), fg='orangered', bg='white')
        slot2.place(x=55, y=210)

        self.username = Entry(self.entrySlots, font=('times new roman', 15, 'bold'), bg='lightgray')
        self.username.place(x=55, y=145, width=300, height=35)

        self.password = Entry(self.entrySlots, font=('times new roman', 15, 'bold'), bg='lightgray')
        self.password.place(x=55, y=245, width=300, height=35)

        loginButton = Button(self.entrySlots, command=self.login, text="LOGIN HERE", fg="black", bg="#ff884d",
                             width=250, height=50, font=('times new roman', 24, 'bold'))
        loginButton.place(x=80, y=320)

        # loginBtn = Button(entrySlots, text="LOGIN", cursor="hand2", font=("times new roman", 20), fg="white", bg="orangered",
        #               bd=0, width=15, height=1)
        # loginBtn.place(x=90, y=400)

        forgetBtn = Button(self.entrySlots, text="Forgotten password?", font=('calibri', 12), cursor="hand2",
                           bg='white', fg='black', borderwidth=3)
        forgetBtn.place(x=211, y=280)

        # Label(self.entrySlots, text="Don't have an account?", font=('calibri', 12), fg='black', bg='white').place(x=120,y=380)
        registerBtn = Button(self.entrySlots, command=self.register_page, text="Don't have an account? Sign Up",
                             font=('calibri', 15), cursor="hand2", bg='white', fg='black', borderwidth=3)
        registerBtn.place(x=70, y=370)

    def login(self):
        if self.username.get() == "" or self.password.get() == "":
            self.set_info_label(self.entrySlots,"Empty username or password!",x=55, y=90)
        else:
            try:
                conn = pymysql.connect(host='localhost', user='root', password='1228', database='pythongui')
                cur = conn.cursor()
                cur.execute('select * from register where username=%s and password=%s',
                            (self.username.get(), self.password.get()))
                row = cur.fetchone()
                if row == None:
                    self.clear_info_label()
                    self.set_info_label(self.entrySlots,"Wrong username or password!",x=55, y=90)
                    self.login_entry_clear()
                else:
                    self.enter_system()
                    conn.close()
            except Exception as e:
                errorLabel = Label(self.entrySlots, text="Error, {}".format(str(e)), font=('optima', 14), fg='red',
                                   bg='white')
                errorLabel.place(x=55, y=90)


    def register_page(self):
        self.register_frame = Frame(self.root, bg="white")
        self.register_frame.place(x=0, y=0, height=700, width=1200)
        Label(self.register_frame, image=self.img).place(x=0, y=0, width=1200, height=700)
        self.reg_entrys = Frame(self.register_frame, bg='white')
        self.reg_entrys.place(x=600, y=130, height=450, width=560)

        title = Label(self.reg_entrys, text="SIGN UP", font=('impact', 32, 'bold'), fg='black',
                      bg='white')
        title.place(x=35, y=20)

        slot1 = Label(self.reg_entrys, text="Username", font=('optima', 24, 'bold'), fg='orangered', bg='white')
        slot1.place(x=35, y=110)

        slot2 = Label(self.reg_entrys, text="Password", font=('optima', 24, 'bold'), fg='orangered', bg='white')
        slot2.place(x=35, y=210)

        slot3 = Label(self.reg_entrys, text="Email", font=('optima', 24, 'bold'), fg='orangered', bg='white')
        slot3.place(x=300, y=110)

        slot4 = Label(self.reg_entrys, text="Confirm Password", font=('optima', 24, 'bold'), fg='orangered', bg='white')
        slot4.place(x=300, y=210)

        self.signUsername = Entry(self.reg_entrys, font=('times new roman', 15, 'bold'), bg='lightgray')
        self.signUsername.place(x=35, y=145, width=230, height=35)

        self.signPassword = Entry(self.reg_entrys, font=('times new roman', 15, 'bold'), bg='lightgray')
        self.signPassword.place(x=35, y=245, width=230, height=35)

        self.signEmail = Entry(self.reg_entrys, font=('times new roman', 15, 'bold'), bg='lightgray')
        self.signEmail.place(x=300, y=145, width=230, height=35)

        self.cfPassword = Entry(self.reg_entrys, font=('times new roman', 15, 'bold'), bg='lightgray')
        self.cfPassword.place(x=300, y=245, width=230, height=35)

        signupButton = Button(self.reg_entrys, command=self.register, text="SIGN UP", fg="white", bg="#3399ff",
                              width=380,
                              height=30)
        signupButton.place(x=80, y=320)
        haveActBtn = Button(self.reg_entrys, command=self.login_page, text="Already have an account? Sign in",
                             font=('calibri', 15), cursor="hand2", bg='white', fg='black', borderwidth=3)
        haveActBtn.place(x=140, y=370)

    def register(self):
        if self.signUsername.get() == "" or self.signEmail.get() == "" or self.signPassword.get() == "" or self.cfPassword.get() == "":
            self.set_info_label(self.reg_entrys,"Empty fields!",x=35, y=90)
        elif self.signPassword.get() != self.cfPassword.get():
            self.clear_info_label()
            self.set_info_label(self.reg_entrys, "Password and confirm password does not match!", x=35, y=90)
        else:
            try:
                conn = pymysql.connect(host="localhost", user="root", password="1228", database="pythongui")
                cur = conn.cursor()
                cur.execute("select * from register where email=%s", self.signEmail.get())
                row = cur.fetchone()
                if row != None:
                    self.clear_info_label()
                    self.set_info_label(self.reg_entrys, "This email is already used!", x=35, y=90)
                    self.register_entry_clear()
                else:
                    cur.execute("insert into register values(%s,%s,%s,%s)",
                                (self.signUsername.get(), self.signEmail.get(), self.signPassword.get(),
                                 self.cfPassword.get()))
                    conn.commit()
                    conn.close()
                    self.clear_info_label()
                    self.set_info_label(self.reg_entrys, "Signed up successfully!", x=35, y=90,fg='#00b359')
                    self.register_entry_clear()
            except Exception as e:
                errorLabel = Label(self.reg_entrys, text="Error, {}".format(str(e)), font=('optima', 14), fg='red',
                                   bg='white')
                errorLabel.place(x=35, y=90)

    def login_entry_clear(self):
        self.username.delete(0, END)
        self.password.delete(0, END)

    def register_entry_clear(self):
        self.signUsername.delete(0, END)
        self.signPassword.delete(0, END)
        self.signEmail.delete(0, END)
        self.cfPassword.delete(0, END)

    def enter_system(self):
        sysMainFrame = Frame(root, bg="#e6ffff")
        sysMainFrame.place(x=0, y=0, height=700, width=1200)
        title = Label(sysMainFrame, text="Welcome to Smart Medicine Dispenser System",
                      font=('times new roman', 48, 'bold'),
                      fg="black", bg="#e6ffff")
        title.place(x=130, y=100)
        logoutBtn = Button(sysMainFrame, command=self.login_page, text="Sign out", font=('calibri', 14), cursor="hand2",
                           bg='grey', fg='white', borderwidth=3)
        logoutBtn.place(x=1105, y=0)


root = Tk()

ob = Login(root)

root.mainloop()

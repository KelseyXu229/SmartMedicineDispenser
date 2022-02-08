from tkinter import *
from tkmacosx import *
from tkinter import ttk

from PIL import ImageTk

import sqlite3
from sqlite3 import Error

#############################################################################################################################
# Note: 1. Please install all of the relevant packages first
#       2. login.db is only used in login process, it is independent to any other parts,
#          please feel free to use your own methods to set up the database of your parts.
#
# Login system of Smart medicine dispenser For MAC
# This part implements the login functionalities for doctors and patients
# 1. This program can establish a local login.db database automatically for storing the user accounts, emails and passwords.
#    -login.db includes two tables: patients and doctors.
#       (Since doctors can be patients, patients can be doctors...They may use the same email to register in our system...)
#       -Table 'patients' has fields: username, email, password
#       -Table 'doctors' has fields: username, email, password
# 2. The main frame background image is stored in img directory
# 3. Login page has slots:
#        - Role: doctor or patient
#        - Username/Email: email is the unique ID of each user account, username can be duplicated
#        - Password: Casual password, I'll add regex to filter qualified passwords and emails in next sprint
# 4. Login logic:
#        - All the slots should be filled
#        - Can switch to signup page
#        - If you are a patient:
#           - Both Email and password can be found in patients table
#        - If you are a doctor:
#           - Both Email and password can be found in doctors table
#        - Errors can handled:
#                - Any slot is not filled
#                - Email and password does not match
#                - Not registered
# 5. Register logic:
#        - Can switch to signup page
#        - All the slots should be filled
#        - Password and confirm password should match
#        - If you are a patient:
#           - Username, email and password should be stored in patients table
#        - If you are a doctor:
#           - Username, email and password should be stored in doctors table
#        - Errors can handled:
#                - Any slot is not filled
#                - Password and confirm password do not match
#                - Email has already used
#
#############################################################################################################################
HEADER = 32


def create_connection():
    connection = None
    try:
        conn = sqlite3.connect(r"login.db")
        conn.text_factory = str
        # conn.execute("DROP TABLE IF EXISTS patients;")
        conn.execute("CREATE TABLE IF NOT EXISTS patients(username text,  email text, password text);")
        # conn.execute("DROP TABLE IF EXISTS doctors;")
        conn.execute("CREATE TABLE IF NOT EXISTS doctors(username text, email text, password text);")
        conn.commit()
        return conn
    except Error as e:
        print("Error occurred: " + str(e))


class Login:

    def __init__(self, root):
        self.root = root
        self.username = None
        self.img = None
        self.password = None
        self.entrySlots = None
        self.infoLabel = Label()
        self.role = None
        self.registerRole = None
        self.conn = None

        self.root.title("Smart Medicine Dispenser Login System")

        self.root.geometry("1200x700+50+0")

        self.root.resizable(False, False)

        self.img = ImageTk.PhotoImage(file="img/mainframe.jpg")

        self.login_page()

    def clear_info_label(self):
        if len(self.infoLabel.place_info()):
            self.infoLabel.place_forget()

    def set_info_label(self, frame, text, x, y, fg='red', bg='white'):
        self.infoLabel = Label(frame, text=text, font=('optima', 14), fg=fg,
                               bg=bg)
        self.infoLabel.place(x=x, y=y)


    def login_page(self):
        """
        Frames:
        self.root -> loginFrame -> self.entrySlots
        Create a login page, including:
        1. Create a slot to choose you are a patient or a doctor.
        2. Create a username entry
        3. Create a password entry
        4. Create a Forgotten password button
        5. Create a Login Here button
        6. Create a sign up button
        :return:
        """
        loginFrame = Frame(self.root, bg="white")
        loginFrame.place(x=0, y=0, height=700, width=1200)

        img = Label(loginFrame, image=self.img).place(x=0, y=0, width=1200, height=700)

        self.entrySlots = Frame(loginFrame, bg='white')
        self.entrySlots.place(x=680, y=130, height=450, width=420)
        title = Label(self.entrySlots, text="LOGIN HERE", font=('impact', HEADER, 'bold'), fg='black',
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
                             width=250, height=50, font=('times new roman', 20, 'bold'))
        loginButton.place(x=80, y=320)

        self.role = ttk.Combobox(self.entrySlots, width="5", values=("Doctor", "Patient"), background='white')
        self.role.place(x=280, y=80)

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
        """
        Implement the login functionalities.
        1. Check there is any empty slots.

        :return:
        """

        if self.username.get() == "" or self.password.get() == "":
            self.clear_info_label()
            self.set_info_label(self.entrySlots, "Empty username or password!", x=55, y=90)
        elif self.role.get() == "":
            self.clear_info_label()
            self.set_info_label(self.entrySlots, "Choose your role!", x=55, y=90)
        else:
            try:
                print(1)
                self.conn = create_connection()
                cur = self.conn.cursor()
                if self.role.get() == "Doctor":
                    cur.execute('select * from doctors where email=? and password=?',
                                (self.username.get(), self.password.get()))
                    row = cur.fetchone()
                    if row is None:
                        self.clear_info_label()
                        self.set_info_label(self.entrySlots, "Wrong username or password!", x=55, y=90)
                        self.login_entry_clear()
                    else:
                        self.enter_doctor_system()
                else:
                    cur.execute('select * from patients where email=? and password=?',
                                (self.username.get(), self.password.get()))
                    row = cur.fetchone()
                    if row is None:
                        self.clear_info_label()
                        self.set_info_label(self.entrySlots, "Wrong username or password!", x=55, y=90)
                        self.login_entry_clear()
                    else:
                        self.enter_patient_system()
                self.conn.close()
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

        Label(self.reg_entrys, text="You're a ", font=('optima', 22, 'bold'), fg='orangered', bg='white').place(x=300,
                                                                                                                y=70)
        self.registerRole = ttk.Combobox(self.reg_entrys, width="12", values=("Doctor", "Patient"), background='white')
        self.registerRole.place(x=395, y=75)

        signupButton = Button(self.reg_entrys, command=self.register, text="SIGN UP", fg="white", bg="#3399ff",
                              width=380,
                              height=30)
        signupButton.place(x=80, y=320)
        haveActBtn = Button(self.reg_entrys, command=self.login_page, text="Already have an account? Sign in",
                            font=('calibri', 15), cursor="hand2", bg='white', fg='black', borderwidth=3)
        haveActBtn.place(x=140, y=370)

    def register(self):
        if self.signUsername.get() == "" or self.signEmail.get() == "" or self.signPassword.get() == "" or self.cfPassword.get() == "":
            self.set_info_label(self.reg_entrys, "Empty fields!", x=35, y=90)
        elif self.signPassword.get() != self.cfPassword.get():
            self.clear_info_label()
            self.set_info_label(self.reg_entrys, "Passwords does not match!", x=35, y=90)
        elif self.registerRole.get() == "":
            self.set_info_label(self.reg_entrys, "Choose a role!", x=35, y=90)
        else:
            try:
                self.conn = create_connection()
                cur = self.conn.cursor()
                if self.registerRole.get() == "Doctor":
                    cur.execute("select * from doctors where email=?", (self.signEmail.get(),))
                    row = cur.fetchone()
                    if row is not None:
                        self.clear_info_label()
                        self.set_info_label(self.reg_entrys, "This email is already used!", x=35, y=90)
                        self.register_entry_clear()
                    else:
                        cur.execute("insert into doctors values(?,?,?)",
                                    (self.signUsername.get(), self.signEmail.get(), self.signPassword.get()))
                        self.conn.commit()
                        self.clear_info_label()
                        self.set_info_label(self.reg_entrys, "A doctor Signed up successfully!", x=35, y=90,
                                            fg='#00b359')
                        self.register_entry_clear()
                else:
                    cur.execute("select * from patients where email=?", (self.signEmail.get(),))
                    row = cur.fetchone()
                    if row is not None:
                        self.clear_info_label()
                        self.set_info_label(self.reg_entrys, "This email is already used!", x=35, y=90)
                        self.register_entry_clear()
                    else:
                        cur.execute("insert into patients values(?,?,?)",
                                    (self.signUsername.get(), self.signEmail.get(), self.signPassword.get()))
                        self.conn.commit()
                        self.clear_info_label()
                        self.set_info_label(self.reg_entrys, "A patient Signed up successfully!", x=35, y=90,
                                            fg='#00b359')
                        self.register_entry_clear()
                self.conn.close()
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

    ################################################
    # Doctor system part: Need to be modified by Kriti and Mahsa
    ################################################
    def enter_doctor_system(self):
        # Kriti and Mahsa should complete other pages start from here
        sysMainFrame = Frame(root, bg="#e6ffff")
        sysMainFrame.place(x=0, y=0, height=700, width=1200)
        title = Label(sysMainFrame, text="Welcome to Smart Medicine Dispenser Doctor System",
                      font=('times new roman', 48, 'bold'),
                      fg="black", bg="#e6ffff")
        title.place(x=130, y=100)
        logoutBtn = Button(sysMainFrame, command=self.login_page, text="Sign out", font=('calibri', 14), cursor="hand2",
                           bg='grey', fg='white', borderwidth=3)
        logoutBtn.place(x=1105, y=0)

    ################################################
    # Patient system part: Need to be modified by Kriti and Mahsa
    ################################################
    def enter_patient_system(self):
        # Kriti and Mahsa should complete other pages start from here
        sysMainFrame = Frame(root, bg="#e6ffff")
        sysMainFrame.place(x=0, y=0, height=700, width=1200)
        title = Label(sysMainFrame, text="Welcome to Smart Medicine Dispenser Patient System",
                      font=('times new roman', 48, 'bold'),
                      fg="black", bg="#e6ffff")
        title.place(x=130, y=100)
        logoutBtn = Button(sysMainFrame, command=self.login_page, text="Sign out", font=('calibri', 14), cursor="hand2",
                           bg='grey', fg='white', borderwidth=3)
        logoutBtn.place(x=1105, y=0)


root = Tk()

ob = Login(root)

root.mainloop()

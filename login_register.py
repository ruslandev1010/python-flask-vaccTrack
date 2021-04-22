from tkinter import *
from functools import partial

def validateLogin(Username, Password, Email):
    print("Enter Username:", Username.get())
    print("Enter Password:", Password.get())
    print("Enter Email Address:", Email.get())
    return

#for the window

tkwindow = TK()
tkwindow.geometry('200x150')
tkwindow.title('VaccTrack APP')

#the username label annd text entry box
usernameLabel = Label(tkwindow, text="User name").grid(row=0, column=0)
username = StringVar()
usernameEntry = Entry(tkwindow, textvariable=Username).grid(row=0, column=1)

#the password label and password entry box
passwordLabel = Label(tkwindow, text="Password").grid(row=1, column=0)
password = StringVar()
passwordEntry = Entry(tkwindow, textvariable = Password, show= '*').grid(row=1, column=1)

#the email label and email entry box
emailLabel = Label(tkwindow, text="Email").grid(row=0, column=0)
email = StringVar()
emailEntry = Entry(tkwindow, textvariable= Email).grid(row=0, column=0)

validateLogin = partial(validateLogin, Username, Password, Email)

#login button
loginButton = Button(tkwindow, text="Login", command=validateLogin).grid(row=4, column=0)

tkwindow.mainloop()
#coding:utf-8

from os import name
from tkinter import *
from tkinter import messagebox
import sqlite3
from sqlite3 import Connection
import database as db

def bookAdd():
    winAdd = Toplevel()
    xLeft = int(winAdd.winfo_screenwidth()//2 - 300)
    yTop = int(winAdd.winfo_screenheight()//2 - 500)
    winAdd.geometry(f"+{xLeft}+{yTop}")
    winAdd.resizable(False, False)
    winAdd.iconbitmap("D:\Etudes\Ecole\TFE\TFE_Biblio\Code\Blacky-Book2\Blacky-Book\BookSeel.ico")
    winAdd.title("Add-Book")

    frameAdd = LabelFrame(winAdd)
    frameAdd2 = Frame(winAdd)

    labelName = Label(frameAdd, text = "Nom: ")
    entryName = Entry(frameAdd, width= 30, textvariable= nameBook)
    labelAuthor = Label(frameAdd, text="Auteur: ")
    entryAuthor = Entry(frameAdd, width=30, textvariable=authorBook)
    buttonAdd = Button(frameAdd2, text="Ajouter", command= lambda: createbook())
    buttonQuitAdd = Button(frameAdd2, text="Quitter", command= lambda: quitWin(winAdd))

    frameAdd.pack(padx=50, pady=(25,15))
    frameAdd2.pack(padx=50, pady=(25,15))

    labelName.grid(padx=25)
    entryName.grid(row=0, column=1)
    labelAuthor.grid(row=1)
    entryAuthor.grid(row=1, column=1)
    buttonAdd.grid(padx=25)
    buttonQuitAdd.grid(row=0, column=1)

    def createbook():
        books = {"id": -1, "name": entryName.get(), "author": entryAuthor.get()}
        db.createBook(c, books)
        populateBooks()
        win.update()
        winAdd.destroy()
        messagebox.showinfo("Succès","Votre livre à bien été ajouté. Merci pour votre participation")


def deleteBook():
    id = lbBooks.curselection() [0]+1
    db.deleteBook(c, id)
    populateBooks()
    messagebox.showwarning("Attention","Votre livre à bien été supprimer! ?\nSi en cas d'erreur, vous pouvez toujours ajouter votre livre via la boutton \"Ajouter\"")
   

def searchBook():
    searchName = search.get()
    if searchName != "":
        books = db.searchBook(c, name)
        if searchName == books["name"]:
            nameBook.set(books["name"])
            authorBook.set(books["author"])
        else:
            messagebox.showinfo("Oups","Nous n'avons pas trouver votre livre :(")

def lbClick(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0] + 1
        reader = db.read(c, index)
        mail.set(reader["mail"])
        pwd.set("")

def lbClickBook(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0] + 1
        books = db.readBook(c, index)
        nameBook.set(books["name"])
        authorBook.set(books["author"])
       
def connectUser():
    readerMail = mail.get()
    readerPwd = pwd.get()
    if readerMail != "" and readerPwd != "":
        id = getID(readerMail)
        if id >= 0:
            reader = db.getReader(c, id)
            if readerPwd == reader["pwd"]:
                winCon.destroy()
                entrySearch.config(state="normal")
                buttonSearch.config(state="normal")
                win.update()
            else:
                labelStatus.config(text="Mot de passe incorrect", fg="RED")
                winCon.update()
        else:
            labelStatus.config(text="L'utilisateur n'existe pas", fg="RED")
            winCon.update()


def getID(mail):
    tmp = db.getAllReaders(c)
    for reader in tmp:
        if mail == reader["mail"]:
            return reader["rowid"]
    return -1

def getidBook(name):
    tmp = db.getAllBooks(c)
    for book in tmp:
        if name == book["name"]:
            return book["rowid"]
    return -1

def newuser():
    winNewUser = Toplevel()
    winNewUser.attributes("-topmost", True)

    firs_name = StringVar()
    last_name = StringVar()
    dateOfBirth = StringVar()
    mail = StringVar()
    pwd = StringVar()
    validPwd = StringVar()

    xLeft = int(win.winfo_screenwidth()//2 - 500)
    yTop = int(win.winfo_screenheight()//2 - 500)
    winNewUser.geometry(f"1000x800+{xLeft}+{yTop}")
    winNewUser.resizable(False, False)
    winNewUser.title("Nouvelle utilisateur")
    winNewUser.iconbitmap("D:\Etudes\Ecole\TFE\TFE_Biblio\Code\Blacky-Book2\Blacky-Book\BookSeel.ico")
    frameNewUser = LabelFrame(winNewUser,text="Remplissez les champs pour vous connecter",padx=25, pady=25)

    frameNewUser2=Frame(winNewUser)

    labelFirstName = Label(frameNewUser,text="Prénom: ")
    entryFirstName = Entry(frameNewUser,width=30, textvariable=firs_name)
    labelLastName= Label(frameNewUser,text="Nom: ")
    entryLastName= Entry(frameNewUser, width=30, textvariable=last_name)
    labelDateOfBirth=Label(frameNewUser,text="Date de naissance: ")
    entryDateOfBirth=Entry(frameNewUser, width=30, textvariable=dateOfBirth)
    labelMail = Label(frameNewUser,text="Mail: ")
    entryMail = Entry(frameNewUser, width=30, textvariable=mail)
    labelPwdUser = Label(frameNewUser, text="Mot de passe: ")
    entryPwdUSer = Entry(frameNewUser, width=30, textvariable=pwd, show='*')
    labelValidPwd = Label(frameNewUser,text="Confirmer le mot de passe: ")
    entryValidPwd = Entry(frameNewUser, width=30, textvariable=validPwd, show='*')
    labelStatuePwd = Label(frameNewUser, text="", fg="RED")

    buttonNewUser = Button(frameNewUser2, text="Nouveau", command= lambda: validUser())
    buttonQuit = Button(frameNewUser2, text="Quitter",command= lambda: quitWin(winNewUser))

    frameNewUser.pack(padx=50, pady=(25,15))
    frameNewUser2.pack(pady=(0, 15))

    labelFirstName.grid(padx=25)
    entryFirstName.grid(row=0, column=1, pady=10)
    labelLastName.grid(row=1, pady=10)
    entryLastName.grid(row=1, column=1, pady=10)
    labelDateOfBirth.grid(row=2, pady=10)
    entryDateOfBirth.grid(row=2, column=1 , pady=10)
    labelMail.grid(row=3, pady=10)
    entryMail.grid(row=3, column=1 ,pady=10)
    labelPwdUser.grid(row=4, pady=10)
    entryPwdUSer.grid(row=4, column=1, pady=10)
    labelValidPwd.grid(row=5, pady=10)
    entryValidPwd.grid(row=5, column=1, pady=10)
    labelStatuePwd.grid(row=6, column=0, columnspan = 2)

    buttonNewUser.grid(row=6, pady=10, padx=50)
    buttonQuit.grid(row=6, column=2, pady=10,padx=50)

    def validUser():
        """Création d'un contact dans la base de donnée"""

        if entryPwdUSer.get() == entryValidPwd.get():
            readers = {"id": -1, "first_name": entryFirstName.get(), "last_name": entryLastName.get(), "birthday": entryDateOfBirth.get(), "mail": entryMail.get(), 
                        "pwd": entryPwdUSer.get()}
            db.createReader(c, readers)
            populate()
            winNewUser.destroy()
        else:
            labelStatuePwd.config(text="Mot de passe incorrect\nVérifier si ils sont identique",fg="RED")
            winNewUser.update()
               
db_path = "data.db"

# MAIN WINDOW ===============================================================

win = Tk()

nameBook = StringVar()
authorBook = StringVar()
search = StringVar()

frameBooks = LabelFrame(win, text="Recherche", padx=25, pady=25)
frameBooks2 = LabelFrame(win, text= "Livres")
frameBooks3 = Frame(win)

entrySearch = Entry(frameBooks, width = 30, textvariable = search, state="disabled")
buttonSearch = Button(frameBooks, text="Chercher", state="disabled", command=searchBook)
buttonAdd = Button(frameBooks, text="Ajouter", command=bookAdd)
buttonDelete = Button(frameBooks, text="Supprimer", command=deleteBook)

labelNameBook = Label(frameBooks2, text="Nom: ")
entryNameBook = Entry(frameBooks2, width=30, textvariable=nameBook, state="disabled")
labelNameAuthor = Label(frameBooks2, text="Auteur: ")
entryNameAuthor = Entry(frameBooks2, width=30, textvariable=authorBook, state="disabled")
lbBooks = Listbox(frameBooks2)
lbLoan = Listbox(frameBooks2)

labelNameBook.grid(row=0, column=1, pady=10)
entryNameBook.grid(row=0, column=2)
labelNameAuthor.grid(row=1, column=1, pady=10)
entryNameAuthor.grid(row=1, column=2)
lbBooks.grid(row=0, column=3, rowspan=3, columnspan=2)
lbBooks.bind("<<ListboxSelect>>", lbClickBook)
lbLoan.grid(row=0, column=6, rowspan=3)
lbLoan.insert(0, ' Vos emprunt:')

frameBooks.pack(padx=50, pady=15)
frameBooks2.pack(padx=15, pady=5)
frameBooks3.pack()

entrySearch.grid()
buttonSearch.grid(row=0, column=1)
buttonAdd.grid(row=0, column=2)
buttonDelete.grid(row=0, column=3)

buttonLoan = Button(frameBooks3, text= "Emprunter")
buttonBringBack = Button(frameBooks3, text="Rendre")
buttonQuitBooks = Button(frameBooks3, text="Quitter", command= lambda: quitWin(win))

buttonLoan.grid()
buttonBringBack.grid(row=0, column=1, padx=50)
buttonQuitBooks.grid(row=0, column=2)


# CONNECTION WINDOW =========================================================

winCon = Toplevel()

mail = StringVar()
pwd = StringVar()

xLeft = int(win.winfo_screenwidth()//2 - 500)
yTop = int(win.winfo_screenheight()//2 - 500)
win.geometry(f"720x360+{xLeft}+{yTop}")
win.resizable(False, False)
win.iconbitmap("D:\Etudes\Ecole\TFE\TFE_Biblio\Code\Blacky-Book2\Blacky-Book\BookSeel.ico")
win.title("Blacky Books")

xLeft = int(winCon.winfo_screenwidth()//2 - 300)
yTop = int(winCon.winfo_screenheight()//2 - 500)
winCon.geometry(f"+{xLeft}+{yTop}")
winCon.resizable(False, False)
winCon.title("Connexion")
winCon.iconbitmap("D:\Etudes\Ecole\TFE\TFE_Biblio\Code\Blacky-Book2\Blacky-Book\BookSeel.ico")
frameCon = LabelFrame(winCon, text="Connectez-vous", padx=25, pady=25)

frameCon2 = Frame(winCon)

labelMail = Label(frameCon, text="Mail :")
entryMail = Entry(frameCon, width=30, textvariable = mail)
labelPwd = Label(frameCon, text="Mot de passe :")
entryPwd = Entry(frameCon, width=30, textvariable=pwd,show='*')
buttonConnect = Button(frameCon, text="Connecter", command=connectUser)
labelStatus = Label(frameCon, text="", fg="RED")

buttonNewUser = Button(frameCon2, text="Nouvel utilisateur",command=newuser)
buttonQuitCon = Button(frameCon2, text="Quitter", command=lambda: quitWin(win))

lbReaders = Listbox(frameCon)
"""
for i in readers:
    lbReaders.insert(END, f"{i[1]} {i[2]}")
"""
frameCon.pack(padx=50, pady=(25, 15))
frameCon2.pack(pady=(0, 15))

labelMail.grid(pady=10)
entryMail.grid(row=0, column=1, pady=10)
labelPwd.grid(row=1, pady=10)
entryPwd.grid(row=1, column=1, pady=10)
buttonConnect.grid(row=2, column=1, pady=10)
labelStatus.grid(row=3, column=0, columnspan=2)

lbReaders.grid(row=0, column=2, rowspan=3, padx=(25, 0))
lbReaders.bind("<<ListboxSelect>>", lbClick)

buttonNewUser.grid(pady=10, padx=(0, 40))
buttonQuitCon.grid(row=0, column=1, pady=10)

def populate():
    lbReaders.delete(0, END)

    for i in db.getAllReaders(c):
        lbReaders.insert(i["rowid"], f"{i['first_name']} {i['last_name']}")

def populateBooks():
    lbBooks.delete(0, END)

    for i in db.getAllBooks(c):
        lbBooks.insert(i["rowid"],f"{i['name']}")

def quitWin(window):
    window.destroy()


if __name__ == '__main__':
    c = db.load(db_path)
    populate()
    populateBooks()
    winCon.attributes("-topmost", True) 
    win.mainloop()

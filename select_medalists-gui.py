import sqlite3
from tkinter import *

""" Classes """

class MainWindow:
    def __init__(self, parent):
        self.parent = parent
        # Set up the main GUI window
        self.parent.geometry("450x450")
        self.parent.title("Olympic Medalists")
        self.parent.columnconfigure(0,weight=1)
        self.parent.rowconfigure(1,weight=1)
        
        menubar = MainMenu(self.parent)
        content = MainFrame(self.parent,"frame1")

class MainMenu:
    def __init__(self, parent):
        self.parent = parent
        # create a menu bar
        self.toolbar = Frame(self.parent ,bg="#006494", padx=10, pady=5)
        self.toolbar.grid(row=0, column=0, sticky=E+W)
        
        # The menu buttons
        self.btn_all = Button(self.toolbar, text = "All", command = select_all)
        self.btn_all.grid(row=0, column=0, padx=10)

        self.btn_medal = Button(self.toolbar, text = "Medal", command = select_medal)
        self.btn_medal.grid(row=0, column=1, padx=10)

        self.btn_medalist = Button(self.toolbar, text = "Medalist", command = add_medalist)
        self.btn_medalist.grid(row=0, column=2, padx=10)

class MainFrame:
    def __init__(self, parent, FrameID):
        self.parent = parent
        self.id = FrameID

        self.frame_main = Frame(self.parent ,bg="#ffcc00", padx=10, pady=5)
        self.frame_main.grid(row=1, column=0, sticky=N+E+W+S)

        medalists = select_all()
        for i,row in enumerate(medalists):
            rowID =  int(i)
            Label(self.frame_main, text=row[0],bg="#ffcc00", anchor="w").grid(row=rowID, column=0, padx=10, sticky=E+W)
            Label(self.frame_main, text=row[1],bg="#ffcc00", anchor="w").grid(row=rowID, column=1, padx=10, sticky=E+W)
            Label(self.frame_main, text=row[2],bg="#ffcc00", anchor="w").grid(row=rowID, column=2, padx=10, sticky=E+W)
            Label(self.frame_main, text=row[3],bg="#ffcc00", anchor="w").grid(row=rowID, column=3, padx=10, sticky=E+W)


        self.frame_add = Frame(self.parent, bg="#006494", padx=10, pady=5)
        self.frame_add.grid(row=2, column=0, sticky=E+W)
        
        entry_add = Entry(self.frame_add)
        entry_add.grid(row=0,column=0)

        self.btn_medal = Button(self.frame_add, text = "Medal", command = select_medal)
        self.btn_medal.grid(row=0, column=1, padx=10)



""" Functions """

def select_all():
    frame = "f1"
    with sqlite3.connect("medals.db") as db:
        cursor = db.cursor()
        cursor.execute("select Medal,FirstName,LastName,Event from Medalists")
        medalists = cursor.fetchall()
        print(medalists)
        return medalists

def select_medal():
    medaltype = entry_add.get()
    with sqlite3.connect("medals.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT Medal,FirstName,LastName,Event FROM Medalists WHERE Medal='{0}'".format(medaltype))
        medalists = cursor.fetchall()
        return medalists

def add_medalist():
    NewFirstName = input("Please enter the First Name: ")
    NewLastName = input("Please enter the Last Name: ")
    NewMedal = input("Please enter the medal awarded: ")
    NewEvent = input("Please enter the Event: ")

    newrecord = (NewMedal, NewFirstName, NewLastName, NewEvent)

    with sqlite3.connect("medals.db") as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Medalists(Medal,FirstName,LastName,Event) VALUES (?,?,?,?)",newrecord)
        db.commit()

def menu():
    print("\nWhat would you like to see? ")
    print("1. All medalists")
    print("2. Show medalists by medal")
    print("3. Add a new medalist")
    choice = input("Please enter your choice (1,2 or 3) ")
    if choice == "1":
        medalists = select_all()
        for row in medalists:
            print("{0:8} {1:6} {2:10} {3}".format(row[0], row[1], row[2], row[3]))
    elif choice == "2":
        medaltype = input("Which medal type do you want?")
        medalists = select_medal(medaltype)
        for row in medalists:
            print("{0:8} {1:6} {2:10} {3}".format(row[0], row[1], row[2], row[3]))
    elif choice =="3":
        add_medalist()
    else:
        print("Please choose a valid option")
    menu()

def main():
    root = Tk()
    app = MainWindow(root)
    

main()


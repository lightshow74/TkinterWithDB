import sqlite3
from tkinter import *

""" Classes """

class MainWindow:
    def __init__(self, parent):
        self.parent = parent
        # Set up the main GUI window
        self.parent.geometry("450x450")
        self.parent.title("Olympic Medalists")
        menubar = MainMenu(self.parent)
        fr_selectall = MainFrame(self.parent,"frameAll")
        fr_selectmedal = MainFrame(self.parent,"frameMedal")

class MainMenu:
    def __init__(self, parent):
        self.parent = parent
        # create a menu bar
        self.toolbar = Frame(self.parent ,bg="#006494", padx=10, pady=5)
        self.toolbar.pack(fill="x")
        
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
        self.frame_main.pack(fill="both", expand=1)

        medalists = select_all()

        for i,row in enumerate(medalists):
            rowID =  int(i)
            Label(self.frame_main, text=row[0],bg="#ffcc00", anchor="w").grid(row=rowID, column=0, padx=10, sticky=E+W)
            Label(self.frame_main, text=row[1],bg="#ffcc00", anchor="w").grid(row=rowID, column=1, padx=10, sticky=E+W)
            Label(self.frame_main, text=row[2],bg="#ffcc00", anchor="w").grid(row=rowID, column=2, padx=10, sticky=E+W)
            Label(self.frame_main, text=row[3],bg="#ffcc00", anchor="w").grid(row=rowID, column=3, padx=10, sticky=E+W)

        """
        # create a frame for content frames to sit inside
        self.id = Frame(self.parent, bg="#ffcc00", padx=10, pady=10)
        self.id.pack(fill="both", expand = 1)

        f1 = Frame("main",bg="#ffbbcc").pack(fill="both", expand = 1)
        #content_intro = ContentFrame(self.id, "intro")
        
"""
"""class ContentFrame:
    def __init__(self, parent, FrameID):
        self.parent = parent
        self.id = FrameID
        #self.content = content
        
        # create a frame for the forms
        self.id = Frame(self.parent, bg="#ffbbcc")
        self.id.grid(row=1, column=0, sticky='news')

"""



""" Functions """

def select_all():
    with sqlite3.connect("medals.db") as db:
        cursor = db.cursor()
        cursor.execute("select Medal,FirstName,LastName,Event from Medalists")
        medalists = cursor.fetchall()
        print(medalists)
        return medalists

def select_medal(medal):
    medaltype=medal
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

def raise_frame(frame):
    frame.tkraise()

def main():
    root = Tk()
    app = MainWindow(root)

    root.mainloop()


main()


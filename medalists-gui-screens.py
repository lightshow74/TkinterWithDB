import sqlite3
from tkinter import *

""" Classes """

class MenuBtn:
    def __init__(self, parent,text,command,row,col):
        self.parent = parent
        self.text = text
        self.command = command
        self.row = row
        self.col = col
        
        Button(self.parent, text = self.text, command = self.command).grid(row=self.row, column=self.col, padx=10)
        

class MainWindow:
    def __init__(self, parent):
        self.parent = parent
        # Set up the main GUI window
        self.parent.geometry("450x450")
        self.parent.title("Olympic Medalists")
        self.parent.columnconfigure(0,weight=1)
        self.parent.rowconfigure(1,weight=1)
        
        # Main Menu Bar
        toolbar = Frame(self.parent ,bg="#006494", padx=10, pady=5)
        toolbar.grid(row=0, column=0, sticky=E+W)
        
        # The menu buttons
        btn_all = MenuBtn(toolbar,"All",lambda: self.show_frame(f1),0,0)
        btn_medal = MenuBtn(toolbar,"Medal",lambda: self.show_frame(f2),0,1)
        btn_medalist = MenuBtn(toolbar,"Medalist",lambda: self.show_frame(f3),0,2)


        # Main Content Area
        frame_main = Frame(self.parent ,bg="#ffcc00", padx=10, pady=5)
        frame_main.grid(row=1, column=0, sticky=N+E+W+S)

        # Content Frames

        f1 = Frame(frame_main, bg="#ffcc00", padx=0, pady=5)
        f2 = Frame(frame_main, bg="#ffcc00", padx=0, pady=5)
        f3 = Frame(frame_main, bg="#ffcc00", padx=0, pady=5)

        for frame in (f1, f2, f3):
            frame.grid(row=1, column=0, sticky=N+E+W+S)

        # Frame 1 - Select All
        medalists = select_all()
        for i,row in enumerate(medalists):
            rowID =  int(i)
            Label(f1, text=row[0],bg="#ffcc00", anchor="w").grid(row=rowID, column=0, padx=10, sticky=E+W)
            Label(f1, text=row[1],bg="#ffcc00", anchor="w").grid(row=rowID, column=1, padx=10, sticky=E+W)
            Label(f1, text=row[2],bg="#ffcc00", anchor="w").grid(row=rowID, column=2, padx=10, sticky=E+W)
            Label(f1, text=row[3],bg="#ffcc00", anchor="w").grid(row=rowID, column=3, padx=10, sticky=E+W)

        # Frame 2 - Select Medal

        f2_form = Frame(f2, bg="#ffcc00", padx=0, pady=0)
        f2_form.grid(row=0, column=0, sticky=W)
        f2_results = Frame(f2, bg="#ffcc00", padx=0, pady=0)
        f2_results.grid(row=0, column=1, sticky=N+E+W+S)

        variable = StringVar(f2_form)
        variable.set("Gold") # default value

        def medaltype(medal):
            select_medal_results = select_medal(variable.get())
            print(variable.get())
            for i,row in enumerate(select_medal_results):
                rowID =  int(i)
                Label(f2_results, text=row[0],bg="#ffcc00", anchor="w").grid(row=rowID, column=0, padx=10, sticky=E+W)
                Label(f2_results, text=row[1],bg="#ffcc00", anchor="w").grid(row=rowID, column=1, padx=10, sticky=E+W)
                Label(f2_results, text=row[2],bg="#ffcc00", anchor="w").grid(row=rowID, column=2, padx=10, sticky=E+W)
                Label(f2_results, text=row[3],bg="#ffcc00", anchor="w").grid(row=rowID, column=3, padx=10, sticky=E+W)
       
        o = OptionMenu(f2_form, variable, "Gold", "Silver", "Bronze", command=medaltype).pack()

        # Frame 3 - Add Medal

        Label(f3, text="First Name", bg="#ffcc00", anchor="w").grid(row=0, column=0,sticky=E+W)
        Label(f3, text="Last Name", bg="#ffcc00", anchor="w").grid(row=1, column=0,sticky=E+W)
        Label(f3, text="Medal", bg="#ffcc00", anchor="w").grid(row=2, column=0,sticky=E+W)
        Label(f3, text="Event", bg="#ffcc00", anchor="w").grid(row=3, column=0,sticky=E+W)
        
        NewFirstName = Entry(f3).grid(row=0,column=1)
        NewLastName = Entry(f3).grid(row=1,column=1)
        NewMedal = Entry(f3).grid(row=2,column=1)
        NewEvent = Entry(f3).grid(row=3,column=1)

        def Add_Medal_Var():
            firstname = NewFirstName.get()
            lastname = NewLastName.get()
            event = NewEvent.get()
            medal = NewMedal.get()
            add_medalist(medal,firstname,lastname,event)

        Button(f3, text = "Add Medalist", command = Add_Medal_Var).grid(row=4, column=1, padx=10)

        self.show_frame(f1)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = page_name
        frame.tkraise()




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
        medal = cursor.fetchall()
        return medal

def add_medalist(medal,firstname,lastname,event):
    NewFirstName = firstname
    NewLastName = lastname
    NewMedal = medal
    NewEvent = event

    newrecord = (NewMedal, NewFirstName, NewLastName, NewEvent)
    print(newrecord)
"""
    with sqlite3.connect("medals.db") as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Medalists(Medal,FirstName,LastName,Event) VALUES (?,?,?,?)",newrecord)
        db.commit()
"""
        

def main():
    root = Tk()
    app = MainWindow(root) 

    root.mainloop()

main()



"""


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

    f1 = Frame(root, bg="#ffcc00", padx=10, pady=5)
    f2 = Frame(root, bg="#ffcc00")
    f3 = Frame(root, bg="#ffcc00")
    f4 = Frame(root, bg="#ffcc00")

    for frame in (f1, f2, f3, f4):
        frame.grid(row=1, column=0, sticky=N+E+W+S)

    f1.tkraise()
    
    medalists = select_all()
    for i,row in enumerate(medalists):
        rowID =  int(i)
        Label(f1, text=row[0],bg="#ffcc00", anchor="w").grid(row=rowID, column=0, padx=10, sticky=E+W)
        Label(f1, text=row[1],bg="#ffcc00", anchor="w").grid(row=rowID, column=1, padx=10, sticky=E+W)
        Label(f1, text=row[2],bg="#ffcc00", anchor="w").grid(row=rowID, column=2, padx=10, sticky=E+W)
        Label(f1, text=row[3],bg="#ffcc00", anchor="w").grid(row=rowID, column=3, padx=10, sticky=E+W)



main()
"""

from tkinter import Tk, Button, Label, Scrollbar, Listbox, StringVar, Entry, W,E,N,S, END
from tkinter import ttk
from tkinter import messagebox

from mysql_config import dbConfig
import mysql.connector as pyo 

conn = pyo.connect(**dbConfig)
print(conn) 

class Bookdb:
    def __init__(self):
        self.con = pyo.connect(**dbConfig)
        self.cursor = self.con.cursor()
        print("You have established a connection ...")
        print(self.con)

    def __del__(self):
        self.con.close()

    def view(self):
        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()
        return rows
    
    def insert(self,title,author,isbn):
        sql=("INSERT INTO books (title,author,isbn) VALUES (%s,%s,%s)") 
        values = [ title,author,isbn]
        self.cursor.execute(sql,values)
        self.con.commit()
        messagebox.showinfo(title="Book Database", message="New book added to the Book Table of mybooks DATABASE")
   
    def update(self,id, title,author,isbn):
        update_sql=("UPDATE books SET title=%s, author=%s, isbn =%s WHERE id =%s")
        self.cursor.execute(update_sql, [title, author, isbn, id ])
        self.con.commit()
        messagebox.showinfo(title="mybooks Database", message="Book table updated")
   
    def delete(self,id ):
        delete_sql=("DELETE from books where id =%s")
        self.cursor.execute(delete_sql,[id])
        self.con.commit()
        messagebox.showinfo(title="mybooks Database", message=" row deleted ")


def get_selected_row(event):
	global selected_tuple 
	index = list_box.curselection()[0]
	selected_tuple = list_box.get(index)
	title_entry.delete(0,'end') # clears the input after inserting
	title_entry.insert('end', selected_tuple[1])
	author_entry.delete(0,'end')
	author_entry.insert('end',selected_tuple[2])
	isbn_entry.delete(0, 'end')
	isbn_entry.insert('end',selected_tuple[3])    

db = Bookdb()  #  Bookdb is the class created to access 

def view_records():
    list_box.delete(0,'end')
    for row in db.view():
        list_box.insert('end',row) 

def add_book():
    db.insert(title_text.get(), author_text.get(), isbn_text.get() )
    list_box.delete(0, 'end')
    list_box.insert ('end',(title_text.get(), author_text.get(), isbn_text.get()))
    title_entry.delete(0, 'end')
    author_entry.delete(0, 'end')
    isbn_entry.delete(0,'end')
    conn.commit()

def delete_records():
    db.delete(selected_tuple[0])
    conn.commit() 


def clear_screen():
    list_box.delete(0,'end')
    title_entry.delete(0,'end')
    author_entry.delete(0,'end')
    isbn_entry.delete(0,'end')

def update_records():
    db.update(selected_tuple[0], title_text.get(), author_text.get(), isbn_text.get())
    title_entry.delete(0,'end')
    author_entry.delete(0,'end')
    isbn_entry.delete(0,'end')

    
def on_closing():
    dd=db
    if messagebox.askokcancel("Quit","Do you want to quit?"):
        root.destroy()
        del dd



#====================================GUI========================================

root=Tk() 

#  ---- Window creation for bookapp ----
root.title("My Books Database Application")
root.configure(background="#101010") # -- 101010 is blackish grey colour
root.geometry("900x550") #  -- Geometry() to set the dimensions of the tkinter application window. 
root.resizable(False,False) # -- making width, height unchangable 

#  ---- Creating Labels, Entry boxes, List box, Scroll bar and Buttons ----

# -- 1)Title --
title_label = ttk.Label(root, text="Title",background="#101010", foreground ="#66FFB2" , font=("TkDefaultFont",16))
title_label.place(x=185,y=27)

title_text= StringVar()
title_entry= ttk.Entry(root, width=20, textvariable=title_text)
title_entry.place(x=55,y=30)

# -- 2)Author --
author_label = ttk.Label(root, text="Author",background="#101010", foreground ="#66FFB2" ,font=("TkDefaultFont",16))
author_label.place(x=405,y=27)

author_text= StringVar()
author_entry= ttk.Entry(root, width=20, textvariable=author_text)
author_entry.place(x=275,y=30)

# -- 3)ISBN --
isbn_label = ttk.Label(root, text="ISBN",background="#101010", foreground ="#66FFB2" , font=("TkDefaultFont",16))
isbn_label.place(x=640,y=27)

isbn_text= StringVar()
isbn_entry= ttk.Entry(root, width=20, textvariable=isbn_text)
isbn_entry.place(x=510,y=30)

# -- 4)Add Button --
add_btn = Button(root, text="  Add Book  ",border=4, borderwidth=6,  bg="#0000CC",fg="white",font="system 12", command=add_book)
add_btn.place(x=740,y=25) 

# -- 5)List box --
list_box = Listbox(root, height=16, width=66, bd = 5, relief= 'solid', font="helvetica 13", bg="#99FFCC")
list_box.place(x=50, y=110) 
list_box.bind('<<ListboxSelect>>',get_selected_row)

# -- 6)Scroll bar --
scroll_bar = Scrollbar(root)
scroll_bar.place(x=655,y=250)

# -- Cofiguring list box and scrollbar --
list_box.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_box.yview)

# -- 7)View button --
viewButton = Button(root, text="View All Records", border=4, borderwidth=6, bg='#FF0000', fg='white', font='System 12', command=view_records)
viewButton.place(x=725,y=135)

# -- 8)Modify button --
modifyButton = Button(root, text="  Modify Record  ",border=4, borderwidth=6,  bg='#999900', fg='white', font='system 12', command=update_records)
modifyButton.place(x=725,y=195)

# -- 9)Delete button --
deleteButton = Button(root, text="  Delete Record  ",border=4, borderwidth=6,  bg='#006633', fg='white', font='system 12', command=delete_records)
deleteButton.place(x=725,y=255)

# -- 10)Clear screen button --
clearButton = Button(root, text="   Clear Screen   ", border=4, borderwidth=6, bg='#0046D1', fg='white', font='system 12', command=clear_screen)
clearButton.place(x=725,y=315)

# -- 11)Exit button --
exitButton = Button(root, text=" Exit Application ", border=4, borderwidth=6, bg='#4C0099', fg='white', font='system 12', command=on_closing)
exitButton.place(x=725,y=375)



root.mainloop() 
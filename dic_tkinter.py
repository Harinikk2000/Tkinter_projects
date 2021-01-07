"""
VIEW DICTIONARY
ADD WORD AND MEANING
UPDATE WORD AND MEANING
DELETE WORD FROM RECORD
CLEAR THE ENTRY
EXIT
"""



"""
--
-- Database: `dictionary`
--

-- --------------------------------------------------------

--
-- Table structure for table `english`
--

CREATE TABLE `english` (
  `sno` int(11) NOT NULL,
  `word` varchar(25) NOT NULL,
  `definition` varchar(100) NOT NULL DEFAULT ''
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `english`
--

INSERT INTO `english` (`sno`, `word`, `definition`) VALUES
(1, 'table', 'to keep things'),
(2, 'rose', 'a flower in garden'),
(3, 'apple', 'a fruit'),
(4, 'head', 'a part of body'),
(5, 'pen', 'a tool to write'),
(6, 'bottle', 'to hold a quantity of water or liquid'),
(7, 'note', 'to note things'),
(8, 'pencil', 'to write something'),
(9, 'cold', 'to feel cool and freezed'),
(10, 'eraser', 'to eraser the writen things'),
(11, 'window', 'for the purpose of air and light'),
(12, 'water', 'to provide energy');
"""


from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image
from tkinter import messagebox
import pyttsx3


root=Tk()
import mysql.connector


root.title("Dictionary")
root.geometry("1366x768+0+0")  #resolution of ur screen
root.config(bg="#90EE90")
root.state("zoomed") #to get screen in full screen

leftFrame=Frame(root,bg="#87CEEB")   #for radiobuttons
leftFrame.pack(side=TOP,fill=X)

bottomFrame=Frame(root,bg="#90EE90",width=1988,height=520)   #for fill details
bottomFrame.pack(side=TOP,fill=X)

rightFrame = Frame(root, width=550)    #for treeview
rightFrame.place(relx = 1, x =-590, y = 30) 

#****************************************************************************************

def getData(event):             #to get values when the record is clicked
    selected_row = tv.focus()
    data = tv.item(selected_row)
    global row
    row = data["values"]
    #print(row)
    i_sno.set(row[0])
    i_name.set(row[1])
    i_meaning.set(row[2])
def save():         #add the record
    global c
    db = mysql.connector.connect(host="localhost",user="root",passwd="",database="dictionary")
    con = db.cursor()
    a=i_name.get()         #to get the values from entry box
    b=i_meaning.get()  
    if a=="" or b=="" :
        messagebox.showerror("Error in Input", "Please Fill all the details")
        return
    con.execute("insert into english(word, definition) values ('"+a+"','"+b+"')")  
    engine = pyttsx3.init()
    engine.say("Word added successfully!")    
    engine.runAndWait()  
    messagebox.showinfo("Add word", "Word added successfully!")
    db.commit()
    db.close()
    aa.grid_forget()                #to vanish the label and entry box
    name.grid_forget()
    name_1.grid_forget()
    meaning_1.grid_forget()
    meaning.grid_forget()
    submit.grid_forget()
    lab1.grid_forget()
    lab2.grid_forget()
    clear()
def update():  
    global c
    db = mysql.connector.connect(host="localhost",user="root",passwd="",database="dictionary")
    con = db.cursor()   
    a=i_name.get()
    b=i_meaning.get() 
    d=i_sno.get()
    if a=="" or b=="" or d=="":
        messagebox.showerror("Error in Input", "Please Fill all the details")
        return
    con.execute("update english set word='"+a+"', definition='"+b+"' where sno='%s'"%(d))
    db.commit()
    db.close()
    engine = pyttsx3.init()
    engine.say("Word updated successfully, click on to view dictionary to see the changes made ")    
    engine.runAndWait() 
    messagebox.showinfo("Update word", "Updation successful!")
    bb.grid_forget()
    name.grid_forget()
    name_1.grid_forget()
    meaning_1.grid_forget()
    meaning.grid_forget()
    sno.grid_forget()
    submit.grid_forget()
    sno_1.grid_forget()
    lab1.grid_forget()
    lab2.grid_forget()
    clear()
def delete():
    global c
    db = mysql.connector.connect(host="localhost",user="root",passwd="",database="dictionary")
    con = db.cursor()   
    e=i_sno.get()
    if e=="":
        messagebox.showerror("Error in Input", "Please Fill all the details")
        return
    con.execute("delete from english where sno='%s'"%(e))    
    db.commit()
    db.commit()
    db.close()
    engine = pyttsx3.init()
    engine.say("Word deleted")    
    engine.runAndWait() 
    messagebox.showinfo("Delete word", "Word deleted successfully!")
    clear()
    sno.grid_forget()
    sno_1.grid_forget()
    d.grid_forget()
    submit.grid_forget()
    
def clear():
    if i_sno != ""  :
        i_sno.set("")                 #to clear the entry box
        i_name.set("")   
        i_meaning.set("")
    
    else:
        i_name.set("")   
        i_meaning.set("")

def search():                     #like query
    db = mysql.connector.connect(host="localhost",user="root",passwd="",database="dictionary")
    con = db.cursor()   
    c=i_name.get()
    if c=="":
        messagebox.showerror("Error in Input", "Please Fill all the details")
        return
    sql="select sno,word,definition from english where word like '%{a}%';".format(a=c)
    con.execute(sql)
    records = con.fetchall()
    
    tv.delete(*tv.get_children())       #it clear the treeview and re-enter the records
    for row in records:
            tv.insert("",END,values=row)
    db.commit()
    db.close()
    clear()
    

def define():               #to view meaning of a word typed
    db = mysql.connector.connect(host="localhost",user="root",passwd="",database="dictionary")
    con = db.cursor()   
    c=i_name.get()
    if c=="":
        messagebox.showerror("Error in Input", "Please Fill all the details")
        return
    sql="select definition from english where word='%s'"%(c);
    con.execute(sql)
    records = con.fetchone() 
    if records==None:
        messagebox.showinfo("Word not found", "Word not found!! \t Enter a valid word!")

    engine = pyttsx3.init()
    engine.say("The meaning of "+c+ " is " + " " +records[0]) 
    engine.runAndWait()     
    messagebox.showinfo("Meaning", "The meaning of "+c+ " is " + " " +records[0])
    
    
    db.commit()
    db.close()
    clear()
    sno.grid_forget()    
    d.grid_forget()
    submit.grid_forget()
    submit1.grid_forget()

img=Image.open("mic1.jpg")
re=img.resize((30,30),Image.ANTIALIAS)
new=ImageTk.PhotoImage(re) 
img1=Image.open("mic1.jpg")
re1=img1.resize((30,30),Image.ANTIALIAS)
new1=ImageTk.PhotoImage(re1)
 

    
i_sno=IntVar()
i_name = StringVar()   
i_meaning = StringVar()
def radio():
    select=int(var.get())
    if(select==1):
        tv.delete(*tv.get_children())   #it clear the treeview and re-enter the records
        db = mysql.connector.connect(host="localhost",user="root",passwd="",database="dictionary")
        con = db.cursor()
        sql = "select * from english order by sno"
        con.execute(sql)
        records = con.fetchall()

        for row in records:
            tv.insert("",END,values=row)
        db.commit()
        db.close()
        
    if(select==2):       
        global name,name_1,aa,meaning,meaning_1,submit,lab,lab1,lab2,submit1
            
        aa=Label(bottomFrame,text = "Add Word",font=("Arial Bold", 20),fg="black",bg="#90EE90")
        aa.grid(row=2,column=4,padx=10,pady=10,columnspan=2)              
        name=Label(bottomFrame,text="Word",font=("Arial Bold", 14),fg="black",bg="#90EE90")
        name.grid(row=4,column=3,padx=5,pady=10,sticky=W)
        name_1=Entry(bottomFrame,textvariable=i_name,width=30,font=("Arial Bold", 14),fg="black",bg="white")
        name_1.grid(row=4,column=4,padx=5,sticky=W)
        lab1=Button(bottomFrame,text="hii",image=new,bd=0,bg="#90EE90")
        lab1.grid(row=4,column=6)
        
        meaning=Label(bottomFrame,text="Meaning",font=("Arial Bold", 14),fg="black",bg="#90EE90")
        meaning.grid(row=6,column=3,padx=5,sticky=W)
        meaning_1=Entry(bottomFrame,textvariable=i_meaning,width=30,font=("Arial Bold", 14),fg="black",bg="white")
        meaning_1.grid(row=6,column=4,padx=5,sticky=W)     
        lab2=Button(bottomFrame,text="hii",image=new,bd=0,bg="#90EE90")
        lab2.grid(row=6,column=6)
        submit=Button(bottomFrame,text="ADD",command=save,width=10,font=("Arial Bold", 14),fg="black",bg="#87CEEB")
        submit.grid(row=7,column=4,padx=5,pady=10,columnspan=2)
        
       
    if(select==3):            
        global bb,sno,sno_1
        bb=Label(bottomFrame,text = "Update word",font=("Arial Bold", 20),fg="black",bg="#90EE90")
        bb.grid(row=2,column=4,padx=10,pady=10,columnspan=2)
        sno=Label(bottomFrame,text="sno",font=("Arial Bold", 14),fg="black",bg="#90EE90")
        sno.grid(row=4,column=3,padx=5,pady=10,sticky=W)
        sno_1=Entry(bottomFrame,textvariable=i_sno,width=30,font=("Arial Bold", 14),fg="black",bg="white")
        sno_1.grid(row=4,column=4,padx=5,pady=10,sticky=W)       
        
        name=Label(bottomFrame,text="Word",font=("Arial Bold", 14),fg="black",bg="#90EE90")
        name.grid(row=6,column=3,padx=5,pady=10,sticky=W)
        name_1=Entry(bottomFrame,textvariable=i_name,width=30,font=("Arial Bold", 14),fg="black",bg="white")
        name_1.grid(row=6,column=4,padx=5,sticky=W)
        lab1=Button(bottomFrame,text="hii",image=new,bd=0,bg="#90EE90")
        lab1.grid(row=6,column=6)
        
        meaning=Label(bottomFrame,text="Meaning",font=("Arial Bold", 14),fg="black",bg="#90EE90")
        meaning.grid(row=8,column=3,padx=5,sticky=W)
        meaning_1=Entry(bottomFrame,textvariable=i_meaning,width=30,font=("Arial Bold", 14),fg="black",bg="white")
        meaning_1.grid(row=8,column=4,padx=5,sticky=W)
        lab2=Button(bottomFrame,text="hii",image=new,bd=0,bg="#90EE90")
        lab2.grid(row=8,column=6)
        submit=Button(bottomFrame,text="UPDATE",command=update,width=10,font=("Arial Bold", 14),fg="black",bg="#87CEEB")
        submit.grid(row=9,column=4,padx=5,pady=10,columnspan=2)
  
       
    if(select==4):
        global d
        d=Label(bottomFrame,text = "Delete word",font=("Arial Bold", 20),fg="black",bg="#90EE90")
        d.grid(row=2,column=4,padx=10,pady=10,columnspan=2)
        sno=Label(bottomFrame,text="sno",font=("Arial Bold", 14),fg="black",bg="#90EE90")
        sno.grid(row=4,column=3,padx=5,pady=10,sticky=W)
        sno_1=Entry(bottomFrame,textvariable=i_sno,width=30,font=("Arial Bold", 14),fg="black",bg="white")
        sno_1.grid(row=4,column=4,padx=5,pady=10,sticky=W)      
        submit=Button(bottomFrame,text="DELETE",command=delete,width=10,font=("Arial Bold", 14),fg="black",bg="#87CEEB")
        submit.grid(row=5,column=4,padx=5,pady=10,columnspan=2)
    
    if (select==5):
        d=Label(bottomFrame,text = "Enter a part of word you remember!!",font=("Arial Bold", 20),fg="black",bg="#90EE90")
        d.grid(row=2,column=4,padx=10,pady=10,columnspan=2)
        sno=Entry(bottomFrame,textvariable=i_name,width=30,font=("Arial Bold", 14),fg="black",bg="white")
        sno.grid(row=4,column=4,padx=5,pady=10,sticky=W)
        submit=Button(bottomFrame,text="SEARCH",command=search,width=10,font=("Arial Bold", 14),fg="black",bg="#87CEEB")
        submit.grid(row=4,column=5,padx=5,pady=10,columnspan=2)
        submit1=Button(bottomFrame,text="DEFINITION",command=define,width=10,font=("Arial Bold", 14),fg="black",bg="#87CEEB")
        submit1.grid(row=5,column=5,padx=5,pady=10,columnspan=2)
        
    if(select==6):
        clear()
        
           
var = IntVar()
name=Label(leftFrame,text="DICTIONARY",font=("Arial Bold", 30),fg="black",bg="#87CEEB")
name.grid(row=0,column=3,sticky=W,padx=10,pady=20)

R1 = Radiobutton(leftFrame, text="View Dictionary",variable=var, value=1,command=radio,bg="#87CEEB",font=("Arial Bold",14,"bold"))
R1.grid(row=2,column=2,sticky=W,padx=10)
R2 = Radiobutton(leftFrame, text="Add word",variable=var, value=2,command=radio,bg="#87CEEB",font=("Arial Bold",14,"bold"))
R2.grid(row=3,column=2,sticky=W,padx=10)
R3 = Radiobutton(leftFrame, text="Update word",variable=var, value=3,command=radio,bg="#87CEEB",font=("Arial Bold",14,"bold"))
R3.grid(row=4,column=2,sticky=W,padx=10)
R4 = Radiobutton(leftFrame, text="Delete word",variable=var, value=4,command=radio,bg="#87CEEB",font=("Arial Bold",14,"bold"))
R4.grid(row=5,column=2,sticky=W,padx=10)
R7=Radiobutton(leftFrame,text="Search",variable=var,command=radio,value=5,bg="#87CEEB",font=("Arial Bold",14,"bold"))
R7.grid(row=6,column=2,sticky=W,padx=10)
R5 = Radiobutton(leftFrame, text="Clear",variable=var, value=6,command=radio,bg="#87CEEB",font=("Arial Bold",14,"bold"))
R5.grid(row=7,column=2,sticky=W,padx=10)
R6=Radiobutton(leftFrame,text="Exit",variable=var,command=root.destroy,value=7,bg="#87CEEB",font=("Arial Bold",14,"bold"))
R6.grid(row=8,column=2,sticky=W,padx=10)



style=ttk.Style()
#pick theme for treeview
style.theme_use("alt")


"""
style.configure("Treeview",background="silver",foreground="black",font=("Calibri",16,"bold"),rowheight=25,fieldbackground="silver")
#change selected color
style.map('Treeview',background=[('selected','green')])

tv=ttk.Treeview(rightFrame,column=(1,2,3))
tv.heading("1",text='ID')
tv.column(1,width=10)
tv.heading("2",text='WORD')
tv.column(1,width=30)
tv.heading("3",text="MEANING")
tv.column(1,width=140)

tv['show']='headings'
tv.bind("<ButtonRelease-1>",getData)
tv.pack(fill=X)
"""

#rightFrame scrollbar for treeview
tree_scroll = Scrollbar(rightFrame)
tree_scroll.pack(side=RIGHT,fill=Y)

#creating tree view
tv=ttk.Treeview(rightFrame,yscrollcommand=tree_scroll.set)
tree_scroll.config(command=tv.yview)   #configure scrollbar for treeview


tv['columns']=("ID","WORD","MEANING")
tv.column("#0",width=0,stretch=NO)
tv.column("ID",anchor=CENTER,width=50)
tv.column("WORD",anchor=W,width=140)
tv.column("MEANING",anchor=W,width=250)

tv.heading("#0",text="",anchor=W)
tv.heading("ID",text="ID",anchor=CENTER)
tv.heading("WORD",text="WORD",anchor=CENTER)
tv.heading("MEANING",text="MEANING",anchor=CENTER)
tv['show']='headings'
tv.bind("<ButtonRelease-1>",getData)    #butt-1 is for leftclick of mouse
tv.pack(fill=X)


root.mainloop()     #to display in screen

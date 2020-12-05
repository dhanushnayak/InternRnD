import Times_of_India
import Firstpost
import Indiaexpress
import Moneycontrol
import tkinter 
from PIL import Image, ImageTk
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from tkinter import ttk
import requests
from io import BytesIO
import os
top = tkinter.Tk()
top.geometry('1200x750')
top.configure(background="black")
def check_connection(svc):
   
    client = MongoClient(svc)
    try:
       # The ismaster command is cheap and does not require auth.
       client.admin.command('ismaster')
    except ConnectionFailure:
       return False
def times(froms,to,svc,rvar):
    ti=Times_of_India.times_of_india(page_from=froms,page_to=to,svc=svc,content=rvar)
    if ti.fetch():
            tkinter.messagebox.showinfo("Success","Updated to "+svc)
    else:
        tkinter.messagebox.showerror("Error","Not inserted to "+svc)
 
def firstpost(froms,to,svc,rvar):
    ti=Firstpost.Firstpost(page_from=froms,page_to=to,svc=svc,content=rvar)
    if ti.fetch():
            tkinter.messagebox.showinfo("Success","Updated to "+svc)
    else:
        tkinter.messagebox.showerror("Error","Not inserted to "+svc)
def indian(froms,to,svc,rvar):
    ti=Indiaexpress.indianexpress(page_from=froms,page_to=to,svc=svc,content=rvar)
    if ti.fetch():
            tkinter.messagebox.showinfo("Success","Updated to "+svc)
    else:
        tkinter.messagebox.showerror("Error","Not inserted to "+svc)
def moneycontrol(froms,to,svc,rvar):
    ti=Moneycontrol.moneycontrol(page_from=froms,page_to=to,svc=svc,content=rvar)
    
    if ti.fetch():
            tkinter.messagebox.showinfo("Success","Updated to "+svc)
    else:
        tkinter.messagebox.showerror("Error","Not inserted to "+svc)
def printf():
    if content.get()=="Times of India":
        if path.get()=="Provide Driver Path":
            tkinter.messagebox.showerror("showerror", "Path Not Found")
        elif pagefrom.get() == "Ex : 1" or pageto.get=="Ex : 3" or pagefrom.get()=="" or pageto.get()=="" or int(pageto.get())<int(pagefrom.get()):
            
            tkinter.messagebox.showerror("showerror", "Provide Proper Pages")
        elif rvar.get()=="":
            tkinter.messagebox.showerror("showerror", "Select the Category")
        elif check_connection(svc.get()) == False:
            tkinter.messagebox.showerror("DatabaseError","Mongo SVC Error")
        elif os.path.exists(path.get())==False:
            tkinter.messagebox.showerror("Path Not Found","Path of driver is wrong")
        else:
            print(rvar.get())
            times(pagefrom.get(),pageto.get(),svc.get(),rvar.get())
    if content.get()=="First Post":
        if path.get()=="Provide Driver Path":
            tkinter.messagebox.showerror("showerror", "Path Not Found")
        elif pagefrom.get() == "Ex : 1" or pageto.get=="Ex : 3" or pagefrom.get()=="" or pageto.get()=="" or int(pageto.get())<int(pagefrom.get()):
            
            tkinter.messagebox.showerror("showerror", "Provide Proper Pages")
        elif rvar.get()=="":
            tkinter.messagebox.showerror("showerror", "Select the Category")
        elif check_connection(svc.get()) == False:
            tkinter.messagebox.showerror("DatabaseError","Mongo SVC Error")
        else:
            print(rvar.get())
            firstpost(pagefrom.get(),pageto.get(),svc.get(),rvar.get())
    if content.get()=="Indian Express":
        if path.get()=="Provide Driver Path":
            tkinter.messagebox.showerror("showerror", "Path Not Found")
        elif pagefrom.get() == "Ex : 1" or pageto.get=="Ex : 3" or pagefrom.get()=="" or pageto.get()=="" or int(pageto.get())<int(pagefrom.get()):
            
            tkinter.messagebox.showerror("showerror", "Provide Proper Pages")
        elif rvar.get()=="":
            tkinter.messagebox.showerror("showerror", "Select the Category")
        elif check_connection(svc.get()) == False:
            tkinter.messagebox.showerror("DatabaseError","Mongo SVC Error")
        else:
            print(rvar.get())
            indian(pagefrom.get(),pageto.get(),svc.get(),rvar.get())
    if content.get()=="Money Control":
        tkinter.messagebox.showinfo("Money Control","Sports = market and Business = mutual-funds" )
        if path.get()=="Provide Driver Path":
            tkinter.messagebox.showerror("showerror", "Path Not Found")
        elif pagefrom.get() == "Ex : 1" or pageto.get=="Ex : 3" or pagefrom.get()=="" or pageto.get()=="" or int(pageto.get())<int(pagefrom.get()):
            
            tkinter.messagebox.showerror("showerror", "Provide Proper Pages")
        elif rvar.get()=="":
            tkinter.messagebox.showerror("showerror", "Select the Category")
        elif check_connection(svc.get()) == False:
            tkinter.messagebox.showerror("DatabaseError","Mongo SVC Error")
        else:
            print(rvar.get())
            if rvar.get()=="sports":
                r = "market"
            else:
                r = "mutual-funds"
            moneycontrol(pagefrom.get(),pageto.get(),svc.get(),r)
    
        
    
    print(content.get())
    print(path.get())
    print(rvar.get())
    print(svc.get())
    print(pagefrom.get())
    print(pageto.get())

class Example(tkinter.Frame):
    def __init__(self, master, *pargs):
        tkinter.Frame.__init__(self, master, *pargs)

        respo = requests.get("https://raw.githubusercontent.com/dhanushnayak/Python_module_making/master/bg2.png")
        self.image = Image.open(BytesIO(respo.content))
        self.img_copy= self.image.copy()


        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = tkinter.Label(self, image=self.background_image)
        self.background.pack(fill="both", expand=True)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self,event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)



e = Example(top)
e.pack()


uname = tkinter.Label(top, text = "Websites",bg="#0a0a29",fg="#3b57ab",font=('courier', 15,"bold")).place(x = 200,y = 250)  
  
#creating label  
password = tkinter.Label(top, text = "Driver Path ",bg="#0a0a29",fg="#3b57ab",font=('courier', 15,"bold")).place(x = 200, y = 300)  

radiovalue = tkinter.Label(top, text = "Content ",bg="#0a0a29",fg="#3b57ab",font=('courier', 15,"bold")).place(x = 200, y = 350)  
path = tkinter.StringVar()
path.set("Provide Driver Path")
svc = tkinter.StringVar()
svc.set("mongodb://localhost:27017/")
rvar = tkinter.StringVar()

pagefrom = tkinter.StringVar()
pagefrom.set("Ex : 1")
pageto = tkinter.StringVar()
pageto.set("Ex : 3")
r1 = tkinter.Radiobutton(top, text='Sports', variable=rvar, value='sports',bg="#0a0a29",fg="#3b57ab",font=('courier', 15,"bold")).place(x=350,y=350)
r2 = tkinter.Radiobutton(top, text='Business', variable=rvar, value='business',bg="#0a0a29",fg="#3b57ab",font=('courier', 15,"bold")).place(x=500,y=350)
mongosvc = tkinter.Label(top,text="MongoDB SVC",bg="#0a0a29",fg="#3b57ab",font=('courier', 15,"bold")).place(x=200,y=400)
e2 = tkinter.Entry(top, width = 29,textvariable=path,font = ('courier', 15)).place(x =350, y = 300)  
e3 = tkinter.Entry(top, width = 29,textvariable=svc,font = ('courier', 15)).place(x =350, y = 400)  
page = tkinter.Label(top,text="Page",bg="#0a0a29",fg="#3b57ab",font=('courier', 15,"bold")).place(x=200,y=450)
page1 = tkinter.Entry(top, width = 12,textvariable=pagefrom,font = ('courier', 15)).place(x=350,y=450)
page2 = tkinter.Entry(top,width=12, textvariable=pageto,font = ('courier', 15)).place(x=550,y=450)
sbmitbtn = tkinter.Button(top, text = "Submit",bg="#8080ff",activebackground = "green", activeforeground = "black",width=15,height=2,command=printf).place(x = 470, y = 500)

n = tkinter.StringVar() 
content = ttk.Combobox(top, width = 27,  
                            textvariable = n,font = ('courier', 15)) 

  
content['values'] = ("Times of India","First Post","Indian Express","Money Control") 
  

content.place(x = 350, y = 250)  

content.current(0)

top.mainloop()


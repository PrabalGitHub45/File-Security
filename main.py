from tkinter import *
import tkinter as tk
import customtkinter as ct
from tkinter import filedialog
from tkinter.messagebox import showinfo
import subprocess
from playsound import playsound
import webbrowser
import backend
import os

backend.start()

source=''
dest=''
key=''
selected=0

#Select source folder
def chooseFolder1():
    global source
    if set_combo2.get()=='On':
        playsound('Sounds/input_folder.mp3')
    source = filedialog.askdirectory()
    if tabview.get()=='Encrypt':
        etl1.config(text=source)
    else:
        tl1.config(text=source)
    return source

#Select destination folder
def chooseFolder2():
    global dest
    if set_combo2.get()=='On':
        playsound('Sounds/output_folder.mp3')
    dest = filedialog.askdirectory()
    if tabview.get()=='Encrypt':
        etl2.config(text=dest)
    else:
        tl2.config(text=dest)
    return dest

#select key file
def browseFiles():
    if radio_var.get()==1:
        showinfo(message="You can't select key in Encrypt mode !")
    else:
        global key
        if set_combo2.get()=='On':
            playsound('Sounds/key_file.mp3')
        key = filedialog.askopenfilename(initialdir = "/",
                                        title = "Select a File",
                                        filetypes = (("Key files",
                                                        "*.key*"),
                                                    ))
        with open(key,'r') as conKey:
            txt_box.insert(tk.INSERT,conKey.read())


#Call of Encrypt and Decrypt operation and play sound
def chooser():
     global combo
     isDel=2
     if combo.get()=='Keep Encrypted files':
         isDel=0
     elif combo.get()=='Remove Encrypted files':
         isDel=1
     if set_combo2.get()=='On':
        playsound('Sounds/start_operation.mp3')

     if source=='' or  dest=='':
         showinfo(message="Please select input and output folder properly !")
     else: 
            if tabview.get()=='Encrypt':
                backend.Encrypt(source,dest)

          
            if tabview.get()=='Decrypt':
                if txt_box.get()=='':
                    showinfo(message="Please select the key !")
                else:
                    backend.Decrypt(source,dest,txt_box.get(),isDel)

          
#Open the history file and play sound
def history(temp):
    if set_combo2.get()=='On' and temp==1:
        subprocess.Popen(['gedit', 'sample.txt'])
        playsound('Sounds/history.mp3')
    if set_combo2.get()=='Off' and temp==1:
        subprocess.Popen(['notepad', 'sample.txt'])
    if set_combo2.get()=='On' and temp==0:
        playsound('Sounds/about.mp3')
        webbrowser.open_new_tab(os.path.abspath('About/main.html'))
    if set_combo2.get()=='Off' and temp==0:
        webbrowser.open_new_tab(os.path.abspath('About/main.html'))


#Play tab sound while selecting a tab
def tabSound():
    if set_combo2.get()=='On' and tabview.get()=='Encrypt':
        playsound('Sounds/encrypt.mp3')
    elif set_combo2.get()=='On' and tabview.get()=='Decrypt':
        playsound('Sounds/decrypt.mp3')

window = ct.CTk()
appIcon = PhotoImage(file='images/Security2.png')
window.title('Encryption & Decryption')
window.iconphoto(False , appIcon)
window.maxsize(width=900 , height=600)
window.minsize(width=900 , height=600)
ct.set_appearance_mode('light')

#Create a frame for settings
frame = ct.CTkFrame(master=window, width=150, height=600)
frame.place(x=0,y=0)

#Create tab for encrypt and decrypt selection mode
tabview = ct.CTkTabview(
    window,
    width=650,
    height=500,
    border_width=2,
    corner_radius=16,
    border_color=('#99084e','#626ade'),
    fg_color=('#c9c5b9','#302e2f'),
    command=tabSound
    )

tabview.place(x=200,y=36)
tabview.add("Encrypt")
tabview.add("Decrypt")
tabview.set("Encrypt")

#Change the mode
def switch_event(full):
    #global switch_var
    #if switch_var.get()=='on':
    #     ct.set_appearance_mode('dark')
    #else:
    #     ct.set_appearance_mode('light')
    if set_combo2.get()=='On':
        playsound('Sounds/mode.mp3')
    if set_combo.get()=='Dark Mode':
        ct.set_appearance_mode('dark')
    else:
        ct.set_appearance_mode('light')
    print("switch toggled, current value:", set_combo.get())


#Create design for settings frame
set=ct.CTkLabel(
    frame,
    text='Settings',
    font=('Comic Sans MS',22)
    )
set.place(x=22,y=10)

set_history=ct.CTkButton(
    frame,
    width=110,
    text="History",
    font=('simple',13),
    fg_color=('#1a9140','#521ba6'),
    command=lambda:history(1)
)
set_history.place(x=10,y=120)

set_about=ct.CTkButton(
    frame,
    width=110,
    text="About",
    font=('simple',13),
    fg_color=('#1a9140','#521ba6'),
    command=lambda:history(0)
)
set_about.place(x=10,y=174)

set_appr=ct.CTkLabel(
    frame,
    text='Apperance mode:',
    font=('Simple',13)
    )
set_appr.place(x=10,y=360)

set_combo=StringVar()
set_mode = ct.CTkOptionMenu(
    frame,                     
    values=["Light Mode", "Dark Mode"],
    width=120,
    height=30,
    corner_radius=8,
    command=switch_event,
    font=('simple',12),
    variable=set_combo,
    fg_color=('#1a9140','#521ba6')
    )
set_mode.set('Light Mode')
set_mode.place(x=10,y=400)

set_sond=ct.CTkLabel(
    frame,
    text='Sound effects:',
    font=('Simple',13)
    )
set_sond.place(x=10,y=460)

set_combo2=StringVar()
set_sound= ct.CTkOptionMenu(
    frame,                     
    values=["Off", "On"],
    width=120,
    height=30,
    corner_radius=8,
    font=('simple',12),
    variable=set_combo2,
    fg_color=('#1a9140','#521ba6')
    )
set_sound.set('Off')
set_sound.place(x=10,y=500)
#l1=ct.CTkLabel(
#    window,
#    text='Type :-',
#    font=('Comic Sans MS',26)
#    )
#l1.place(x=150,y=37)

radio_var = IntVar()

#Create desigen for Encrypt--------------------------------------------->
el2=ct.CTkLabel(
    tabview.tab("Encrypt"),
    text='Input Folder : ',
    font=('Comic Sans MS',20)
    )
el2.place(x=20,y=40)

etl1=Label(
    tabview.tab("Encrypt"),
    text='Display location here',
    height=2,
    width=43)
etl1.place(x=160,y=40)

ebtn1 = ct.CTkButton(
    tabview.tab("Encrypt"),
    width=80,
    height=42,
    border_width=0,
    corner_radius=8,
    font=('Comic Sans MS',18),
    text="Browse",
    fg_color=('#952ea3','red'),
    
    command=chooseFolder1
    )
ebtn1.place(x=520,y=40)


el3=ct.CTkLabel(
    tabview.tab("Encrypt"),
    text='Output Folder : ',
    font=('Comic Sans MS',20)
    )
el3.place(x=20,y=140)

etl2=Label(
    tabview.tab("Encrypt"),
    text='Display location here',
    height=2,
    width=42)
etl2.place(x=170,y=140)

ebtn2 = ct.CTkButton(
    tabview.tab("Encrypt"),                   
    width=80,
    height=42,
    border_width=0,
    corner_radius=8,
    font=('Comic Sans MS',18),
    text="Browse",
    fg_color=('#952ea3','red'),
    command=chooseFolder2
    )
ebtn2.place(x=520,y=140)


thunder = PhotoImage(file="images/thunder.png").subsample(2, 2)
ebtn4 = ct.CTkButton(
    tabview.tab("Encrypt"),                   
    width=90,
    height=50,
    border_width=0,
    corner_radius=8,
    text="Start",
    command=chooser,
    font=('Comic Sans MS',18),
    fg_color=('#258a88','#4a8a53'),
    compound = LEFT,
    image=thunder
    )
ebtn4.place(x=260,y=260)


#Create design for decrypt
l2=ct.CTkLabel(
    tabview.tab("Decrypt"),
    text='Input Folder : ',
    font=('Comic Sans MS',20)
    )
l2.place(x=20,y=30)

tl1=Label(
    tabview.tab("Decrypt"),
    text='Display location here',
    height=2,
    width=43)
tl1.place(x=160,y=30)

btn1 = ct.CTkButton(
    tabview.tab("Decrypt"),
    width=80,
    height=42,
    border_width=0,
    corner_radius=8,
    font=('Comic Sans MS',18),
    text="Browse",
    fg_color=('#952ea3','red'),
    
    command=chooseFolder1
    )
btn1.place(x=520,y=30)


l3=ct.CTkLabel(
    tabview.tab("Decrypt"),
    text='Output Folder : ',
    font=('Comic Sans MS',20)
    )
l3.place(x=20,y=120)

tl2=Label(
    tabview.tab("Decrypt"),
    text='Display location here',
    height=2,
    width=42)
tl2.place(x=170,y=120)

btn2 = ct.CTkButton(
    tabview.tab("Decrypt"),                   
    width=80,
    height=42,
    border_width=0,
    corner_radius=8,
    font=('Comic Sans MS',18),
    text="Browse",
    fg_color=('#952ea3','red'),
    command=chooseFolder2
    )
btn2.place(x=520,y=120)

image_key=PhotoImage(file='images/key_img.png').subsample(1, 1)

btn3 = ct.CTkButton(
    tabview.tab("Decrypt"),                   
    width=80,
    height=36,
    border_width=0,
    corner_radius=10,
    text="Select Key file",
    command=browseFiles,
    font=('Comic Sans MS',18),
    image=image_key,
    fg_color=('#4d630b','#276375')
    )
btn3.place(x=20,y=220)

Or=ct.CTkLabel(
    tabview.tab("Decrypt"),
    text='Or',
    font=('Comic Sans MS',18)
    )
Or.place(x=205,y=220)


txt_box=ct.CTkEntry(
    tabview.tab("Decrypt"),
    width=380,
    height=36

)
txt_box.place(x=235,y=220)
    
l4=ct.CTkLabel(
    tabview.tab("Decrypt"),
    text='Check operation: ',
    font=('Comic Sans MS',20)
    )
l4.place(x=81,y=300)

combo=StringVar()
combobox = ct.CTkOptionMenu(
    tabview.tab("Decrypt"),                     
    values=["Keep Encrypted files", "Remove Encrypted files"],
    width=220,
    height=34,
    corner_radius=8,
    font=('simple',14),
    variable=combo,
    fg_color=('#b0643e','#c4218e')
    )
combobox.set('select option')
combobox.place(x=250,y=300)

thunder = PhotoImage(file="images/thunder.png").subsample(2, 2)
btn4 = ct.CTkButton(
    tabview.tab("Decrypt"),                   
    width=90,
    height=50,
    border_width=0,
    corner_radius=8,
    text="Start",
    command=chooser,
    font=('Comic Sans MS',18),
    fg_color=('#258a88','#4a8a53'),
    compound = LEFT,
    image=thunder
    )
btn4.place(x=390,y=382)


window.mainloop()   

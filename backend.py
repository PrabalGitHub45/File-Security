from tkinter import *
from tkinter import ttk
import tkinter as tk
import customtkinter as ct
from cryptography.fernet import Fernet
from tkinter.messagebox import showinfo
import os
import datetime

def start():
    x = datetime.datetime.now()
    date_and_time = x.strftime("%x")+' at '+x.strftime("%X")
    row=f'\n<-----------------------------------------Season start on {date_and_time}----------------------------------------->\n\n'
    with open('sample.txt' , 'a') as samf:
        samf.write(row)

def writeFile(type,key,inp_fileName,out_fileName):
    x = datetime.datetime.now()
    date_and_time = x.strftime("%x")+'\t'+x.strftime("%X")
    row=f'{date_and_time}\t{type}\t\t{key}\t\t{inp_fileName}\t\t{out_fileName}\n'

    with open('sample.txt' , 'a') as samf:
        samf.write(row)


def Encrypt(path , path2):
    app = ct.CTk()
    app.geometry('720x450')
    pb = ttk.Progressbar(
        app,
        orient='horizontal',
        mode='determinate',
        length=700
    )
    pb.grid(column=0, row=0)
    # create scrollable textbox
    tk_textbox = tk.Text(app, highlightthickness=0)
    tk_textbox.grid(row=1, column=0 , columnspan=10)
    ctk_textbox_scrollbar = ct.CTkScrollbar(app, command=tk_textbox.yview)
    ctk_textbox_scrollbar.grid(row=1, column=1, sticky="ns")
    # connect textbox scroll event to CTk scrollbar
    tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

    key = Fernet.generate_key()
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)
    fernet = Fernet(key)

    dir_list = os.listdir(path)
    dir_len=len(dir_list)
    print(f'Key is : {key}')

    for files in dir_list:

        with open(path+'/'+files , 'rb') as file:
            original = file.read()    

        encrypted = fernet.encrypt(original)

        with open(path2+'/'+'EN_'+files , 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        
        print('Encrypt '+files+' successfully.')

        tk_textbox.insert("0.0",'Encrypted '+path+'/'+files+' successfully\n')
        pb['value']+=(100/dir_len)
        writeFile('Encrypt' , key , path+'/'+files , path2+'/'+'EN_'+files)
        app.update()

    showinfo(message="All operations are done !")
    app.destroy()


def Decrypt(path , path2 , key_path , isDel):
    app = ct.CTk()
    app.geometry('720x450')
    pb = ttk.Progressbar(
        app,
        orient='horizontal',
        mode='determinate',
        length=700
    )
    pb.grid(column=0, row=0)
    # create scrollable textbox
    tk_textbox = tk.Text(app, highlightthickness=0)
    tk_textbox.grid(row=1, column=0 , columnspan=10)
    #isDel=int(input('0 ------> remain save encrypted files.\n1 ------>  remove encrypted files.\nEnter your choice :'))

    key=key_path
    try :
        f = Fernet(key)
    except:
        print('Key format not valid.')
        showinfo(message="Key format not valid !")
        os._exit(Decrypt)
    dir_list = os.listdir(path)
    dir_len=len(dir_list)
    i = 0
    def decrypt_file(file):
        nonlocal i
        with open(path+'/'+file, 'rb') as encrypted_file:
            encrypted = encrypted_file.read()
        try:
            decrypted = f.decrypt(encrypted)
            
            with open(path2+'/'+file[3:], 'wb') as decrypted_file:
                decrypted_file.write(decrypted)

            if isDel==1:
                os.remove(path+'/'+file)
            
            print('Decrypt '+file+' successfully.')
            tk_textbox.insert("0.0",'Decrypted '+path+'/'+file+' successfully\n')
            writeFile('Decrypt' , key , path+'/'+file , path2+'/'+file[3:])
        except:
            print('<----------Wrong key------------>')
            print('Decrypt '+file+' failed !.')
            tk_textbox.insert("0.0",'Decryption for '+path+'/'+file+' has failed\n')
        
        i += 1
        pb['value']=(i/dir_len)*100
        if i < dir_len:
            app.after(1, decrypt_file, dir_list[i])

    decrypt_file(dir_list[0])
    app.mainloop()


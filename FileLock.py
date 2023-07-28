import secrets
import sys
import tkinter as tk
from PIL import Image, ImageTk
import os
from tkinter import messagebox
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC



backend = default_backend()
iterations = 100_000

def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))

def password_encrypt(message: bytes, password: str, iterations: int = iterations) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )

def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)
###############################################################################


    
    
global t
def set_window():
    global window
    window = tk.Tk()
    window.geometry("400x300")
    path = os.getcwd()
    icon_address = path+'/icons/lock1.jpg'
    _ico = Image.open(icon_address)
    ico = ImageTk.PhotoImage(_ico)
    window.wm_iconphoto(False, ico)
    window.title('FileLocker - Lock')
set_window()

def lock():
    password = entry2.get()
    source = entry.get()
    file_base_name = os.path.basename(source)
    with open(os.getcwd()+'/locked-files/'+file_base_name+'.LF', '+w') as lf_file:
        S = open(source, 'r').read()
        PS = password_encrypt(bytes(S, 'utf-8'), password)
        lf_file.write(PS.decode())
    quit()


    

def new_window():
    e = entry.get()
    try:
        
        File = os.path.split(e)
        if len(File[1].split('.'))<2:
               dfsfsdf = ffffft
        File_ = File[1].split('.')
        F_l = len(File_)-1
        File_ = File_[F_l]
        messagebox.showinfo('File information', "file extension : "+File_+' * \n'+'file path: '+e+' * \n'+'file size : '+str(os.path.getsize(e))+' * ')
    except:
        messagebox.showinfo('File information',"file extension : "+"null * \n"+'file path : '+e+' * \n'+'file size : '+str(os.path.getsize(e))+' * ')
    lock()

    ##    

    


def path_not_found():
    if entry.get() == '':
        messagebox.showerror("Path is empty!", "Please write your file path")
    else:
      messagebox.showerror("File not found", "Error getting file from "+entry.get())

      
def password_not_found():
    messagebox.showerror("Password is empty!", "Please write your password")

    
def build():
    try:
        open(entry.get(), 'r')
    except:
        path_not_found()
        sys.exit(1)
    try:
        entry2.get()[0]
    except:
        password_not_found()
        sys.exit(1)
    new_window()
        




###
f = tk.Frame(master=window)
f2 = tk.Frame(master=window)
f3 = tk.Frame(master=window)
f4 = tk.Frame(master=window)
f5 = tk.Frame(master=window)
f6 = tk.Frame(master=window)
f7 = tk.Frame(master=window)
label = tk.Label(master=f, text="*FileLock*", font=('Times', 17), fg="darkblue")
entry = tk.Entry(master=f2, font=("", 11), width=20)
label2 = tk.Label(master=f2, font=("Serif", 11), text="↔ write file path")
label_E = tk.Label(master=f3)
entry2 = tk.Entry(master=f4, font=("Serif", 11), width=20)
label3 = tk.Label(master=f4, font=("Serif", 11), text="↔ write a password")
button = tk.Button(master=f5, font=("Times", 14), text="Build", bg="lightseagreen", fg='white', command=build)
label_E2 = tk.Label(master=f6)
label_E3 = tk.Label(master=f6)


f.pack()
label.pack(side=tk.TOP)
label_E.pack(side=tk.LEFT)
f3.pack(fill=tk.BOTH)
f2.pack(fill=tk.BOTH)
entry.pack(side=tk.LEFT)
label2.pack(side=tk.LEFT)
f4.pack(fill=tk.BOTH)
entry2.pack(side=tk.LEFT)
label3.pack(side=tk.LEFT)
label_E2.pack()
label_E3.pack()
f6.pack(fill=tk.BOTH)
button.pack()
f5.pack(fill=tk.BOTH)


window.mainloop()

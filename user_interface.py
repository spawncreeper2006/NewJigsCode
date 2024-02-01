from tkinter import Tk, Frame
import tkinter as tk
from tkinter import ttk

from sql_client import LoginClient, LoginQueryResponse

from typing import Callable, Any

user_interface = Callable[[Frame, Tk], None]



def start_window(frame: Frame, root: Tk, start_func: Callable[[Frame, Tk], None]):
    
    frame.destroy()
    frame = Frame(master=root)
    frame.pack(fill='both')
    start_func(frame, root)




def create_account(login_client: LoginClient, user_id: str, username: str, password: str, usertype: str, position: str, frame: Frame, root: Tk) -> None:

    login_client.insert_into(LoginQueryResponse(
        int(user_id),
        username,
        password,
        usertype,
        position
    ))

    frame.quit()

    

def create_account_window(frame: Frame, root: Tk, login_client: LoginClient) -> None:

    user_id_var = tk.StringVar()
    username_var = tk.StringVar()
    password_var = tk.StringVar()
    usertype_var = tk.StringVar()
    position_var = tk.StringVar()
    
    tk.Label(frame, text='Create Account', font=('Calibri', 15)).pack(side='top', pady=(0, 30))

    tk.Label(frame, text='User ID', font=('Calibri', 10)).pack(side='top')
    tk.Entry(frame, textvariable=user_id_var, width=30, font=('Calibri', 5)).pack(side='top', pady=(10, 15))

    tk.Label(frame, text='Username', font=('Calibri', 10)).pack(side='top')
    tk.Entry(frame, textvariable=username_var, width=30, font=('Calibri', 5)).pack(side='top', pady=(10, 15))

    tk.Label(frame, text='Password', font=('Calibri', 10)).pack(side='top')
    tk.Entry(frame, textvariable=password_var, width=30, show='*', font=('Calibri', 5)).pack(side='top', pady=(10, 15))

    tk.Label(frame, text='User Type', font=('Calibri', 10)).pack(side='top')
    tk.Entry(frame, textvariable=usertype_var, width=30, font=('Calibri', 5)).pack(side='top', pady=(10, 15))

    tk.Label(frame, text='Position', font=('Calibri', 10)).pack(side='top')
    tk.Entry(frame, textvariable=position_var, width=30, font=('Calibri', 5)).pack(side='top', pady=(10, 15))

    tk.Button(
        frame,
        text='Create Account',
        command=lambda: create_account(
            login_client,
            user_id_var.get(),
            username_var.get(),
            password_var.get(),
            usertype_var.get(),
            position_var.get(),
            frame,
            root
        )
    ).pack(side='top', pady=10)

    tk.Button(
        frame,
        text='Back to Logon',
        command=lambda: start_window(frame,
                                     root,
                                     lambda frame, root: login_window(frame, root, login_client))
        ).pack(side='top', pady=10)
    

    frame.mainloop()


def validate_login(login_client: LoginClient, username: str, password: str, frame: Frame, root: Tk) -> None:

    login_query_response = login_client.query('username', username)
    if not login_query_response.is_valid:
        #invalid username
        print ('login failed')
        return None
    
    elif not login_query_response.password == password:
        
        #correct username but wrong password
        print ('login failed')
        return None
    
    print ('login success')

    frame.quit()

def login_window(frame: Frame, root: Tk, login_client: LoginClient) -> None:



    username_var = tk.StringVar()
    password_var = tk.StringVar()

    

    tk.Label(frame, text='Login', font=('Calibri', 15)).pack(side='top', pady=(0, 100))

    tk.Label(frame, text='Username', font=('Calibri', 15)).pack(side='top')
    tk.Entry(frame, textvariable=username_var, width=30, font=('Calibri', 10)).pack(side='top', pady=(10, 40))

    tk.Label(frame, text='Password', font=('Calibri', 15)).pack(side='top')
    tk.Entry(frame, textvariable=password_var, width=30, show='*', font=('Calibri', 10)).pack(side='top', pady=(10, 40))

    tk.Button(
        frame,
        text='Create Account',
        command=lambda: start_window(frame,
                                     root,
                                     lambda frame, root: create_account_window(frame, root, login_client))
    ).pack(side='top', pady=10)

    tk.Button(
        frame,
        text='Done',
        command=lambda: validate_login(login_client, username_var.get(), password_var.get(), frame, root)
        ).pack(side='top', pady=10)
    
    frame.mainloop()
    

def main():
    root = Tk()
    root.title('JigsApp')
    root.geometry('500x500')


    frame = Frame(master=root)
    frame.pack(fill='both')

    login_client = LoginClient('contact.db')
    login_client.connect()

    login_window(frame, root, login_client)


    login_client.disconnect()


if __name__ == '__main__':
    main()
from tkinter import *
from tkinter import ttk

CONTACT_WINDOW_DIMENSIONS = (400, 200)
MESSAGE_WRITE_WINDOW_DIMENSIONS = (400, 250)


message = ''
button_pressed = ''

def reduce_text(text: str, char_limit=50) -> str:
    
    lines = []
    words = []
    for word in text.split():
        words.append(word)
        if len(' '.join(words)) > char_limit:
            words.pop()
            lines.append(' '.join(words))
            words = [word]

        else:
            words.append(word)

    lines.append(' '.join(words))
    return '\n'.join(lines)

       

def MessageWriteWindow(message_reciever: str) -> (str, str):
    '''Asks the user to input a message and returns a tuple with archive / send as 0th element and the message as the second element.'''

    global message, button_pressed
    message = ''
    button_pressed = ''

    root = Tk()

    root.title("New Message to " + message_reciever)
    root.geometry(f"{MESSAGE_WRITE_WINDOW_DIMENSIONS[0]}x{MESSAGE_WRITE_WINDOW_DIMENSIONS[1]}")
    root.resizable(False,False)


    textbox = Text(root, width=20, height=5)
    textbox.place(x=120, y=0)


    def archive_action():
        global message, button_pressed
        message = textbox.get("1.0","end-1c")
        button_pressed = 'archive'
        root.destroy()

    def send_action():
        global message, button_pressed
        message = textbox.get("1.0","end-1c")
        button_pressed = 'send'
        root.destroy()
        


    Button(root, text="Archived Messages", command=archive_action).place(x=50, y=200)
    Button(root, text = 'Send Message', command=send_action).place(x=200, y=200)






    root.mainloop()

    return (button_pressed, message)



def ContactsWindow(contacts: list) -> str:
    '''Prompts the user to choose a contact and returns selected.'''

    def click_action():
        text = clicked.get()
        label.config( text = text )
        MessageWriteWindow(text)

    root = Tk()
    root.title("Contact Selection")
    root.geometry(f"{CONTACT_WINDOW_DIMENSIONS[0]}x{CONTACT_WINDOW_DIMENSIONS[1]}")




    clicked=StringVar()
    Button( root , text = "Compose Message", command = click_action).pack()
    label = Label( root , text = " ")
    label.pack()

    clicked.set( contacts[0] )

    drop = OptionMenu(root , clicked , *contacts)
    drop.pack()

    root.mainloop()




def MessageViewerWindow(messages: list):
    messages = list(map(reduce_text, messages))
    root = Tk()
    root.title('Message Viewer')
    root.resizable(False,False)

    main_frame = Frame(root)
    main_frame.pack(fill = BOTH, expand=1 )

    canvas = Canvas(main_frame)
    canvas.pack(side = LEFT, fill = BOTH, expand=1 )



    # #create scroll bars
    # horizon = ttk.Scrollbar(main_frame, orient=HORIZONTAL, command=canvas.xview)
    # horizon.pack(side = RIGHT, fill=X)
    vertical = ttk.Scrollbar(main_frame, orient=VERTICAL, command = canvas.yview)
    vertical.pack(side = RIGHT, fill=Y)

    # #configure canvas things you know how it is
    # canvas.configure(xscrollcommand = horizon.set)
    # canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
    canvas.configure(yscrollcommand=vertical.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

    # frame = Frame(canvas)

    # canvas.create_window((0,0), window=frame, anchor="nw")


    # file = open(username+"_"+destination_user+".txt","r")
    # global filename
    # filename = (username+"_"+destination_user+".txt")
    # contents = file.read()
    # file.close()
    # canvas.create_text(1, 1, text=contents , anchor='nw', font='TkMenuFont', fill='black')



    canvas.create_text(1, 1, text='\n\n'.join(messages) , anchor='nw', font='TkMenuFont', fill='black')

    root.mainloop()

#print (MessageViewerWindow(['fhue 9frohuidh duifweh fuiweo hdsuiofhdsf ewhui oyfewuhf wi fhoufiweh uoeuuiweodhfudsiof sdhufi odsofh dsiufe hiwu owe']))
#print (reduce_text('d hasiodfifdofjsaif osdjfdi odpjsifdsofjdif dso pfjdsif osdf jsdiop fdsjf idsp'))

# print (ContactsWindow(['contact1', 'contact2', 'contact3']))

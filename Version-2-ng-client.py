# import required modules
import json
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 8478

BLACK = ("#1874CD")
PINK = ("#104E8B")
RED = ("#7D9EC0")
WHITE = ("white")
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 12)

# Creating a socket object
# AF_INET: we are going to use IPv4 addresses
# SOCK_STREAM: we are using TCP packets for communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define a dictionary for unfamiliar words and their descriptions
word_definitions = {
    "Bamboozled": "thrown into a state of confusion or bewilderment especially by being deliberately fooled or misled",
    "Pursuant": "in conformity with",
    "Aggregate": "to collect or gather",
    "Cacophony": "a harsh mixture of sound",
    "Sanctimony": "hypocritical religious devotion or righteousness",
    "Verisimilitude":"something merely seems to be true or real",
    "Bibble": "to drink often, to eat and or/ drink noisily",
    "Obdurate": "stubbornly persistent in wrongdoing",
    "tbh": "To be honest",
    "Feigned": "Not genuine or real",
    "Venerate": "to honor",
    "Aberrant": "deviating from the usual or natural type",
    "Deviating": "to stray especially from a standard, principle, or topic",
    "Pragmatic": "relating to matters of fact or practical affairs often to the exclusion of intellectual or artistic matters",
    "Equivocal": "uncertain",
    "Jabber": "to talk in a noisy or excited manner",
    "Jostle": "make one's way by pushing or shoving",
    "Impeccable": "Flawless",
    "Mallleable": "easily influenced",
    "Aggrandize": "enhanced power",
    "Beguile": "influence others",
    "Fatuous": "devoid of intelligence",
    "Iconoclast": "someone who criticize",
    "Inveterate": "habitual",
    "inveterate": "habitual",
    "Pejorative": "showing disapproval",
    "Travesty": "imitation",
    "Brusque": "unfriendly",
    "Sanguine": "confidently optimistic and cheerful",
    "Bereft": "deprived or robbed of the possession or use of something",
    "Agastopia": "express facination or love",
    "Thwart": "to oppose successfully",
    "Myopic": "lacking in foresight, or discernment",
    "Muesli": "a breakfast cereal",
    "Flummox": "Confuse",
    "Noxious": "physical harmful or destructive to living beings",
    "Behoove": "to be necessary or proper",
    "Burgeon": "to grow or expand rapidly",
    "Convivial": " relating to, occupied with, or fond of feasting, drinking, and good company",
    "Effete": "having lost character, vitality, or strength",
    "Galvanize": "to stimulate or excite as if by an electric shock",
    "Melange" : "a mixture often of incongruous elements",
    "Obfuscate": "to throw into shadow",
    "ineffable": "incapable of being expressed in words",
    "pulchritudinuos": "Beautiful",
    "Catastrophic": "a momentous tragic event ranging from extreme misfortune to utter overthrow or ruin",
    
        # Add more unfamiliar words and their descriptions as needed
}

def add_message_with_definition(message):
    # Check if the message contains an unfamiliar word
    words = message.split()
    for word in words:
        # If the word is unfamiliar, replace it with the description
        if word in word_definitions:
            message = message.replace(word, f"{word} ({word_definitions[word]})")
    # Add the modified message to the message box
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    # try except block
    try:

        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Succesfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")


    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username","Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
   
 def send_message():
    message = message_textbox.get()
    username = username_textbox.get()
    if message != '' and username != '':
        data = {'username': username, 'content': message}
        client.sendall(json.dumps(data).encode())
        message_textbox.delete(0, tk.END)
    else:
        messagebox.showerror("Empty message", "Message or username cannot be empty")
root = tk.Tk()
root.geometry("900x600")
root.title("AICE")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=3)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame = tk.Frame(root, width=900, height=150, bg=BLACK)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=900, height=300, bg=PINK) 
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=900, height=150, bg=BLACK) 
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg= BLACK, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame,  font=FONT, bg=BLACK, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=RED, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=PINK, fg=WHITE, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=RED, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=7)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=PINK, fg=WHITE, width=90, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("-")[0]
            content = message.split('-')[1]
            full_message = f"[{username}] {content}"
            # Add the message with word definitions to the message box
            add_message_with_definition(full_message)
        else:
            messagebox.showerror("Error","Message received from server is empty")

# main function
def main():

    root.mainloop()


if __name__ == '__main__':
    main()
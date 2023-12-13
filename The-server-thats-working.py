from flask import Flask, render_template
from flask_socketio import SocketIO, send
import socket
import threading


app = Flask(__name__)
socketio = SocketIO(app)
socketio.init_app(app)


HOST = '127.0.0.1'
PORT = 8478 # You can use any port between 0 to 65535
LISTENER_LIMIT = 10
active_clients = [] # List of all currently connected users

# Function to listen for upcoming messages from a client
# Define a dictionary for unfamiliar words and their descriptions
word_definitions = {
    "unfamiliar_word_1": "Description of unfamiliar_word_1",
    "unfamiliar_word_2": "Description of unfamiliar_word_2",
    # Add more unfamiliar words and their descriptions as needed
}

def replace_unfamiliar_words(message):
    # Check if the message contains an unfamiliar word
    words = message.split()
    for word in words:
        # If the word is unfamiliar, replace it with the description
        if word in word_definitions:
            message = message.replace(word, f"{word} ({word_definitions[word]})")
    return message

def listen_for_messages(client, username):
    while True:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '-' + replace_unfamiliar_words(message)  # Replace unfamiliar words with descriptions
            send_messages_to_all(username, final_msg)
        else:
            print(f"The message sent from client {username} is empty")

#Define your routes

@app.route('/')
def index():
    return render_template('Jc.html')

@app.route('/chat')
def chat():
    return render_template('HTML.html')

@app.route('/about')
def about():
    return render_template('About us.html')


@socketio.on('message')
def handle_message(message):
    # Handle messages received from the client
    print('Received message:', message)
    # Broadcast the message to all clients
    socketio.emit('message', message)

# Function to send message to a single client
def send_message_to_client(client, message):

    client.sendall(message.encode())

# Function to send any new message to all the clients that
# are currently connected to this server
def send_messages_to_all(from_username, message):
    
    for user in active_clients:

        send_message_to_client(user[1], message)

# Function to handle client
def client_handler(client):
    
    # Server will listen for client message that will
    # Contain the username
    while 1:

        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

# - Main-function
def main():

    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Creating a try catch block
    try:
        # Provide the server with an address in the form of
        # host IP and port
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"unable to bind to host{HOST} and port{PORT}")

    # Set server limit
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections
    while 1:

        client, address = server.accept()
        print(f"Succesfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()  # Call the main function to start the server
    socketio.run(app, host='0.0.0.0', port=PORT, debug=True)  # Run the Flask app with SocketIO

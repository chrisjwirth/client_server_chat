import socket

from server_helpers import GameManager
from socket_helpers import send_data, receive_data


class Server:
    HOST = "localhost"
    PORT = 8000
    
    def __init__(self):
        self.print_instructions = True

    def run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST, self.PORT))
            s.listen()

            print(f"Server listening on: {self.HOST} on port: {self.PORT}")
            connection, address = s.accept()

            with connection as c:
                print(f"Connected by {address}")
                print("Waiting for message...")

                while True:
                    message = receive_data(c)
                    if not message:
                        break
                    elif message == "GAME":
                        GameManager(c).initialize_game()
                        break
                    else:
                        print(message)
                        self.__print_instructions()
                        reply = input("> ")
                        if reply == "/q":
                            break
                        send_data(c, reply)

    def __print_instructions(self):
        if self.print_instructions:
            print("Type /q to quit")
            print("Enter message to send...")
            self.print_instructions = False


if __name__ == "__main__":
    Server().run_server()


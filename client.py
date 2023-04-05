import socket

from socket_helpers import send_data, receive_data


class Client:
    HOST = "localhost"
    PORT = 8000

    def run_client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))

            print(f"Connected to {self.HOST} on port: {self.PORT}")
            print("Type /q to quit")
            print("Enter message to send...or enter GAME to start a game of hangman")

            while True:
                message = input("> ")
                if message == "/q":
                    break
                send_data(s, message)

                reply = receive_data(s)
                if not reply:
                    break
                print(f"{reply}")

                if reply.startswith("Game Over."):
                    break


if __name__ == "__main__":
    Client().run_client()


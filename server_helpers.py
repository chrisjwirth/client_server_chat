from hangman import Hangman
from socket_helpers import send_data, receive_data


class GameManager:
    def __init__(self, connection):
        self.connection = connection

    def initialize_game(self):
        self.__initialize_hangman()

    def __initialize_hangman(self):
        word_to_guess = self.__get_hangman_word()
        if not word_to_guess:
            return
        
        self.hangman = Hangman(word_to_guess)

        instructions = (
            f"Your opponent has determined the word you need to guess.\n"
            f"Please guess a single letter at a time.\n\n"
            f"{self.hangman.game_status()}"
        )
        send_data(self.connection, instructions)

        self.__play_hangman()
    
    def __play_hangman(self):
        game_in_progress = True

        while game_in_progress:
            guess = receive_data(self.connection)
            if not guess:
                break

            print(f"Received guess: {guess}")

            valid_guess = self.hangman.guess_letter(guess)
            game_status = self.hangman.game_status()
            if valid_guess:
                print(f"{game_status}\n")
                reply = game_status
            else:
                print("The guess was invalid!")
                reply = (
                    f"Invalid guess! Please provide a single un-guessed letter.\n"
                    f"{game_status}"
                )

            send_data(self.connection, reply)
            game_in_progress = self.hangman.game_in_progress()

    @staticmethod
    def __get_hangman_word():
        instructions = (
            "A game of hangman has been started.\n"
            "What word should your opponent attempt to guess?\n"
            "Type /q to quit\n"
            "> "
        )
        
        word_to_guess = input(instructions)
        return word_to_guess if word_to_guess != "/q" else False


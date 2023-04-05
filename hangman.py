from enum import Enum


class Hangman:
    hangman_ascii = [
        ":)",
        " O",
        " O\n |",
        " O\n/|",
        " O\n/|\\",
        " O\n/|\\\n/",
        " O\n/|\\\n/ \\"
    ]

    class GameState(Enum):
        STARTING = "STARTING"
        IN_PROGRESS = "IN_PROGRESS"
        PLAYER_WON = "PLAYER_WON"
        PLAYER_LOST = "PLAYER_LOST"

    def __init__(self, word_to_guess):
        self.word_to_guess = word_to_guess.upper()
        self.incorrect_guesses = 0
        self.guessed_letters = set()
        self.remaining_letters = set()
        self.game_state = self.GameState.STARTING
        for letter in self.word_to_guess:
            self.remaining_letters.add(letter)

    def game_in_progress(self):
        return self.game_state in (self.GameState.STARTING, self.GameState.IN_PROGRESS)

    def game_status(self):
        hangman_board = f"---\n{self.hangman_ascii[self.incorrect_guesses]}\n---"

        guesses = f"Guessed: "
        for letter in sorted(self.guessed_letters):
            guesses += f"{letter} "

        word = "Word: "
        for letter in self.word_to_guess:
            word += "_ " if letter in self.remaining_letters else f"{letter} "

        if self.game_state == self.GameState.PLAYER_WON:
            return f"Game Over. Word Guessed!\n{hangman_board}\n{word}\n"
        elif self.game_state == self.GameState.PLAYER_LOST:
            return f"Game Over. Word Not Guessed\n{hangman_board}\n{guesses}\n{word}\n"
        elif self.game_state == self.GameState.IN_PROGRESS:
            return f"{hangman_board}\n{guesses}\n{word}\n"
        else:
            return f"{word}\n"

    def guess_letter(self, letter):
        letter = letter.upper()

        if len(letter) > 1 or letter in self.guessed_letters:
            return False

        self.guessed_letters.add(letter)

        if letter in self.remaining_letters:
            self.remaining_letters.remove(letter)
        else:
            self.incorrect_guesses += 1

        self.__update_game_state()
        return True

    def __update_game_state(self):
        if len(self.remaining_letters) == 0:
            self.game_state = self.GameState.PLAYER_WON
        elif self.incorrect_guesses == len(self.hangman_ascii) - 1:
            self.game_state = self.GameState.PLAYER_LOST
        else:
            self.game_state = self.GameState.IN_PROGRESS


import random

# Hangman stages: 0 mistakes means the gallows is empty; 6 means game over.
HANGMAN_PICS = [
    r"""
     +---+
     |   |
         |
         |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
         |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
     |   |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
    =========
""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
    =========
""",
]

WORDS = [
    "python", "computer", "keyboard", "program", "developer",
    "function", "variable", "internet", "hangman", "database",
    "school", "garden", "rainbow", "journey", "elephant",
    "chocolate", "hospital", "mountain", "language", "notebook",
]


def choose_word():
    """Return a randomly selected word."""
    return random.choice(WORDS).lower()


def display_game(secret_word, guessed_letters, wrong_guesses):
    """Display the gallows, masked word, and guessed letters."""
    print(HANGMAN_PICS[wrong_guesses])

    masked_word = " ".join(
        letter.upper() if letter in guessed_letters else "_"
        for letter in secret_word
    )
    print("Word:              ", masked_word)

    if guessed_letters:
        print("Guessed letters:   ", " ".join(sorted(guessed_letters)).upper())
    else:
        print("Guessed letters:    (none)")

    print(f"Attempts remaining: {6 - wrong_guesses}")


def get_guess(guessed_letters):
    """Ask until the player enters one valid, new letter."""
    while True:
        guess = input("\nGuess a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter exactly one letter (A-Z).")
        elif guess in guessed_letters:
            print(f"You already guessed '{guess.upper()}'. Try another letter.")
        else:
            return guess


def play_game():
    """Run one complete game of Hangman."""
    secret_word = choose_word()
    guessed_letters = set()
    wrong_guesses = 0
    max_attempts = 6

    print("\n========== HANGMAN ==========")
    print("Guess the hidden word one letter at a time.")
    print(f"You have {max_attempts} incorrect guesses available.")

    while wrong_guesses < max_attempts:
        display_game(secret_word, guessed_letters, wrong_guesses)

        # A set prevents duplicate letters and makes checking easy.
        if all(letter in guessed_letters for letter in secret_word):
            print("\n" + "=" * 30)
            print("🎉 YOU WIN! 🎉")
            print(f"The word was: {secret_word.upper()}")
            print("=" * 30)
            return

        guess = get_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in secret_word:
            print(f"Good guess! '{guess.upper()}' is in the word.")
        else:
            wrong_guesses += 1
            print(f"Sorry! '{guess.upper()}' is not in the word.")

    display_game(secret_word, guessed_letters, wrong_guesses)
    print("\n" + "=" * 30)
    print("GAME OVER — YOU LOSE!")
    print(f"The correct word was: {secret_word.upper()}")
    print("=" * 30)


def main():
    """Start games until the player chooses to quit."""
    while True:
        play_game()
        again = input("\nWould you like to play again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("\nThanks for playing Hangman. Goodbye!")
            break


if __name__ == "__main__":
    main()

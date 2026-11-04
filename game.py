
import random

from wordle import (words, get_feedback, filter_words, recommend_by_entropy)


def play_game():
    answer = random.choice(words)
    possible_words = words.copy()

    print("Welcome to Wordle!")
    print("You have 6 attempts to guess the word.")
    print("G = Green, Y = Yellow, X = Gray")

    for attempt in range(1, 7):
        print(f"\n--- Attempt {attempt}/6 ---")

        recommendation = recommend_by_entropy(possible_words, words, max_candidates=100)
        print(f"Solver recommendation: {recommendation}")

        guess = input("Enter your guess: ").upper()

        if len(guess) != 5 or not guess.isalpha():
            print("Please enter a valid 5-letter word.")
            continue

        feedback = get_feedback(guess, answer)

        symbols = {
            "green": "🟩",
            "yellow": "🟨",
            "gray": "⬛"
        }

        display = "".join(symbols[color] for color in feedback)
        print(f"{guess}: {display}")

        if guess == answer:
            print(f"\nCongratulations! You solved it in {attempt} attempts!")
            return

        possible_words = filter_words(
            possible_words, guess, feedback
        )

        print(f"Remaining possible answers: {len(possible_words)}")

    print(f"\nGame over! The answer was {answer}.")


if __name__ == "__main__":
    play_game()

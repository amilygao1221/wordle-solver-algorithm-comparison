
from functools import lru_cache

# Step 1: Generate Wordle feedback
def get_feedback(guess, answer):
    feedback = ["gray"] * len(guess)
    remaining = list(answer)

    # Pass 1: Find green letters
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            feedback[i] = "green"
            remaining[i] = None

    # Pass 2: Find yellow letters
    for i in range(len(guess)):
        if feedback[i] == "green":
            continue

        if guess[i] in remaining:
            feedback[i] = "yellow"
            remaining.remove(guess[i])

    return feedback


#缓存
@lru_cache(maxsize=200000)
def get_feedback_cached(guess, answer):
    return tuple(get_feedback(guess, answer))


# Step 2: Create a word list
from pathlib import Path

word_file = Path(__file__).with_name("words.txt")

with open(word_file, "r", encoding="utf-8") as file:
    words = [
        line.strip().upper()
        for line in file
        if len(line.strip()) == 5 and line.strip().isalpha()
    ]


# Step 3: Filter possible answers
def filter_words(words, guess, feedback):
    possible = []

    for word in words:
        if get_feedback(guess, word) == feedback:
            possible.append(word)

    return possible

def recommend_word(possible_words):
    if not possible_words:
        return None

    letter_frequency = {}

    # Count how many candidate words contain each letter
    for word in possible_words:
        for letter in set(word):
            letter_frequency[letter] = (
                letter_frequency.get(letter, 0) + 1
            )

    best_word = None
    best_score = -1

    # Score each candidate word
    for word in possible_words:
        score = sum(
            letter_frequency[letter]
            for letter in set(word)
        )

        if score > best_score:
            best_score = score
            best_word = word

    return best_word



#Entropy
import math
from collections import Counter


def calculate_entropy(guess, possible_words):
    if not possible_words:
        return 0.0

    patterns = []

    for answer in possible_words:
        pattern = get_feedback_cached(guess, answer)
        patterns.append(pattern)

    counts = Counter(patterns)
    total = len(possible_words)

    entropy = 0.0

    for count in counts.values():
        probability = count / total
        entropy -= probability * math.log2(probability)

    return entropy



def recommend_by_entropy(possible_words, allowed_guesses,
                         max_candidates=100):

    if not possible_words:
        return None

    if len(possible_words) == 1:
        return possible_words[0]

    guesses = allowed_guesses[:max_candidates]
    guesses = list(dict.fromkeys(guesses + possible_words))

    possible_set = set(possible_words)

    best_word = None
    best_entropy = -1

    # Maximum theoretically possible entropy
    max_entropy = math.log2(len(possible_words))

    for guess in guesses:
        entropy = calculate_entropy(guess, possible_words)

        if entropy > best_entropy + 1e-10:
            best_entropy = entropy
            best_word = guess

        elif abs(entropy - best_entropy) <= 1e-10:
            if guess in possible_set and best_word not in possible_set:
                best_word = guess

        # Stop only when the maximum entropy is achieved
        # AND the guess is a possible answer
        if (
            best_entropy >= max_entropy - 1e-10
            and best_word in possible_set
        ):
            break

    return best_word





# Step 4: Multi-round Original Wordle Solver Loop
def run_solver():
    color_map = {
        "g": "green",
        "y": "yellow",
        "x": "gray"
    }

    possible_words = words.copy()
    round_number = 1

    while True:
        print(f"\n--- Round {round_number} ---")
        print(f"Remaining possible words: {len(possible_words)}")

        recommendation = recommend_word(possible_words)
        print(f"Recommended next guess: {recommendation}")

        guess = input("Enter your guess (or 'quit' to exit): ").upper()

        if guess == "QUIT":
            break

        if len(guess) != 5 or not guess.isalpha():
            print("Please enter a valid 5-letter word.")
            continue

        feedback_input = input(
            "Enter feedback (g=green, y=yellow, x=gray): "
        ).lower()

        if len(feedback_input) != 5 or any(
            c not in color_map for c in feedback_input
        ):
            print("Invalid feedback.")
            continue

        feedback = [color_map[c] for c in feedback_input]

        possible_words = filter_words(
            possible_words, guess, feedback
        )

        print("Possible answers:", possible_words)

        if feedback_input == "ggggg":
            print("Word solved!")
            break

        if not possible_words:
            print("No matching words found.")
            break

        round_number += 1


if __name__ == "__main__":
    test_words = ["TRACE", "CRATE", "SLATE", "STARE"]

    print(
        "Entropy of TRACE:",
        calculate_entropy("TRACE", test_words)
    )

    print(
        "Best guess:",
        recommend_by_entropy(test_words, test_words)
    )

    # Uncomment this when you want to use the original solver
    # run_solver()
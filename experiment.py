
import random
import time
import statistics

from wordle import (
    words,
    get_feedback,
    filter_words,
    recommend_word,
    recommend_by_entropy
)


DICTIONARY_SIZES = [100, 500, 1000]
NUM_GAMES = 50
SEED = 42


def play_game(answer, strategy, word_list):
    possible_words = word_list.copy()

    for attempt in range(1, 7):

        if strategy == "frequency":
            guess = recommend_word(possible_words)

        elif strategy == "entropy":
            guess = recommend_by_entropy(
                possible_words,
                word_list,
                max_candidates=100
            )

        else:
            raise ValueError("Unknown strategy")

        if guess is None:
            return 7

        if guess == answer:
            return attempt

        feedback = get_feedback(guess, answer)

        possible_words = filter_words(
            possible_words,
            guess,
            feedback
        )

    return 7


def evaluate_strategy(strategy, word_list, answers):
    guesses = []

    start_time = time.perf_counter()

    for answer in answers:
        attempts = play_game(answer, strategy, word_list)
        guesses.append(attempts)

    runtime = time.perf_counter() - start_time

    wins = [g for g in guesses if g <= 6]

    return {
        "strategy": strategy,
        "dictionary_size": len(word_list),
        "games": len(answers),
        "win_rate": len(wins) / len(answers),
        "avg_guesses": (
            statistics.mean(wins) if wins else None
        ),
        "runtime": runtime
    }


def run_experiment():
    rng = random.Random(SEED)
    results = []

    for size in DICTIONARY_SIZES:
        print(f"\nTesting dictionary size: {size}")

        word_list = rng.sample(words, size)
        answers = rng.sample(word_list, NUM_GAMES)

        for strategy in ["frequency", "entropy"]:
            result = evaluate_strategy(
                strategy, word_list, answers
            )

            results.append(result)

            print(
                f"{strategy.upper():10s} | "
                f"Win Rate: {result['win_rate']:.1%} | "
                f"Avg Guesses: {result['avg_guesses']} | "
                f"Runtime: {result['runtime']:.2f}s"
            )

    return results


if __name__ == "__main__":
    results = run_experiment()

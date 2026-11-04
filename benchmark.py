
import random
import time

from wordle import (
    words,
    get_feedback,
    filter_words,
    recommend_word,
    recommend_by_entropy
)


def play_with_solver(answer, strategy, word_list):
    possible_words = word_list.copy()

    for attempt in range(1, 7):
        if strategy == "frequency":
            guess = recommend_word(possible_words)
        else:
            guess = recommend_by_entropy(
                possible_words,
                word_list,
                max_candidates=100
            )

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

    return 7  # Failed to solve within 6 guesses


def run_benchmark():
    random.seed(42)

    # Start with a small dictionary for speed
    word_list = random.sample(words, min(100, len(words)))

    # Same answers for both strategies
    answers = random.sample(word_list, min(50, len(word_list)))

    results = {}

    for strategy in ["frequency", "entropy"]:
        guesses = []

        start = time.perf_counter()

        for answer in answers:
            count = play_with_solver(
                answer, strategy, word_list
            )
            guesses.append(count)

        runtime = time.perf_counter() - start

        wins = [g for g in guesses if g <= 6]

        results[strategy] = {
            "win_rate": len(wins) / len(guesses),
            "avg_guesses": (
                sum(wins) / len(wins) if wins else None
            ),
            "runtime": runtime
        }

    for strategy, metrics in results.items():
        print(f"\n--- {strategy.upper()} ---")
        print(f"Win rate: {metrics['win_rate']:.1%}")
        print(f"Average guesses (wins only): {metrics['avg_guesses']}")
        print(f"Total runtime: {metrics['runtime']:.2f} seconds")


if __name__ == "__main__":
    run_benchmark()

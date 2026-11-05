
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv")

# Figure 1: Average guesses
plt.figure(figsize=(8, 5))

for strategy in ["frequency", "entropy"]:
    subset = df[df["strategy"] == strategy]

    plt.plot(
        subset["dictionary_size"],
        subset["avg_guesses"],
        marker="o",
        label=strategy.capitalize()
    )

plt.xlabel("Dictionary Size")
plt.ylabel("Average Guesses")
plt.title("Wordle Solver: Guessing Efficiency")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("guessing_efficiency.png", dpi=200)
plt.show()


# Figure 2: Runtime
plt.figure(figsize=(8, 5))

for strategy in ["frequency", "entropy"]:
    subset = df[df["strategy"] == strategy]

    plt.plot(
        subset["dictionary_size"],
        subset["runtime"],
        marker="o",
        label=strategy.capitalize()
    )

plt.xlabel("Dictionary Size")
plt.ylabel("Runtime (seconds, log scale)")
plt.yscale("log")
plt.title("Wordle Solver: Computational Cost")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("runtime_comparison.png", dpi=200)
plt.show()

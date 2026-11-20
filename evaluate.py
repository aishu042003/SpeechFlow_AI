
import argparse
import re
from pathlib import Path


def normalize(text):
    return re.findall(r"\w+", text.lower())


def word_error_rate(reference, hypothesis):
    ref = normalize(reference)
    hyp = normalize(hypothesis)

    if not ref:
        return 0.0 if not hyp else 1.0

    previous = list(range(len(hyp) + 1))

    for i, ref_word in enumerate(ref, start=1):
        current = [i] + [0] * len(hyp)

        for j, hyp_word in enumerate(hyp, start=1):
            substitution = previous[j - 1] + (
                ref_word != hyp_word
            )
            insertion = current[j - 1] + 1
            deletion = previous[j] + 1

            current[j] = min(
                substitution,
                insertion,
                deletion
            )

        previous = current

    return previous[-1] / len(ref)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="SpeechFlow AI - Word Error Rate Evaluation"
    )

    parser.add_argument("reference")
    parser.add_argument("hypothesis")

    args = parser.parse_args()

    reference = Path(args.reference).read_text(
        encoding="utf-8"
    )

    hypothesis = Path(args.hypothesis).read_text(
        encoding="utf-8"
    )

    result = word_error_rate(reference, hypothesis)

    print(f"Word Error Rate: {result:.3f}")
    print(f"Accuracy: {max(0, 1 - result) * 100:.2f}%")

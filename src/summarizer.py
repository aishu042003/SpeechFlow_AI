import re
from collections import Counter

STOPWORDS = set(
    "the a an and or but if then is are was were to of in on for with "
    "this that it as at by from".split()
)

def summarize_text(text, max_sentences=4):
    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text.strip())
        if sentence.strip()
    ]
    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    all_words = re.findall(r"\w+", text.lower())
    frequencies = Counter(
        word for word in all_words
        if word not in STOPWORDS and len(word) > 2
    )

    scored = []
    for index, sentence in enumerate(sentences):
        tokens = re.findall(r"\w+", sentence.lower())
        score = sum(frequencies[token] for token in tokens) / max(len(tokens), 1)
        scored.append((score, index, sentence))

    selected = sorted(scored, reverse=True)[:max_sentences]
    selected.sort(key=lambda item: item[1])
    return " ".join(item[2] for item in selected)
import re
from collections import Counter

def analyze_conversation(text, segments=None):
    words = re.findall(r"\b[\w']+\b", text)
    sentences = [
        sentence for sentence in re.split(r"(?<=[.!?])\s+", text.strip())
        if sentence
    ]

    duration_seconds = 0.0
    if segments:
        duration_seconds = max(
            (float(segment.get("end", 0)) for segment in segments),
            default=0.0,
        )

    duration_minutes = duration_seconds / 60
    frequent = Counter(word.lower() for word in words if len(word) > 3)

    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "estimated_duration_seconds": round(duration_seconds, 2),
        "words_per_minute": round(len(words) / duration_minutes, 1) if duration_minutes else None,
        "frequent_words": [
            {"word": word, "count": count}
            for word, count in frequent.most_common(10)
        ],
    }
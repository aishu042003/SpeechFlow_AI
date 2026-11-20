"""Keyword-based text tone estimate; this is not vocal emotion recognition."""
KEYWORDS = {
    "positive": {"happy", "great", "good", "excellent", "love", "wonderful", "thanks", "thank"},
    "negative": {"sad", "angry", "bad", "terrible", "hate", "worried", "upset", "fear"},
    "uncertain": {"maybe", "perhaps", "unsure", "possibly", "think", "might"},
}

def analyze_emotion(text):
    words = {word.strip(".,!?;:").lower() for word in text.split()}
    scores = {label: len(words.intersection(terms)) for label, terms in KEYWORDS.items()}

    if not any(scores.values()):
        tone = "neutral_or_unclear"
    else:
        tone = max(scores, key=scores.get)

    return {
        "estimated_tone": tone,
        "keyword_matches": scores,
        "notice": "Approximate text heuristic only; it does not identify a person's actual feelings.",
    }
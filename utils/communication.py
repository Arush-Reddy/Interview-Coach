import re


FILLER_PHRASES = ("you know", "i mean", "kind of", "sort of", "um", "uh", "like", "actually", "basically")


def analyze_communication(answer, duration_seconds=None):
    """Count filler phrases and estimate a simple communication score."""
    normalized_answer = answer.lower()
    filler_counts = {
        phrase: len(re.findall(rf"\b{re.escape(phrase)}\b", normalized_answer))
        for phrase in FILLER_PHRASES
    }
    filler_counts = {phrase: count for phrase, count in filler_counts.items() if count}

    words = re.findall(r"\b[\w'-]+\b", answer)
    word_count = len(words)
    total_fillers = sum(filler_counts.values())
    communication_score = max(1, round(10 - min(total_fillers * 0.5, 5)))

    words_per_minute = None
    if duration_seconds and duration_seconds > 0:
        words_per_minute = round(word_count / duration_seconds * 60)
        if words_per_minute < 90 or words_per_minute > 190:
            communication_score = max(1, communication_score - 1)

    return {
        "word_count": word_count,
        "filler_counts": filler_counts,
        "total_fillers": total_fillers,
        "communication_score": communication_score,
        "words_per_minute": words_per_minute,
    }

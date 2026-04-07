"""
sentiment_service.py

Core sentiment analysis logic.

Features:
- Sentence-level analysis
- Multi-language support via translation (non-EN → EN)
- Aggregated sentiment metrics
- Volatility calculation
"""

from typing import List, Dict
import re

from textblob import TextBlob
from deep_translator import GoogleTranslator


# =========================================================
# TRANSLATION
# =========================================================

def translate_to_en(text: str, source_lang: str) -> str:
    """
    Translate text to English using GoogleTranslator.

    Fallback: returns original text if translation fails.

    Args:
        text (str): Input text
        source_lang (str): Language code (e.g., 'de', 'es')

    Returns:
        str: Translated text (or original if error)
    """
    try:
        return GoogleTranslator(
            source=source_lang.lower(),
            target="en"
        ).translate(text)
    except Exception:
        return text


# =========================================================
# MAIN ANALYSIS
# =========================================================

def analyze_sentiment(text: str, language: str) -> Dict:
    """
    Perform sentiment analysis on input text.

    Pipeline:
    - Split into sentences
    - Translate if needed
    - Analyze each sentence
    - Aggregate results

    Args:
        text (str): Input text
        language (str): Language code (EN, DE, etc.)

    Returns:
        dict: Structured sentiment analysis result
    """

    text = text.strip()

    if not text:
        return {"ok": False, "error": "No text was provided."}

    sentences = split_into_sentences(text)

    if not sentences:
        return {"ok": False, "error": "No valid sentences were found."}

    sentence_results = []
    polarities = []

    for idx, sentence in enumerate(sentences, start=1):

        if language == "EN":
            text_for_analysis = sentence
        else:
            text_for_analysis = translate_to_en(sentence, language)

        polarity = TextBlob(text_for_analysis).sentiment.polarity
        label = get_sentiment_label(polarity)

        sentence_results.append({
            "index": idx,
            "sentence": sentence,
            "translated": text_for_analysis,
            "polarity": round(polarity, 3),
            "label": label,
        })

        polarities.append(polarity)

    # =========================================================
    # GLOBAL METRICS
    # =========================================================

    global_polarity = sum(polarities) / len(polarities)
    global_label = get_sentiment_label(global_polarity)

    positive_count = sum(1 for s in sentence_results if s["label"] == "positive")
    neutral_count = sum(1 for s in sentence_results if s["label"] == "neutral")
    negative_count = sum(1 for s in sentence_results if s["label"] == "negative")

    # =========================================================
    # VOLATILITY
    # =========================================================

    labels = [s["label"] for s in sentence_results]

    if len(labels) > 1:
        changes = sum(1 for i in range(1, len(labels)) if labels[i] != labels[i - 1])
        volatility = changes / (len(labels) - 1)
    else:
        volatility = 0

    # =========================================================
    # SUMMARY
    # =========================================================

    summary = (
        f"The overall sentiment is {global_label}. "
        f"The text contains {positive_count} positive, "
        f"{neutral_count} neutral, and {negative_count} negative sentences."
    )

    return {
        "ok": True,
        "language": language,
        "global_polarity": round(global_polarity, 3),
        "global_label": global_label,
        "summary": summary,
        "sentence_results": sentence_results,
        "counts": {
            "positive": positive_count,
            "neutral": neutral_count,
            "negative": negative_count,
        },
        "volatility": round(volatility, 2),
    }


# =========================================================
# HELPERS
# =========================================================

def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences using regex.

    Returns:
        list[str]: Clean sentence list
    """
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def get_sentiment_label(polarity: float) -> str:
    """
    Map polarity score to label.

    Returns:
        str: positive | neutral | negative
    """
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    return "neutral"
# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
# keyword_sentiment_analysis.py
"""
Keyword‑based sentiment analysis tool tuned for detecting grooming, exploitation,
and bullying language that targets children online.

Given input text, the script first scores multi‑word phrases (e.g. “our little
secret”, “send me a pic”), then single‑word tokens. Phrases and tokens are
organised into **negative** (threat / grooming / harassment), **positive**
(support / protection) and **neutral** categories.  The final sentiment is the
sign of the aggregate score.

Usage (CLI):
    python keyword_sentiment_analysis.py "Your chat transcript here"

You can import `analyze_sentiment(text)` from another Python program.

Extending keywords:  Either edit the `PHRASE_CONFIG` / `TOKEN_CONFIG` below or
pass a JSON file (`--kw my_keywords.json`) with the same structure.
"""
from __future__ import annotations
import json
import pathlib
import re
import sys
from collections import Counter
from typing import Dict, List, Tuple

# ---------------------------------------------------------------------------
# 1. KEYWORD LISTS  – weights are tuned (‑ve for harmful content, +ve protective)
# ---------------------------------------------------------------------------
PHRASE_CONFIG: Dict[str, float] = {
    # Sexual grooming & manipulation
    "our little secret": -2.0,
    "special friendship": -1.8,
    "best friends forever": -1.5,
    "i’m here for you": -1.5,
    "love you": -1.2,
    "i care about you": -1.2,
    "are you alone": -1.8,
    "do you want to be famous": -1.5,
    "want to see something cool": -1.4,
    "let me help you with that": -1.3,

    # Explicit / inappropriate language
    "wanna play a game": -1.2,
    "role‑play": -1.5,

    # Creating vulnerability
    "you’re so mature for your age": -1.8,
    "no one understands you": -1.5,
    "i won’t tell anyone": -1.7,
    "you’re the only one who gets me": -1.4,
    "they won’t believe you": -1.7,

    # Requests for personal information
    "where are you from": -1.5,
    "send me a pic": -2.0,
    "what’s your real name": -1.4,
    "can you video chat": -1.6,

    # Baiting / pressure
    "i won’t tell if you do it": -1.9,
    "prove you’re real": -1.6,
    "i’ll show you mine if you show me yours": -2.2,
    "show me more": -1.8,
    "you’re so pretty": -1.3,
    "you’re so handsome": -1.3,

    # Manipulating power dynamics
    "i’m in charge": -1.4,
    "i won’t hurt you": -1.6,
    "if you loved me, you would": -2.0,
    "everyone does it": -1.2,

    # Filter‑avoidance slang / abbreviations
    "asl": -1.0,  # age/sex/location
    "gfe": -1.2,
    "cu l8r": -0.5,
    "wyd": -0.5,
    "420": -0.5,
    "2m4u": -0.8,
    "fwb": -1.0,

    # Harassment / bullying
    "you’re ugly": -1.5,
    "no one likes you": -1.5,
    "kill yourself": -3.0,
    "nobody cares": -1.8,
    "everyone’s laughing at you": -1.7,
    "you deserve it": -1.6,
    "you asked for it": -1.6,

    # Exploiting vulnerability
    "don’t tell your parents": -2.0,
    "they’ll get mad if you tell them": -1.8,
    "it’s just a joke": -1.0,
}

TOKEN_CONFIG: Dict[str, Dict[str, float]] = {
    "positive": {
        "protect": 1.5,
        "safe": 1.2,
        "secure": 1.2,
        "rescue": 1.5,
        "support": 1.2,
        "report": 1.0,
        "trusted": 1.0,
        "education": 1.0,
        "awareness": 1.0,
    },
    "negative": {
        # Single‑word sexual or explicit terms
        "naked": -2.0,
        "undressed": -1.8,
        "sexting": -1.7,
        "pics": -1.4,
        "kissing": -1.2,
        "touching": -1.3,
        "hugs": -0.8,
        "hot": -1.0,
        "mature": -1.0,
        "teen": -1.5,
        # Generic threat terms
        "predator": -2.0,
        "groom": -1.8,
        "abuse": -1.8,
        "harm": -1.5,
        "victim": -1.2,
        "bully": -1.4,
    },
    "neutral": {
        "child": 0.0,
        "children": 0.0,
        "online": 0.0,
        "internet": 0.0,
        "law": 0.0,
    },
}

# Thresholds – tweak to make classifier stricter or looser
THRESHOLDS = {"positive": 1.0, "negative": -1.0}

# ---------------------------------------------------------------------------
# 2. HELPERS
# ---------------------------------------------------------------------------

def normalise(text: str) -> str:
    """Lower‑case the text and collapse whitespace."""
    return re.sub(r"\s+", " ", text.lower()).strip()


def phrase_score(text: str) -> Tuple[float, Counter]:
    """Score multi‑word phrases first (no overlapping counts)."""
    score = 0.0
    counts: Counter = Counter()
    remaining = text
    for phrase, weight in PHRASE_CONFIG.items():
        if phrase in remaining:
            occurrences = len(re.findall(re.escape(phrase), remaining))
            counts[phrase] = occurrences
            score += weight * occurrences
            # Remove matched phrases to avoid double‑scoring their tokens
            remaining = remaining.replace(phrase, " ")
    return score, counts, remaining


def token_score(text: str) -> Tuple[float, Counter]:
    """Score single‑word tokens after phrase removal."""
    tokens = re.findall(r"[a-zA-Z']+", text)
    score = 0.0
    counts: Counter = Counter()
    for tok in tokens:
        for cat, words in TOKEN_CONFIG.items():
            if tok in words:
                weight = words[tok]
                counts[tok] += 1
                score += weight
                break
    return score, counts


def classify(total: float) -> str:
    if total >= THRESHOLDS["positive"]:
        return "positive"
    if total <= THRESHOLDS["negative"]:
        return "negative"
    return "neutral"

# ---------------------------------------------------------------------------
# 3. PUBLIC API
# ---------------------------------------------------------------------------

def analyze_sentiment(text: str, *, debug: bool = False) -> Dict[str, object]:
    text_norm = normalise(text)
    p_score, p_counts, remainder = phrase_score(text_norm)
    t_score, t_counts = token_score(remainder)
    total = p_score + t_score
    sentiment = classify(total)
    if debug:
        print("DEBUG phrase counts:", p_counts)
        print("DEBUG token counts:", t_counts)
        print("DEBUG total score:", total)
    return {
        "sentiment": sentiment,
        "score": total,
        "phrase_hits": p_counts,
        "token_hits": t_counts,
    }

# ---------------------------------------------------------------------------
# 4. CLI ENTRY
# ---------------------------------------------------------------------------

def load_custom_keywords(path: str | pathlib.Path) -> None:
    """Merge external JSON {"phrases": {...}, "tokens": {cat: {...}}}."""
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(p)
    data = json.loads(p.read_text())
    PHRASE_CONFIG.update(data.get("phrases", {}))
    for cat, words in data.get("tokens", {}).items():
        if cat not in TOKEN_CONFIG:
            raise ValueError(f"Unknown token category {cat}")
        TOKEN_CONFIG[cat].update(words)


def main(argv: List[str] | None = None) -> None:
    argv = argv or sys.argv[1:]

    # ---------------- INTERACTIVE PROMPT MODE ----------------
    # If the user supplied no arguments, fall back to stdin prompt.
    if not argv:
        user_text = input("Enter the message to analyse: ")
        result = analyze_sentiment(user_text)
        print(json.dumps(result, indent=2))
        return  # done

    # ---------------- CLI ARGUMENT MODE ----------------------
    if "-h" in argv or "--help" in argv:
        print("Usage:
  python keyword_sentiment_analysis.py \"text to analyse\" [--debug] [--kw file.json]
  python keyword_sentiment_analysis.py            # then type message when prompted")
        sys.exit(0)

    debug = False
    if "--debug" in argv:
        debug = True
        argv.remove("--debug")

    if "--kw" in argv:
        idx = argv.index("--kw")
        kw_path = argv.pop(idx + 1)
        argv.pop(idx)
        load_custom_keywords(kw_path)

    text = " ".join(argv)
    res = analyze_sentiment(text, debug=debug)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main() "__main__":
    main()

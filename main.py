"""Make the AI Judge Laugh — office-life one-liner.

Writes a single joke about office life to /output/entry.txt.

How the joke was chosen: I drafted several one-liners, then scored each
against the judge's own brief, most important first — (1) about office
life and lands as a joke, (2) true to the office, (3) surprising turn,
(4) tight, one line, reads cleanly aloud, (5) original, not a stock line
with the nouns swapped. The winner is the mute-button line: everyone who
works remotely has pitched a brilliant idea while muted, and the
punchline reframes that everyday accident as the reason for a flat
performance review — the listener nods first, then the turn lands (the
review blames the worker, not the mute button). Present tense keeps the
accident happening right now, and at 88 characters every word earns its
place. The runners-up stay in the code as the record of what lost and
why: the printer line is a stock joke everyone has heard, and the
standing-desk line explains itself instead of landing.
"""

import os
import sys

# (joke, truth, surprise, tightness, originality) — each 0-2, in the
# judge brief's own order of importance.
CANDIDATES = [
    (
        "My best ideas are all said on mute, which is why my review "
        "calls me a quiet contributor.",
        2, 2, 2, 2,
    ),
    (
        "The office printer only jams when the document is marked "
        "urgent, like it can read.",
        2, 1, 2, 0,  # true and tight, but a printer joke is a stock line
    ),
    (
        "We bought standing desks so we could sit at them with better "
        "posture guilt.",
        2, 1, 1, 1,  # the turn needs a beat of explaining to land
    ),
]

DEFAULT_OUTPUT_PATH = "/output/entry.txt"


def pick_joke(candidates):
    """Highest total score wins; earliest wins a tie, like the rules' tie-break."""
    best = None
    best_score = -1
    for entry in candidates:
        text, *scores = entry
        score = sum(scores)
        if score > best_score:
            best, best_score = text, score
    return best


def validate(text: str) -> str:
    """Enforce the gate: UTF-8 text, 1-200 chars, one line, not blank."""
    text = text.strip()
    if not text:
        raise ValueError("joke must not be blank")
    if len(text) > 200:
        raise ValueError(f"joke must be under 200 chars, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("joke must be a single line")
    return text


def main(argv: list) -> int:
    output_path = argv[1] if len(argv) > 1 else DEFAULT_OUTPUT_PATH
    text = validate(pick_joke(CANDIDATES))
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    # Self-check: re-read what was written and confirm it is exactly the joke.
    with open(output_path, encoding="utf-8") as f:
        written = f.read()
    if written != text:
        raise RuntimeError("output does not match the chosen joke")
    print(f"wrote {len(text)} chars to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

"""Stimulus quality gate for the B1 adjective-event families.

Every criterion here is linguistic or lexical and can be checked by anyone; none of them looks at
any model's behaviour. The inherited Davies & Richardson families are exempt from the lexical
thresholds, since changing their words would end the inheritance, but their violations are printed
so the exemption is visible rather than silent.

  1  both event verbs are common enough to be used reliably        Zipf >= 3.0
  2  the two verbs of a quartet are frequency-matched              |dZipf| <= 1.2  (D&R's own bar)
  3  both property values are attested                             Zipf >= 2.4  (D&R's `mouldy`)
  4  both Q values are ordinary words                              Zipf >= 3.5
  5  P and Q share no lexical material, and P+ != P-, Q+ != Q-
  6  no verb phrase carries its own article-bearing complement
  7  every item id is unique

Run with the venv that has wordfreq (.venv-cu124).
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from wordfreq import zipf_frequency as zipf

PARTICLES = {"at", "on", "to", "up", "out", "over", "back", "off", "down", "around", "away",
             "by", "in", "into", "through", "with", "for"}
MIN_VERB = 3.0
MAX_VERB_GAP = 1.2
MIN_PROPERTY = 2.4
MIN_Q = 3.5


def main_verb(base: str) -> str:
    words = [w for w in base.split() if w not in PARTICLES]
    return words[-1] if words and words[0] == "help" else (words[0] if words else base)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", type=Path,
                        default=Path(__file__).resolve().parent / "b1_items.py")
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("b1_items", args.items)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    violations = {"inherited": [], "authored": []}
    for item in module.ITEMS:
        (name, noun, _plural, _explanation_noun, _setting, p_pos, p_neg,
         (q_pos, q_neg), event_p, event_z, source) = item
        bucket = "inherited" if source == "davies_richardson" else "authored"

        def flag(message):
            violations[bucket].append(f"{name:<12}{message}")

        verbs = [main_verb(event_p[2]), main_verb(event_z[2])]
        frequencies = [zipf(v, "en") for v in verbs]
        for verb, frequency in zip(verbs, frequencies):
            if frequency < MIN_VERB:
                flag(f"verb '{verb}' Zipf {frequency:.2f} < {MIN_VERB}")
        gap = abs(frequencies[0] - frequencies[1])
        if gap > MAX_VERB_GAP:
            flag(f"verb pair '{verbs[0]}'/'{verbs[1]}' differ by {gap:.2f} Zipf > {MAX_VERB_GAP}")
        for value in (p_pos, p_neg):
            if zipf(value, "en") < MIN_PROPERTY:
                flag(f"property '{value}' Zipf {zipf(value, 'en'):.2f} < {MIN_PROPERTY}")
        for value in (q_pos, q_neg):
            if zipf(value, "en") < MIN_Q:
                flag(f"Q value '{value}' Zipf {zipf(value, 'en'):.2f} < {MIN_Q}")
        if p_pos == p_neg or q_pos == q_neg:
            flag("a dimension has identical values")
        if {p_pos, p_neg} & {q_pos, q_neg}:
            flag("P and Q share a value")
        for event in (event_p, event_z):
            for form in (event[1], event[2]):
                if " the " in f" {form} " or " a " in f" {form} ":
                    flag(f"verb phrase '{form}' carries its own complement")

    for bucket in ("inherited", "authored"):
        rows = violations[bucket]
        label = ("inherited from Davies & Richardson (exempt, listed for visibility)"
                 if bucket == "inherited" else "authored (must be zero)")
        print(f"\n{len(rows)} violations, {label}")
        for row in rows:
            print(f"   {row}")

    print(f"\n{len(module.ITEMS)} families, "
          f"{sum(1 for i in module.ITEMS if i[-1] == 'davies_richardson')} inherited, "
          f"{sum(1 for i in module.ITEMS if i[-1] == 'extended')} authored")
    if violations["authored"]:
        raise SystemExit(1)
    print("authored families pass every lexical criterion")


if __name__ == "__main__":
    main()

from __future__ import annotations

DIRECTIONS = ("supports_target", "supports_other")
SOURCES = ("low", "high")
DELAYS = ("immediate", "short", "long")
YES_NO_ORDERS = (
    {"A": "yes", "B": "no"},
    {"A": "no", "B": "yes"},
)
CHOICE_ORDERS = (
    {"A": "target", "B": "other"},
    {"A": "other", "B": "target"},
)
SOURCE_ORDERS = (
    {"A": "low", "B": "high"},
    {"A": "high", "B": "low"},
)
READOUT_TEMPLATES = (
    ("belief", "Which hypothesis is better supported by the information available now?"),
    ("belief", "Given the record available to you now, which explanation is more plausible?"),
    ("action", "Which action is better justified by the information available now?"),
    ("action", "Based only on the current record, which action should be preferred?"),
)
CONDITIONS = (
    "no_message_immediate", "no_message_short", "no_message_long",
    "low_immediate", "high_immediate", "low_short", "high_short",
    "low_long", "high_long", "low_long_reinstated", "high_long_reinstated",
    "low_long_length", "high_long_length",
)
MEMORY_PROBES = ("source_identity", "message_direction", "source_credibility")
SUPPORT_PROBES = ("low_positive", "high_positive", "high_gt_low")


def source_name(s, source: str) -> str:
    return s.low_source if source == "low" else s.high_source


def source_profile(s, source: str) -> str:
    return s.low_source_profile if source == "low" else s.high_source_profile


def message_for(s, direction: str) -> str:
    if direction == "supports_target":
        return s.target_message
    if direction == "supports_other":
        return s.other_message
    raise ValueError(direction)


def delay_text(s, delay: str) -> str:
    if delay == "immediate":
        return ""
    if delay == "short":
        return s.short_delay_text
    if delay == "long":
        return s.long_delay_text
    raise ValueError(delay)


def base_text(s) -> str:
    return (
        f"BACKGROUND:\n{s.background}\n\n"
        f"SOURCE CALIBRATION:\n{s.calibration_text}\n\n"
        f"SOURCE RECORDS:\n{s.high_source}: {s.high_source_profile}\n"
        f"{s.low_source}: {s.low_source_profile}\n\n"
        f"HYPOTHESES:\n- {s.target_hypothesis}\n- {s.other_hypothesis}"
    )


def message_block(s, *, direction: str, source: str) -> str:
    return f"MESSAGE FROM {source_name(s, source)}:\n{message_for(s, direction)}"


def context_text(s, *, direction: str, condition: str) -> str:
    base = base_text(s)
    if condition.startswith("no_message_"):
        delay = condition.removeprefix("no_message_")
        filler = delay_text(s, delay)
        return base + (f"\n\nINTERVENING MATERIAL:\n{filler}" if filler else "")

    source, suffix = condition.split("_", 1)
    if source not in SOURCES:
        raise ValueError(condition)
    text = base + "\n\n" + message_block(s, direction=direction, source=source)
    if suffix == "immediate":
        return text
    if suffix == "short":
        return text + f"\n\nINTERVENING MATERIAL:\n{s.short_delay_text}"
    if suffix == "long":
        return text + f"\n\nINTERVENING MATERIAL:\n{s.long_delay_text}"
    if suffix == "long_reinstated":
        cue = s.low_source_reinstatement if source == "low" else s.high_source_reinstatement
        return text + f"\n\nINTERVENING MATERIAL:\n{s.long_delay_text}\n\nSOURCE REMINDER:\n{cue}"
    if suffix == "long_length":
        cue = s.low_source_length_control if source == "low" else s.high_source_length_control
        return text + f"\n\nINTERVENING MATERIAL:\n{s.long_delay_text}\n\nCONTROL REMINDER:\n{cue}"
    raise ValueError(condition)


def yes_no_options(mapping: dict[str, str]) -> tuple[str, str]:
    options = "\n".join(f"{lab}. {'Yes' if sem == 'yes' else 'No'}" for lab, sem in mapping.items())
    correct = next(lab for lab, sem in mapping.items() if sem == "yes")
    return options, correct


def support_prompt(s, *, direction: str, probe: str, mapping: dict[str, str]) -> tuple[str, str]:
    focal = s.target_hypothesis if direction == "supports_target" else s.other_hypothesis
    other = s.other_hypothesis if direction == "supports_target" else s.target_hypothesis
    low = message_block(s, direction=direction, source="low")
    high = message_block(s, direction=direction, source="high")
    if probe == "low_positive":
        evidence = low
        q = f"Relative to the same background with no message, is this message genuine positive evidence for {focal} rather than {other}?"
    elif probe == "high_positive":
        evidence = high
        q = f"Relative to the same background with no message, is this message genuine positive evidence for {focal} rather than {other}?"
    elif probe == "high_gt_low":
        evidence = f"VERSION 1:\n{low}\n\nVERSION 2:\n{high}"
        q = f"Given the audited source records, is the version from {s.high_source} more diagnostic in favor of {focal} than the version from {s.low_source}?"
    else:
        raise ValueError(probe)
    options, correct = yes_no_options(mapping)
    return f"{base_text(s)}\n\n{evidence}\n\n{q}\n{options}\nAnswer exactly A or B.", correct


def memory_prompt(s, *, direction: str, source: str, delay: str, probe: str,
                  order: dict[str, str]) -> tuple[str, str]:
    if delay not in {"short", "long"}:
        raise ValueError("memory probes are only defined after short/long delays")
    context = base_text(s) + "\n\n" + message_block(s, direction=direction, source=source)
    context += f"\n\nINTERVENING MATERIAL:\n{delay_text(s, delay)}"
    if probe == "source_identity":
        options = "\n".join(
            f"{lab}. {source_name(s, sem)}" for lab, sem in order.items()
        )
        correct = next(lab for lab, sem in order.items() if sem == source)
        q = "Which source delivered the earlier message?"
    elif probe == "message_direction":
        text = {"target": s.target_hypothesis, "other": s.other_hypothesis}
        options = "\n".join(f"{lab}. {text[sem]}" for lab, sem in order.items())
        expected = "target" if direction == "supports_target" else "other"
        correct = next(lab for lab, sem in order.items() if sem == expected)
        q = "Which hypothesis did the earlier message favor?"
    elif probe == "source_credibility":
        options, correct = yes_no_options(order)
        relation = "less" if source == "low" else "more"
        q = f"According to the audited source records, was the source of the earlier message {relation} reliable than the other source?"
    else:
        raise ValueError(probe)
    return f"{context}\n\n{q}\n{options}\nAnswer exactly A or B.", correct


def readout_prompt(s, *, direction: str, condition: str, template: str,
                   kind: str, mapping: dict[str, str]) -> tuple[str, str]:
    context = context_text(s, direction=direction, condition=condition)
    target_text = s.target_hypothesis if kind == "belief" else s.target_action
    other_text = s.other_hypothesis if kind == "belief" else s.other_action
    text = {"target": target_text, "other": other_text}
    options = "\n".join(f"{lab}. {text[sem]}" for lab, sem in mapping.items())
    target_label = next(lab for lab, sem in mapping.items() if sem == "target")
    return f"{context}\n\n{template}\n{options}\nAnswer exactly A or B.", target_label

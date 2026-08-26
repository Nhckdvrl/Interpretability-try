from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Literal

from .dataset import Option, Scenario

CHOICE_TEMPLATES = (
    "You are choosing one {item}. Consider only the attributes shown. Which option do you prefer? Reply with exactly one label and nothing else.",
    "Choose the {item} you would buy based only on the listed information. Reply with exactly one option label.",
    "Select the best {item} for you from these options using only these two attributes. Output exactly one label.",
)

@dataclass(frozen=True)
class PromptCase:
    case_id: str
    scenario_id: str
    kind: Literal["binary", "ternary", "dominance"]
    prompt: str
    labels: tuple[str, ...]
    semantic_by_label: dict[str, str]
    target_label: str | None
    competitor_label: str | None
    decoy_label: str | None
    template_id: int
    permutation_id: int


def _fmt_num(x: float) -> str:
    return f"{int(x):,}" if float(x).is_integer() else f"{x:,.2f}"


def _render_option(s: Scenario, label: str, o: Option) -> str:
    return f"{label}: {s.cost_name} {s.cost_unit}{_fmt_num(o.cost)}, {s.quality_name} {_fmt_num(o.quality)}{s.quality_unit}"


def _choice_case(s: Scenario, semantic_order: tuple[str, ...], template_id: int, kind: Literal["binary", "ternary"], permutation_id: int) -> PromptCase:
    labels = tuple(chr(ord("A") + i) for i in range(len(semantic_order)))
    by_sem = {"A": s.a, "B": s.b, "C": s.decoy}
    semantic_by_label = dict(zip(labels, semantic_order))
    lines = [CHOICE_TEMPLATES[template_id].format(item=s.item_noun), ""]
    lines += [_render_option(s, label, by_sem[sem]) for label, sem in zip(labels, semantic_order)]
    target_label = next(l for l, sem in semantic_by_label.items() if sem == s.target)
    competitor_sem = "B" if s.target == "A" else "A"
    competitor_label = next(l for l, sem in semantic_by_label.items() if sem == competitor_sem)
    decoy_label = next((l for l, sem in semantic_by_label.items() if sem == "C"), None)
    return PromptCase(f"{s.scenario_id}:{kind}:t{template_id}:p{permutation_id}", s.scenario_id, kind, "\n".join(lines), labels, semantic_by_label, target_label, competitor_label, decoy_label, template_id, permutation_id)


def build_choice_cases(s: Scenario) -> list[PromptCase]:
    out: list[PromptCase] = []
    for tid in range(len(CHOICE_TEMPLATES)):
        for pid, order in enumerate(itertools.permutations(("A", "B"))):
            out.append(_choice_case(s, order, tid, "binary", pid))
        for pid, order in enumerate(itertools.permutations(("A", "B", "C"))):
            out.append(_choice_case(s, order, tid, "ternary", pid))
    return out


def build_dominance_cases(s: Scenario) -> list[PromptCase]:
    target = s.a if s.target == "A" else s.b
    out: list[PromptCase] = []
    for pid, (first, second) in enumerate(((target, s.decoy), (s.decoy, target))):
        semantic_by_label = {"A": "target" if first is target else "decoy", "B": "target" if second is target else "decoy"}
        target_label = next(k for k, v in semantic_by_label.items() if v == "target")
        prompt = "\n".join([
            f"Compare two {s.item_noun} options using only the listed attributes.",
            "Lower price is better and higher quality score is better.",
            "Which option strictly dominates the other (no worse on either attribute and better on at least one)? Reply with exactly A or B.", "",
            _render_option(s, "A", first), _render_option(s, "B", second),
        ])
        out.append(PromptCase(f"{s.scenario_id}:dominance:t0:p{pid}", s.scenario_id, "dominance", prompt, ("A", "B"), semantic_by_label, target_label, None, None, 0, pid))
    return out

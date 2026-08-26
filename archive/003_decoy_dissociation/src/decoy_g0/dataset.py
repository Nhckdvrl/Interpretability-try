from __future__ import annotations

from dataclasses import asdict, dataclass
import itertools
import json
from pathlib import Path
from typing import Iterable, Literal


@dataclass(frozen=True)
class Domain:
    name: str
    item_noun: str
    cost_name: str
    quality_name: str
    cost_unit: str
    quality_unit: str
    cheap_costs: tuple[float, ...]
    cost_gaps: tuple[float, ...]
    low_qualities: tuple[float, ...]
    quality_gaps: tuple[float, ...]


@dataclass(frozen=True)
class Option:
    key: str
    cost: float
    quality: float


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    domain: str
    item_noun: str
    cost_name: str
    quality_name: str
    cost_unit: str
    quality_unit: str
    a: Option
    b: Option
    target: Literal["A", "B"]
    decoy: Option
    decoy_strength: float

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Scenario":
        return cls(
            scenario_id=d["scenario_id"], domain=d["domain"], item_noun=d["item_noun"],
            cost_name=d["cost_name"], quality_name=d["quality_name"],
            cost_unit=d["cost_unit"], quality_unit=d["quality_unit"],
            a=Option(**d["a"]), b=Option(**d["b"]), target=d["target"],
            decoy=Option(**d["decoy"]), decoy_strength=float(d["decoy_strength"]),
        )


DOMAINS: tuple[Domain, ...] = (
    Domain("phone", "phone", "price", "quality score", "$", "/100", (399, 499, 599, 699, 799), (150, 250, 350), (60, 66, 72, 78), (10, 16, 22)),
    Domain("car", "car", "price", "quality score", "$", "/100", (18000, 22000, 26000, 30000, 34000), (6000, 10000, 14000), (58, 64, 70, 76), (10, 16, 22)),
    Domain("frying_pan", "frying pan", "price", "quality score", "$", "/100", (20, 30, 40, 50, 60), (15, 25, 35), (58, 64, 70, 76), (10, 16, 22)),
    Domain("property", "apartment", "price", "quality score", "$", "/100", (250000, 325000, 400000, 475000, 550000), (75000, 125000, 175000), (58, 64, 70, 76), (10, 16, 22)),
)


def dominates(x: Option, y: Option) -> bool:
    """Cost is lower-is-better; quality is higher-is-better."""
    no_worse = x.cost <= y.cost and x.quality >= y.quality
    strictly_better = x.cost < y.cost or x.quality > y.quality
    return no_worse and strictly_better


def make_decoy(target: Option, strength: float) -> Option:
    if not 0 < strength < 0.5:
        raise ValueError("decoy strength must be in (0, 0.5)")
    return Option("C", round(target.cost * (1.0 + strength), 4), round(target.quality * (1.0 - strength), 4))


def generate_scenarios(strengths: Iterable[float] = (0.05, 0.10, 0.15), domains: Iterable[Domain] = DOMAINS) -> list[Scenario]:
    scenarios: list[Scenario] = []
    for d in domains:
        idx = 0
        for cheap_cost, cost_gap, low_q, q_gap in itertools.product(d.cheap_costs, d.cost_gaps, d.low_qualities, d.quality_gaps):
            a = Option("A", float(cheap_cost), float(low_q))
            b = Option("B", float(cheap_cost + cost_gap), float(low_q + q_gap))
            if dominates(a, b) or dominates(b, a):
                continue
            for target_key in ("A", "B"):
                target = a if target_key == "A" else b
                for strength in strengths:
                    decoy = make_decoy(target, float(strength))
                    assert dominates(target, decoy)
                    sid = f"{d.name}-{idx:04d}-target{target_key}-s{int(strength*100):02d}"
                    scenarios.append(Scenario(sid, d.name, d.item_noun, d.cost_name, d.quality_name, d.cost_unit, d.quality_unit, a, b, target_key, decoy, float(strength)))
            idx += 1
    return scenarios


def write_jsonl(path: str | Path, scenarios: Iterable[Scenario]) -> None:
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for s in scenarios:
            f.write(json.dumps(s.to_dict(), ensure_ascii=False) + "\n")


def read_jsonl(path: str | Path) -> list[Scenario]:
    with Path(path).open("r", encoding="utf-8") as f:
        return [Scenario.from_dict(json.loads(line)) for line in f if line.strip()]

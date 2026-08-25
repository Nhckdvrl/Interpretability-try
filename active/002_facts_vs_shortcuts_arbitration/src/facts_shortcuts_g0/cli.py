from __future__ import annotations

import argparse
from pathlib import Path

from .preflight import GateConfig, run_preflight


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Strict public-data G0 for facts-available-but-comparison-wrong entity comparisons."
    )
    p.add_argument("--results-dir", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, default=Path("artifacts/g0"))
    p.add_argument("--min-total-eligible", type=int, default=500)
    p.add_argument("--min-total-strict-failures", type=int, default=50)
    p.add_argument("--min-group-failures", type=int, default=10)
    p.add_argument("--min-group-failure-rate", type=float, default=0.02)
    p.add_argument("--min-passing-groups", type=int, default=2)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    gate = GateConfig(
        min_total_eligible=args.min_total_eligible,
        min_total_strict_failures=args.min_total_strict_failures,
        min_group_failures=args.min_group_failures,
        min_group_failure_rate=args.min_group_failure_rate,
        min_passing_groups=args.min_passing_groups,
    )
    result = run_preflight(args.results_dir, args.output_dir, gate)
    print(result.verdict)
    print(result.reason)
    print(f"facts-available cases: {result.total_eligible}")
    print(f"strict natural failures: {result.total_strict_failures}")
    print(f"passing model-dataset groups: {result.passing_groups}")


if __name__ == "__main__":
    main()

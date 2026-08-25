from __future__ import annotations

import argparse
from .bfcl import BFCL_COMMIT, download_category


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", default="simple_python")
    ap.add_argument("--out-dir", default="data/bfcl")
    a = ap.parse_args()
    p, g = download_category(a.category, a.out_dir)
    print(f"Pinned BFCL commit: {BFCL_COMMIT}")
    print(p)
    print(g)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build normalized OKF graph JSON from wiki Markdown."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from okf_lib import ROOT, add_check_arg, build_okf_graph, check_output, repo_rel, write_json


DEFAULT_OUTPUT = ROOT / "exports/okf/code-agent-harness-okf-graph.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output graph JSON path.")
    add_check_arg(parser)
    args = parser.parse_args()

    graph = build_okf_graph()
    content = json.dumps(graph, indent=2, ensure_ascii=False) + "\n"
    output = args.output if args.output.is_absolute() else ROOT / args.output

    if args.check:
        errors = check_output(output, content)
        if errors:
            print("OKF graph check failed:")
            for error in errors:
                print(f"- {error}")
            return 1
        print(f"OKF graph is up to date: {repo_rel(output)}")
        return 0

    write_json(output, graph)
    print(f"Wrote {repo_rel(output)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

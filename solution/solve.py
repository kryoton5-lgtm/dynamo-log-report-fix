import json
import re
from collections import Counter
from pathlib import Path

ACCESS_LOG = Path("/app/access.log")
REPORT = Path("/app/report.json")
REQUEST_RE = re.compile(r'"[A-Z]+\s+(\S+)\s+HTTP/[^\"]+"')


def main() -> None:
    path_counts: Counter[str] = Counter()
    client_ips: set[str] = set()
    total_requests = 0

    for raw_line in ACCESS_LOG.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        total_requests += 1
        client_ips.add(line.split(maxsplit=1)[0])

        match = REQUEST_RE.search(line)
        if match is None:
            raise ValueError(f"Malformed request line: {raw_line!r}")
        path_counts[match.group(1)] += 1

    if not path_counts:
        raise ValueError("The access log contains no parseable request paths")

    report = {
        "total_requests": total_requests,
        "unique_ips": len(client_ips),
        "top_path": path_counts.most_common(1)[0][0],
    }
    REPORT.write_text(json.dumps(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

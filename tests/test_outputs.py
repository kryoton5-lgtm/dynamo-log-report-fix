import hashlib
import json
from pathlib import Path

REPORT = Path("/app/report.json")
ACCESS_LOG = Path("/app/access.log")
EXPECTED_KEYS = {"total_requests", "unique_ips", "top_path"}
ORIGINAL_ACCESS_LOG_SHA256 = (
    "e83c0cb8dd9c33cbe0954cc038bd0ff90834cf48747e257d931dce5b2408d38e"
)


def _load_report() -> dict[str, object]:
    assert REPORT.is_file(), "missing regular file: /app/report.json"
    try:
        data = json.loads(REPORT.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AssertionError("/app/report.json must contain valid UTF-8 JSON") from exc
    assert isinstance(data, dict), "/app/report.json must contain one JSON object"
    return data


def test_success_criterion_1_report_schema() -> None:
    """Criterion 1: report.json is a JSON object containing exactly the required keys."""
    data = _load_report()
    assert set(data) == EXPECTED_KEYS, (
        f"expected exactly {sorted(EXPECTED_KEYS)!r}, got {sorted(data)!r}"
    )


def test_success_criterion_2_total_requests() -> None:
    """Criterion 2: total_requests is the integer count of non-empty request lines."""
    data = _load_report()
    assert type(data["total_requests"]) is int, "total_requests must be a JSON integer"
    assert data["total_requests"] == 6, (
        f"expected total_requests=6, got {data['total_requests']!r}"
    )


def test_success_criterion_3_unique_ips() -> None:
    """Criterion 3: unique_ips is the integer count of distinct client IPs."""
    data = _load_report()
    assert type(data["unique_ips"]) is int, "unique_ips must be a JSON integer"
    assert data["unique_ips"] == 3, (
        f"expected unique_ips=3, got {data['unique_ips']!r}"
    )


def test_success_criterion_4_top_path() -> None:
    """Criterion 4: top_path is the most frequently requested path."""
    data = _load_report()
    assert type(data["top_path"]) is str, "top_path must be a JSON string"
    assert data["top_path"] == "/index.html", (
        f"expected top_path='/index.html', got {data['top_path']!r}"
    )


def test_success_criterion_5_access_log_unchanged() -> None:
    """Criterion 5: the original /app/access.log remains byte-for-byte unchanged."""
    assert ACCESS_LOG.is_file(), "missing regular file: /app/access.log"
    actual_hash = hashlib.sha256(ACCESS_LOG.read_bytes()).hexdigest()
    assert actual_hash == ORIGINAL_ACCESS_LOG_SHA256, "/app/access.log was modified"

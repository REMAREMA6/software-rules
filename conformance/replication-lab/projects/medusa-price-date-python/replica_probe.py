import json
from datetime import datetime
from datetime import timezone


def is_iso_date(value):
    if isinstance(value, dict) and "__date" in value:
        value = value["__date"]
    if not isinstance(value, str) or not value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def validate_price_list_dates(data, empty_string_is_missing=True, validate_end=True, start_first=True, enforce_order=False):
    fields = ["starts_at", "ends_at"] if start_first else ["ends_at", "starts_at"]
    for field in fields:
        if field == "ends_at" and not validate_end:
            continue
        value = data.get(field)
        if value is None:
            continue
        if value == "" and empty_string_is_missing:
            continue
        if value == "" and not empty_string_is_missing:
            raise ValueError(("invalid_data", field))
        if value and not is_iso_date(value):
            raise ValueError(("invalid_data", field))

    if enforce_order and data.get("starts_at") and data.get("ends_at"):
        start = datetime.fromisoformat(data["starts_at"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(data["ends_at"].replace("Z", "+00:00"))
        if start > end:
            raise ValueError(("invalid_data", "date_range"))


def capture(empty_string_is_missing=True, validate_end=True, start_first=True, enforce_order=False):
    cases = [
        ("omitted-both", {}),
        ("null-both", {"starts_at": None, "ends_at": None}),
        ("empty-string-both", {"starts_at": "", "ends_at": ""}),
        ("valid-start-iso", {"starts_at": "2026-01-01T00:00:00.000Z"}),
        ("valid-end-iso", {"ends_at": "2026-12-31T23:59:59.999Z"}),
        ("invalid-start", {"starts_at": "not-a-date"}),
        ("invalid-end", {"ends_at": "not-a-date"}),
        ("date-object-start", {"starts_at": {"__date": "2026-01-01T00:00:00.000Z"}}),
        ("reversed-range", {"starts_at": "2026-12-31T00:00:00.000Z", "ends_at": "2026-01-01T00:00:00.000Z"}),
        ("both-invalid-start-first", {"starts_at": "bad-start", "ends_at": "bad-end"}),
    ]
    scenarios = []
    for label, data in cases:
        try:
            validate_price_list_dates(
                data,
                empty_string_is_missing=empty_string_is_missing,
                validate_end=validate_end,
                start_first=start_first,
                enforce_order=enforce_order,
            )
            scenarios.append({
                "label": label,
                "input": data,
                "outcome": "accepted",
                "errorType": None,
                "errorName": None,
                "isMedusaError": False,
                "errorField": None,
            })
        except ValueError as error:
            error_type, error_field = error.args[0]
            scenarios.append({
                "label": label,
                "input": data,
                "outcome": "rejected",
                "errorType": error_type,
                "errorName": "ValueError",
                "isMedusaError": False,
                "errorField": error_field,
            })
    return {
        "capturedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "completedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "implementation": "Independent Python 3.12 ISO-8601 price-list date validator",
        "scenarios": scenarios,
    }


if __name__ == "__main__":
    print(json.dumps(capture(), indent=2))

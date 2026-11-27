import base64
import hashlib
import hmac
import json
from datetime import datetime, timezone


def b64url_decode(value):
    return base64.urlsafe_b64decode(value + "=" * ((4 - len(value) % 4) % 4))


def parse_token(token):
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("invalid-token")
    header = json.loads(b64url_decode(parts[0]))
    claims = json.loads(b64url_decode(parts[1]))
    signature = b64url_decode(parts[2])
    if not isinstance(header, dict) or not isinstance(claims, dict):
        raise ValueError("invalid-token")
    return parts, header, claims, signature


def verify_one(scenario, verify_signature=True, verify_exp=True, verify_nbf=True,
               enforce_issuer=True, enforce_audience=True, allow_hs384=False,
               require_claims=True):
    parts, header, claims, signature = parse_token(scenario["token"])
    options = scenario["verificationOptions"]
    alg = header.get("alg")
    allowed = ["HS256", "HS384"] if allow_hs384 else options["algorithms"]
    if alg not in allowed:
        return {"label": scenario["label"], "outcome": "rejected", "errorCategory": "algorithm-not-allowed", "claims": None, "protectedHeader": None}

    key = b64url_decode(scenario["keyBase64url"])
    if verify_signature:
        digest = {"HS256": hashlib.sha256, "HS384": hashlib.sha384}.get(alg)
        if digest is None:
            return {"label": scenario["label"], "outcome": "rejected", "errorCategory": "algorithm-not-allowed", "claims": None, "protectedHeader": None}
        signing_input = (parts[0] + "." + parts[1]).encode("ascii")
        expected_signature = hmac.new(key, signing_input, digest).digest()
        if not hmac.compare_digest(signature, expected_signature):
            return {"label": scenario["label"], "outcome": "rejected", "errorCategory": "signature-invalid", "claims": None, "protectedHeader": None}

    issuer = options.get("issuer")
    audience = options.get("audience")
    if enforce_issuer and issuer is not None:
        if require_claims and "iss" not in claims:
            return {"label": scenario["label"], "outcome": "rejected", "errorCategory": "issuer-missing", "claims": None, "protectedHeader": None}
        if "iss" in claims and claims["iss"] != issuer:
            return {"label": scenario["label"], "outcome": "rejected", "errorCategory": "issuer-mismatch", "claims": None, "protectedHeader": None}
    if enforce_audience and audience is not None:
        if require_claims and "aud" not in claims:
            return {"label": scenario["label"], "outcome": "rejected", "errorCategory": "audience-missing", "claims": None, "protectedHeader": None}
        if "aud" in claims:
            token_aud = claims["aud"]
            matches = token_aud == audience if isinstance(token_aud, str) else isinstance(token_aud, list) and audience in token_aud
            if not matches:
                return {"label": scenario["label"], "outcome": "rejected", "errorCategory": "audience-mismatch", "claims": None, "protectedHeader": None}

    now = options["currentDateEpochSeconds"]
    if verify_nbf and "nbf" in claims:
        value = claims["nbf"]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return {"label": scenario["label"], "outcome": "rejected", "errorCategory": "claim-invalid", "claims": None, "protectedHeader": None}
        if value > now:
            return {"label": scenario["label"], "outcome": "rejected", "errorCategory": "token-not-yet-valid", "claims": None, "protectedHeader": None}
    if verify_exp and "exp" in claims:
        value = claims["exp"]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return {"label": scenario["label"], "outcome": "rejected", "errorCategory": "claim-invalid", "claims": None, "protectedHeader": None}
        if value <= now:
            return {"label": scenario["label"], "outcome": "rejected", "errorCategory": "token-expired", "claims": None, "protectedHeader": None}

    return {
        "label": scenario["label"],
        "outcome": "accepted",
        "errorCategory": None,
        "claims": claims,
        "protectedHeader": header,
    }


def capture(source, **mutations):
    return {
        "capturedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "implementation": "Independent Python 3.12 HMAC/JWT claim verifier",
        "scenarios": [verify_one(item, **mutations) for item in source["scenarios"]],
    }


if __name__ == "__main__":
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument("source_capture")
    args = parser.parse_args()
    source = json.loads(Path(args.source_capture).read_text())
    print(json.dumps(capture(source), indent=2))

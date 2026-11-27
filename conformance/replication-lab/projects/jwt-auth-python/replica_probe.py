import base64
import hashlib
import hmac
import json
from datetime import datetime, timezone



def b64url_encode(value):
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def sign_token_fixture(payload, alg, key):
    header = {"alg": alg}
    header_part = b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    payload_part = b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = (header_part + "." + payload_part).encode("ascii")
    digest = {"HS256": hashlib.sha256, "HS384": hashlib.sha384}[alg]
    signature = hmac.new(key, signing_input, digest).digest()
    return header_part + "." + payload_part + "." + b64url_encode(signature)


def sign_token_fixture_capture():
    now = 1700000000
    issuer = "https://issuer.example"
    audience = "api.example"
    secret = b"software-rules-jose-hmac-key-32bytes!!"
    secret384 = b"software-rules-jose-hmac-key-48bytes!!"
    base_options = {
        "algorithms": ["HS256"],
        "issuer": issuer,
        "audience": audience,
        "currentDateEpochSeconds": now,
    }
    cases = [
        ("valid-token", {"sub": "user-1", "iss": issuer, "aud": audience, "exp": now + 600, "nbf": now - 60}, "HS256", secret, False, "accepted", None),
        ("expired-token", {"sub": "user-1", "iss": issuer, "aud": audience, "exp": now - 1, "nbf": now - 60}, "HS256", secret, False, "rejected", "token-expired"),
        ("not-before-future", {"sub": "user-1", "iss": issuer, "aud": audience, "exp": now + 600, "nbf": now + 1}, "HS256", secret, False, "rejected", "token-not-yet-valid"),
        ("issuer-mismatch", {"sub": "user-1", "iss": "https://wrong-issuer.example", "aud": audience, "exp": now + 600}, "HS256", secret, False, "rejected", "issuer-mismatch"),
        ("audience-mismatch", {"sub": "user-1", "iss": issuer, "aud": "other-api.example", "exp": now + 600}, "HS256", secret, False, "rejected", "audience-mismatch"),
        ("tampered-signature", {"sub": "user-1", "iss": issuer, "aud": audience, "exp": now + 600}, "HS256", secret, True, "rejected", "signature-invalid"),
        ("algorithm-not-allowed", {"sub": "user-1", "iss": issuer, "aud": audience, "exp": now + 600}, "HS384", secret384, False, "rejected", "algorithm-not-allowed"),
        ("missing-exp-is-optional", {"sub": "user-1", "iss": issuer, "aud": audience}, "HS256", secret, False, "accepted", None),
        ("audience-array-match", {"sub": "user-1", "iss": issuer, "aud": [audience, "other-api.example"], "exp": now + 600}, "HS256", secret, False, "accepted", None),
        ("missing-issuer", {"sub": "user-1", "aud": audience, "exp": now + 600}, "HS256", secret, False, "rejected", "issuer-missing"),
        ("missing-audience", {"sub": "user-1", "iss": issuer, "exp": now + 600}, "HS256", secret, False, "rejected", "audience-missing"),
    ]
    scenarios = []
    for label, payload, alg, key, tamper, outcome, category in cases:
        token = sign_token_fixture(payload, alg, key)
        if tamper:
            parts = token.split(".")
            parts[2] = ("B" if parts[2][0] == "A" else "A") + parts[2][1:]
            token = ".".join(parts)
        accepted = outcome == "accepted"
        scenarios.append({
            "label": label,
            "token": token,
            "keyBase64url": b64url_encode(key),
            "verificationOptions": base_options,
            "outcome": outcome,
            "errorCategory": category,
            "claims": payload if accepted else None,
            "protectedHeader": {"alg": alg} if accepted else None,
        })
    return {"scenarios": scenarios}


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
    scenarios = []
    for item in source["scenarios"]:
        observed = verify_one(item, **mutations)
        # Preserve the exact token and verification policy supplied by the source
        # so the normalized capture records identical inputs on both sides.
        observed["verificationOptions"] = item["verificationOptions"]
        observed["token"] = item["token"]
        observed["keyBase64url"] = item["keyBase64url"]
        scenarios.append(observed)
    return {
        "capturedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "implementation": "Independent Python 3.12 HMAC/JWT claim verifier",
        "scenarios": scenarios,
    }


if __name__ == "__main__":
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument("source_capture")
    args = parser.parse_args()
    source = json.loads(Path(args.source_capture).read_text())
    print(json.dumps(capture(source), indent=2))

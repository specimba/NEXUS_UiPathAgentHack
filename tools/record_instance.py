#!/usr/bin/env python3
"""Record a live NEXUS Sentinel instance timeline for the AgentHack submission.

Drives the public policy adapter end-to-end using the four committed sample
bodies and writes a self-contained evidence bundle under
``artifacts/instance-timeline/``.

Reconciliation note (important): the four samples are of two shapes.
  * ``01-safety-hold.json`` and ``02-approved-remediation.json`` are *evaluate*
    request bodies -> POSTed to ``/api/v1/case/evaluate``.
  * ``03-verification-failed.json`` and ``04-verification-passed.json`` are
    *verify* request bodies (they carry ``checks`` and an
    ``evaluation_audit_id`` placeholder) -> POSTed to ``/api/v1/case/verify``
    with the placeholder replaced by the auditId minted by the most recent
    evaluate call. This is what produces the intended verdict chain
    HOLD -> ALLOW/approval -> verification failed -> verification passed ->
    closure. Posting a verify body to /evaluate would 422 (the adapter models
    are ``extra="forbid"``), so the script routes by body shape.

Stdlib only: urllib, json, time, datetime, argparse.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ENDPOINT = "https://nexus-sentinel-policy-adapter.onrender.com"

# Samples in the order they should be exercised.
SAMPLE_ORDER = [
    "01-safety-hold.json",
    "02-approved-remediation.json",
    "03-verification-failed.json",
    "04-verification-passed.json",
]

REPO_ROOT = Path(__file__).resolve().parent.parent
SAMPLES_DIR = REPO_ROOT / "samples"
OUT_DIR = REPO_ROOT / "artifacts" / "instance-timeline"

# Key substrings that would mark a value as sensitive. There are none in these
# samples, but redaction is applied defensively before anything is written.
SECRET_KEY_MARKERS = ("secret", "token", "password", "passwd", "authorization",
                      "credential", "api_key", "apikey", "bearer")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def redact(value):
    """Recursively redact any value whose key name looks sensitive."""
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            if any(marker in k.lower() for marker in SECRET_KEY_MARKERS):
                out[k] = "***REDACTED***"
            else:
                out[k] = redact(v)
        return out
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value


def post_json(endpoint: str, path: str, body: dict):
    """POST a JSON body; return (http_status, parsed_json_or_text, error_str)."""
    url = endpoint.rstrip("/") + path
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, _parse(raw), None
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        return exc.code, _parse(raw), f"HTTPError {exc.code}"
    except urllib.error.URLError as exc:
        return None, None, f"URLError: {exc.reason}"
    except Exception as exc:  # noqa: BLE001 - defensive; record whatever happened
        return None, None, f"{type(exc).__name__}: {exc}"


def get_json(endpoint: str, path: str):
    url = endpoint.rstrip("/") + path
    req = urllib.request.Request(url, method="GET", headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, _parse(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as exc:
        return exc.code, _parse(exc.read().decode("utf-8", errors="replace")), f"HTTPError {exc.code}"
    except urllib.error.URLError as exc:
        return None, None, f"URLError: {exc.reason}"
    except Exception as exc:  # noqa: BLE001
        return None, None, f"{type(exc).__name__}: {exc}"


def _parse(raw: str):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"_raw": raw}


def is_verify_body(body: dict) -> bool:
    return "checks" in body or "evaluation_audit_id" in body


def fetch_fingerprint(endpoint: str, audit_id: str):
    """Fetch input_fingerprint for an audit record (evaluate response omits it)."""
    if not audit_id:
        return None, None
    status, payload, _ = get_json(endpoint, f"/api/v1/audit/{audit_id}")
    if status == 200 and isinstance(payload, dict):
        return payload.get("input_fingerprint"), payload
    return None, None


def run(endpoint: str) -> dict:
    events = []
    seq = 0
    last_eval_audit_id = None
    verdict_chain = []
    started = time.time()

    for name in SAMPLE_ORDER:
        sample_path = SAMPLES_DIR / name
        body = json.loads(sample_path.read_text(encoding="utf-8"))
        seq += 1

        if is_verify_body(body):
            # Route to /verify, linking to the most recent evaluate auditId.
            call_body = dict(body)
            substituted = last_eval_audit_id or call_body.get("evaluation_audit_id")
            call_body["evaluation_audit_id"] = substituted
            status, resp, err = post_json(endpoint, "/api/v1/case/verify", call_body)
            resp = resp or {}
            verified = resp.get("verified") if isinstance(resp, dict) else None
            events.append({
                "seq": seq,
                "stage": "Verify Recovery",
                "sample": name,
                "call": "verify",
                "endpoint": endpoint.rstrip("/") + "/api/v1/case/verify",
                "timestamp_utc": _utc_now(),
                "http_status": status,
                "error": err,
                "request_body": redact(call_body),
                "response": resp,
                "auditId": resp.get("audit_id") if isinstance(resp, dict) else None,
                "verdict": None,
                "verified": verified,
                "fingerprint": None,
                "evaluationAuditId": resp.get("evaluation_audit_id") if isinstance(resp, dict) else substituted,
            })
            if verified is True:
                verdict_chain.append("VERIFICATION_PASSED")
            elif verified is False:
                verdict_chain.append("VERIFICATION_FAILED")
        else:
            # Route to /evaluate.
            status, resp, err = post_json(endpoint, "/api/v1/case/evaluate", body)
            resp = resp or {}
            audit_id = resp.get("audit_id") if isinstance(resp, dict) else None
            verdict = resp.get("verdict") if isinstance(resp, dict) else None
            if audit_id:
                last_eval_audit_id = audit_id
            fingerprint, _audit_rec = fetch_fingerprint(endpoint, audit_id)
            events.append({
                "seq": seq,
                "stage": "Evaluate Release Risk",
                "sample": name,
                "call": "evaluate",
                "endpoint": endpoint.rstrip("/") + "/api/v1/case/evaluate",
                "timestamp_utc": _utc_now(),
                "http_status": status,
                "error": err,
                "request_body": redact(body),
                "response": resp,
                "auditId": audit_id,
                "verdict": verdict,
                "verified": None,
                "fingerprint": fingerprint,
                "evaluationAuditId": audit_id,
            })
            if verdict:
                verdict_chain.append(verdict)

    # Two close-loop resolution markers derived from the verify outcomes.
    for ev in events:
        if ev["call"] == "verify" and isinstance(ev["response"], dict):
            resp = ev["response"]
            verified = resp.get("verified")
            marker = {
                "seq": None,
                "stage": "Close-Loop Resolution",
                "sample": ev["sample"],
                "call": "resolution_marker",
                "timestamp_utc": _utc_now(),
                "resolved_from_verify_seq": ev["seq"],
                "verified": verified,
                "recommended_stage": resp.get("recommended_stage"),
                "reentry_stage": resp.get("reentry_stage"),
                "retry_exhausted": resp.get("retry_exhausted"),
                "outcome": "CLOSURE" if verified else "REWORK_REENTRY",
            }
            events.append(marker)

    runtime = time.time() - started

    # Audit-chain integrity: every verify's evaluation_audit_id must equal a
    # real evaluate auditId captured this run.
    eval_audit_ids = {e["auditId"] for e in events if e["call"] == "evaluate" and e["auditId"]}
    verify_links = [
        {"sample": e["sample"], "evaluationAuditId": e["evaluationAuditId"],
         "matches_evaluate": e["evaluationAuditId"] in eval_audit_ids}
        for e in events if e["call"] == "verify"
    ]
    chain_ok = bool(verify_links) and all(v["matches_evaluate"] for v in verify_links)

    return {
        "instance_id": "instance-1",
        "endpoint": endpoint,
        "generated_utc": _utc_now(),
        "runtime_seconds": round(runtime, 3),
        "verdict_chain": verdict_chain,
        "audit_chain_integrity": {
            "ok": chain_ok,
            "evaluate_audit_ids": sorted(eval_audit_ids),
            "verify_links": verify_links,
        },
        "events": events,
    }


def render_markdown(result: dict) -> str:
    lines = ["# NEXUS Sentinel — Instance Timeline (instance-1)", ""]
    lines.append(f"- **Endpoint:** `{result['endpoint']}`")
    lines.append(f"- **Generated (UTC):** {result['generated_utc']}")
    lines.append(f"- **Runtime:** {result['runtime_seconds']} s")
    lines.append(f"- **Verdict chain:** {' -> '.join(result['verdict_chain']) or '(none)'}")
    lines.append("")
    for ev in result["events"]:
        if ev["call"] == "resolution_marker":
            lines.append(f"## [resolution] {ev['stage']} — {ev['outcome']}")
            lines.append(f"- from verify seq: {ev['resolved_from_verify_seq']}")
            lines.append(f"- verified: `{ev['verified']}` | recommended_stage: "
                         f"`{ev.get('recommended_stage')}` | reentry: `{ev.get('reentry_stage')}`")
            lines.append("")
            continue
        lines.append(f"## Stage {ev['seq']}: {ev['stage']} ({ev['call']}) — `{ev['sample']}`")
        lines.append(f"- **Timestamp (UTC):** {ev['timestamp_utc']}")
        lines.append(f"- **HTTP status:** {ev['http_status']}" + (f" | **error:** {ev['error']}" if ev['error'] else ""))
        resp = ev["response"] if isinstance(ev["response"], dict) else {}
        case_id = resp.get("case_id")
        if ev["call"] == "evaluate":
            lines.append(f"- **Case:** `{case_id}` | **Verdict:** `{ev['verdict']}` | "
                         f"**Risk:** `{resp.get('risk_level')}`")
            lines.append(f"- **Required human role:** `{resp.get('required_human_role')}` | "
                         f"**Recommended stage:** `{resp.get('recommended_stage')}`")
            lines.append(f"- **auditId:** `{ev['auditId']}`")
            lines.append(f"- **input_fingerprint (sha256):** `{ev['fingerprint']}`")
            if resp.get("reason_codes"):
                lines.append(f"- **Reason codes:** {', '.join(resp['reason_codes'])}")
        elif ev["call"] == "verify":
            lines.append(f"- **Case:** `{case_id}` | **Verified:** `{ev['verified']}`")
            lines.append(f"- **evaluationAuditId (linkage):** `{ev['evaluationAuditId']}`")
            lines.append(f"- **verify auditId:** `{ev['auditId']}` | "
                         f"**recommended_stage:** `{resp.get('recommended_stage')}` | "
                         f"**reentry_stage:** `{resp.get('reentry_stage')}`")
            if resp.get("reason_codes"):
                lines.append(f"- **Reason codes:** {', '.join(resp['reason_codes'])}")
        lines.append("")
    return "\n".join(lines)


def render_summary(result: dict) -> str:
    ci = result["audit_chain_integrity"]
    lines = ["# Instance Timeline — SUMMARY", ""]
    lines.append(f"- **Instance:** {result['instance_id']}")
    lines.append(f"- **Endpoint:** `{result['endpoint']}`")
    lines.append(f"- **Generated (UTC):** {result['generated_utc']}")
    lines.append(f"- **Total runtime:** {result['runtime_seconds']} s")
    lines.append("")
    lines.append("## Verdict / outcome sequence")
    lines.append("")
    lines.append(f"`{' -> '.join(result['verdict_chain'])}`")
    lines.append("")
    lines.append("Expected narrative: HOLD -> ALLOW/approval -> verification failed -> "
                 "verification passed -> closure.")
    lines.append("")
    lines.append("## Audit-chain integrity (verify.evaluation_audit_id -> evaluate.auditId)")
    lines.append("")
    lines.append(f"- **Integrity OK:** {ci['ok']}")
    lines.append(f"- **Evaluate audit IDs:** {', '.join(f'`{a}`' for a in ci['evaluate_audit_ids']) or '(none)'}")
    for link in ci["verify_links"]:
        lines.append(f"- verify `{link['sample']}` -> `{link['evaluationAuditId']}` "
                     f"(matches evaluate: **{link['matches_evaluate']}**)")
    lines.append("")
    lines.append("## HTTP call results")
    lines.append("")
    lines.append("| seq | stage | call | sample | status | error |")
    lines.append("|---|---|---|---|---|---|")
    for ev in result["events"]:
        if ev["call"] == "resolution_marker":
            continue
        lines.append(f"| {ev['seq']} | {ev['stage']} | {ev['call']} | {ev['sample']} | "
                     f"{ev['http_status']} | {ev['error'] or ''} |")
    lines.append("")
    lines.append("## Exact request bodies used (secrets redacted — none present)")
    lines.append("")
    for ev in result["events"]:
        if ev["call"] not in ("evaluate", "verify"):
            continue
        lines.append(f"### {ev['sample']} -> {ev['call']}")
        lines.append("```json")
        lines.append(json.dumps(ev["request_body"], indent=2))
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Record a NEXUS Sentinel instance timeline.")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT,
                        help=f"Adapter base URL (default: {DEFAULT_ENDPOINT})")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    result = run(args.endpoint)

    (OUT_DIR / "instance-1.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8")
    (OUT_DIR / "instance-1.md").write_text(
        render_markdown(result), encoding="utf-8")
    (OUT_DIR / "SUMMARY.md").write_text(
        render_summary(result), encoding="utf-8")

    # Console confirmation.
    evaluate_calls = [e for e in result["events"] if e["call"] == "evaluate"]
    verify_calls = [e for e in result["events"] if e["call"] == "verify"]
    ok_eval = sum(1 for e in evaluate_calls if e["http_status"] == 200)
    ok_verify = sum(1 for e in verify_calls if e["http_status"] == 200)
    print(f"endpoint: {args.endpoint}")
    print(f"verdict chain: {' -> '.join(result['verdict_chain'])}")
    print(f"evaluate 200: {ok_eval}/{len(evaluate_calls)} | verify 200: {ok_verify}/{len(verify_calls)}")
    print(f"audit-chain integrity ok: {result['audit_chain_integrity']['ok']}")
    for e in result["events"]:
        if e["call"] in ("evaluate", "verify"):
            print(f"  seq {e['seq']:>1} {e['call']:<9} {e['sample']:<30} "
                  f"HTTP {e['http_status']} err={e['error']}")
    print(f"wrote: {OUT_DIR / 'instance-1.json'}")
    print(f"wrote: {OUT_DIR / 'instance-1.md'}")
    print(f"wrote: {OUT_DIR / 'SUMMARY.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

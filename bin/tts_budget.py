#!/usr/bin/env python3
"""tts_budget.py - the audio ledger reader/writer for the 100%-local pipeline.

Named for its budget-era origin (daily cloud-TTS caps); since 2026-11-07 the doctrine
is local-only, so this is a provenance + retake tool, not a spend gate:
  - summary: today's takes per engine, QA failures, lines that hit the retake rule
  - next:    the local engine for a line, by role (ROLE_ENGINE below)
  - log:     append a take. REFUSES any engine outside the local suite (the
             ALLOWED_ENGINES allowlist) - the out-of-policy rule is enforced in code,
             not in memory.

Usage:
  tts_budget.py LEDGER summary [--date YYYY-MM-DD]
  tts_budget.py LEDGER next LINE_ID --role narration|subject|sfx|ui-sfx|scratch
  tts_budget.py LEDGER log --line-id ID --engine E --voice V --take N --result R --rms-qa pass --file F [--date ...]
    (--file is required for a PASS; a failed attempt with no output may omit it)
    (--engine is validated against the allowlist and normalised: path prefix, case and underscores)

Exit 0 on success; 2 on ledger/argument/policy errors. Ledger format: see
assets/tts-ledger.template.json. Ledger is committed text; media never enters git.
"""
import argparse
import datetime
import fcntl
import json
import os
import sys

ROLE_ENGINE = {
    "narration": "moss-nano-tts",  # CPU ONNX, 48 kHz stereo; -r reference clone or -v preset
    "scratch": "moss-nano-tts",
    "subject": "moss-voice",       # GPU 1.7B, 24 kHz mono; zero-reference timbre from description
    "sfx": "moss-sfx-v2",          # cinematic, 48 kHz stereo, <=30 s
    "ui-sfx": "moss-sfx-v2",       # rapid mechanical, sole SFX tool (policy 2026-11-13)
}
# Cloud TTS/image/video removed 2026-11-07: anything not on the local suite is refused.
ALLOWED_ENGINES = set(ROLE_ENGINE.values()) | {"moss-transcribe", "kokoro"}
RETAKE_LIMIT = 2  # fails on one line in one day => change the input, not the policy


def load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ledger not found: {path} (copy assets/tts-ledger.template.json)", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"ledger is not valid JSON: {e}", file=sys.stderr)
        sys.exit(2)


def today(entries, date):
    return [e for e in entries if e.get("date", "").startswith(date)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ledger")
    ap.add_argument("cmd", choices=["summary", "next", "log"])
    ap.add_argument("line_id", nargs="?")
    ap.add_argument("--role", choices=sorted(ROLE_ENGINE), default="narration")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--engine"); ap.add_argument("--voice"); ap.add_argument("--take", type=int)
    ap.add_argument("--result"); ap.add_argument("--rms-qa", dest="rms_qa"); ap.add_argument("--file")
    ap.add_argument("--line-id", dest="line_id_flag", help="alternative to the positional LINE_ID")
    a = ap.parse_args()
    a.line_id = a.line_id_flag or a.line_id

    # `log` is read-modify-write: hold an exclusive lock for the whole operation so
    # parallel batch writers serialise instead of dropping each other's entries.
    lockf = None
    if a.cmd == "log":
        if not os.path.isfile(a.ledger):
            load(a.ledger)  # prints the "ledger not found" hint and exits 2 before any lock file
        lockf = open(a.ledger + ".lock", "w")
        fcntl.flock(lockf, fcntl.LOCK_EX)
    led = load(a.ledger)
    entries = led.get("entries", [])
    day = today(entries, a.date)

    if a.cmd == "summary":
        per_engine = {}
        fails = 0
        fail_lines = {}
        for e in day:
            eng = e.get("engine", "?")
            per_engine[eng] = per_engine.get(eng, 0) + 1
            if e.get("result") != "PASS" or e.get("rms_qa") != "pass":
                fails += 1
                fail_lines[e.get("line", "?")] = fail_lines.get(e.get("line", "?"), 0) + 1
        print(json.dumps({
            "date": a.date, "takes": len(day), "by_engine": per_engine,
            "qa_failures": fails,
            "retake_rule_lines": sorted(l for l, n in fail_lines.items() if n >= RETAKE_LIMIT),
            "policy": "local-only; cloud engines rejected by log"}, indent=2))
        return

    if a.cmd == "next":
        if not a.line_id:
            print("next needs LINE_ID", file=sys.stderr); sys.exit(2)
        engine = ROLE_ENGINE[a.role]
        line_today = [e for e in day if e.get("line") == a.line_id]
        fails = sum(1 for e in line_today if e.get("engine") == engine and e.get("result") != "PASS")
        note = None
        if fails >= RETAKE_LIMIT:
            note = ("retake rule hit: change the input (text, voice description, reference clip), "
                    "not the engine - re-rolls are free, identical inputs are not")
        elif fails:
            note = f"{fails} failed take(s) logged today for this line on {engine}"
        print(json.dumps({"line": a.line_id, "role": a.role, "engine": engine,
                          "takes_today": len(line_today), "fails_today": fails,
                          "note": note,
                          "engine_source": "house default per role; the project's route table wins where it differs"},
                         indent=2))
        return

    if a.cmd == "log":
        if not a.line_id:
            print("log needs a LINE_ID (positional or --line-id); unattributable entries break the retake rule", file=sys.stderr)
            sys.exit(2)
        if a.engine:
            a.engine = os.path.basename(a.engine.strip()).lower().replace("_", "-")
            if a.engine not in ALLOWED_ENGINES:
                print(f"OUT OF POLICY (2026-11-07): engine '{a.engine}' is not callable in this pipeline. "
                      f"Allowed engines: {', '.join(sorted(ALLOWED_ENGINES))}.",
                      file=sys.stderr)
                sys.exit(2)
        missing = [k for k, v in dict(engine=a.engine, voice=a.voice, take=a.take,
                                      result=a.result, rms_qa=a.rms_qa).items() if v in (None, "")]
        # a PASS needs its media path (provenance); a failed attempt may have produced no file
        if (a.result or "").upper() == "PASS" and not a.file:
            missing.append("file")
        if missing:
            print(f"log needs --{(' --'.join(missing)).replace('_', '-')}", file=sys.stderr); sys.exit(2)
        a.result, a.rms_qa = a.result.upper(), a.rms_qa.lower()  # summary/next compare exact "PASS"/"pass"
        entry = {"date": a.date, "line": a.line_id, "engine": a.engine,
                 "voice": a.voice, "take": a.take, "result": a.result,
                 "rms_qa": a.rms_qa}
        if a.file:
            entry["file"] = a.file
        entries.append(entry)
        led["entries"] = entries
        tmp = a.ledger + ".tmp"
        with open(tmp, "w") as f:
            json.dump(led, f, indent=2)
            f.write("\n")
        os.replace(tmp, a.ledger)  # atomic: a crash never truncates the committed ledger
        if lockf:
            fcntl.flock(lockf, fcntl.LOCK_UN)
        print(json.dumps({"logged": True, "takes_today": len(today(entries, a.date))}, indent=2))


if __name__ == "__main__":
    main()

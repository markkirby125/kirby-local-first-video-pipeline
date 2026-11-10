#!/usr/bin/env python3
"""audio_qa.py - per-second RMS speech gate for TTS takes. Exit 0 PASS, 1 FAIL.

Stops bad takes entering the cut: an overall-mean check hides a take that is mostly
silence (verified failure, 2026-11-06). Also defuses the VLC trap: m4a and
high-samplerate stereo exports decode near-silently in VLC but correctly in ffmpeg/mpv -
this script uses ffmpeg, so it is the authority, and a VLC-only "it's silent" report is
never a re-roll reason.

Usage: audio_qa.py FILE [--min-speech SEC] [--threshold DB] [--json]
  --min-speech  minimum total speech seconds expected (default: any speech at all)
  --threshold   window RMS above this counts as speech (default -38 dB)
Deps: python3 stdlib + ffmpeg on PATH. No numpy/scipy needed.
"""
import argparse
import json
import re
import subprocess
import sys


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def rms_windows(path, threshold_db):
    """One RMS value per ~1 s window via ffmpeg astats with forced 1 s sample blocks."""
    sr = 48000
    probe = run(["ffprobe", "-v", "error", "-select_streams", "a:0",
                 "-show_entries", "stream=sample_rate", "-of", "csv=p=0", path])
    if probe.stdout.strip().isdigit():
        sr = int(probe.stdout.strip())
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af",
             f"asetnsamples=n={sr}:p=0,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-",
             "-f", "null", "-"])
    if r.returncode != 0:
        print(f"FAIL decode: ffmpeg cannot read {path}\n{r.stderr[-400:]}", file=sys.stderr)
        return None, sr
    vals = []
    for m in re.finditer(r"RMS_level=(-?[\d.]+|-inf)", r.stdout):
        v = m.group(1)
        vals.append(float("-120") if v == "-inf" else float(v))
    return vals, sr


def loudness(path):
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"])
    m = re.search(r"I:\s+(-?[\d.]+) LUFS", r.stderr[r.stderr.rfind("Summary:"):] if "Summary:" in r.stderr else r.stderr)
    return float(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--min-speech", type=float, default=0.0, help="min speech seconds expected")
    ap.add_argument("--threshold", type=float, default=-38.0, help="window dB threshold for speech")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    vals, sr = rms_windows(a.file, a.threshold)
    if vals is None:
        sys.exit(1)
    if not vals:
        print("FAIL no audio windows measured", file=sys.stderr)
        sys.exit(1)

    speech = [i for i, v in enumerate(vals) if v > a.threshold]
    n = len(speech)  # 1 s windows, so n == speech seconds
    lead = speech[0] if speech else None
    trail = len(vals) - 1 - speech[-1] if speech else None
    span = (speech[0], speech[-1] + 1) if speech else None  # seconds, half-open
    lufs = loudness(a.file)
    if lufs is None:
        print("warning: integrated loudness could not be measured (advisory only; take judged on speech windows)", file=sys.stderr)

    ok = n > 0 and n >= a.min_speech
    rep = {"file": a.file, "windows": len(vals), "speech_windows": n,
           "speech_seconds": float(n), "speech_span": span,
           "leading_silence_s": lead, "trailing_silence_s": trail,
           "lufs_integrated": lufs, "threshold_db": a.threshold,
           "result": "PASS" if ok else "FAIL"}
    if a.json:
        print(json.dumps(rep, indent=2))
    else:
        w = max(len(str(k)) for k in rep)
        for k, v in rep.items():
            print(f"{k:>{w}} : {v}")
        if not ok:
            print("\nFAIL: %s" % ("no speech detected above %.0f dB" % a.threshold if n == 0
                                 else "speech %.1f s < required %.1f s" % (n, a.min_speech)),
                  file=sys.stderr)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

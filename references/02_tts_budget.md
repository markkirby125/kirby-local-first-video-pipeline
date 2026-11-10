# 02 - The MOSS Audio Suite and the Ledger

Audio is 100% local. Engines are chosen by **role**, not by budget — there is no spend to
gate and no quota to protect:

```text
NARRATION / HOST        moss-nano-tts    (CPU, 48 kHz stereo) — voice clone from a locked
                                           3–5 s reference clip (-r) or a preset (-v Junhao)
CHARACTER / SUBJECT VO  moss-voice       (GPU 1.7B, 24 kHz mono) — zero-reference timbre
                                           from a text description (-i)
CINEMATIC SFX           moss-sfx-v2      (48 kHz stereo, ≤30 s) — paper rustles, gavel
                                           strikes, document stamps, monitor bleeps
RAPID / UI SFX          sa3-sfx          (44.1 kHz stereo) — mechanical clicks, transitions
VERIFICATION            moss-transcribe  (0.9B) — timestamps, diarization, duration checks
LEGACY SCRATCH          kokoro bm_george (24 kHz mono) — only where a project already uses
                                           it; new projects scratch with moss-nano-tts
```

`moss-nano-tts` is fast enough (~2.4 s per 5 s take on CPU, zero VRAM) that a separate
scratch pass is optional, not required: generate the real narration first. Where a
scratch-then-final workflow is still used, finals are drop-in replacements of identical
or re-measured duration (verified with `moss-transcribe`).

## Voice locks — what the cloud removal bought us

- **One fixed voice per character per season.** The lock lives in the project's voice
  bible/cast file, not in per-line code: narration locks to the project's narrator
  reference clip (the reference channel's is a forensic-narrator sample; `Junhao` is the clean
  fallback preset); each character locks to one `moss-voice` description string.
- Because every engine is local, acoustic continuity is permanent — the same reference
  clip or description reproduces the same voice in every episode, forever. Provider voice
  drift (the old Gemini/ElevenLabs problem) cannot happen.
- **Retake rule:** two failed takes on a line in one day ⇒ change the input (text, voice
  description, reference clip), not the policy. Cloud re-rolls are not an exit; there is
  no ladder to climb.

## The ledger (`@tts_ledger`)

Every audio generation is logged — appended immediately after QA, with result and rms_qa recorded.
Committed as text. Template: `assets/tts-ledger.template.json`; entries:

```json
{ "date": "2026-11-08", "line": "ep02-<role>-014", "engine": "moss-voice",
  "voice": "weary gravelly 50yo belter miner", "take": 1, "result": "PASS",
  "rms_qa": "pass", "file": "voice/ep02/<role>-014-t1.wav" }
```

The ledger is a **provenance + QA record**, not a budget: it proves every sound in the
cut came from a route the table names, and it feeds the retake rule.
`bin/tts_budget.py LEDGER CMD …` (named for its budget-era origin; LEDGER is the ledger
path, e.g. `tts-ledger.json`) reads it: `summary` prints today's
takes and QA failures; `next LINE_ID --role narration|scratch|subject|sfx|ui-sfx` reports the house-default
engine for that role and today's fails on the line (it does not read the route table;
where the project's route table differs, the route table wins);
`next` roles map to route-table keys as: `narration` to `tts.narration`, `scratch` to
`tts.scratch`, `subject` to `tts.character_voice`, `sfx` to `sfx.primary`, `ui-sfx` to
`sfx.rapid`. Full `log` form (every take, pass or fail):
`bin/tts_budget.py tts-ledger.json log --line-id ep02-014 --engine moss-voice --voice "<description>" --take 1 --result PASS --rms-qa pass --file voice/ep02/014-t1.wav`
(a failed attempt uses `--result FAIL --rms-qa fail` and may omit `--file`).
`log` **refuses to record a cloud engine** — the out-of-policy rule is enforced in code,
not in memory.

## Audio QA (`bin/audio_qa.py`) — the gate that stops bad takes

Run on EVERY take before it enters the cut:

- **Per-second RMS windows** (ffmpeg `astats=reset=1`), speech threshold ≈ -38 dB — an
  overall mean hides an 8-second-silence take (this exact failure happened).
- Span check: speech must cover the expected line span; leading/trailing silence is
  trimmed and re-measured, not "accepted with a note".
- Loudness report per take (integrated LUFS) so takes are compared like-for-like; final
  mix normalises to the channel target in assembly.
- **VLC trap**: m4a and high-samplerate stereo exports decode near-silently in VLC and
  perfectly in mpv/ffmpeg. A "silent take" report from VLC is never a re-roll reason —
  the script (ffmpeg) is the authority; WAV copies are the listening format.

Exit code 0 = PASS (speech found, and at least `--min-speech` seconds if set); exit 1 = FAIL
(no speech above the threshold, too little speech, or ffmpeg cannot decode the file). It
prints the speech-window count, span, leading/trailing silence and LUFS, not a per-window
list of failures. Wire it into the pipeline so no
human (or agent) waves a take through on faith.

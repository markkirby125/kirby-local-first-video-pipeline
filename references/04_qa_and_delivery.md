# 04 - QA Gates and Delivery

## Audio

- `bin/audio_qa.py <file>` on **every** take before acceptance (per-second RMS,
  speech-span, loudness — see `02`). FAIL = re-roll with a changed input per the retake
  rule, never "accept with a note".
- **Duration verification:** run `moss-transcribe` on the assembled narration track and
  check its measured timestamps against the script cuts — the machine-checkable
  substitute for "listening".
- Final mix measured, not heard: loudness-normalise to the channel target. House default
  is **−14 LUFS / TP ≤ −1.0 dBTP** (the reference channel); channels with their own spec keep
  their own numbers.
- Listen-backs in mpv/ffmpeg or WAV copies, never VLC-alone verdicts (decode trap, `02`).

## Visual

- Every channel's own review gate runs on the final export (frame extraction + agent
  visual open with the sampling stated; the sci-fi microdrama channel's own freeze-check script with
  deliberate-holds reviewed by eye; pixel channels' slop checklist). This skill adds the
  routing/provenance audit, not a second visual opinion:
  - [ ] Every engine in the delivery is named in the route table — nothing outside the
    local suite (the ledger cannot even log a cloud engine; see `02`).
  - [ ] Every take in the cut has `rms_qa: pass` in the ledger.
  - [ ] Narration durations verified against the script via `moss-transcribe`.

## Git hygiene (microdrama-channel rules, house-wide here)

- Commit text only: scripts, shot lists, ledgers, route tables, upload text. Media
  (frames, clips, audio, exports) stays out of git and is backed up separately.
- Commit messages plain, short, present tense. No co-author, "Generated with", or
  session-attribution lines of any kind.

## Delivery note (per video)

State, honestly: route table used (and any dated deviations), ledger summary (takes per
engine, retakes, QA failures), **cloud usage: zero — and out of policy, not merely
unspent**, QA gate results with the sampling actually used, and anything re-voiced or
re-rolled plus why. A delivery that cannot state its provenance is not done.

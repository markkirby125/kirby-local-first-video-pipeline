# 04 - QA Gates and Delivery

## Pre-production / Pre-TTS Gate (before scripting & before audio)

- **Engine-readable phonetic respellings (directional, single-source practitioner transcript anecdote — Edward Sturm Ep. 1,233 featuring Jonathan Berthold, logged in `../../docs/yt_dossier_nov2026_mapping.md` when in monorepo):** Before invoking `moss-voice` or `moss-nano-tts`, log every spoken proper noun in the project's `bible/pronunciation.md` (required whenever proper nouns appear in speech; distinct from `bible/voices.md` character style rows) and inject approved English-readable respellings (never raw IPA; approved by a human or named independent reviewer — if no human or independent reviewer is available, put `PENDING` in `approved_by`, stop TTS synthesis for the affected lines, and report to the operator) into the script-text input for TTS while authoring visible subtitle tracks and on-screen caption text from the canonical script (and, wherever `03_visual_routes.md` / `05_channel_integrations.md` feed `moss-transcribe` `.ass`/`.srt` output into burn-in for respelled dialogue or narration, run a post-ASR replacement pass from `bible/pronunciation.md` so respellings never appear on screen). For voice selection, `bible/voices.md` is the canonical voice lock for **both** engines (`moss-nano-tts` uses the locked `-r` clone ref or `-v` preset recorded there, while `moss-voice` uses the documented `-i <description>` voice description); `@tts_ledger`'s `voice` field strictly records what was used post-QA. Note: English-readable respellings are heuristics, not a zero-error guarantee — post-synthesis `moss-transcribe` verification below can flag possible engine misreads for human confirmation. Inline schemas:
  ```markdown
  <!-- bible/pronunciation.md -->
  | proper_noun | respelling | approved_by | notes |
  |---|---|---|---|

  <!-- bible/voices.md -->
  | character | engine | voice_or_ref | style_note | locked_on | test_sentence_result |
  |---|---|---|---|---|---|
  ```
- **Primary-source claim ledger for stats & quotes (Nov 2026):** Before generating agent-authored scripts (pre-production claim sourcing) and before TTS synthesis (final gate), log every real-world verifiable factual claim (numbers, dates, quotes, named attributions, and causal claims — **invented in-world facts in fiction are exempt; real-world claims stay in scope even when a character says them**; **common knowledge** such as undisputed encyclopedic facts without novel attribution, e.g., water freezes at 0 °C or Paris is the capital of France, is exempt) in the project's `bible/claims.md` using the inline schema below:
  ```markdown
  | claim | primary_source_url | quoted_passage | verified_by | verified_date |
  |---|---|---|---|---|
  ```
  Ungrounded AI-authored summaries are **not** valid primary sources: `quoted_passage` must be copied verbatim from the fetched `primary_source_url` (recording fetch date in `verified_date`, ISO `YYYY-MM-DD`), and the generating agent must not record itself as `verified_by` for its own claims (`verified_by` records the verifying human or an independent verifying agent; any close or ambiguous source match requires human sign-off or a second independent verifier — if no human or independent verifier is available, put `PENDING` in `verified_by`, stop work on the affected lines, and report to the operator; never self-certify). Missing sources or unverified real-world claims block script generation, voice synthesis, and final cut assembly for the affected lines.
- Pre-production & pre-TTS gate checklist:
  - [ ] Pre-production `bible/claims.md` ledger populated & independently verified for all spoken/visual real-world stats and factual claims.
  - [ ] Pre-TTS `bible/pronunciation.md` respelling heuristics logged & approved for every spoken proper noun.
  - [ ] Consent record ID and date noted as prose under the `bible/voices.md` table (never a new column or row) for every `-r` reference clip of a real person's voice or of unknown origin (consent gate, `02_tts_budget.md`).

## Audio

- **Post-synthesis / pre-accept `moss-transcribe` proper-noun check:** Before marking a synthesized take accepted in QA, verify every rendered proper noun with `moss-transcribe` on the output audio, compare ASR output against the canonical `proper_noun` in `bible/pronunciation.md` (accepting either the canonical form or its approved respelling; the respelling is TTS input only), flag any ASR mismatch for human listen-back, and trigger a retake when a human confirms an engine misread (ASR transcription errors on accurate audio do not force a retake; **autonomous fallback:** if no human is available to resolve a mismatch, mark the take `PENDING`, stop, and report to the operator — never accept an unconfirmed mismatch; reduces unverified AI-podcast mispronunciation risk).

- `bin/audio_qa.py <file> --min-speech <expected speech seconds, 1-2 s below the line length>` on **every** take before
  acceptance (without `--min-speech` the "too little speech" FAIL cannot fire; per-second RMS,
  speech-span, loudness; see `02`). Log every take, pass or fail, with `bin/tts_budget.py tts-ledger.json log …`
  (full form in `02`). FAIL = re-roll; after two failed takes on a line in
  one day, change the input per the retake rule. Never "accept with a note".
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
  - [ ] Post-synthesis `moss-transcribe` proper-noun check passed and canonical spelling restored on captions/subtitles.
  - [ ] Every engine in the delivery is named in the route table — nothing outside the
    local suite (the ledger cannot even log a cloud engine; see `02`).
  - [ ] Every take in the cut has `result: PASS` and `rms_qa: pass` in the ledger, and `summary` shows `unresolved_pending_lines: []` (a PENDING take cannot ship).
  - [ ] Narration durations verified against the script via `moss-transcribe`.

## Git hygiene (microdrama-channel rules, applied here)

- Commit text only: scripts, shot lists, ledgers, route tables, upload text. Media
  (frames, clips, audio, exports) stays out of git and is backed up separately.
- Commit messages plain, short, present tense. No co-author, "Generated with", or
  session-attribution lines of any kind.

## Delivery note (per video)

State, honestly: route table used (and any dated deviations), required pre-production `bible/claims.md` and `bible/pronunciation.md` ledger sign-off plus the voice-clone consent record and post-synthesis `moss-transcribe` proper-noun check, ledger summary (takes per engine, retakes, QA failures, `unresolved_pending_lines: []`), **cloud usage: zero — and out of policy, not merely unspent**, QA gate results with the sampling actually used, and anything re-voiced or re-rolled plus why. A delivery that cannot state its provenance is not done.

# Local-First Video Pipeline 🎥🛡️

> **SOP for producing narration-led video on a 100% local stack: the MOSS audio suite
> (`moss-nano-tts` narration · `moss-voice` character VO · `moss-sfx-v2` / `sa3-sfx`
> sound design · `moss-transcribe` verification), MOSS MCP stills, coded ffmpeg/PIL
> assembly. Cloud TTS (Gemini, ElevenLabs) and generative video models are OUT OF
> POLICY — never called, no gates, no quotas.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Architecture: Hollow Shell](https://img.shields.io/badge/Architecture-Hollow%20Shell-brightgreen.svg)](SKILL.md)

Every engine and speed number in this skill was **measured on the production machine and
dated** (2026-11-07), and the pipeline is built to read actual errors rather than trust
stored facts. The out-of-policy rule is enforced in code (`bin/tts_budget.py log`
refuses cloud engines), not in memory.

## The doctrine

```text
LOCAL APPS ONLY — every stage, unlimited
┌──────────────────────────────────────────────────────┐
│ moss-nano-tts   narration & host VO (CPU, 48 kHz)    │
│ moss-voice      character / subject VO (GPU, 1.7B)   │
│ moss-sfx-v2     cinematic sound design (48 kHz)      │
│ sa3-sfx         rapid mechanical UI SFX (44.1 kHz)   │
│ moss-transcribe timestamps, diarization, duration QA │
│ MOSS MCP        stills, plates, thumbs (local GPU)   │
│ Chromium/PIL    inserts, captions, overlays          │
│ ffmpeg          assembly, repair, packaging          │
└──────────────────────────────────────────────────────┘
There is no cloud column. Out of policy since 2026-11-07: Gemini, ElevenLabs,
Nano Banana, Flow/Veo, LTX-Video — motion is coded, not generated.
```

## What's in the box

- `references/01` — measured local capacity table + the read-the-error rule + route-table format
- `references/02` — the MOSS audio roles, voice locks, the retake rule, ledger format, audio QA
- `references/03` — MOSS-first stills; the no-generative-video policy; coded motion recipes
- `references/04` — QA gates: per-second-RMS audio QA, duration verification, provenance audit, git hygiene
- `references/05` — per-channel wiring: Fast Evidence (reference), pixel-art football channel, sci-fi microdrama + tabletop-scenery channels (legacy history), stickman
- `bin/audio_qa.py` — the audio gate that stops bad takes (stdlib + ffmpeg only)
- `bin/tts_budget.py` — ledger reader/writer; refuses any engine outside the local suite
- `assets/` — route-table and TTS-ledger templates (local-only shapes)

### 🪄 The Magic Prompt

Copy and paste this into any AI coding app (Claude Code, Cursor, Windsurf, Grok, Kimi, Reasonix):

```markdown
@agent Install the Local-First Video Pipeline skill from: https://github.com/markkirby125/kirby-local-first-video-pipeline
1. Read `SKILL.md` and `references/` from the repository.
2. Place into your environment's skills/rules directory preserving the dispatcher structure.
3. Confirm when installation is complete.
```

## Attribution

Distilled from the author's internal production practice, re-verified 2026-11-07, the day cloud TTS and generative video were removed from policy.

## License

MIT License. Copyright (c) 2026 Mark Kirby. Distributed as part of the [Kirby Skills Library](https://github.com/markkirby125/kirby-skills).

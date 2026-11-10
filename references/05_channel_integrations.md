# 05 - Channel Integrations

How the routing/ledger layer wraps each channel in the stack. The channel's own skill or
spec runs production; this layer decides where generation happens. Since 2026-11-07 the
doctrine is local-only for every channel this skill wires; the two legacy cloud-era
sections are kept as history, not as routes.

## The reference channel (reference implementation)

Narration-led forensic explainer; the first full build on the local-only doctrine and
this skill's integration test. Route table: `moss-nano-tts` narration (locked forensic
narrator reference clip, `Junhao` as clean preset) → `moss-voice` expert/patient quotes →
`moss-sfx-v2` cinematic stamps/gavels/bleeps + `sa3-sfx` UI clicks → `moss-transcribe`
duration verification → MOSS stills → Chromium captions / PIL overlays → ffmpeg assembly
→ audio QA + provenance audit. No generative video. Masters −14 LUFS / −1.0 dBTP.

## Pixel-art football channel (8-bit)

Already fully local by design: deterministic pixel renderer, synthesised chiptune,
ffmpeg; captions instead of TTS. Uses this skill for the provenance audit (perpetually
"zero cloud") and — if narration is ever added — `moss-nano-tts` across its 20 languages.
`kirby-pixel-character-consistency` governs its characters.

## Narrated sci-fi microdrama channel — legacy cloud-era section (history)

Pre-rule routing was Veo shots via Flow + Gemini TTS dialogue (per-character dialect prompts) with
ElevenLabs as escape hatch. Those routes are **out of policy now**. Its local floor is
this skill's: `moss-voice` designs <character A>, <character B>, <character C> timbres offline with permanent
continuity, `moss-sfx-v2` for airlocks/reactor hums/hull groans, `moss-nano-tts` for
radio comms and PA announcements, and `moss-transcribe` feeds speaker-tagged `.ass`
straight into the channel's own subtitle script. Voice locks stay in the project's voice bible. Historical only: a
project whose spec still names cloud routes must be migrated to the local suite before
production. (Same rule as `references/00_dispatcher.md`.)

## Tabletop-scenery channel — legacy cloud-era section (history)

Pre-rule design centred on Veo-native-sound ambience Shorts with a 40-credit/Short
ceiling. Out of policy now; the local replacements: `moss-voice` for NPC/monster timbres
(goblins, dragons, tavern keeps), `moss-sfx-v2` for spells/combat/doors, `moss-transcribe`
for session playbacks and campaign logs, the channel's own packaging script (−14 LUFS / −1.0 dBTP) as the
local packaging floor.

## Stickman channels

Deterministic stickman rendering (stickman-shorts family) — local by design; this layer
audits provenance. Thumbnail assists would be MOSS first.

## Wiring a new channel (checklist)

1. Copy the two templates from `assets/` into the channel repo as `route-table.json` and
   `tts-ledger.json`; fill the route table
   (local engines only; the templates have no cloud fields, and the route table is checked
   by manual audit, while the ledger is checked in code). Delete the `_example_*` keys
   after copying. The two gate scripts stay in
   this skill: run `bin/audio_qa.py` and `bin/tts_budget.py` by their path in the installed
   skill folder (or copy `bin/` into the channel repo); a missing script means the gate did
   not run, so stop.
2. Fill the route table's `loudness_target` and `review_gate` fields
   (house default if none: −14 LUFS / TP ≤ −1.0 dBTP).
3. First video: state provenance in the delivery (expected: zero cloud — permanently).
4. Deviations are not expected; any change of *local* route gets a dated note — the
   drift rule.

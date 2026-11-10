# Dispatcher: Local-First Video Pipeline

SOP for producing narration-led video across the local production stack under one doctrine:
**local apps only.** Every stage runs on models and tools installed on this machine —
there is no cloud column, no budget gate, and no quota to protect. Updated 2026-11-07,
when cloud TTS (Gemini, ElevenLabs) and generative video models were removed from policy
house-wide. The routes below were verified on the author's machine on 2026-11-07 and are
summarised in this skill.

## The doctrine in one table

| Stage | Route (always local, unlimited) |
|---|---|
| Script / shot list / narration text | Agent, no media generated |
| Narration & host VO | **moss-nano-tts** — CPU ONNX, 48 kHz stereo, ~2.4 s per 5 s take; voice clone from a 3–5 s reference clip (`-r`) or a preset (`-v Junhao`) |
| Character / subject / expert VO | **moss-voice** — GPU 1.7B, 24 kHz mono; zero-reference timbre from a text description (`-i`) |
| Cinematic SFX & stingers | **moss-sfx-v2** — 48 kHz stereo, up to 30 s (paper rustles, gavel strikes, document stamps, monitor bleeps) |
| Rapid / mechanical UI SFX | **sa3-sfx** — 44.1 kHz stereo, ~14 s per 4 s take (clicks, transitions) |
| Timestamps, diarization, duration QA | **moss-transcribe** — 0.9B ASR + diarization, `.ass`/`.srt` with 10 ms timestamps |
| Stills, plates, thumbnails | **MOSS MCP** (`moss-image:*` → SwarmUI on its default local port) — unlimited |
| Insert graphics, captions, subs | Chromium `render.mjs` / the channel's own subtitle script / pixelkit / PIL |
| Assembly, repair, packaging | ffmpeg + PIL overlays — **coded motion only, no video models** |
| QA | Per-second RMS audio QA (`bin/audio_qa.py`) + moss-transcribe duration verification |

## 🚫 Out of policy (removed 2026-11-07, house-wide)

* **Cloud TTS — Gemini, ElevenLabs**: never called, for any reason. There is no budget
  gate left to approve them; a take that fails locally is re-rolled or re-voiced locally.
* **Generative video models — cloud (Flow/Veo) and local (LTX-Video)**: not declared in
  any route table. Motion is coded (ffmpeg/PIL) only.
* The two channels that predate the rule (the sci-fi microdrama and tabletop-scenery channels) are noted as history
  in `05_channel_integrations.md`. Historical only: a project whose spec still names cloud
  routes must be migrated to the local suite before production.

## 🏷️ Canonical Asset Tag Register

| Asset Variable | Data Type | Role |
|---|---|---|
| `@route_table` | Data (per project) | Stage→engine choices, declared up front; the only place routing is decided. Template in `assets/route-table.template.json`. Cloud engines are never declared. |
| `@tts_ledger` | Data (per project, committed) | Every audio generation: date, engine, voice/clone ref, line id, take, QA result. Appended immediately after QA, with result and rms_qa recorded; audited after. Template in `assets/tts-ledger.template.json`. |
| `@retake_rule` | Rule | Two failed takes on a line in one day ⇒ change the input (text, voice description, reference clip), never the policy. |
| `@qa_gates` | Checklist | Audio QA (`bin/audio_qa.py`) on every take; moss-transcribe duration verification against the script; the project's own visual review gate on every video. |

## 🧭 Operational Routing Matrix

| Module | Read when | Covers |
|---|---|---|
| [`01_routing_table.md`](01_routing_table.md) | Always, first | Measured local capacity (dated), verify-by-reading-errors, route-table format. |
| [`02_tts_budget.md`](02_tts_budget.md) | Any narration/dialogue/SFX | The MOSS audio roles, ledger discipline, voice locks, the retake rule. |
| [`03_visual_routes.md`](03_visual_routes.md) | Stills or motion | MOSS-first stills, the no-video-models policy, insert graphics. |
| [`04_qa_and_delivery.md`](04_qa_and_delivery.md) | Before anything ships | Audio QA, duration verification, provenance audit, git hygiene, delivery notes. |
| [`05_channel_integrations.md`](05_channel_integrations.md) | Starting a channel job | Per-channel wiring: Fast Evidence (reference), pixel-art football channel, sci-fi microdrama + tabletop-scenery channels (legacy), stickman. |

## 🛑 When NOT to Use This Skill

* **The channel already has a stricter pipeline skill** (a stricter project-specific
  pipeline spec, if the project has one): that spec runs the film; this skill supplies the
  routing and ledger layer around it.
* **Pure-text or code tasks with no media**: nothing to route.

## Machine facts this skill depends on (verified on one local machine, 2026-11-07)

- SwarmUI + ComfyUI on a local GPU (>= 16 GB VRAM), each on its default local port.
- Global CLIs on `~/.local/bin`: `moss-nano-tts`, `moss-voice`, `moss-sfx-v2`, `moss-transcribe`, `sa3-sfx`. Call them directly; never activate virtualenvs manually.
- `moss-nano-tts` runs purely on CPU (ONNX, 8 threads, 0 MB VRAM) — it leaves VRAM free for image generation. Prefer it for narration for that reason alone.
- **Gotcha:** the first MOSS MCP image call after idle loads the model into VRAM and the MCP call may time out at 30 s while SwarmUI keeps generating — poll the output file; the image lands.
- **Listen in mpv/ffmpeg, never VLC-alone:** m4a and high-samplerate stereo exports can decode near-silently in VLC while ffmpeg/mpv read them correctly. `bin/audio_qa.py` uses ffmpeg and is the authority.

## 🔗 Related Skills in the Kirby Ecosystem

* [Kirby Pixel Character Consistency](../../kirby-pixel-character-consistency/SKILL.md) — sprite identity for the pixel/stickman channels.
* [Kirby YT Faceless Formula](../../kirby-yt-faceless-formula/SKILL.md) — production pipeline patterns.
* [Kirby Skills Collection](../../kirby-skills-collection/SKILL.md) — master registry.

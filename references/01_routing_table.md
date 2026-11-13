# 01 - The Routing Table

Every engine in this table is **installed on this machine and verified working**; speed
numbers were measured and dated. There are no quotas to track — but local services still
fail in local ways, and the rule that keeps this table honest is unchanged:

> **Read the error, not the doc.** Attempt the request; on failure read the actual error
> (VRAM cold-load timeouts, missing weights, GPU OOM), log the failed attempt in the
> ledger (`--result FAIL --rms-qa fail` with the usual fields, full form in `02`; `--file`
> may be omitted when no output was produced), name the
> error in the delivery note (a route change also gets a dated deviation whose reason names
> it), and fix the route. Never assume a stored fact is still true. Refresh this file when observation
> contradicts it (then update the number and date).

## Measured local capacity (planning defaults)

Speeds below were measured on one local 16 GB-class GPU; expect them to differ on other hardware.

| Resource | Output | Speed (measured) | Hardware | As of |
|---|---|---|---|---|
| `moss-nano-tts` (MOSS-TTS-Nano-100M-ONNX) | 48 kHz stereo speech | ~2.4 s for a 5 s take | CPU (ONNX, 8 threads, 0 MB VRAM) | 2026-11-07 |
| `moss-voice` (MOSS-VoiceGenerator 1.7B) | 24 kHz mono dialogue | ~4.1 s for a short take | GPU (bf16, ~30 tok/s) | 2026-11-07 |
| `moss-sfx-v2` (MOSS-SoundEffect-v2.0 1.3B) | 48 kHz stereo, ≤ 30 s | ~30 s for a 4 s SFX | GPU DiT + CPU DAC | 2026-11-07 |
| `sa3-sfx` (Stable Audio Open 1.0) | 44.1 kHz stereo | ~14 s for a 4 s SFX | GPU (not used for SFX, policy 2026-11-13) | 2026-11-07 |
| `moss-transcribe` (MOSS-Transcribe-Diarize 0.9B) | text + `.ass`/`.srt`, 10 ms timestamps | ~7.9 s for an 8.5 s clip | GPU | 2026-11-07 |
| MOSS MCP stills (SwarmUI/ComfyUI, default local ports) | episode-grade frames | unlimited, bulk fine | local GPU (>= 16 GB VRAM) | 2026-11-07 |
| ffmpeg / PIL / headless Chromium | inserts, captions, assembly | unlimited, byte-identical re-renders | CPU | 2026-11-07 |
| Cloud TTS / image / video APIs | — | **out of policy — never declared** | — | 2026-11-07 |

## Route-table format (per project)

Declared before production starts; the only place routing is decided. Template:
`assets/route-table.template.json`. Cloud engines are not fields here — there is no
"fallback", "overflow" or "gate" any more.

```json
{
  "project": "reference-channel",
  "declared": "2026-11-07",
  "tts": { "narration": "moss-nano-tts", "character_voice": "moss-voice", "scratch": "moss-nano-tts" },
  "sfx": { "primary": "moss-sfx-v2", "rapid": "moss-sfx-v2" },
  "transcription": "moss-transcribe",
  "stills": { "default": "moss" },
  "video": { "default": "none-needed", "policy": "no-generative-video-models" },
  "assembly": "ffmpeg-local",
  "loudness_target": { "lufs": -14, "truepeak_dbtp_max": -1.0, "_source": "house default (channel has no own spec yet)" },
  "review_gate": "audio_qa.py per take; ffmpeg frame extraction + agent visual open on final MP4",
  "deviations": []
}
```

Rules:
* A stage missing from the table means "local default" — the table names *which local*,
  never a cloud engine.
* Changing a route mid-production is a table edit + a dated note, never a silent switch
  (the human-drift rule from `kirby-pixel-character-consistency`, applied to routing).
* Ledger and route table are **committed text**; media never enters git.

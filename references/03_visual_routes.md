# 03 - Visual Routes: Stills and Coded Motion

## Stills: MOSS, always

- **MOSS MCP** (`moss-image:generate_image` / `list_models` / `check_status`) drives
  SwarmUI + ComfyUI on a local GPU (>= 16 GB VRAM) — verified producing episode-grade frames
  (720×1280 cel-style). Unlimited, no daily cap. Installed models: MOSS Image finetune
  (default), Z-Image Turbo FP8, SDXL 1.0.
- **Gotcha (verified):** the first call after idle loads the model into VRAM and the MCP
  call may time out at 30 s while SwarmUI keeps generating — poll the output file; the
  image lands.
- Reshoots, retakes, plates, style frames, thumbnails: all local, all free. Bulk
  generation is explicitly fine.
- Cloud image APIs (Nano Banana etc.) are **out of policy**. If MOSS can't match a
  locked look, change the prompt, seed, or installed model — never the engine class.

## Motion: coded assembly only — no video models

**Generative video is out of policy, cloud and local.** History, for context only:
Flow/Veo was the old gated route, and LTX-Video 2B was verified rendering locally on the
one local 16 GB-class GPU (480×704×65 frames in under 40 s) on 2026-11-07 — the same day both were
removed from policy. The motion recipes are not distributed with this skill.

Motion is *made*, not generated:

- **ffmpeg assembly**: concat / drawtext / zoompan / xfade over MOSS stills and coded
  plates — pans, punches, wipes, document pushes are all filter graphs.
- **PIL overlays**: captions, evidence tags, highlight boxes, lower thirds, pixel fonts.
  (Prefer Pillow over the GIMP adapter in batch — the Flatpak batch-hang gotcha.)
- **Repair locally, never re-roll** — the ep01 rule, and cheaper than ever now that
  re-rolls cost nothing but time: a bad frame is fixed with compositing, not regeneration.

## Insert graphics and text — always local

Headless Chromium (`<project>/templates/tools/render.mjs`), the channel's own subtitle script (ass/srt + libass
burn-in — feed it `moss-transcribe` output directly), pixelkit's 5x7 font stack for pixel
channels, Pillow for one-off fixes. Zero API dependencies; byte-identical re-renders.

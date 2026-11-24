---
name: kirby-local-first-video-pipeline
description: Standard operating procedure for producing narration-led video on a 100% local stack - MOSS audio suite (moss-nano-tts narration, moss-voice character VO, moss-sfx-v2 sound design (sole SFX tool), moss-transcribe verification), MOSS MCP stills, coded ffmpeg/PIL assembly. Cloud TTS (Gemini, ElevenLabs) and generative video models are OUT OF POLICY in this pipeline - never called, no budget gates, no quotas. Use for any video task on a local-only stack.
category: technique
triggers: [local-first, local-only, video-pipeline, narration, moss-nano-tts, moss-voice, moss-sfx-v2, moss-transcribe, moss-image, no-cloud-tts, kokoro]
risk: unverified
author: paul-kirby
tags: [kirby, ai-agent, workflow]
---

# SOP: Local-First Video Pipeline (100% local apps)

> **SUPERSEDED IN PART, 2026-11-24.** `moss-nano-tts` and `moss-voice` are not installed: you retired them on 2026-11-11 (quality rejected; see `~/AI_projects/youtube/CLAUDE.md`, Master Audio Policy, rule 2), and `~/moss-nano` was archived at `~/AI_projects/archive/retired-2026-11-23/moss-nano`. The single TTS engine is now `moss-tts` (GPU). Every `moss-nano-tts` or `moss-voice` route, CPU/VRAM figure and timing below describes the retired engines as of 2026-11-07 and does not apply to `moss-tts`. `moss-sfx-v2`, `moss-transcribe` and `moss-image` are unchanged and installed. When this file and `youtube/CLAUDE.md` disagree, `youtube/CLAUDE.md` wins.

**To execute this skill, you MUST first read the dispatcher instructions located at:**
`references/00_dispatcher.md`

Do not guess or hallucinate the instructions. Read the file above to proceed.

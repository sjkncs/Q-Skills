---
name: mulerouter
description: Generates images, videos, audio, speech, and music using MuleRouter or MuleRun multimodal APIs. Text-to-Image, Image-to-Image, Text-to-Video, Image-to-Video, Reference-to-Video, Video-to-Video, video editing (VACE, keyframe interpolation), Text-to-Speech, Text-to-Music. Use when the user wants to generate, edit, or transform images, videos, speech, or music using AI models like Wan2.6, Veo3, Nano Banana Pro, Midjourney, Kling V3, Kling V3 Omni, MiniMax Speech 2.8, MiniMax Music 2.5, ByteDance Seedance 2.0.
compatibility: Requires Node.js 18+, the `mulerouter` npm CLI, MULEROUTER_API_KEY env var, and one of MULEROUTER_BASE_URL or MULEROUTER_SITE env var. Needs network access to api.mulerouter.ai or api.mulerun.com. The API key is sent in Authorization headers to the configured endpoint.
homepage: https://github.com/openmule/mulerouter-skills
allowed-tools: Bash(mulerouter *) Bash(npx mulerouter*) Bash(npm install*) Read
metadata:
  clawdbot:
    requires:
      env: ["MULEROUTER_API_KEY"]
      env_one_of: ["MULEROUTER_BASE_URL", "MULEROUTER_SITE"]
      bins: ["node", "npm"]
    primaryEnv: "MULEROUTER_API_KEY"
    install: "npm install -g mulerouter"
    files: ["references/*"]
---

# MuleRouter API

Generate images, videos, speech, and music via the **`mulerouter` npm CLI**, which fronts the MuleRouter / MuleRun multimodal API gateways.

Every model is invoked as `mulerouter run <provider>/<model>/<action> --flag value …`. The CLI handles task submission, polling, image base64 conversion, and result extraction.

## Required Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MULEROUTER_API_KEY` | **Yes** | API key ([get one here](https://www.mulerouter.ai/app/api-keys?utm_source=github_claude_plugin)) |
| `MULEROUTER_BASE_URL` | **Yes\*** | Full base URL, e.g. `https://api.mulerouter.ai`. Wins over SITE. |
| `MULEROUTER_SITE` | **Yes\*** | `mulerouter` or `mulerun`. Used only if BASE_URL unset. |

\*One of `MULEROUTER_BASE_URL` / `MULEROUTER_SITE` is required.

Only `MULEROUTER_*`-prefixed variables are loaded from `.env`. Do NOT `export` secrets inline — use `.env` or a pre-set shell env.

## Installation

```bash
npm install -g mulerouter        # or: npx -y mulerouter@latest
mulerouter --version
mulerouter config                # diagnose env / show effective configuration
```

## Discovery & invocation

Always discover before invoking. The CLI is self-documenting.

```bash
mulerouter list [--provider X] [--site mulerouter|mulerun] [--tag SOTA]
mulerouter params <provider>/<model>/<action>     # full flag schema with types/defaults/enums
mulerouter run <provider>/<model>/<action> --flag value ...
```

Run `mulerouter params <id>` instead of guessing flag names or memorising enums. The per-endpoint sections below only list the **non-obvious** items (site requirement, special quirks); fall back to `params` for everything else.

## Common flags

| Flag | Default | Notes |
|------|---------|-------|
| `--site mulerouter\|mulerun` | env | Required for endpoints routed on only one gateway (see Models). |
| `--no-wait` | off | Submit and return `{task_id, api_path}` without polling. |
| `--poll-interval <sec>` | 20 | Polling cadence when waiting. |
| `--max-wait <sec>` | 900 | Hard timeout. Use ≥1800 for long videos, ~120 for images. |
| `--json` | off | Machine-readable output. |
| `--api-key` / `--base-url` | env | One-off overrides. |

Async lifecycle: `mulerouter run ... --no-wait --json` → grab `task_id` and `api_path` from the JSON (both top-level `task_id` and `task_info.id` are present) → `mulerouter status <api_path> <task_id> [--wait]`. All endpoints go through this task-poll flow; some (like `midjourney/diffusion`) typically complete on the first poll, but there is no synchronous code path.

The CLI does **not** validate model parameter constraints client-side beyond enum membership — numeric range hints (e.g. "duration 3..15"), "at-least-one-of" requirements (e.g. kling i2v needs first or last frame), and conditional requirements are enforced by the upstream API. Bad inputs come back as a 400 from the server.

## Image inputs

Flags `--image / --images / --first-frame / --last-frame / --last-frame-image / --first-frame-url / --last-frame-url / --ref-images-url / --reference-images / --mask / --mask-image-url` accept local paths (auto-validated and base64-encoded), HTTPS URLs, or `data:image/...` URIs. For array-typed flags pass a single-quoted JSON literal: `--images '["/tmp/a.png","https://example.com/b.png"]'`. Same convention for `--multi-prompt`, `--elements`, `--video`, `--videos`, `--audios`.

## `--model` flag

Never pass `--model` except:

- `alibaba/wan2.1-vace-plus/generation` — must pass `--model wan2.1-vace-plus` (legacy).
- `google/veo3/generation` — pass `--model {veo-3.1, veo-3.1-fast, veo-3}` to pick the variant.

## Models

Format: ``endpoint`` — `--site <site>` — `api_path` — notes (only when something is non-obvious). Run `mulerouter params <endpoint>` for the full flag schema.

### Alibaba (15)

- `alibaba/wan2.1-vace-plus/generation` — any site — `/vendors/alibaba/v1/wan2.1-vace-plus/generation` — **requires `--model wan2.1-vace-plus`** + `--function {image_reference,video_repainting,video_edit,video_extension,video_outpainting}`.
- `alibaba/wan2.1-kf2v-plus/generation` — any site — `/vendors/alibaba/v1/wan2.1-kf2v-plus/generation` — keyframe interpolation: requires `--image` (first) **and** `--last-frame`.
- `alibaba/wan2.2-t2v-plus/generation` — any site — `/vendors/alibaba/v1/wan2.2-t2v-plus/generation`.
- `alibaba/wan2.2-i2v-plus/generation` — any site — `/vendors/alibaba/v1/wan2.2-i2v-plus/generation` — `--resolution {480P,1080P}` only.
- `alibaba/wan2.2-i2v-flash/generation` — any site — `/vendors/alibaba/v1/wan2.2-i2v-flash/generation` — `--resolution {480P,720P}` only (no 1080P).
- `alibaba/wan2.5-t2v-preview/generation` — any site — `/vendors/alibaba/v1/wan2.5-t2v-preview/generation`.
- `alibaba/wan2.5-i2v-preview/generation` — any site — `/vendors/alibaba/v1/wan2.5-i2v-preview/generation`.
- `alibaba/wan2.5-t2i-preview/generation` — any site — `/vendors/alibaba/v1/wan2.5-t2i-preview/generation`.
- `alibaba/wan2.5-i2i-preview/generation` — any site — `/vendors/alibaba/v1/wan2.5-i2i-preview/generation` — requires `--images` (max 2).
- `alibaba/wan2.6-t2v/generation` `[SOTA]` — any site — `/vendors/alibaba/v1/wan2.6-t2v/generation`.
- `alibaba/wan2.6-i2v/generation` `[SOTA]` — any site — `/vendors/alibaba/v1/wan2.6-i2v/generation` — only `--image` is required; prompt is optional.
- `alibaba/wan2.6-t2i/generation` — any site — `/vendors/alibaba/v1/wan2.6-t2i/generation`.
- `alibaba/wan2.6-image/generation` — any site — `/vendors/alibaba/v1/wan2.6-image/generation` — multi-image input editing; requires `--images`.
- `alibaba/happy-horse-1-0-t2v/generation` — **`--site mulerun`** — `/vendors/alibaba/v1/happy-horse-1-0-t2v/generation`.
- `alibaba/happy-horse-1-0-i2v/generation` — **`--site mulerun`** — `/vendors/alibaba/v1/happy-horse-1-0-i2v/generation` — only `--image` required.

Example:
```bash
mulerouter run alibaba/wan2.6-t2v/generation --prompt "A cat walking through a garden"
```

### Google (5 actions, 4 models)

- `google/nano-banana/generation` — **`--site mulerun`** — `/vendors/google/v1/nano-banana/generation`.
- `google/nano-banana/edit` — **`--site mulerun`** — `/vendors/google/v1/nano-banana/edit` — requires `--images`.
- `google/nano-banana-2/generation` `[SOTA]` — any site — `/vendors/google/v1/nano-banana-2/generation`.
- `google/nano-banana-2/edit` `[SOTA]` — any site — `/vendors/google/v1/nano-banana-2/edit` — requires `--images` (1–14).
- `google/nano-banana-pro/generation` `[SOTA]` — any site — `/vendors/google/v1/nano-banana-pro/generation`.
- `google/nano-banana-pro/edit` `[SOTA]` — any site — `/vendors/google/v1/nano-banana-pro/edit` — requires `--images` (1–10).
- `google/veo3/generation` `[SOTA]` — **`--site mulerun`** — `/vendors/google/v1/veo/generation` (path is `veo`, not `veo3`) — **use `--model` to pick variant** (`veo-3.1` / `veo-3.1-fast` / `veo-3`).

### KlingAI (7)

All on either site. `--prompt` and `--negative-prompt` cap at 2500 chars. Reference elements with `<<<element_N>>>` in prompts; reference videos with `@Video1`.

- `klingai/kling-v3-t2v/generation` `[SOTA]` — `/vendors/klingai/v1/kling-v3/text-to-video/generation` — provide `--prompt` or `--multi-prompt`.
- `klingai/kling-v3-i2v/generation` `[SOTA]` — `/vendors/klingai/v1/kling-v3/image-to-video/generation` — at least one of `--first-frame` / `--last-frame` required.
- `klingai/kling-v3-omni-t2v/generation` `[SOTA]` — `/vendors/klingai/v1/kling-v3-omni/text-to-video/generation`.
- `klingai/kling-v3-omni-i2v/generation` `[SOTA]` — `/vendors/klingai/v1/kling-v3-omni/image-to-video/generation` — `--last-frame` requires `--first-frame`; if neither, `--aspect-ratio` is required.
- `klingai/kling-v3-omni-ref2v/generation` `[SOTA]` — `/vendors/klingai/v1/kling-v3-omni/reference-image-to-video/generation` — combine `--images` / `--elements` / `--first-frame` / `--last-frame`; total ≤ 7.
- `klingai/kling-v3-omni-v2v/generation` `[SOTA]` — `/vendors/klingai/v1/kling-v3-omni/reference-video-to-video/generation` — requires `--prompt` and `--video <url>` (string URL, mp4/mov 3–10s, 720–2160px, ≤200MB). `--aspect-ratio {16:9,9:16,1:1}` is required at runtime (upstream returns 4002 if omitted). `--keep-audio true|false` (default false).
- `klingai/kling-v3-omni-v2v-edit/generation` `[SOTA]` — `/vendors/klingai/v1/kling-v3-omni/video-to-video/edit` — requires `--prompt` and `--video <url>` (string URL, same constraints). `--keep-audio true|false` (default false). `--mode std` → 720P output, `--mode pro` → 1080P.

### Midjourney (2)

- `midjourney/diffusion/generation` `[SOTA]` — any site — `/vendors/midjourney/v1/tob/diffusion` — typically completes on the first poll. Use Midjourney inline syntax inside `--prompt` (`--ar 16:9`, `--v 7`, etc.).
- `midjourney/video/generation` `[SOTA]` — any site — `/vendors/midjourney/v1/tob/video-diffusion` — for I2V, embed the image URL inside `--prompt`. `--video-type 0` (480p, default) / `1` (720p).

### MiniMax — all `--site mulerun` (4)

- `minimax/speech-2.8-hd/generation` — `/vendors/minimax/v1/speech-2.8-hd/text-to-speech/generation` — requires `--prompt` + `--voice-id` (see [MINIMAX_VOICES.md](references/MINIMAX_VOICES.md)). ⚠ **Output schema — two paths:**
  - **Recommended**: pass `--output-format url` → `audios[0]` is an HTTPS URL, same as music endpoints.
  - **Fallback** (`--output-format hex` or when the URL path returns hex anyway): `audios[0]` is a hex-encoded MP3 byte string (with ID3 header). Decode: `echo "<hex>" | xxd -r -p > out.mp3`; report the local file path.
- `minimax/speech-2.8-turbo/generation` — `/vendors/minimax/v1/speech-2.8-turbo/text-to-speech/generation` — same flags + same `--output-format` handling as `-hd`.
- `minimax/music-2.0/generation` — `/vendors/minimax/v1/music-2.0/text-to-music/generation` — requires `--lyrics-prompt` (use `[verse]` / `[chorus]` tags). `--prompt` describes style. Output: real HTTPS URL in `audios[0]` (gateway always converts to URL, no `--output-format` needed).
- `minimax/music-2.5/generation` — `/vendors/minimax/v1/music-2.5/text-to-music/generation` — provide either `--lyrics-prompt` or `--lyrics-optimizer` + `--prompt`. Output: real HTTPS URL in `audios[0]`.

### OpenAI (2 actions, 1 model)

- `openai/gpt-image-2/generation` `[SOTA]` — **`--site mulerouter`** — `/vendors/openai/v1/gpt-image-2/generation`.
- `openai/gpt-image-2/edit` `[SOTA]` — **`--site mulerouter`** — `/vendors/openai/v1/gpt-image-2/edit` — requires `--images`.

### ByteDance Seedance (6)

Any site. `seedance-2.0-fast` caps at 720p and does not accept `camera_fixed` / `watermark`.

- `bytedance/seedance-2.0/text-to-video` and `bytedance/seedance-2.0-fast/text-to-video`.
- `bytedance/seedance-2.0/image-to-video` and `bytedance/seedance-2.0-fast/image-to-video` — local paths auto-base64; optional `--last-frame-image`.
- `bytedance/seedance-2.0/reference-to-video` and `bytedance/seedance-2.0-fast/reference-to-video` — combine `--images` / `--videos` / `--audios`. `--videos` only accepts HTTPS URLs; `--audios` cannot be used alone.

Seedance constraints: `--duration` is `{-1, 4..15}` (no 2 or 3); `--seed` range `-1..4294967295`.

## Model selection

When the user is vague about which model to use, list candidates with `mulerouter list --output-type <type> [--tag SOTA]` and ask the user via `AskUserQuestion`. Never silently pick.

## Tips

1. Suggested `--max-wait`: image 300, video 900–1800, speech/music 180.
2. TTS requires `--voice-id`; check `mulerouter params minimax/speech-2.8-turbo/generation` or [MINIMAX_VOICES.md](references/MINIMAX_VOICES.md).
3. Do not paste raw base64 on the command line — use a local file path.
4. Match `--site` to the original submission when calling `mulerouter status`.

## References

- [REFERENCE.md](references/REFERENCE.md) — CLI subcommands, flags, async lifecycle
- [MODELS.md](references/MODELS.md) — Endpoint catalog with availability matrix
- [MINIMAX_VOICES.md](references/MINIMAX_VOICES.md) — MiniMax TTS voice IDs

# Model Catalog

Full inventory of endpoints accessible through `mulerouter run <id> ...`. For invocation flags per endpoint, see the corresponding section in [../SKILL.md](../SKILL.md). For CLI-wide flags, see [REFERENCE.md](REFERENCE.md).

## Discovery

```bash
mulerouter list                                # all endpoints
mulerouter list --provider alibaba             # filter by provider
mulerouter list --site mulerun                 # filter by gateway
mulerouter list --output-type video --tag SOTA # composite filter
mulerouter params <provider>/<model>/<action>  # detailed schema
```

## Site Legend

- **both** — endpoint is routed on both `mulerouter` and `mulerun`. `--site` is optional.
- **mulerouter** — routed only on `api.mulerouter.ai`. Pass `--site mulerouter` (or use default).
- **mulerun** — routed only on `api.mulerun.com`. Pass `--site mulerun` explicitly.

## Endpoint Inventory (37 total)

### Alibaba

| Endpoint | Tag | Output | Site | API Path |
|----------|-----|--------|------|----------|
| `alibaba/wan2.1-vace-plus/generation` | | video | both | `/vendors/alibaba/v1/wan2.1-vace-plus/generation` |
| `alibaba/wan2.1-kf2v-plus/generation` | | video | both | `/vendors/alibaba/v1/wan2.1-kf2v-plus/generation` |
| `alibaba/wan2.2-t2v-plus/generation` | | video | both | `/vendors/alibaba/v1/wan2.2-t2v-plus/generation` |
| `alibaba/wan2.2-i2v-plus/generation` | | video | both | `/vendors/alibaba/v1/wan2.2-i2v-plus/generation` |
| `alibaba/wan2.2-i2v-flash/generation` | | video | both | `/vendors/alibaba/v1/wan2.2-i2v-flash/generation` |
| `alibaba/wan2.5-t2v-preview/generation` | | video | both | `/vendors/alibaba/v1/wan2.5-t2v-preview/generation` |
| `alibaba/wan2.5-i2v-preview/generation` | | video | both | `/vendors/alibaba/v1/wan2.5-i2v-preview/generation` |
| `alibaba/wan2.5-t2i-preview/generation` | | image | both | `/vendors/alibaba/v1/wan2.5-t2i-preview/generation` |
| `alibaba/wan2.5-i2i-preview/generation` | | image | both | `/vendors/alibaba/v1/wan2.5-i2i-preview/generation` |
| `alibaba/wan2.6-t2v/generation` | SOTA | video | both | `/vendors/alibaba/v1/wan2.6-t2v/generation` |
| `alibaba/wan2.6-i2v/generation` | SOTA | video | both | `/vendors/alibaba/v1/wan2.6-i2v/generation` |
| `alibaba/wan2.6-t2i/generation` | | image | both | `/vendors/alibaba/v1/wan2.6-t2i/generation` |
| `alibaba/wan2.6-image/generation` | | image | both | `/vendors/alibaba/v1/wan2.6-image/generation` |
| `alibaba/happy-horse-1-0-t2v/generation` | | video | mulerun | `/vendors/alibaba/v1/happy-horse-1-0-t2v/generation` |
| `alibaba/happy-horse-1-0-i2v/generation` | | video | mulerun | `/vendors/alibaba/v1/happy-horse-1-0-i2v/generation` |

### ByteDance — Seedance

| Endpoint | Tag | Output | Site | API Path |
|----------|-----|--------|------|----------|
| `bytedance/seedance-2.0/text-to-video` | | video | both | `/vendors/bytedance/v1/seedance-2.0/text-to-video/generation` |
| `bytedance/seedance-2.0/image-to-video` | | video | both | `/vendors/bytedance/v1/seedance-2.0/image-to-video/generation` |
| `bytedance/seedance-2.0/reference-to-video` | | video | both | `/vendors/bytedance/v1/seedance-2.0/reference-to-video/generation` |
| `bytedance/seedance-2.0-fast/text-to-video` | | video | both | `/vendors/bytedance/v1/seedance-2.0-fast/text-to-video/generation` |
| `bytedance/seedance-2.0-fast/image-to-video` | | video | both | `/vendors/bytedance/v1/seedance-2.0-fast/image-to-video/generation` |
| `bytedance/seedance-2.0-fast/reference-to-video` | | video | both | `/vendors/bytedance/v1/seedance-2.0-fast/reference-to-video/generation` |

### Google

| Endpoint | Tag | Output | Site | API Path |
|----------|-----|--------|------|----------|
| `google/nano-banana/generation` | | image | mulerun | `/vendors/google/v1/nano-banana/generation` |
| `google/nano-banana/edit` | | image | mulerun | `/vendors/google/v1/nano-banana/edit` |
| `google/nano-banana-2/generation` | SOTA | image | both | `/vendors/google/v1/nano-banana-2/generation` |
| `google/nano-banana-2/edit` | SOTA | image | both | `/vendors/google/v1/nano-banana-2/edit` |
| `google/nano-banana-pro/generation` | SOTA | image | both | `/vendors/google/v1/nano-banana-pro/generation` |
| `google/nano-banana-pro/edit` | SOTA | image | both | `/vendors/google/v1/nano-banana-pro/edit` |
| `google/veo3/generation` | SOTA | video | mulerun | `/vendors/google/v1/veo/generation` |

### KlingAI

| Endpoint | Tag | Output | Site | API Path |
|----------|-----|--------|------|----------|
| `klingai/kling-v3-t2v/generation` | SOTA | video | both | `/vendors/klingai/v1/kling-v3/text-to-video/generation` |
| `klingai/kling-v3-i2v/generation` | SOTA | video | both | `/vendors/klingai/v1/kling-v3/image-to-video/generation` |
| `klingai/kling-v3-omni-t2v/generation` | SOTA | video | both | `/vendors/klingai/v1/kling-v3-omni/text-to-video/generation` |
| `klingai/kling-v3-omni-i2v/generation` | SOTA | video | both | `/vendors/klingai/v1/kling-v3-omni/image-to-video/generation` |
| `klingai/kling-v3-omni-ref2v/generation` | SOTA | video | both | `/vendors/klingai/v1/kling-v3-omni/reference-image-to-video/generation` |
| `klingai/kling-v3-omni-v2v/generation` | SOTA | video | both | `/vendors/klingai/v1/kling-v3-omni/reference-video-to-video/generation` |
| `klingai/kling-v3-omni-v2v-edit/generation` | SOTA | video | both | `/vendors/klingai/v1/kling-v3-omni/video-to-video/edit` |

### Midjourney

| Endpoint | Tag | Output | Site | API Path |
|----------|-----|--------|------|----------|
| `midjourney/diffusion/generation` | SOTA | image | both | `/vendors/midjourney/v1/tob/diffusion` |
| `midjourney/video/generation` | SOTA | video | both | `/vendors/midjourney/v1/tob/video-diffusion` |

Note: every endpoint in this catalog goes through the same async task-poll lifecycle on the client (`mulerouter run` POSTs then polls until terminal). `midjourney/diffusion/generation` typically completes on the first poll; other video/image endpoints take longer.

### MiniMax (all mulerun-only)

| Endpoint | Tag | Output | Site | API Path |
|----------|-----|--------|------|----------|
| `minimax/speech-2.8-hd/generation` | | audio | mulerun | `/vendors/minimax/v1/speech-2.8-hd/text-to-speech/generation` |
| `minimax/speech-2.8-turbo/generation` | | audio | mulerun | `/vendors/minimax/v1/speech-2.8-turbo/text-to-speech/generation` |
| `minimax/music-2.0/generation` | | audio | mulerun | `/vendors/minimax/v1/music-2.0/text-to-music/generation` |
| `minimax/music-2.5/generation` | | audio | mulerun | `/vendors/minimax/v1/music-2.5/text-to-music/generation` |

### OpenAI

| Endpoint | Tag | Output | Site | API Path |
|----------|-----|--------|------|----------|
| `openai/gpt-image-2/generation` | SOTA | image | mulerouter | `/vendors/openai/v1/gpt-image-2/generation` |
| `openai/gpt-image-2/edit` | SOTA | image | mulerouter | `/vendors/openai/v1/gpt-image-2/edit` |

## Result Keys

The `mulerouter run` JSON output places generated media URLs under `result[<resultKey>]`:

| Output type | resultKey |
|-------------|-----------|
| image | `images` |
| video | `videos` |
| audio | `audios` |

## See Also

- [../SKILL.md](../SKILL.md) — full per-endpoint flag documentation
- [REFERENCE.md](REFERENCE.md) — CLI subcommands, env vars, async lifecycle
- [MINIMAX_VOICES.md](MINIMAX_VOICES.md) — MiniMax TTS voice IDs

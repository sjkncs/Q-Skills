# mulerouter CLI Reference

Reference for the `mulerouter` npm CLI used to invoke MuleRouter / MuleRun multimodal endpoints. Install with `npm install -g mulerouter` (or run via `npx -y mulerouter@latest`).

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MULEROUTER_API_KEY` | **Yes** | Bearer token sent in the `Authorization` header. |
| `MULEROUTER_BASE_URL` | one-of | Full base URL (e.g. `https://api.mulerouter.ai`). Takes priority over `MULEROUTER_SITE`. |
| `MULEROUTER_SITE` | one-of | `mulerouter` or `mulerun`. Used only when `MULEROUTER_BASE_URL` is unset. |

A `.env` file in the working directory is auto-loaded; only `MULEROUTER_*`-prefixed variables are read. Other variables in the file are ignored.

## Subcommands

### `mulerouter list [flags]`

List registered endpoints.

| Flag | Description |
|------|-------------|
| `--provider <name>` | Filter by provider (e.g. `alibaba`, `google`, `klingai`, `midjourney`, `minimax`, `openai`, `bytedance`). |
| `--site <site>` | `mulerouter` or `mulerun`. Filters to endpoints available on that gateway. |
| `--output-type <type>` | `image` / `video` / `audio`. |
| `--tag <tag>` | Filter by tag (e.g. `SOTA`). |
| `--providers` | List provider names only (no endpoints). |
| `--json` | Emit JSON. |

### `mulerouter params <provider>/<model>[/<action>]`

Print the parameter schema (name, type, required, default, enum) for one endpoint. Use this before crafting a `run` call when uncertain about flags. If `<action>` is omitted and unambiguous, it is auto-resolved. Flag: `--json`.

### `mulerouter run <provider>/<model>[/<action>] [flags]`

Invoke an endpoint. CLI flags follow `--snake-or-kebab-name <value>`; the CLI converts `-` to `_` when building the request body. Unknown flags pass through as model parameters (via `allowUnknownOption`). `--key=value` and `--no-key` (→ `false`) syntax both work.

Common flags applicable to every `run`:

| Flag | Default | Description |
|------|---------|-------------|
| `--site <site>` | env value | Override `MULEROUTER_SITE` for this call. Required when an endpoint is routed on only one gateway. |
| `--api-key <key>` | env value | Override `MULEROUTER_API_KEY`. |
| `--base-url <url>` | env value | Override `MULEROUTER_BASE_URL`. |
| `--no-wait` | off | Submit the task and return its id/api_path without polling. |
| `--poll-interval <sec>` | `20` | Seconds between status polls (when waiting). |
| `--max-wait <sec>` | `900` | Total seconds to wait before timing out. |
| `--quiet` | off | Suppress progress output. |
| `--json` | off | Emit machine-readable JSON instead of plain text. |
| `--extra <key=value>` | — | Repeatable. Pass parameters not declared in the endpoint registry. |

### `mulerouter status <api-path> <task-id> [flags]`

Check status of an async task previously submitted with `--no-wait`. The first argument is the `api_path` returned by the submit step (also documented in [MODELS.md](MODELS.md) and in each SKILL.md model section).

| Flag | Description |
|------|-------------|
| `--wait` | Block until terminal status (uses `--poll-interval` / `--max-wait`). |
| `--api-key <key>` | Override `MULEROUTER_API_KEY`. |
| `--base-url <url>` | Override `MULEROUTER_BASE_URL`. |
| `--site <site>` | Must match the site the task was submitted to. |
| `--poll-interval <sec>` | Polling cadence when `--wait`. Default `20`. |
| `--max-wait <sec>` | Hard timeout when `--wait`. Default `900`. |
| `--quiet` | Suppress progress output. |
| `--json` | Emit JSON. |

### `mulerouter config`

Print the effective configuration (loaded env vars, resolved base URL, site, etc.) and any setup help. Useful for diagnosing "where is my config coming from?" issues.

## Image Parameter Handling

The following flag names are treated as image parameters and accept local file paths, HTTPS URLs, or `data:image/...` URIs:

```
image, images, first_frame, last_frame, last_frame_image,
first_frame_url, last_frame_url, ref_images_url, reference_images,
mask, mask_image_url
```

When a local path is supplied, the CLI:

1. Validates the file extension (`.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.webp`, `.tiff`, `.tif`, `.svg`, `.ico`, `.heic`, `.heif`, `.avif`).
2. Reads and base64-encodes the file.
3. Sends the encoded payload in place of the path.

URLs and `data:` URIs are forwarded unchanged.

For array-valued image flags, pass a single-quoted JSON literal:

```bash
--images '["/tmp/a.png","https://example.com/b.png"]'
```

## Other JSON Flags

`--multi-prompt`, `--elements`, `--video`, `--videos`, `--audios`, `--reference-images`, `--ref-images-url` all take JSON literals. Examples:

```bash
--multi-prompt '[{"prompt":"opening shot","duration":3},{"prompt":"closing","duration":5}]'
--video '[{"video_url":"https://example.com/clip.mp4","refer_type":"feature","keep_original_sound":"no"}]'
```

## Async Lifecycle

Every `mulerouter run` invocation is task-based — there is no synchronous code path in the CLI:

1. `mulerouter run <id> ...` POSTs to the api_path, receives `{task_info: {id, status, ...}, api_path}` (the response also hoists `task_id` to the top level for convenience).
2. Unless `--no-wait` is passed, the CLI polls `GET <api_path>/<task_id>` every `--poll-interval` seconds.
3. On terminal status (`completed` / `succeeded` / `failed`), the final task body is printed; generated media URLs are under `result[<resultKey>]`.

Some endpoints (notably `midjourney/diffusion/generation`) typically complete on the very first poll, but the lifecycle is the same as long-running video jobs.

## Client-side Validation

The CLI validates **only** enum membership for parameters that declare an `enum`. It does **not** enforce:

- Numeric ranges (e.g. "duration 3..15" in a description string)
- "At-least-one-of" requirements (e.g. kling i2v needs first or last frame)
- Conditional requirements (e.g. mask requires images)

Out-of-range or incomplete inputs are forwarded to the API and returned as a 400.

## `--model` Flag

Reserved by the gateway. **Never pass `--model`** except:

- `alibaba/wan2.1-vace-plus/generation` — must pass `--model wan2.1-vace-plus` (legacy quirk).
- `google/veo3/generation` — pass `--model {veo-3.1,veo-3.1-fast,veo-3}` to pick the variant.

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success. |
| `1` | Generic error (invalid flags, network failure, missing env). |
| `2` | Task reached non-success terminal state (`failed`). |
| `124` | Polling timed out (`--max-wait` exceeded). |

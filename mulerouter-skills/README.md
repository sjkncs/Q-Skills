# MuleRouter Skill

Claude Code skill for generating images, videos, speech, and music via MuleRouter / MuleRun multimodal APIs. Wraps the [`mulerouter` npm CLI](https://www.npmjs.com/package/mulerouter).

## Features

- Text-to-Image generation
- Text-to-Video generation
- Image-to-Video transformation
- Image-to-Image editing
- Video editing (VACE, keyframe interpolation)
- Text-to-Speech and Text-to-Music

## Requirements

- Node.js 18+
- The `mulerouter` npm CLI (`npm install -g mulerouter`)
- API key from MuleRouter or MuleRun

## Setup

```bash
# install the CLI
npm install -g mulerouter

# set credentials (or use a .env file — see .env.example)
export MULEROUTER_API_KEY="your-api-key"
export MULEROUTER_BASE_URL="https://api.mulerouter.ai"   # or:
# export MULEROUTER_SITE="mulerouter"                    # mulerouter | mulerun
```

`MULEROUTER_BASE_URL` takes priority over `MULEROUTER_SITE` when both are set.

## Usage

```bash
# discover endpoints
mulerouter list
mulerouter list --tag SOTA
mulerouter params alibaba/wan2.6-t2v/generation

# generate a video
mulerouter run alibaba/wan2.6-t2v/generation \
  --prompt "A cat walking through a garden"

# generate an image
mulerouter run alibaba/wan2.6-t2i/generation \
  --prompt "A serene mountain lake"
```

See [SKILL.md](SKILL.md) for per-endpoint flag documentation, [references/MODELS.md](references/MODELS.md) for the full model catalog, and [references/REFERENCE.md](references/REFERENCE.md) for CLI subcommand details.

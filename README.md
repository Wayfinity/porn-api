# Porn API: generate AI porn images and video with one REST call

Official examples for the [SpicyAPI](https://www.spicyapi.com) **porn API**, a REST API that generates original adult images, video and chat from a prompt. One key, pay per generation, no subscription, OpenAI SDK compatible. Spicy API (spicyapi.com) is not affiliated with spicyapi.ai.

> This repository contains code only. No explicit media is stored here. 18+ only; read the [acceptable use policy](https://www.spicyapi.com/acceptable-use) before your first call.

## Which kind of porn API do you need?

There are two kinds, and most search results mix them up:

| | Data APIs | Generation APIs (this one) |
|---|---|---|
| What you get | JSON about existing tube videos: titles, tags, embeds | New images and video created for each request |
| Content | Someone else's, same for every site that uses it | Unique to your product and your users |
| Good for | Aggregators, search, tube clones | Companion apps, bots, creator tools, games |
| Examples | json-porn, Pornhub and xvideos wrappers | SpicyAPI |

If you need original NSFW content on demand without running GPUs, keep reading.

## Quickstart

1. Sign up at [spicyapi.com/auth](https://www.spicyapi.com/auth) and copy your key from Dashboard, API Keys.
   Tick **Sandbox** to get a free key that returns sample output and bills nothing.
2. Export it:

```bash
export SPICYAPI_KEY="sk-spicy-..."
```

3. Generate an image:

```bash
curl https://api.spicyapi.com/v1/images/generations \
  -H "Authorization: Bearer $SPICYAPI_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "spicy-image-1", "prompt": "a woman on a beach at golden hour, photorealistic", "size": "832*1216", "n": 1}'
```

```json
{
  "id": "req_8f2a91c4",
  "object": "image.generation",
  "model": "spicy-image-1",
  "data": [{ "url": "https://cdn.spicyapi.com/outputs/a1b2/req_8f2a91c4-0.png" }],
  "cost_usd": 0.06
}
```

4. Turn that image into video (asynchronous, poll the task):

```bash
curl https://api.spicyapi.com/v1/videos/generations \
  -H "Authorization: Bearer $SPICYAPI_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "spicy-motion-2", "prompt": "slow build, steady rhythm", "image_url": "<url from step 3>", "resolution": "720P", "duration": 5}'

curl https://api.spicyapi.com/v1/videos/tasks/<id> -H "Authorization: Bearer $SPICYAPI_KEY"
```

## Examples in this repo

| File | What it shows |
|---|---|
| [`examples/curl.sh`](examples/curl.sh) | Image, then video, then polling, in plain curl |
| [`examples/python_openai.py`](examples/python_openai.py) | Images and streaming chat through the OpenAI SDK, video over HTTP |
| [`examples/node.mjs`](examples/node.mjs) | The same flow in Node 18+ with no dependencies |

## Endpoints

| Endpoint | What it does |
|---|---|
| `GET /v1/models` | Live model catalog with limits and prices |
| `GET /v1/account` | Balance and account status |
| `POST /v1/images/generations` | Text to image, 1 to 4 images per call |
| `POST /v1/images/edits` | Prompt-driven edits with up to 3 reference images |
| `GET /v1/images` | List the images your account generated |
| `POST /v1/videos/generations` | Image to video or text to video, returns a task |
| `GET /v1/videos/tasks/{id}` | Poll a video task |
| `POST /v1/chat/completions` | Uncensored chat, OpenAI compatible, streaming |

Base URL `https://api.spicyapi.com`. Full reference: [spicyapi.com/docs](https://www.spicyapi.com/docs). OpenAPI: [openapi.json](https://www.spicyapi.com/openapi.json).

## Pricing

Pay per generation from a prepaid balance. Images from $0.06, video from $0.05 per second, chat from $0.10 per 1M prompt tokens. Blocked prompts cost nothing and failed generations are refunded automatically. Every response carries the exact `cost_usd`. Current prices: [spicyapi.com/pricing](https://www.spicyapi.com/pricing).

## Errors

`401` bad key, `402` insufficient balance, `400` invalid parameters, `422` prompt blocked (not billed), `429` model at capacity. All errors look like `{"error": {"message": "...", "type": "..."}}`.

## Content rules

Adults only. Every prompt is moderated before billing. No minors in any form, no real people in images or video (with or without consent; a voice clone needs the speaker's written consent), and image inputs must be images your own account generated. Your product must age-gate its users.

## For AI agents

MCP server at `https://www.spicyapi.com/api/mcp`, skills at [Wayfinity/spicyapi-skills](https://github.com/Wayfinity/spicyapi-skills), machine-readable docs at [llms.txt](https://www.spicyapi.com/llms.txt).

## License

MIT. Support: support@spicyapi.com

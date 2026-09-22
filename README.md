# Krea API — Python client

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Hosted on Synexa](https://img.shields.io/badge/hosted%20on-Synexa-6366f1.svg)](https://synexa.ai/explore/krea/krea-2-large?utm_source=github&utm_medium=ugc&utm_campaign=krea-dev&utm_content=readme-badge&utm_term=tier-c)

Krea is a creative platform known for its real-time generation canvas, image enhancer and its own image models. Krea 2 Large is the company's text-to-image model, tuned for a photographic look that avoids the over-smoothed, plastic skin and saturated palette common in diffusion output. This repository is a small Python client for the Krea API as hosted on Synexa, so you can generate Krea 2 Large images from a script with one `pip install` and an API token.

You get a blocking `run()` that takes a prompt and returns image URLs, a non-blocking create-and-poll path for batch jobs, and webhook delivery for services that would rather be called back. The client has a single runtime dependency and ships no weights. It is aimed at developers adding image generation to a product, a content pipeline or an internal tool who want Krea's model as an HTTP call rather than a GPU deployment.

> **Try it now:** [https://synexa.ai/explore/krea/krea-2-large](https://synexa.ai/explore/krea/krea-2-large?utm_source=github&utm_medium=ugc&utm_campaign=krea-dev&utm_content=readme-top&utm_term=tier-c) — the hosted model behind this client. New accounts get a free trial credit.

## Contents

- [Why this client](#why-this-client)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Hosted models](#hosted-models)
- [Parameters](#parameters)
- [Advanced usage](#advanced-usage)
- [About Krea](#about-krea)
- [Use cases](#use-cases)
- [FAQ](#faq)
- [License](#license)

## Why this client

- **The weights are not published.** Krea 2 Large is a hosted model; there is no checkpoint to download, so a hosted endpoint is the only way to call it programmatically outside Krea's own app.
- **No GPU or serving stack.** Large text-to-image models of this class need a datacenter GPU with tens of gigabytes of VRAM and a serving layer with batching and queueing. The endpoint runs on Synexa's fleet and you pay per image.
- **No cold start.** The model stays resident on the endpoint; the first request of the day costs the same as the hundredth, and there is nothing to warm up on your side.
- **Predictable cost.** `krea/krea-2-large` is billed at $0.06 per run, so a thousand-image batch costs $60 and you know that before you submit it.

## Installation

```bash
pip install git+https://github.com/krea-dev/krea-api.git
```

Then set your API key (create one at [synexa.ai](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=krea-dev&utm_content=readme-apikey&utm_term=tier-c)):

```bash
export SYNEXA_API_KEY="sk-..."
```

## Quickstart

```python
import krea_api

output = krea_api.run({
    "prompt": "A cinematic shot of a lighthouse at dawn, soft fog, warm light"
})
print(output)   # URL(s) of the generated result
```

Or with an explicit client:

```python
from krea_api import Client

client = Client(api_key="sk-...")
output = client.run({"prompt": "A cinematic shot of a lighthouse at dawn, soft fog, warm light"})
```

## Hosted models

| Model | Category | What it does | Price / run |
|---|---|---|---|
| [`krea/krea-2-large`](https://synexa.ai/explore/krea/krea-2-large?utm_source=github&utm_medium=ugc&utm_campaign=krea-dev&utm_content=readme-models&utm_term=tier-c) | text-to-image | Krea 2 Large generates high-fidelity images from text with a distinctly photographic, non-plasticky look. | $0.06 |

The default model is **`krea/krea-2-large`**; pass `model="owner/name"` to `run()` to use another one from the table.

## Parameters

### `krea/krea-2-large`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `prompt` | string | yes | `A rain-slicked Tokyo side street at nigh…` | — | Text description of the image to generate. |
| `aspect_ratio` | string | no | `1:1` | 1:1, 4:3, 3:2, 16:9, 2.35:1, 4:5, 2:3, 9:16 | Aspect ratio of the generated image. |
| `creativity` | string | no | `medium` | raw, low, medium, high | Controls how loosely the model interprets the prompt. Higher values produce more creative results that may drift from the prompt; lower values stay closer to the prompt. |
| `seed` | integer | no | `random` | — | Random seed for reproducible generation. |

## Advanced usage

**Submit without blocking, then poll:**

```python
prediction = client.run(input, wait=False)      # returns immediately
prediction = client.wait(prediction, timeout=300)
print(prediction["output"])
```

**Webhook on completion:**

```python
client.run(input, wait=False, webhook="https://your-app.example/hooks/synexa")
```

**Errors:**

```python
from krea_api import ModelError, PredictionTimeout

try:
    output = client.run(input)
except ModelError as e:
    print("failed:", e, e.prediction and e.prediction.get("id"))
except PredictionTimeout:
    print("still running — poll later")
```

Status values you will see on a prediction: `starting` → `processing` → `succeeded` | `failed`.

## About Krea

Krea ([krea.ai](https://www.krea.ai)) is a creative AI platform. It became known for a real-time canvas where an image updates as you draw or move shapes, and has since added an upscaler and enhancer, video generation, training on your own images, and a model hub that fronts third-party image and video models alongside its own. Krea also collaborated with Black Forest Labs on FLUX.1 Krea [dev], an open-weights model that targets the same anti-plastic aesthetic.

Krea 2 Large is Krea's own text-to-image model. Its stated goal is realism without the tells that make AI images recognisable: waxy skin, uniform bokeh, over-contrasted lighting and a narrow colour range. Given a text prompt it produces a single high-resolution image; the hosted endpoint exposes an `aspect_ratio` control, a `creativity` slider that decides how loosely the prompt is interpreted (higher values drift further from the literal prompt, lower values stay close to it) and a `seed` for reproducible output. The model is strongest on photographic subjects such as people, products, interiors, landscapes and editorial scenes, and is not a specialist for typography or diagrams.

Typical usage is product and lifestyle imagery, stock-style photography for landing pages and ads, concept art with a photographic finish, and seed-locked variations where you want to change the prompt slightly while holding composition. Output is one image per run; batch by issuing several runs, which the poll-based path handles without blocking.

The hosted endpoint used by this client is `krea/krea-2-large` on Synexa, which is Krea's own Krea 2 Large model served through Synexa's API. It is not a substitute or look-alike; the same model is available in Krea's app and on Krea's own platform at [krea.ai](https://www.krea.ai), which also offers features this client does not cover, such as the real-time canvas, enhancer and custom training.

**Official project:** https://www.krea.ai

## Use cases

- **Product and lifestyle imagery** — call `run()` with a prompt describing the product, setting and lighting, and an `aspect_ratio` matching the ad slot.
- **Landing-page hero images** — generate a set of candidates from one prompt with different seeds through the poll path and pick the best in review.
- **Editorial illustration** — describe the scene and set `creativity` low to keep the model on the brief for article headers that must match the copy.
- **Concept exploration** — raise `creativity` and vary the prompt to get looser interpretations early in a design process.
- **Seed-locked variations** — fix `seed`, change one phrase in the prompt, and compare how the composition holds across runs.
- **Programmatic asset pipelines** — enqueue hundreds of prompts from a spreadsheet and receive results by webhook as they complete.

## FAQ

**Is there a Krea API?**

Yes. Krea offers an API on its own platform, and Krea 2 Large is also hosted on Synexa as `krea/krea-2-large`. This client talks to the Synexa endpoint, which takes a text prompt and returns a generated image.

**How much does the Krea API cost through this client?**

The hosted `krea/krea-2-large` endpoint is billed at $0.06 per run, where one run produces one image. There is no subscription; you pay per completed generation.

**Can I run Krea without a GPU?**

With this client, yes. Generation happens on Synexa's GPUs; your machine only needs Python and network access. Krea 2 Large weights are not published, so there is no local option to compare against.

**Does this client work with ComfyUI or FLUX.1 Krea [dev]?**

No. It does not load local checkpoints or drive ComfyUI; it only calls the hosted endpoint. FLUX.1 Krea [dev] is a separate open-weights model and is not what this endpoint serves.

**What input formats does it accept?**

The only required field is `prompt`, a text description of the image. Optional fields are `aspect_ratio`, `creativity` (how loosely the prompt is interpreted) and `seed` (for reproducible output). There is no image input on this endpoint.

**Is this the official Krea SDK?**

No. This is an independent client that wraps the Synexa-hosted endpoint. Krea's official product and API are at https://www.krea.ai.

## Related

- [Krea](https://www.krea.ai) — official platform, app and API
- [Synexa Python client](https://github.com/synexa-ai/synexa-python) — the general-purpose SDK this client builds on
- [krea/krea-2-large on Synexa](https://synexa.ai/explore/krea/krea-2-large) — the hosted Krea 2 Large endpoint
- [black-forest-labs/flux-schnell on Synexa](https://synexa.ai/explore/black-forest-labs/flux-schnell) — a fast, low-cost alternative for drafts
- [google/nano-banana-pro on Synexa](https://synexa.ai/explore/google/nano-banana-pro) — image generation and editing with reference images

## License

MIT. This is an independent, community-maintained client and is not affiliated with or endorsed by the authors of Krea. Model weights and trademarks belong to their respective owners.



_Last reviewed: 2026-09-22_

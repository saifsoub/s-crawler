# S/Crawler

> **Evidence-aware cross-estate crawling for live discovery, provenance, depth, and product-state evidence.**

S/Crawler turns crawling into an inspectable evidence workflow:

```text
Authorized estate
  ↓
Live crawl
  ↓
L0 → requested depth
  ↓
Normalize + deduplicate
  ↓
Provenance + conflicts
  ↓
Asset registry
  ↓
Product state + terminal outcome
```

## Live product surface

**Live UI:** https://s-crawler-live-5k218z.v2.appdeploy.ai/

The live surface now supports:
- multiple seed URLs;
- configurable depth up to L10;
- same-domain control;
- live crawl metrics;
- evidence-aware asset registry;
- controlled DISCOVER → TRACE → VERIFY → RECONSTRUCT → CLASSIFY → SCORE → PACKAGE → EXPOSE stages;
- product states and explicit terminal outcomes;
- responsive mobile layout.

The hosted UI uses a live AppDeploy crawl adapter. The canonical repository engine remains the Playwright-backed Python crawler.

## Agent surface

A private ChatGPT plugin is available for the S/Crawler operating contract:

https://chatgpt.com/plugins/plugins_6ab4fd0de8c08191bd6f9239499856f6

The plugin preserves the evidence-aware crawl discipline: define scope, keep Level 0 explicit, preserve provenance, separate fact from inference, log conflicts, and never fabricate execution evidence.

## AgentMarkup

The live Vite surface is wired with **@agentmarkup/vite**.

Current machine-readable output is configured to generate:
- `llms.txt`;
- JSON-LD WebSite metadata;
- markdown mirrors for the client-rendered surface;
- homepage discovery metadata.

No AI-crawler allow/block policy or Content-Signal training policy is asserted by default.

## Canonical engine

The repository implementation includes:
- Playwright rendering;
- explicit Level 0 → N traversal;
- same-domain filtering;
- URL normalization;
- deduplication;
- parent/level tracking;
- Flask `POST /crawl` API;
- `GET /health`;
- unit tests;
- browser/E2E coverage;
- GitHub Actions CI.

Run locally:

```bash
pip install -r requirements.txt
playwright install chromium
python app.py
```

Then:

```bash
curl -X POST http://localhost:8080/crawl \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com","max_depth":5,"same_domain":true}'
```

## Evidence contract

A page record should preserve:

```json
{
  "url": "https://example.com/page",
  "level": 2,
  "title": "Example",
  "status": 200,
  "parent": "https://example.com/",
  "links": [],
  "error": null
}
```

A finished result must distinguish:
- static inspection;
- unit execution;
- live HTTP integration;
- browser execution;
- actual crawl execution.

**If the crawler did not run, we do not say it ran.**

## Acceptance

A release candidate should demonstrate:

- [x] Level 0 is the supplied seed.
- [x] Configurable depth traversal.
- [x] JavaScript-aware canonical Playwright engine.
- [x] URL normalization and fragment removal.
- [x] Deduplication.
- [x] Same-domain control.
- [x] Inspectable title, URL, level, parent, status, and errors.
- [x] Frontend wired to a real backend.
- [x] Live public product surface.
- [x] Browser/E2E test coverage.
- [x] AgentMarkup machine-readable surface.
- [x] ChatGPT S/Crawler plugin.
- [ ] Export formats.
- [ ] Resumable crawl frontier.
- [ ] Content hashing / change detection.

## Positioning

S/Crawler is not trying to replace every crawler. It composes crawling with evidence, provenance, product state, and action.

| Tool | Primary strength | Relationship to S/Crawler |
|---|---|---|
| Firecrawl | LLM-oriented extraction and managed crawling | Product/reference peer |
| Crawlee | Programmable crawling framework | Engine/reference peer |
| Playwright | Browser rendering and automation | Canonical browser-engine foundation |
| Scrapy | High-scale crawling pipelines | Scale reference |
| Beautiful Soup | HTML parsing | Parser utility |

The differentiator is the loop:

```text
crawl → evidence → provenance → state → action
```

## Ownership

Owned and maintained by S/Agency by Seif Alsoub.

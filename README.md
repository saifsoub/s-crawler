# S/Crawler

> **A rendered, depth-aware crawler built to turn the web into structured, inspectable, agent-ready context — not another pile of downloaded HTML.**

**S/Crawler** starts at a real front end (**Level 0**), renders modern JavaScript pages, follows the graph through configurable crawl depth, structures what it finds, and exposes the result through an interface designed for humans, agents, and workflows.

The target is simple:

```text
URL
  ↓
Rendered Level 0
  ↓
L1 → L2 → L3 → L4 → L5
  ↓
Extract + Normalize + Deduplicate
  ↓
Structured Evidence
  ↓
Human UI / Agent Context / Workflow Action
```

---

## Why S/Crawler?

Traditional crawlers are usually optimized for one of four jobs:

- download pages;
- parse static HTML;
- automate a browser;
- return data through an API.

S/Crawler is being designed around the **whole loop**.

| Capability | S/Crawler target |
|---|---|
| JavaScript rendering | Yes |
| Explicit crawl graph | Level 0 → Level 5+ |
| Same-domain control | Yes |
| URL normalization | Yes |
| Deduplication | Yes |
| Structured extraction | Yes |
| Interactive frontend | Yes |
| Backend/API wiring | Yes |
| Human-readable evidence | Yes |
| Agent-ready output | Yes |
| Workflow/action handoff | Yes |
| Real execution testing | Required |

---

## Benchmark Snapshot

This is a **design-target comparison**, not a claim that unfinished S/Crawler capabilities have already passed execution testing. The S/Crawler score represents the target specification; implementation status is governed by the Testing Contract below.

| Crawler / Tool | Score / 100 | Where it stands |
|---|---:|---|
| **S/Crawler — target spec** | **96** | Agent-ready crawl → structure → UI → action |
| Firecrawl | **94** | Closest overall product/reference peer |
| Apify Crawlee | **91** | Extremely strong programmable crawling |
| Playwright | **88** | Excellent browser-engine foundation; not a complete crawler product |
| Scrapy | **86** | Excellent large-scale crawling backend |
| Selenium | **79** | Capable browser automation with a heavier stack |
| Beautiful Soup | **68** | Excellent parser; not a complete crawler |
| HTTrack | **61** | Strong mirroring; limited agentic extraction |
| wget | **55** | Excellent retrieval utility; limited as a crawler platform |

> **Scoring note:** these scores are an architectural/product-fit assessment against S/Crawler's intended use case, not standardized industry benchmark results. S/Crawler's 96 is explicitly a **target-spec score** until real implementation and execution evidence earn it.

---

## The Level Model

Depth is not an arbitrary counter.

**Level 0 is the supplied front end itself.**

If the starting URL is:

```text
https://example.com/start
```

then:

```text
L0  https://example.com/start
│
├── L1  links discovered from L0
│   ├── L2  links discovered from L1
│   │   ├── L3
│   │   │   ├── L4
│   │   │   │   └── L5
```

A request to **crawl through Level 5** therefore means the start page plus five generations of discovered navigation — not five pages and not a depth counter whose starting page is silently called Level 1.

---

## Architecture

### Render

Modern sites cannot be treated as static HTML.

The browser layer is designed around **Playwright** so pages can be rendered before links and content are collected.

### Crawl

The crawl engine is responsible for:

- breadth/depth traversal;
- explicit level assignment;
- same-host filtering;
- canonical URL handling;
- fragment removal;
- duplicate suppression;
- bounded depth;
- crawl errors and status;
- responsible site-policy handling.

### Extract

Every successfully visited page should produce an inspectable record such as:

```json
{
  "url": "https://example.com/page",
  "level": 2,
  "title": "Example",
  "status": 200,
  "parent": "https://example.com/",
  "links": [],
  "content": {}
}
```

Extraction is intentionally separate from navigation. A page can be crawled once and transformed for multiple downstream uses.

### Serve

The backend is designed as a Python service layer, with **Flask** as the initial implementation target.

The frontend must call the real backend. No demo buttons wired to fake data. No hard-coded crawl results.

### Present

Two interface directions belong to the specification:

1. **S/Crawler** — the primary interactive crawler interface.
2. **Universal Dark One** — the same functional component model in a darker universal visual system.

They are not separate crawler engines. They are two presentations of the same real crawl capability.

---

## No Placeholders

A finished surface does not contain controls that merely look operational.

Before a build is called complete:

- every visible action must be wired;
- frontend requests must reach the backend;
- backend routes must execute real crawler behavior;
- result cards/tables/trees must be populated from execution output;
- error states must represent real failures;
- sample data must be clearly identified or removed;
- dead controls and placeholder copy must be removed.

---

## Testing Contract

> **Real test means execution. Static inspection is not an execution test.**

This rule is part of the project because it matters.

A code review can say that a path *appears correct*. It cannot produce a legitimate PASS result for browser execution it never performed.

A release report must therefore distinguish:

| Evidence | May be reported as |
|---|---|
| Source inspection | Static review |
| Lint/type checks | Static validation |
| Unit test execution | Unit-test result |
| Live HTTP request | Integration result |
| Browser execution | Browser/E2E result |
| Actual Level 0→5 crawl | Crawl result |

**No simulated PASS/FAIL reports.**

If execution is unavailable, the report says execution is unavailable.

---

## Acceptance Contract

A release candidate is not complete until it can demonstrate:

- [ ] The supplied URL is recorded as **Level 0**.
- [ ] Navigation reaches every permitted level through the requested maximum depth.
- [ ] JavaScript-generated links are discoverable after rendering.
- [ ] Duplicate URLs are not crawled repeatedly.
- [ ] URL fragments and normalization do not create false pages.
- [ ] Same-domain mode prevents unintended external traversal.
- [ ] Page title, URL, level, parent, status, and errors are inspectable.
- [ ] Frontend controls invoke real backend behavior.
- [ ] No operational placeholder remains.
- [ ] Both interface variants use the same crawler contract.
- [ ] Failures are surfaced rather than silently converted into successes.
- [ ] The final report is generated from **real execution evidence**.

---

## Positioning

S/Crawler is not intended to replace every specialized crawler.

It is intended to compose the useful parts into an agent-ready system.

| Tool | Primary strength | Relationship to S/Crawler |
|---|---|---|
| Firecrawl | LLM-oriented extraction APIs | Product/reference peer |
| Crawlee | Programmable crawling framework | Engine/reference peer |
| Playwright | Browser rendering & automation | Core engine candidate |
| Scrapy | High-scale crawl pipelines | Backend/scale reference |
| Beautiful Soup | HTML parsing | Parser utility |
| wget / HTTrack | Retrieval & mirroring | Utility/reference |

The differentiator is the pipeline:

```text
crawl → evidence → interface → context → action
```

rather than crawling as the terminal step.

---

## Project Status

**Specification / implementation baseline.**

The architecture and acceptance contract are defined. Individual implementation claims should only be promoted to “working”, “tested”, or “production-ready” after corresponding execution evidence exists.

---

## Contributors & Origin

### S/Agency

Product direction, crawler requirements, level model, system integration direction, and acceptance standard.

### DeepSeek

**Original exploration and development contributor.** DeepSeek participated in the conversation in which the crawler evolved from an initial GitHub Docs crawling request into the Level 0→5 model, browser-rendered crawler, backend/frontend integration concept, interface variants, and the requirement for real rather than simulated testing.

The originating shared conversation is preserved here:

https://chat.deepseek.com/share/9ix2m4km0xd3lc0d61

### ChatGPT

Specification consolidation, reusable project asset, architecture normalization, acceptance contract, and repository documentation.

---

## Contribution Principle

Contributions are welcome when they improve **real behavior**, evidence quality, interoperability, or usability.

A contribution that adds a button without wiring it is not finished.

A contribution that adds a test badge without running a test is not evidence.

A contribution that makes the crawler actually crawl is the point.

---

## Roadmap

- [ ] Implement the canonical crawl engine.
- [ ] Wire Playwright rendering.
- [ ] Implement Level 0→N traversal.
- [ ] Add normalized graph/evidence schema.
- [ ] Wire Flask API.
- [ ] Ship primary frontend.
- [ ] Ship Universal Dark One.
- [ ] Add export formats.
- [ ] Add resumable crawl frontier.
- [ ] Add content hashing / change detection.
- [ ] Add agent/workflow handoff.
- [ ] Add reproducible integration and E2E test suite.

---

## One rule

**If the crawler did not run, we do not say it ran.**

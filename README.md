# VentureRadar — Autonomous B2B Use Case Discovery Agent

Type a B2B industry. Get back ranked AI automation opportunities with product briefs — in 90 seconds.

## The Problem

Venture studios and AI consultancies spend days doing manual discovery: browsing Reddit, reading reviews, cold-calling potential customers — just to figure out *which* workflow to automate first. That discovery step is itself a workflow that can be automated.

## The Solution

A 4-agent autonomous pipeline that researches any B2B industry and returns a ranked, investor-ready report.

## Agent Pipeline

```
Industry Input
      │
      ▼
[Agent 1: Industry Researcher]
  Searches Reddit, HN, LinkedIn, G2 reviews → extracts real pain points with evidence
      │
      ▼
[Agent 2: Competitor Scanner]
  Maps existing tools → finds gaps and underserved problems
      │
      ▼
[Agent 3: Opportunity Scorer]
  Scores top opportunities on: Market Size + Feasibility + Whitespace → ranked list
      │
      ▼
[Agent 4: Brief Writer]
  Writes a product brief per opportunity: problem, solution, buyer, ROI, why now, MVP
      │
      ▼
Discovery Report
```

## Setup

**Step 1 — Get API keys (both free tier)**
- Gemini: [aistudio.google.com](https://aistudio.google.com)
- Serper (web search): [serper.dev](https://serper.dev) — 2,500 free searches

**Step 2 — Add keys to `.env`**
```
GEMINI_API_KEY=...
SERPER_API_KEY=...
```

**Step 3 — Install**
```bash
pip install -r requirements.txt
```

**Step 4 — Run**
```bash
python demo.py
```

Open `http://localhost:7860`, type an industry, click **Run Discovery**.

## Example Output (logistics)

```
#1 Freight Document Processing          Score: 28/30
   Problem: Carriers manually key BOL and POD data — 3 hrs/shipment, 12% error rate
   Solution: Vision + extraction agent that reads any document format
   Buyer: Operations Manager at mid-size 3PL (50-500 employees)
   ROI: Saves ~15 hrs/week per dispatcher, reduces chargebacks by 60%
   Why Now: Gemini Vision can now read handwritten freight docs reliably
   MVP: Upload BOL → extract fields → push to TMS via API

#2 Carrier Rate Negotiation Assistant   Score: 24/30
   ...

#3 Customs Compliance Checker           Score: 21/30
   ...
```

## Why This Architecture

Built with CrewAI's sequential process so each agent's output feeds the next — the Brief Writer only sees pre-scored opportunities, the Scorer only sees research that's already been cross-checked against competitors. This prevents hallucination and keeps the final output grounded in real search results.
# Venture-Radar

# Chess Framework — AI Competitive Intelligence System

> What if you could map a company's competitive position like a chess game? Where piece placement = strategic strength, and board position = market reality.

## Origin

I was building a dataset of AI companies — scoring them on funding, model count, risk exposure, market dominance, unique advantages, and ecosystem strength. Seven companies. Six dimensions. Straightforward spreadsheet work.

But then I realized something: these dimensions are exactly what matter in chess. Material (pieces/resources), Mobility (how many moves available), King Safety (exposure to threat), Center Control (dominance of key squares), Passed Pawns (unique advantages), Piece Coordination (ecosystem integration).

What if I mapped each company as a chess position, where their piece placement showed their actual strategic state? Not as a metaphor, but as a *real analytic framework that happens to look like chess*.

The result: **a system that translates corporate strategy into visual, readable, and — surprisingly — transferable across industries**.

---

## What I Built

### Dataset
7 AI companies scored across 6 strategic dimensions:

| Company | Source |
|---------|--------|
| OpenAI | Crunchbase, company disclosures, news |
| Anthropic | LMSYS Chatbot Arena, enterprise signals |
| Google DeepMind | Public announcements, GitHub model repos |
| Meta AI | Investor reports, open-source activity |
| Microsoft AI | Azure integration data, partnership announcements |
| Mistral | EU regulatory filings, research papers |
| xAI | Funding announcements, X/Twitter integration |

### Dimensions (Raw Scores 0–10)

| Dimension | Definition | Source |
|-----------|-----------|--------|
| **Material** | Total funding raised | Crunchbase, company disclosures |
| **Mobility** | Model portfolio + API integrations | Company websites, HuggingFace |
| **King Safety** | Regulatory risk + runway | EU AI Act compliance, burn rate analysis |
| **Center Control** | LMSYS ranking + enterprise adoption | Chatbot Arena leaderboard, case studies |
| **Passed Pawns** | Unique models with no direct competitor | Patent analysis, market differentiation |
| **Piece Coordination** | Ecosystem strength (cloud ties, tools, partners) | Integration announcements, partnership depth |

### Analysis Pipeline

```
Raw Data Collection
    ↓
Normalization (logarithmic for funding, min-max for others)
    ↓
Weighting System A: Chess Perspective
  (mobility & center control = 0.25 each — tactical focus)
    ↓
Weighting System B: Business Perspective  
  (material & coordination = 0.25/0.20 — structural focus)
    ↓
Position Generation
  (score → piece placement on chess board)
    ↓
Interactive Visualization
  (dual boards + radar charts + breakdown table)
```

---

## Key Findings

### 1. **Different Perspectives, Different Winners**

| Ranking | Chess Perspective | Business Perspective |
|---------|------------------|----------------------|
| #1 | OpenAI (8.86) | Google DeepMind (8.75) |
| #2 | Google DeepMind (8.80) | OpenAI (8.50) |
| #3 | Anthropic (5.65) | Microsoft AI (6.99) |

**Insight:** OpenAI dominates tactically (models, mobility) but Google is stronger structurally (ecosystem, safety). Anthropic has the best center control (LMSYS #1) but lacks ecosystem scale. Microsoft dominates integration but lags on frontier models.

### 2. **Convergence & Divergence**

Companies where **chess ≈ business** (balanced position):
- **Google DeepMind** (+0.05 delta) — equally strong tactically and structurally

Companies where **chess ≠ business** (exposed position):
- **Microsoft AI** (-2.13 delta) — strong ecosystem, weak models
- **xAI** (-1.51 delta) — funded but underdeveloped across dimensions

---

## Methodology Notes

**Why chess, not just a table?**

Three reasons:
1. **Visualization clarity:** A piece's position on the board immediately shows advancement. Advanced = high score. Back rank = underdeveloped. No need to read numbers.

2. **Transferability:** This framework works for any competitive landscape where you can define 6 strategic dimensions and map them to pieces. Automotive (Material = scale, Mobility = model lineup), Pharma (Material = R&D budget, Passed Pawns = unique drugs), Fintech (Material = capital, King Safety = regulatory).

3. **Intuitive narrative:** Non-technical stakeholders understand chess. CEOs, board members, marketing teams all immediately grasp "our king is exposed" (regulatory risk) or "we're losing the center" (market control).

**Weighting logic:**

Chess perspective weights mobility and center control heavily — in chess, a mobile piece in the center is more valuable than raw material quantity.

Business perspective weights material and ecosystem coordination — in business, capital and structural partnerships often matter more than feature count.

This isn't arbitrary. It's a deliberate choice to show how the *same data* yields different conclusions depending on what you prioritize.

---

## Deliverables

### Interactive HTML Report
Open `chess_[Company_A]_vs_[Company_B].html` in a browser to see:
- Dual chess boards (chess vs. business perspective)
- Real-time advantage bars
- Captured pieces (missing strengths)
- Dimension-by-dimension breakdown
- Strategic interpretation

### Generated Positions (Examples)

**OpenAI vs. Anthropic (Chess Perspective)**
- OpenAI: Dominant mobility (pieces scattered across board), strong material, exposed king (safety risk)
- Anthropic: Consolidated center control, weak ecosystem, underdeveloped material

Interpretation: OpenAI is "attacking" but has exposure; Anthropic is defending the center but not expanding.

---

## How to Replicate on Another Industry

1. **Define your 6 dimensions** — What matters in this industry? For automotive: scale, model lineup, charging network, autonomous capability, brand safety, supplier integration.

2. **Score 5-7 competitors** — Use public data: financial reports, market research, news, patent filings.

3. **Normalize each dimension** — Keep everything 0–10 scale for consistency.

4. **Map to chess pieces** — Material→Rooks, Mobility→Knights, Center Control→Bishops, Coordination→Queen, Safety→King, Unique Advantage→Pawns.

5. **Generate positions** — Run the Python script (provided in repo) to auto-generate board positions.

6. **Weigh and compare** — Use dual perspectives (tactical vs. structural) to reveal strategy divergence.

---

## Code & Tools

**Language:** Python 3.14
**Libraries:** `python-chess` (board generation), `pandas` (data normalization), `numpy` (weighting calculations)
**Visualization:** Interactive HTML with CSS styling, no external charting library needed
**Data Format:** CSV input, HTML output

---

## Limitations 

**Current limitations:**
- Scoring is partially qualitative (enterprise signals, unique models require judgment calls)
- Not real-time — based on snapshot data from June 2026
- Limited to 6 dimensions (could expand to 8-10 but readability decreases)


## Attribution & Methodology

Data collected from: Crunchbase (funding), company disclosures (model counts), LMSYS Chatbot Arena (rankings), news sources (partnerships), EU regulatory filings (risk assessment), GitHub (open-source activity).

Normalization: Logarithmic for heavily-skewed dimensions (funding), min-max for bounded dimensions (scores 0–10).

Interpretation: Based on public market signals, not insider information.

---

*Chess Framework by Filippo Leonetti Luparini • June 2026*

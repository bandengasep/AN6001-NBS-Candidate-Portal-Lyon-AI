# NBS Candidate Portal Design

## Problem

The current NBS Degree Advisor is a single-page chatbot. It works well for users who already know what programme they want (Type 2), but offers nothing for users who are undecided and need guidance (Type 1). The UI is functional but not representative of NBS's brand.

## Solution

Revamp the chatbot into a **Candidate Portal** with two user journeys, a professional NTU-branded frontend, and Vercel deployment.

## User Types

**Type 1 -- Undecided**: Users who are not sure which programme fits them. They upload a CV and/or take a quiz. The system recommends programmes via embedding similarity and displays their profile as a spider chart.

**Type 2 -- Decided**: Users who already know what they want. They chat directly with Lyon for detailed programme info. This is the existing chatbot flow, restyled.

## Page Structure

| Route | Page | Purpose |
|-------|------|---------|
| `/` | Splash Page | NTU-styled landing with two pathway cards, programme grid, Lyon teaser, stats bar |
| `/recommend` | Recommendation Wizard | CV upload + 7-step quiz + spider chart + results |
| `/chat` | Lyon Chat | Existing chatbot, restyled to NTU design |
| `/programmes` | Programme Browser | All 22 programmes with filter tabs, NBS links + "Ask Lyon" |

No authentication. All pages are public. Conversation history stays UUID-based.

## Splash Page Design

Matches NTU/NBS website design language:
- NTU brand colors: Red `#E01932`, Blue `#0071BC`, Gold `#F79320`
- Source Sans 3 font (close match to NTU's PF DinText Universal)
- White-dominant backgrounds, clean institutional aesthetic
- Dark thin top bar with NTU links
- White sticky header with red CTA button
- Hero with two pathway cards on the right side
- Stats bar (22 programmes, #1 in Singapore, 100+ nationalities, triple accredited)
- Programme grid with colored top banners (red for MBA, blue for MSc)
- Filter tabs (All / MBA / MSc / PhD / Executive)
- Lyon teaser section with live chat preview
- Structured footer with columns

Prototype: `docs/prototypes/splash-page-concept.html`

## Recommendation Flow (`/recommend`)

### Step 0: CV Upload (optional)
- Drag-and-drop or file picker for PDF resume
- "Skip" button to go straight to quiz
- pdfplumber extracts text, GPT-5.2 parses into structured fields
- Parsed fields pre-fill relevant quiz steps

### Steps 1-7: Quiz (one question per screen)

Progress bar at top. Spider chart builds live on the right side.

| Step | Question Theme | Spider Chart Axis |
|------|---------------|-------------------|
| 1 | Educational background & quantitative comfort | Quantitative Skills |
| 2 | Years & type of work experience | Professional Experience |
| 3 | Leadership/management roles held | Leadership |
| 4 | Interest in technology, data, coding | Tech & Analytics |
| 5 | Interest area: finance, marketing, strategy, etc. | Business Domain |
| 6 | Career goal: switch, advance, specialise, research | Career Ambition |
| 7 | Study preference: full-time vs part-time, duration | Study Flexibility |

Each question is multiple choice (3-4 options), scored numerically behind the scenes.

### Step 8: Results

- User's completed spider chart overlaid with top 3 programme profiles
- Each result shows: name, match score, spider chart overlay
- Two buttons per result: "Visit NBS Page" (external link) + "Ask Lyon" (routes to `/chat?programme=X`)
- Matching via embedding similarity: quiz answers + CV text composed into paragraph, embedded, cosine similarity against programme embeddings in Supabase

## Programme Cards (everywhere)

Every programme card (splash, browser, results) has two actions:
- **"Visit NBS Page"** -- external link to real NTU website, opens in new tab
- **"Ask Lyon"** -- routes to `/chat` with programme pre-loaded as context

URLs come from the programme registry (already scraped).

## Spider Chart

- 7 axes: Quantitative Skills, Professional Experience, Leadership, Tech & Analytics, Business Domain, Career Ambition, Study Flexibility
- Visualization layer only -- not the matching engine
- User profile derived from quiz answers (numeric scores per axis)
- Programme profiles pre-defined and stored in `programs` table
- Displayed using chart.js radar chart via react-chartjs-2

## Technical Architecture

### Frontend
- Add `react-router-dom` for 4 routes
- Add `chart.js` + `react-chartjs-2` for radar/spider chart
- Restyle existing chat components to NTU design language
- New components: SplashPage, RecommendWizard, ProgrammeBrowser, SpiderChart

### Backend (new endpoints)
- `POST /api/recommend/parse-cv` -- accepts PDF, extracts text (pdfplumber), structured extraction (GPT-5.2), returns parsed fields
- `POST /api/recommend/match` -- accepts quiz answers + optional CV text, embeds, cosine similarity against programme embeddings, returns top matches
- `GET /api/programmes/{id}/profile` -- returns programme's spider chart scores

### Database
- Add `profile_scores` JSON column to `programs` table (7 axis scores per programme)
- No other schema changes

### What stays unchanged
- Chat endpoints, LangChain agent, tools (RAG, compare, FAQ)
- Embedding model (text-embedding-3-small, 1536 dimensions)
- Vector store and retrieval pipeline
- Scraper and ingestion pipeline
- Supabase chat_history table
- Lyon personality and GPT-5.2 config

### Deployment
- All on Vercel (frontend static build + backend serverless Python functions)
- Single platform, single URL
- Vercel CLI/plugin available for deployment

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite + Tailwind CSS + react-router-dom |
| Charts | chart.js + react-chartjs-2 |
| Backend | FastAPI (serverless on Vercel) |
| AI | GPT-5.2 (chat + CV parsing), text-embedding-3-small (embeddings) |
| Agent | LangChain with tools |
| Database | Supabase (PostgreSQL + pgvector) |
| Deployment | Vercel |

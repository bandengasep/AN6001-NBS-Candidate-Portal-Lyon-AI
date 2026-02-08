# NBS Candidate Portal Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform the single-page NBS chatbot into a multi-page Candidate Portal with programme recommendations (CV upload + quiz + spider chart + embedding similarity matching), a programme browser, and Vercel deployment.

**Architecture:** Add react-router-dom for 4 routes (splash, recommend, chat, programmes). Add 3 new backend endpoints for CV parsing, recommendation matching, and programme profiles. Deploy everything on Vercel (static frontend + serverless Python backend). Existing chat agent, RAG pipeline, and Supabase setup remain unchanged.

**Tech Stack:** React 18, react-router-dom, chart.js + react-chartjs-2, Tailwind CSS, FastAPI (Vercel serverless), Supabase pgvector, GPT-5.2, text-embedding-3-small

**Design Doc:** `docs/plans/2026-02-08-candidate-portal-design.md`
**Prototype:** `docs/prototypes/splash-page-concept.html`

---

### Task 1: Install frontend dependencies

**Files:**
- Modify: `frontend/package.json`

**Step 1: Install new packages**

Run from WSL:
```bash
cd /mnt/c/dev/AN6001-NBS-Candidate-Portal-Lyon-AI/frontend
npm install react-router-dom chart.js react-chartjs-2
```

**Step 2: Verify install**

Run:
```bash
cd /mnt/c/dev/AN6001-NBS-Candidate-Portal-Lyon-AI/frontend
node -e "require('react-router-dom'); require('chart.js'); require('react-chartjs-2'); console.log('All packages OK')"
```
Expected: `All packages OK`

**Step 3: Commit**

```bash
git add frontend/package.json frontend/package-lock.json
git commit -m "chore: add react-router-dom, chart.js, react-chartjs-2"
```

---

### Task 2: Update Tailwind config with NTU brand colors

**Files:**
- Modify: `frontend/tailwind.config.js`

**Step 1: Replace brand colors**

Replace the `colors` section in `frontend/tailwind.config.js` `theme.extend`:

```javascript
colors: {
  'ntu-red': '#E01932',
  'ntu-red-hover': '#C2142A',
  'ntu-blue': '#0071BC',
  'ntu-gold': '#F79320',
  'ntu-dark': '#2D2D2D',
  'ntu-body': '#4A4A4A',
  'ntu-muted': '#888888',
  'ntu-border': '#E5E5E5',
  // Keep old names as aliases for backward compat in existing chat components
  'nbs-red': '#E01932',
  'nbs-red-dark': '#C2142A',
  'nbs-gold': '#F79320',
},
```

**Step 2: Commit**

```bash
git add frontend/tailwind.config.js
git commit -m "chore: update Tailwind config with NTU brand colors"
```

---

### Task 3: Set up React Router with 4 routes

**Files:**
- Modify: `frontend/src/main.jsx`
- Modify: `frontend/src/App.jsx`
- Create: `frontend/src/pages/SplashPage.jsx` (placeholder)
- Create: `frontend/src/pages/RecommendPage.jsx` (placeholder)
- Create: `frontend/src/pages/ChatPage.jsx` (extract from current App.jsx)
- Create: `frontend/src/pages/ProgrammesPage.jsx` (placeholder)

**Step 1: Create ChatPage by extracting current App.jsx logic**

Create `frontend/src/pages/ChatPage.jsx`:

```jsx
import { Header } from '../components/Layout/Header';
import { Sidebar } from '../components/Layout/Sidebar';
import { ChatContainer } from '../components/Chat/ChatContainer';
import { useChat } from '../hooks/useChat';

export default function ChatPage() {
  const {
    messages,
    isLoading,
    error,
    messagesEndRef,
    sendMessage,
    clearChat,
  } = useChat();

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <Header />
      <div className="flex-1 flex overflow-hidden">
        <Sidebar onQuestionClick={sendMessage} />
        <main className="flex-1 flex flex-col">
          <ChatContainer
            messages={messages}
            isLoading={isLoading}
            error={error}
            messagesEndRef={messagesEndRef}
            onSendMessage={sendMessage}
            onClearChat={clearChat}
          />
        </main>
      </div>
    </div>
  );
}
```

**Step 2: Create placeholder pages**

Create `frontend/src/pages/SplashPage.jsx`:
```jsx
import { Link } from 'react-router-dom';

export default function SplashPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-white">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-ntu-dark mb-4">NBS Candidate Portal</h1>
        <p className="text-ntu-body mb-8">Coming soon - full splash page</p>
        <div className="flex gap-4 justify-center">
          <Link to="/recommend" className="px-6 py-3 bg-ntu-red text-white rounded">Get Recommendations</Link>
          <Link to="/chat" className="px-6 py-3 border border-ntu-red text-ntu-red rounded">Chat with Lyon</Link>
        </div>
      </div>
    </div>
  );
}
```

Create `frontend/src/pages/RecommendPage.jsx`:
```jsx
export default function RecommendPage() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <h1 className="text-2xl font-bold text-ntu-dark">Recommendation Wizard - Coming Soon</h1>
    </div>
  );
}
```

Create `frontend/src/pages/ProgrammesPage.jsx`:
```jsx
export default function ProgrammesPage() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <h1 className="text-2xl font-bold text-ntu-dark">Programme Browser - Coming Soon</h1>
    </div>
  );
}
```

**Step 3: Update main.jsx with BrowserRouter**

Replace `frontend/src/main.jsx`:
```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
)
```

**Step 4: Replace App.jsx with route config**

Replace `frontend/src/App.jsx`:
```jsx
import { Routes, Route } from 'react-router-dom';
import SplashPage from './pages/SplashPage';
import RecommendPage from './pages/RecommendPage';
import ChatPage from './pages/ChatPage';
import ProgrammesPage from './pages/ProgrammesPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<SplashPage />} />
      <Route path="/recommend" element={<RecommendPage />} />
      <Route path="/chat" element={<ChatPage />} />
      <Route path="/programmes" element={<ProgrammesPage />} />
    </Routes>
  );
}

export default App;
```

**Step 5: Verify routing works**

Run:
```bash
cd /mnt/c/dev/AN6001-NBS-Candidate-Portal-Lyon-AI/frontend
npm run dev
```

Check in browser:
- `http://localhost:5173/` shows splash placeholder
- `http://localhost:5173/chat` shows existing chat UI
- `http://localhost:5173/recommend` shows recommend placeholder
- `http://localhost:5173/programmes` shows programmes placeholder

**Step 6: Commit**

```bash
git add frontend/src/main.jsx frontend/src/App.jsx frontend/src/pages/
git commit -m "feat: add react-router with 4 routes (splash, recommend, chat, programmes)"
```

---

### Task 4: Build the Splash Page

**Files:**
- Modify: `frontend/src/pages/SplashPage.jsx`
- Create: `frontend/src/components/Layout/TopBar.jsx`
- Create: `frontend/src/components/Layout/PortalHeader.jsx`
- Create: `frontend/src/components/Layout/Footer.jsx`

**Reference:** `docs/prototypes/splash-page-concept.html` -- translate the HTML/CSS prototype into React + Tailwind components.

**Step 1: Create shared layout components**

Create `frontend/src/components/Layout/TopBar.jsx` -- the dark thin bar at the top with NTU links:
```jsx
export function TopBar() {
  return (
    <div className="bg-ntu-dark py-1.5 px-8 flex justify-end gap-6 text-xs">
      <a href="https://www.ntu.edu.sg" target="_blank" rel="noopener noreferrer"
         className="text-white/70 hover:text-white transition-colors">NTU Home</a>
      <a href="https://www.ntu.edu.sg/business" target="_blank" rel="noopener noreferrer"
         className="text-white/70 hover:text-white transition-colors">NBS Website</a>
      <a href="https://www.ntu.edu.sg/business/admissions" target="_blank" rel="noopener noreferrer"
         className="text-white/70 hover:text-white transition-colors">Admissions</a>
    </div>
  );
}
```

Create `frontend/src/components/Layout/PortalHeader.jsx` -- the white sticky header:
```jsx
import { Link } from 'react-router-dom';

export function PortalHeader() {
  return (
    <header className="bg-white border-b border-ntu-border sticky top-0 z-50 shadow-sm">
      <div className="max-w-[1200px] mx-auto px-8 py-3 flex justify-between items-center">
        <Link to="/" className="flex items-center gap-3 no-underline">
          <div className="w-10 h-10 bg-ntu-red rounded flex items-center justify-center">
            <span className="text-white font-bold text-sm">NBS</span>
          </div>
          <div className="h-7 w-px bg-ntu-border" />
          <div>
            <div className="text-ntu-dark font-semibold text-[1.05rem] leading-tight">Candidate Portal</div>
            <div className="text-ntu-muted text-[0.72rem]">Nanyang Business School</div>
          </div>
        </Link>
        <nav className="hidden md:flex items-center gap-8">
          <Link to="/programmes" className="text-ntu-body text-sm hover:text-ntu-red transition-colors">Programmes</Link>
          <Link to="/chat" className="text-ntu-body text-sm hover:text-ntu-red transition-colors">Ask Lyon</Link>
          <Link to="/recommend" className="bg-ntu-red text-white px-5 py-2 rounded text-sm font-semibold hover:bg-ntu-red-hover transition-colors">Get Started</Link>
        </nav>
      </div>
    </header>
  );
}
```

Create `frontend/src/components/Layout/Footer.jsx`:
```jsx
export function Footer() {
  return (
    <footer className="bg-ntu-dark text-white/60 text-sm">
      <div className="max-w-[1200px] mx-auto px-8 py-10 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <div className="text-white font-semibold mb-2">Nanyang Business School</div>
          <div className="text-white/40 text-xs leading-relaxed">
            Nanyang Technological University, Singapore<br />
            50 Nanyang Avenue, Singapore 639798<br /><br />
            AN6001 AI and Big Data Group Project
          </div>
        </div>
        <div>
          <h4 className="text-white/40 text-xs font-semibold uppercase tracking-wider mb-3">Quick Links</h4>
          <a href="https://www.ntu.edu.sg/business" target="_blank" rel="noopener noreferrer"
             className="block text-white/65 text-sm py-1 hover:text-white transition-colors">NBS Website</a>
          <a href="https://www.ntu.edu.sg/business/admissions" target="_blank" rel="noopener noreferrer"
             className="block text-white/65 text-sm py-1 hover:text-white transition-colors">Admissions</a>
          <a href="https://www.ntu.edu.sg/business/admissions/graduate-studies" target="_blank" rel="noopener noreferrer"
             className="block text-white/65 text-sm py-1 hover:text-white transition-colors">Graduate Studies</a>
        </div>
        <div>
          <h4 className="text-white/40 text-xs font-semibold uppercase tracking-wider mb-3">Resources</h4>
          <a href="/recommend" className="block text-white/65 text-sm py-1 hover:text-white transition-colors">Programme Finder</a>
          <a href="/chat" className="block text-white/65 text-sm py-1 hover:text-white transition-colors">Chat with Lyon</a>
          <a href="/programmes" className="block text-white/65 text-sm py-1 hover:text-white transition-colors">Browse Programmes</a>
        </div>
      </div>
      <div className="max-w-[1200px] mx-auto px-8 py-4 border-t border-white/10 flex justify-between text-xs text-white/35">
        <span>&copy; 2026 Nanyang Technological University. All rights reserved.</span>
        <span>Powered by AI</span>
      </div>
    </footer>
  );
}
```

**Step 2: Build the full SplashPage**

Replace `frontend/src/pages/SplashPage.jsx` with the full page translating the HTML prototype into React + Tailwind. The page includes:
- TopBar + PortalHeader
- Hero section (dark background, headline, two CTA buttons, two pathway cards)
- Stats bar (22 programmes, #1, 100+ nationalities, triple accredited)
- Programme grid (6 featured cards from API, with filter tabs)
- Lyon teaser section (features list + chat mockup)
- Footer

Key: programme cards use `getPrograms()` from `services/api.js`. Each card has two links:
- "Visit NBS Page" -> external URL from programme data (target="_blank")
- "Ask Lyon" -> `<Link to={"/chat?programme=" + prog.name}>`

**Step 3: Update the Layout barrel export**

Modify `frontend/src/components/Layout/index.js` to export the new components:
```javascript
export { Header } from './Header';
export { Sidebar } from './Sidebar';
export { TopBar } from './TopBar';
export { PortalHeader } from './PortalHeader';
export { Footer } from './Footer';
```

**Step 4: Verify splash page renders**

Run dev server, visit `http://localhost:5173/`. Verify:
- NTU-styled header and top bar render
- Hero section with two pathway cards
- Programme cards load from API (or show graceful empty state)
- Footer with links
- "Get Recommendations" navigates to /recommend
- "Chat with Lyon" navigates to /chat

**Step 5: Commit**

```bash
git add frontend/src/pages/SplashPage.jsx frontend/src/components/Layout/
git commit -m "feat: build NTU-styled splash page with hero, programme grid, and Lyon teaser"
```

---

### Task 5: Build the Programme Browser Page

**Files:**
- Modify: `frontend/src/pages/ProgrammesPage.jsx`

**Step 1: Build programme browser**

Full page with:
- TopBar + PortalHeader (shared layout)
- Section header with "Graduate Programmes" title
- Filter tabs: All | MBA | MSc | PhD | Executive (client-side filtering using `degree_type`)
- Programme grid (all 22 from API) with cards identical to splash page
- Each card: coloured top banner (red=MBA, blue=MSc, dark=PhD), name, duration, mode
- Two actions per card: "Visit NBS Page" (external) + "Ask Lyon" (internal link)
- Footer

Uses `getPrograms()` and `getProgramsByType()` from `services/api.js`.

**Step 2: Verify**

Visit `http://localhost:5173/programmes`. Click filter tabs. Click programme cards.

**Step 3: Commit**

```bash
git add frontend/src/pages/ProgrammesPage.jsx
git commit -m "feat: build programme browser with filter tabs and NBS links"
```

---

### Task 6: Add profile_scores to programs table (database migration)

**Files:**
- Create: `scripts/add_profile_scores.sql`
- Create: `scripts/seed_profile_scores.py`

**Step 1: Write SQL migration**

Create `scripts/add_profile_scores.sql`:
```sql
-- Add spider chart profile scores to programs table
-- 7 axes: quantitative, experience, leadership, tech_analytics, business_domain, career_ambition, study_flexibility
-- Each score is 1-5

ALTER TABLE programs
ADD COLUMN IF NOT EXISTS profile_scores jsonb DEFAULT '{}';

COMMENT ON COLUMN programs.profile_scores IS 'Spider chart scores: {quantitative, experience, leadership, tech_analytics, business_domain, career_ambition, study_flexibility} each 1-5';
```

Run in Supabase SQL Editor.

**Step 2: Write seed script**

Create `scripts/seed_profile_scores.py` that updates each programme with hand-curated scores. Example:

```python
"""Seed spider chart profile scores for all programmes."""

PROFILE_SCORES = {
    "Nanyang MBA": {
        "quantitative": 3, "experience": 4, "leadership": 5,
        "tech_analytics": 3, "business_domain": 4, "career_ambition": 5, "study_flexibility": 2
    },
    "Executive MBA": {
        "quantitative": 3, "experience": 5, "leadership": 5,
        "tech_analytics": 2, "business_domain": 4, "career_ambition": 5, "study_flexibility": 4
    },
    "MSc Business Analytics": {
        "quantitative": 5, "experience": 2, "leadership": 2,
        "tech_analytics": 5, "business_domain": 3, "career_ambition": 4, "study_flexibility": 2
    },
    "MSc Financial Engineering": {
        "quantitative": 5, "experience": 2, "leadership": 2,
        "tech_analytics": 4, "business_domain": 4, "career_ambition": 4, "study_flexibility": 2
    },
    # ... scores for all 22 programmes
}
```

The script connects to Supabase and updates each programme's `profile_scores` column.

Run:
```bash
"/mnt/c/Users/User/anaconda3/envs/nbs-msba/python.exe" scripts/seed_profile_scores.py
```

**Step 3: Commit**

```bash
git add scripts/add_profile_scores.sql scripts/seed_profile_scores.py
git commit -m "feat: add spider chart profile scores to programs table"
```

---

### Task 7: Backend -- programme profile endpoint

**Files:**
- Modify: `backend/app/api/routes/programs.py`

**Step 1: Add profile endpoint**

Add to `backend/app/api/routes/programs.py`:

```python
@router.get("/{program_id}/profile")
async def get_program_profile(program_id: str, supabase: SupabaseDep) -> dict:
    """Get a programme's spider chart profile scores."""
    result = supabase.table("programs").select("name, profile_scores").eq("id", program_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Program not found")
    return result.data
```

**Step 2: Verify**

Start backend, then:
```bash
curl http://localhost:8000/api/programs/ | head -20
```
Pick an ID, then:
```bash
curl http://localhost:8000/api/programs/<id>/profile
```
Expected: JSON with `name` and `profile_scores`.

**Step 3: Commit**

```bash
git add backend/app/api/routes/programs.py
git commit -m "feat: add programme profile scores endpoint"
```

---

### Task 8: Backend -- CV parsing endpoint

**Files:**
- Create: `backend/app/api/routes/recommend.py`
- Modify: `backend/app/main.py` (register new router)

**Step 1: Create recommend routes**

Create `backend/app/api/routes/recommend.py`:

```python
"""Recommendation API routes."""

import json
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
import pdfplumber
import io

from app.config import get_settings
from app.rag.embeddings import get_embedding, get_openai_client
from app.api.deps import SupabaseDep

router = APIRouter(prefix="/recommend", tags=["recommend"])


class CVParseResponse(BaseModel):
    """Structured fields extracted from CV."""
    years_experience: int | None = None
    industry: str | None = None
    education_level: str | None = None
    skills: list[str] = []
    quantitative_background: str | None = None
    leadership_experience: str | None = None
    raw_text: str = ""


@router.post("/parse-cv", response_model=CVParseResponse)
async def parse_cv(file: UploadFile = File(...)) -> CVParseResponse:
    """Upload and parse a PDF CV into structured fields.

    Extracts text with pdfplumber, then uses GPT-5.2 to extract
    structured fields for quiz pre-fill.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    try:
        # Read PDF
        contents = await file.read()
        pdf = pdfplumber.open(io.BytesIO(contents))
        raw_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        pdf.close()

        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")

        # Use GPT to extract structured fields
        settings = get_settings()
        client = get_openai_client()

        response = client.chat.completions.create(
            model=settings.chat_model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": """Extract structured information from this CV/resume.
Return JSON with these fields:
- years_experience: integer (total years of work experience, 0 if fresh graduate)
- industry: string (primary industry, e.g. "Finance", "Technology", "Consulting")
- education_level: string (one of: "Diploma", "Bachelor", "Master", "PhD")
- skills: array of strings (top 5-8 relevant skills)
- quantitative_background: string (one of: "Strong", "Moderate", "Limited")
- leadership_experience: string (one of: "Senior/Executive", "Mid-level/Manager", "Junior/None")"""},
                {"role": "user", "content": raw_text[:4000]}
            ]
        )

        parsed = json.loads(response.choices[0].message.content)
        return CVParseResponse(**parsed, raw_text=raw_text[:2000])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing CV: {str(e)}")
```

**Step 2: Register router in main.py**

Add to `backend/app/main.py` after the existing router includes:

```python
from app.api.routes import programs, chat, recommend

# In create_app():
app.include_router(recommend.router, prefix="/api")
```

**Step 3: Verify**

Start backend. Create a test PDF or use an existing one:
```bash
curl -X POST http://localhost:8000/api/recommend/parse-cv \
  -F "file=@test_cv.pdf"
```
Expected: JSON with extracted fields.

**Step 4: Commit**

```bash
git add backend/app/api/routes/recommend.py backend/app/main.py
git commit -m "feat: add CV parsing endpoint with pdfplumber + GPT extraction"
```

---

### Task 9: Backend -- recommendation matching endpoint

**Files:**
- Modify: `backend/app/api/routes/recommend.py`

**Step 1: Add match endpoint**

Add to `backend/app/api/routes/recommend.py`:

```python
class QuizAnswers(BaseModel):
    """User's quiz answers as scores per axis."""
    quantitative: int  # 1-5
    experience: int
    leadership: int
    tech_analytics: int
    business_domain: int
    career_ambition: int
    study_flexibility: int
    cv_text: str | None = None  # Optional raw CV text


class ProgramMatch(BaseModel):
    """A matched programme with score."""
    program_id: str
    name: str
    degree_type: str
    url: str | None
    similarity: float
    profile_scores: dict


class MatchResponse(BaseModel):
    """Recommendation results."""
    user_scores: dict
    matches: list[ProgramMatch]


@router.post("/match", response_model=MatchResponse)
async def match_programmes(answers: QuizAnswers, supabase: SupabaseDep) -> MatchResponse:
    """Match user profile to programmes via embedding similarity.

    Composes quiz answers (+ optional CV text) into a text paragraph,
    embeds it, and compares against programme embeddings in Supabase.
    Returns top 3 matches with spider chart profile scores.
    """
    # Compose user profile as natural language for embedding
    profile_parts = [
        f"I have {_experience_label(answers.experience)} of work experience.",
        f"My quantitative skills are {_level_label(answers.quantitative)}.",
        f"My leadership experience is {_level_label(answers.leadership)}.",
        f"My interest in technology and analytics is {_level_label(answers.tech_analytics)}.",
        f"I am interested in {_domain_label(answers.business_domain)}.",
        f"My career goal is to {_ambition_label(answers.career_ambition)}.",
        f"I prefer {_flexibility_label(answers.study_flexibility)} study.",
    ]
    if answers.cv_text:
        profile_parts.append(f"Background from CV: {answers.cv_text[:1000]}")

    profile_text = " ".join(profile_parts)

    # Embed user profile
    user_embedding = get_embedding(profile_text)

    # Search against programme document embeddings
    result = supabase.rpc(
        "match_documents",
        {
            "query_embedding": user_embedding,
            "match_count": 10,
            "match_threshold": 0.3
        }
    ).execute()

    # Group by programme, take best similarity per programme
    programme_scores = {}
    for doc in (result.data or []):
        prog_name = doc.get("metadata", {}).get("program", "")
        sim = doc.get("similarity", 0)
        if prog_name and (prog_name not in programme_scores or sim > programme_scores[prog_name]):
            programme_scores[prog_name] = sim

    # Get programme details for top matches
    all_programs = supabase.table("programs").select("*").execute()
    program_map = {p["name"]: p for p in (all_programs.data or [])}

    matches = []
    for name, sim in sorted(programme_scores.items(), key=lambda x: -x[1])[:3]:
        prog = program_map.get(name)
        if prog:
            matches.append(ProgramMatch(
                program_id=prog["id"],
                name=prog["name"],
                degree_type=prog["degree_type"],
                url=prog.get("url"),
                similarity=round(sim, 3),
                profile_scores=prog.get("profile_scores", {})
            ))

    user_scores = {
        "quantitative": answers.quantitative,
        "experience": answers.experience,
        "leadership": answers.leadership,
        "tech_analytics": answers.tech_analytics,
        "business_domain": answers.business_domain,
        "career_ambition": answers.career_ambition,
        "study_flexibility": answers.study_flexibility,
    }

    return MatchResponse(user_scores=user_scores, matches=matches)


# Helper functions to convert numeric scores to natural language
def _level_label(score: int) -> str:
    return {1: "very limited", 2: "limited", 3: "moderate", 4: "strong", 5: "very strong"}.get(score, "moderate")

def _experience_label(score: int) -> str:
    return {1: "no", 2: "1-2 years", 3: "3-5 years", 4: "6-10 years", 5: "10+ years"}.get(score, "some")

def _domain_label(score: int) -> str:
    return {1: "general business", 2: "marketing and strategy", 3: "finance and accounting", 4: "technology and analytics", 5: "quantitative research"}.get(score, "business")

def _ambition_label(score: int) -> str:
    return {1: "explore options", 2: "advance in current field", 3: "switch careers", 4: "move into leadership", 5: "pursue research or academia"}.get(score, "advance my career")

def _flexibility_label(score: int) -> str:
    return {1: "full-time intensive", 2: "full-time standard", 3: "either full or part-time", 4: "part-time preferred", 5: "part-time or online only"}.get(score, "flexible")
```

**Step 2: Verify**

```bash
curl -X POST http://localhost:8000/api/recommend/match \
  -H "Content-Type: application/json" \
  -d '{"quantitative": 4, "experience": 3, "leadership": 2, "tech_analytics": 5, "business_domain": 4, "career_ambition": 3, "study_flexibility": 2}'
```
Expected: JSON with `user_scores` and `matches` array (top 3 programmes).

**Step 3: Commit**

```bash
git add backend/app/api/routes/recommend.py
git commit -m "feat: add programme matching endpoint with embedding similarity"
```

---

### Task 10: Frontend API client -- add recommendation endpoints

**Files:**
- Modify: `frontend/src/services/api.js`

**Step 1: Add new API functions**

Add to `frontend/src/services/api.js`:

```javascript
/**
 * Upload and parse a CV (PDF)
 * @param {File} file - PDF file
 * @returns {Promise<{years_experience, industry, education_level, skills, quantitative_background, leadership_experience, raw_text}>}
 */
export async function parseCV(file) {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/recommend/parse-cv', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
}

/**
 * Get programme recommendations based on quiz answers
 * @param {Object} answers - Quiz answers with scores per axis
 * @returns {Promise<{user_scores, matches}>}
 */
export async function getRecommendations(answers) {
  const response = await api.post('/recommend/match', answers);
  return response.data;
}

/**
 * Get a programme's spider chart profile
 * @param {string} programId
 * @returns {Promise<{name, profile_scores}>}
 */
export async function getProgramProfile(programId) {
  const response = await api.get(`/programs/${programId}/profile`);
  return response.data;
}
```

**Step 2: Commit**

```bash
git add frontend/src/services/api.js
git commit -m "feat: add recommendation API client functions"
```

---

### Task 11: Build the SpiderChart component

**Files:**
- Create: `frontend/src/components/Charts/SpiderChart.jsx`
- Create: `frontend/src/components/Charts/index.js`

**Step 1: Create SpiderChart component**

Create `frontend/src/components/Charts/SpiderChart.jsx`:

```jsx
import { Radar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

const AXIS_LABELS = [
  'Quantitative',
  'Experience',
  'Leadership',
  'Tech & Analytics',
  'Business Domain',
  'Career Ambition',
  'Study Flexibility',
];

const AXIS_KEYS = [
  'quantitative',
  'experience',
  'leadership',
  'tech_analytics',
  'business_domain',
  'career_ambition',
  'study_flexibility',
];

/**
 * Spider/Radar chart for user profile and programme comparison.
 *
 * @param {Object} props
 * @param {Object} props.userScores - {quantitative: 1-5, ...} (partial OK, unfilled axes show 0)
 * @param {Array} props.programmeOverlays - [{name, scores: {quantitative: 1-5, ...}}]
 */
export function SpiderChart({ userScores = {}, programmeOverlays = [] }) {
  const userData = AXIS_KEYS.map(k => userScores[k] || 0);

  const datasets = [
    {
      label: 'Your Profile',
      data: userData,
      backgroundColor: 'rgba(224, 25, 50, 0.15)',
      borderColor: '#E01932',
      borderWidth: 2,
      pointBackgroundColor: '#E01932',
      pointRadius: 4,
    },
    ...programmeOverlays.map((prog, i) => {
      const colors = ['#0071BC', '#F79320', '#2D2D2D'];
      const color = colors[i % colors.length];
      return {
        label: prog.name,
        data: AXIS_KEYS.map(k => prog.scores[k] || 0),
        backgroundColor: `${color}15`,
        borderColor: color,
        borderWidth: 2,
        pointBackgroundColor: color,
        pointRadius: 3,
        borderDash: [4, 4],
      };
    }),
  ];

  const data = { labels: AXIS_LABELS, datasets };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    scales: {
      r: {
        min: 0,
        max: 5,
        ticks: {
          stepSize: 1,
          font: { size: 11 },
          backdropColor: 'transparent',
        },
        pointLabels: {
          font: { size: 12, weight: '500' },
          color: '#4A4A4A',
        },
        grid: { color: '#E5E5E5' },
        angleLines: { color: '#E5E5E5' },
      },
    },
    plugins: {
      legend: {
        position: 'bottom',
        labels: { font: { size: 12 }, usePointStyle: true, padding: 16 },
      },
    },
  };

  return <Radar data={data} options={options} />;
}
```

Create `frontend/src/components/Charts/index.js`:
```javascript
export { SpiderChart } from './SpiderChart';
```

**Step 2: Commit**

```bash
git add frontend/src/components/Charts/
git commit -m "feat: add SpiderChart radar component with chart.js"
```

---

### Task 12: Build the Recommendation Wizard page

**Files:**
- Modify: `frontend/src/pages/RecommendPage.jsx`
- Create: `frontend/src/components/Recommend/CVUpload.jsx`
- Create: `frontend/src/components/Recommend/QuizStep.jsx`
- Create: `frontend/src/components/Recommend/Results.jsx`
- Create: `frontend/src/components/Recommend/index.js`

**Step 1: Define quiz questions**

Each question maps to a spider chart axis. Multiple choice, 3-4 options, scored 1-5:

```javascript
const QUIZ_STEPS = [
  {
    axis: 'quantitative',
    question: 'How would you describe your quantitative and analytical skills?',
    options: [
      { label: 'Limited - I prefer qualitative work', value: 1 },
      { label: 'Moderate - I can work with data when needed', value: 3 },
      { label: 'Strong - I enjoy statistics, modelling, and data analysis', value: 4 },
      { label: 'Expert - I have a STEM background or work with data daily', value: 5 },
    ],
  },
  {
    axis: 'experience',
    question: 'How many years of professional work experience do you have?',
    options: [
      { label: 'Fresh graduate or less than 1 year', value: 1 },
      { label: '1-3 years', value: 2 },
      { label: '3-6 years', value: 3 },
      { label: '6-10 years', value: 4 },
      { label: 'More than 10 years', value: 5 },
    ],
  },
  {
    axis: 'leadership',
    question: 'What best describes your leadership or management experience?',
    options: [
      { label: 'No formal leadership roles yet', value: 1 },
      { label: 'Team lead or project lead experience', value: 3 },
      { label: 'Manager overseeing a team or department', value: 4 },
      { label: 'Senior executive or director level', value: 5 },
    ],
  },
  {
    axis: 'tech_analytics',
    question: 'How interested are you in technology, data science, or AI?',
    options: [
      { label: 'Not really my thing', value: 1 },
      { label: 'Somewhat interested', value: 2 },
      { label: 'Very interested - I want to use it in my career', value: 4 },
      { label: 'It is my career - I work in tech/analytics', value: 5 },
    ],
  },
  {
    axis: 'business_domain',
    question: 'Which business area interests you most?',
    options: [
      { label: 'General management and strategy', value: 1 },
      { label: 'Marketing, branding, or consumer insights', value: 2 },
      { label: 'Finance, accounting, or investment', value: 3 },
      { label: 'Data analytics, technology, or operations', value: 4 },
      { label: 'Research or academia', value: 5 },
    ],
  },
  {
    axis: 'career_ambition',
    question: 'What is your primary goal for pursuing a graduate degree?',
    options: [
      { label: 'Explore my options and learn new skills', value: 1 },
      { label: 'Advance in my current field', value: 2 },
      { label: 'Switch to a new career or industry', value: 3 },
      { label: 'Move into senior leadership', value: 4 },
      { label: 'Pursue academic research or a PhD', value: 5 },
    ],
  },
  {
    axis: 'study_flexibility',
    question: 'What is your preferred study mode?',
    options: [
      { label: 'Full-time intensive (12 months or less)', value: 1 },
      { label: 'Full-time standard pace', value: 2 },
      { label: 'Either full-time or part-time', value: 3 },
      { label: 'Part-time - I want to keep working', value: 4 },
    ],
  },
];
```

**Step 2: Build CVUpload component**

`frontend/src/components/Recommend/CVUpload.jsx`:
- Drag-and-drop zone + file picker for PDF
- "Skip" button to go to quiz
- On upload: calls `parseCV()` API, shows loading spinner, returns parsed fields
- Displays extracted info for confirmation before proceeding

**Step 3: Build QuizStep component**

`frontend/src/components/Recommend/QuizStep.jsx`:
- Shows one question at a time with radio button options
- Progress bar at top (step X of 7)
- "Back" and "Next" buttons
- If CV was parsed, pre-selects the closest matching option
- On each answer, updates parent state so SpiderChart can update live

**Step 4: Build Results component**

`frontend/src/components/Recommend/Results.jsx`:
- Shows completed SpiderChart with user profile
- Top 3 programme matches from API, each with:
  - Programme name, degree type, match score
  - Spider chart overlay (user + programme)
  - "Visit NBS Page" button (external link)
  - "Ask Lyon About This" button (Link to `/chat?programme=X`)

**Step 5: Build RecommendPage orchestrator**

`frontend/src/pages/RecommendPage.jsx`:
- Manages wizard state: `step` (0=CV upload, 1-7=quiz, 8=results)
- Manages `answers` object: `{quantitative: N, experience: N, ...}`
- Manages `cvData` from parsed CV
- Layout: TopBar + PortalHeader, two-column on desktop (left=quiz, right=SpiderChart), Footer
- SpiderChart updates live as each quiz answer is given
- On step 8: calls `getRecommendations(answers)` and shows Results

**Step 6: Verify full flow**

1. Visit `/recommend`
2. Skip CV upload
3. Answer all 7 questions, watch spider chart build
4. See top 3 results with overlaid spider charts
5. Click "Ask Lyon" -> navigates to `/chat?programme=X`

**Step 7: Commit**

```bash
git add frontend/src/pages/RecommendPage.jsx frontend/src/components/Recommend/
git commit -m "feat: build recommendation wizard with CV upload, quiz, and spider chart results"
```

---

### Task 13: Restyle the Chat page to NTU design

**Files:**
- Modify: `frontend/src/pages/ChatPage.jsx`
- Modify: `frontend/src/hooks/useChat.js` (update welcome message for Lyon)

**Step 1: Update ChatPage layout**

Wrap the existing chat components with TopBar + PortalHeader + Footer. Remove the old Header. Keep Sidebar but restyle.

```jsx
import { TopBar } from '../components/Layout/TopBar';
import { PortalHeader } from '../components/Layout/PortalHeader';
import { Sidebar } from '../components/Layout/Sidebar';
import { ChatContainer } from '../components/Chat/ChatContainer';
import { useChat } from '../hooks/useChat';
import { useSearchParams } from 'react-router-dom';
import { useEffect } from 'react';

export default function ChatPage() {
  const [searchParams] = useSearchParams();
  const programme = searchParams.get('programme');
  const {
    messages, isLoading, error, messagesEndRef, sendMessage, clearChat,
  } = useChat();

  // If navigated from recommendation with a programme, auto-send a message
  useEffect(() => {
    if (programme && messages.length <= 1) {
      sendMessage(`Tell me more about the ${programme} programme`);
    }
  }, [programme]);

  return (
    <div className="h-screen flex flex-col bg-white">
      <TopBar />
      <PortalHeader />
      <div className="flex-1 flex overflow-hidden">
        <Sidebar onQuestionClick={sendMessage} />
        <main className="flex-1 flex flex-col">
          <ChatContainer
            messages={messages}
            isLoading={isLoading}
            error={error}
            messagesEndRef={messagesEndRef}
            onSendMessage={sendMessage}
            onClearChat={clearChat}
          />
        </main>
      </div>
    </div>
  );
}
```

**Step 2: Update welcome message**

In `frontend/src/hooks/useChat.js`, update the welcome message to Lyon's voice:

```javascript
content: `Hey! Welcome to NBS. I'm Lyon, NTU's resident lion and your degree advisor.

I can help you with:
- **Programme Info**: MBA, MSc, PhD, Executive programmes
- **Admissions**: Requirements, deadlines, how to apply
- **Comparisons**: Compare programmes side by side
- **General Questions**: Rankings, scholarships, campus life

What programme are you eyeing?`,
```

**Step 3: Verify**

- Visit `/chat` -- see Lyon welcome message with NTU header
- Visit `/chat?programme=Nanyang%20MBA` -- auto-sends question about MBA
- Old chat functionality still works

**Step 4: Commit**

```bash
git add frontend/src/pages/ChatPage.jsx frontend/src/hooks/useChat.js
git commit -m "feat: restyle chat page with NTU layout and Lyon welcome message"
```

---

### Task 14: Update CORS and Vite config for Vercel

**Files:**
- Modify: `backend/app/config.py`
- Modify: `frontend/vite.config.js`

**Step 1: Add Vercel domain to CORS**

In `backend/app/config.py`, update default CORS:
```python
cors_origins: str = "http://localhost:5173,http://localhost:3000,https://*.vercel.app"
```

Also update `cors_origins_list` to handle wildcard:
```python
@property
def cors_origins_list(self) -> list[str]:
    """Parse CORS origins from comma-separated string."""
    origins = [origin.strip() for origin in self.cors_origins.split(",")]
    # FastAPI CORS doesn't support wildcards in origins, so we'll handle this at deploy time
    return origins
```

**Step 2: Update Vite for SPA routing**

In `frontend/vite.config.js`, ensure SPA fallback works:
```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
  },
})
```

**Step 3: Commit**

```bash
git add backend/app/config.py frontend/vite.config.js
git commit -m "chore: update CORS and build config for Vercel deployment"
```

---

### Task 15: Set up Vercel deployment

**Files:**
- Create: `vercel.json` (project root)
- Create: `api/index.py` (Vercel serverless entry point for FastAPI)
- Create: `frontend/vercel.json` (SPA rewrite rules)

**Step 1: Create Vercel config for monorepo**

This project has both frontend and backend. For Vercel, the simplest approach:
- Frontend: deploy as the main Vercel project (static build from `frontend/`)
- Backend: deploy as serverless functions via an `api/` directory at root

Create `vercel.json` at project root:
```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/index.py" },
    { "source": "/((?!api/).*)", "destination": "/index.html" }
  ],
  "functions": {
    "api/index.py": {
      "runtime": "python3.11",
      "maxDuration": 60
    }
  }
}
```

Create `api/index.py` (Vercel serverless wrapper for FastAPI):
```python
"""Vercel serverless entry point for the FastAPI backend."""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

from app.main import app
```

Create `requirements.txt` at project root (Vercel reads this for Python deps):
```
# Vercel Python requirements - mirrors backend/requirements.txt
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
langchain>=0.3.0
langchain-openai>=0.2.0
langchain-community>=0.3.0
langgraph>=0.2.0
openai>=1.50.0
supabase>=2.10.0
pydantic>=2.9.0
pydantic-settings>=2.6.0
python-dotenv>=1.0.0
beautifulsoup4>=4.12.0
httpx>=0.28.0
pdfplumber>=0.11.0
aiofiles>=24.1.0
mangum>=0.17.0
```

**Step 2: Set up Vercel project**

Use the Vercel CLI/plugin (already installed):
```bash
cd /mnt/c/dev/AN6001-NBS-Candidate-Portal-Lyon-AI
vercel link
```

Set environment variables on Vercel:
- `OPENAI_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_SERVICE_KEY`

**Step 3: Test local build**

```bash
cd frontend && npm run build
```
Verify `frontend/dist/` is created with `index.html`.

**Step 4: Deploy**

```bash
vercel --prod
```

**Step 5: Verify deployment**

Check the deployed URL:
- `/` shows splash page
- `/chat` shows Lyon
- `/recommend` shows wizard
- `/programmes` shows browser
- `/api/programs/` returns JSON

**Step 6: Commit**

```bash
git add vercel.json api/index.py requirements.txt
git commit -m "feat: add Vercel deployment config (frontend static + backend serverless)"
```

---

### Task 16: Update CLAUDE.md with new project structure

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Update project structure and commands**

Add the new routes, pages, and endpoints to the documentation. Update the deployment section.

**Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md with candidate portal structure"
```

---

## Summary

| Task | What | Files |
|------|------|-------|
| 1 | Install frontend deps | package.json |
| 2 | NTU brand colors in Tailwind | tailwind.config.js |
| 3 | React Router + 4 routes | App.jsx, main.jsx, pages/* |
| 4 | Splash page | SplashPage.jsx, TopBar, PortalHeader, Footer |
| 5 | Programme browser | ProgrammesPage.jsx |
| 6 | DB migration: profile_scores | SQL + seed script |
| 7 | Backend: profile endpoint | programs.py |
| 8 | Backend: CV parsing | recommend.py, main.py |
| 9 | Backend: matching | recommend.py |
| 10 | Frontend API client | api.js |
| 11 | SpiderChart component | Charts/SpiderChart.jsx |
| 12 | Recommendation wizard | RecommendPage.jsx, Recommend/* |
| 13 | Restyle chat page | ChatPage.jsx, useChat.js |
| 14 | CORS + Vite config | config.py, vite.config.js |
| 15 | Vercel deployment | vercel.json, api/index.py |
| 16 | Update docs | CLAUDE.md |

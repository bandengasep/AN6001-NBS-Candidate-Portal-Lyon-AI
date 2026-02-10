# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **AN6001 AI and Big Data Group Project** implementing an **NBS Degree Advisor Chatbot** with **Agentic AI** capabilities. The project demonstrates RAG (Retrieval-Augmented Generation), agentic tool use, and conversational AI in an educational context.

**Current Implementation**: NBS Candidate Portal - A multi-page web application with AI-powered programme recommendations, a chatbot advisor (Lyon), and a programme browser.

**Original Project Concept** (for reference): The initial guideline proposed a banking web application, but the current implementation focuses on the NBS degree advisor as a practical demonstration of agentic AI capabilities.

**Key Features Implemented**:
- Multi-page Candidate Portal (Splash, Recommend, Chat, Programmes)
- Programme Recommendation Wizard (CV upload + 7-question quiz + spider chart)
- RAG-powered chatbot (Lyon) for NBS programme information
- Agentic AI with tool use (search, compare, FAQ)
- Spider chart profile matching via hybrid scoring (profile + semantic similarity)
- Programme browser with filter tabs
- Vector similarity search using Supabase pgvector
- Conversation history and context management
- Programme comparison capabilities
- Modern responsive UI with NTU branding

## Technology Stack (Current Implementation)

**Frontend**: React 18 + Vite + Tailwind CSS + react-router-dom + chart.js
**Backend**: FastAPI (Python 3.11+)
**Database**: Supabase (PostgreSQL + pgvector extension)
**Vector Store**: Supabase pgvector for RAG
**AI Models**:
- GPT-5.2 for conversational AI and CV parsing
- text-embedding-3-small (1536 dimensions) for embeddings
**Agent Framework**: LangChain for agentic capabilities
**Deployment**: Vercel (static frontend + serverless Python backend)

## Project Structure (Current)

```
/api              - Vercel serverless entry point
/backend          - FastAPI application with LangChain agents
  /app
    /api/routes   - REST API endpoints (chat, programs, recommend)
    /agents       - LangChain agent and tools (RAG, compare, FAQ)
    /rag          - RAG pipeline (embeddings, retriever, ingestion)
    /db           - Supabase client and utilities
  /data/scraped   - Scraped NBS program data
/frontend         - React + Vite application
  /src
    /pages        - Route pages (SplashPage, RecommendPage, ChatPage, ProgrammesPage)
    /components
      /Chat       - Chat UI components
      /Charts     - SpiderChart radar component
      /Layout     - TopBar, PortalHeader, Header, Sidebar, Footer
      /Recommend  - CVUpload, QuizStep, Results
    /hooks        - Custom React hooks (useChat)
    /services     - API client (chat, programs, recommend)
/scripts          - Utility scripts (scraping, ingestion, DB setup, seeding)
/data/scraped     - Primary scraped content (all_programs.json)
/docs/plans       - Design docs and implementation plans
/docs/prototypes  - HTML prototypes
```

## Frontend Routes

| Route | Page | Description |
|-------|------|-------------|
| `/` | SplashPage | Landing page with hero, programme grid, Lyon teaser |
| `/recommend` | RecommendPage | CV upload + 7-question quiz + spider chart results |
| `/chat` | ChatPage | Lyon chatbot (supports `?programme=X` query param) |
| `/programmes` | ProgrammesPage | Programme browser with filter tabs |

## Backend API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/programs/` | List all programmes |
| GET | `/api/programs/{id}` | Get programme by ID |
| GET | `/api/programs/{id}/profile` | Get spider chart profile scores |
| GET | `/api/programs/type/{type}` | Filter programmes by degree type |
| POST | `/api/chat/` | Send chat message to Lyon |
| POST | `/api/chat/handoff` | Submit advisor hand-off request (demo) |
| GET | `/api/chat/history/{id}` | Get conversation history |
| POST | `/api/recommend/parse-cv` | Upload + parse PDF CV |
| POST | `/api/recommend/match` | Match quiz answers to programmes |
| GET | `/health` | Health check |

## Development Commands

See `/memory/MEMORY.md` for environment setup, deployment gotchas, and operational lessons.

**Python Environment:**
```bash
"/mnt/c/Users/User/anaconda3/envs/nbs-msba/python.exe" <script>.py
```

**Backend (FastAPI)**:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
pytest tests/  # Run tests (when available)
```

**Frontend (React + Vite)**:
```bash
cd frontend
npm install       # Install dependencies
npm run dev       # Development server
npm run build     # Production build
```

**Database & Data Ingestion**:
```bash
# 1. Set up Supabase database (run SQL in Supabase dashboard)
# See: scripts/supabase_setup.sql

# 2. Deep-scrape NBS website (all 22 programmes, sub-pages, PDFs)
"/mnt/c/Users/User/anaconda3/envs/nbs-msba/python.exe" scripts/deep_scrape.py

# 3. Ingest data into vector store (REQUIRED for chatbot to work)
"/mnt/c/Users/User/anaconda3/envs/nbs-msba/python.exe" scripts/ingest_data.py

# Expected output: ~1,400+ document chunks ingested from 22 programmes
```

## Agentic AI Implementation

The NBS Degree Advisor demonstrates **agentic AI capabilities**:

**Implemented Tools**:
1. **search_nbs_knowledge** (`backend/app/agents/tools/rag_tool.py`): RAG retrieval from vector store
2. **compare_programs** (`backend/app/agents/tools/compare.py`): Multi-program comparison
3. **lookup_faq** (`backend/app/agents/tools/faq.py`): Common questions lookup
4. **schedule_advisor_session** (`backend/app/agents/tools/handoff.py`): Hand-off to human advisor (demo)

**Agent Architecture**:
- LangChain agent (`backend/app/agents/nbs_agent.py`) with tool selection
- Multi-step reasoning for complex queries
- Context-aware responses using conversation history
- Autonomous tool selection based on query type

**Configuration**:
- Model call budget: 6 LLM calls per conversation turn (cost control)
- Recursion limit: 25 graph steps (allows multi-tool workflows)
- See `backend/app/config.py` for settings

## Recent Updates & Improvements

### February 11, 2026 - Hybrid Recommendation Scoring
- **Hybrid scoring**: Replaced pure embedding similarity with profile similarity (normalized Euclidean distance on 7 spider chart axes) + semantic similarity (rescaled cosine sim), combined with adaptive weights
- **Adaptive weights**: With CV uploaded: 40% profile / 60% semantic. Without CV: 80% profile / 20% semantic
- **Score improvement**: Match scores now reach 60-95% for well-matched programmes (was capped at ~50% due to text domain mismatch)
- **All programmes scored**: Profile similarity computed for all 22 programmes, not just vector search hits

### February 10, 2026 - Lyon Humanization & Advisor Hand-off
- **Conversational responses**: System prompt rewritten with drip-feed pattern (2-4 sentences, offer to elaborate) -- no more information dumps
- **GPT-5.2 verbosity**: `text.verbosity: "low"` parameter constrains token budget at API level for concise responses
- **Minimal formatting**: ReactMarkdown restricted to bold/links only; bullet points, headers, and code blocks stripped
- **Paragraph breaks**: Explicit prompt instruction + Responses API content block handling ensures readable line breaks
- **Advisor hand-off (demo)**: `schedule_advisor_session` tool triggers inline HandoffCard form in chat (name, email, topic)
- **Hand-off triggers**: Lyon proactively offers hand-off for knowledge gaps; users can request directly ("talk to a real advisor")

### February 9, 2026 - Reliability Fixes
- **Agent recursion limit fix**: Separated LangGraph execution steps (recursion_limit=25) from LLM call budget (ModelCallLimitMiddleware, run_limit=6). Enables multi-tool workflows without hitting limits
- **Python version pinning**: Added `.python-version` with `3.12` to prevent Vercel upgrade surprises
- **Timeout removal**: Removed aggressive 8s asyncio.timeout that was failing all chat responses
- **Prompt hardening**: Added topic fencing, off-topic rejection, and anti-injection rules to Lyon

### February 9, 2026 - Data Enrichment
- **Deep scraper**: `scripts/deep_scrape.py` crawls all 22 programmes (landing + sub-pages + PDFs)
- **Vector store expansion**: Re-ingested 1,400+ document chunks (from 36) covering tuition, admissions, deadlines, scholarships, career outcomes
- **pgvector IVFFlat fix**: Applied `probes=10` in `match_documents` SQL function to prevent approximate index from missing high-similarity chunks

### February 8, 2026 - Candidate Portal Launch
- **Multi-page portal**: 4 routes (splash, recommend, chat, programmes)
- **Recommendation wizard**: CV upload (pdfplumber + GPT) + 7-question quiz + spider chart matching
- **Programme browser**: Filter tabs, NTU branding, Lyon integration
- **Vercel deployment**: Live at https://nbs-candidate-portal.vercel.app (FastAPI serves frontend via StaticFiles)

### Key Configuration
- **Environment**: `backend/.env` (API keys - DO NOT commit)
- **Vector DB**: Supabase (PostgreSQL + pgvector), project: `wgaehtbuwqzegrfvbrna`
- **Embedding Model**: text-embedding-3-small (1536 dimensions)
- **Chat Model**: GPT-5.2 (configurable in `backend/app/config.py`)

## Version Control

Use Git for collaborative development:
- Create feature branches for each major feature
- Use descriptive commit messages
- Keep commits atomic and focused
- **CRITICAL**: Never commit `backend/.env` or API keys

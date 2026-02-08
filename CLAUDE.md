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
- Spider chart profile matching via embedding similarity
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
| GET | `/api/chat/history/{id}` | Get conversation history |
| POST | `/api/recommend/parse-cv` | Upload + parse PDF CV |
| POST | `/api/recommend/match` | Match quiz answers to programmes |
| GET | `/health` | Health check |

## Development Commands

Once the project is set up, typical commands will include:

**Python Environment:** Use the nbs-msba conda environment for all Python operations:
```bash
"/mnt/c/Users/User/anaconda3/envs/nbs-msba/python.exe" <script>.py
```

**Backend (FastAPI)**:
```bash
cd backend
"/mnt/c/Users/User/anaconda3/envs/nbs-msba/python.exe" -m uvicorn app.main:app --reload --port 8000

# Or using the conda environment directly:
uvicorn app.main:app --reload --port 8000

# Run tests (if available):
pytest tests/
```

**Frontend (if using Node.js-based tooling)**:
```bash
npm install                      # Install dependencies
npm run dev                      # Development server
npm run build                    # Production build
npm test                         # Run tests
```

### Troubleshooting: Rollup Module Error on Windows

If you encounter this error when running `npm run dev`:
```
Error: Cannot find module @rollup/rollup-win32-x64-msvc
```

This is a known npm bug with optional dependencies. **Solution:**

```cmd
cd frontend
rmdir /s /q node_modules
del package-lock.json
npm cache clean --force
npm install
npm run dev
```

**Important:** Always run `npm install` and `npm run dev` from the same environment (both Windows CMD/PowerShell OR both WSL, not mixed). Platform-specific binaries like rollup require matching environments.

**Database & Data Ingestion**:
```bash
# 1. Set up Supabase database (run SQL in Supabase dashboard)
# See: scripts/supabase_setup.sql

# 2. Scrape NBS website data (optional - sample data included)
"/mnt/c/Users/User/anaconda3/envs/nbs-msba/python.exe" scripts/scrape_nbs.py

# 3. Ingest data into vector store (REQUIRED for chatbot to work)
"/mnt/c/Users/User/anaconda3/envs/nbs-msba/python.exe" scripts/ingest_data.py

# Expected output: ~36 document chunks ingested from 9 programs
```

## Key Project Requirements

**Must-Have Features**:
1. **Customer Support System**: AI chatbot that can transition to human support with feedback collection
2. **Dashboard**: Real-time financial updates, alerts, news, stock prices, account movements
3. **User Authentication**: Secure login/logout functionality
4. **Responsive Design**: Mobile, tablet, and desktop compatibility
5. **AI Integration**: Personalized content generation using appropriate models

**Suggested Features** (from guideline):
- Personalized financial advice
- Interactive financial planning tools
- Digital wallets
- Peer-to-peer lending
- Micro-investment platforms
- Live chat with seamless AI-to-human handoff
- FAQ section

## AI Model Integration Strategy

**For Text/Conversation**:
- Use GPT-based models for chatbot, financial advice, content generation
- Consider Claude for more nuanced financial conversations
- Implement proper prompt engineering for banking context

**For Images**:
- Use DALL-E or Stable Diffusion for marketing materials, personalized visuals
- Consider financial compliance when generating images

**API Integration Considerations**:
- Manage rate limits and costs
- Implement caching for repeated queries
- Handle API failures gracefully
- Keep API keys in environment variables (never commit)

## Agentic AI Implementation

The NBS Degree Advisor demonstrates **agentic AI capabilities**:

**Implemented Tools**:
1. **search_nbs_knowledge** (`backend/app/agents/tools/rag_tool.py`): RAG retrieval from vector store
2. **compare_programs** (`backend/app/agents/tools/compare.py`): Multi-program comparison
3. **lookup_faq** (`backend/app/agents/tools/faq.py`): Common questions lookup

**Agent Architecture**:
- LangChain agent (`backend/app/agents/nbs_agent.py`) with tool selection
- Multi-step reasoning for complex queries
- Context-aware responses using conversation history
- Autonomous tool selection based on query type

## Development Phases

**Phase 1: Setup & Core Infrastructure**
- Set up Flask backend with basic routing
- Implement user authentication
- Set up database with user and transaction schemas
- Create basic frontend structure

**Phase 2: AI Integration**
- Integrate chatbot with GPT/Claude API
- Implement prompt templates for banking scenarios
- Add context management for conversations
- Build AI-to-human handoff logic

**Phase 3: Dashboard & Features**
- Real-time financial data integration
- Alert system for account movements
- Personalized content generation
- Interactive financial tools

**Phase 4: Testing & Refinement**
- User testing sessions
- Performance optimization
- Security hardening
- Documentation completion

## Ethical Considerations

**Critical Requirements**:
- Data privacy compliance (handle sensitive financial data securely)
- Transparent AI usage (users should know when interacting with AI)
- Bias mitigation in financial advice
- Secure storage of user credentials and financial information
- Clear terms of service and privacy policy

## Project Deliverables

1. **Presentation Slides** (10-15 slides): Findings, recommendations, demo
2. **Code Repository**: All programming scripts
3. **Data**: Any datasets used (anonymized)
4. **Documentation**: Setup instructions, API documentation, architecture diagrams

## Research & Literature Review

When implementing features, research:
- Existing fintech AI applications (e.g., Bank of America's Erica, Capital One's Eno)
- Best practices for AI in financial services
- Regulatory requirements for financial applications
- Security standards for banking applications

## Recent Updates & Improvements

### February 8, 2026 - Candidate Portal
- **Multi-page Portal**: Added react-router-dom with 4 routes (splash, recommend, chat, programmes)
- **Splash Page**: NTU-styled landing page with hero section, programme grid, Lyon teaser
- **Recommendation Wizard**: CV upload (pdfplumber + GPT extraction) + 7-question quiz + spider chart
- **Programme Browser**: Full programme listing with filter tabs (All, MBA, MSc, PhD, Executive)
- **Chat Restyle**: Updated chat page with NTU layout, Lyon welcome message, `?programme=X` deep linking
- **Spider Chart**: chart.js radar component for profile comparison
- **Backend Endpoints**: CV parsing (`/recommend/parse-cv`), matching (`/recommend/match`), profile scores (`/programs/{id}/profile`)
- **Database**: Added `profile_scores` jsonb column to programs table
- **Vercel Deployment**: Config for static frontend + serverless Python backend
- **NTU Brand Colors**: Updated Tailwind config with full NTU color palette

### February 1, 2026
1. **Fixed Admissions Link** (`frontend/src/components/Layout/Header.jsx:31`)
   - Updated to: `https://www.ntu.edu.sg/business/admissions`

2. **Fixed Empty/Generic Chatbot Responses**
   - **Root Cause**: Database was not populated with program data
   - **Solution**:
     - Ran data ingestion script: 36 document chunks ingested
     - Updated `backend/app/rag/ingestion.py` to process "sections" field
     - Lowered similarity threshold from 0.7 → 0.5 in `backend/app/rag/retriever.py`
   - **Result**: Chatbot now returns detailed, relevant answers

### Key Configuration Files
- **Environment**: `backend/.env` (contains API keys - DO NOT commit)
- **Vector DB**: Supabase with pgvector extension
- **Embedding Model**: text-embedding-3-small (1536 dimensions)
- **Chat Model**: GPT-5.2 (configurable in `backend/app/config.py`)

## Version Control

Use Git for collaborative development:
- Create feature branches for each major feature
- Use descriptive commit messages
- Keep commits atomic and focused
- **CRITICAL**: Never commit `backend/.env` or API keys

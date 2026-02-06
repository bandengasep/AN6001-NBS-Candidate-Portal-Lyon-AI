# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **AN6001 AI and Big Data Group Project** implementing an **NBS Degree Advisor Chatbot** with **Agentic AI** capabilities. The project demonstrates RAG (Retrieval-Augmented Generation), agentic tool use, and conversational AI in an educational context.

**Current Implementation**: NBS Degree Advisor - An AI-powered chatbot that helps prospective students learn about Nanyang Business School programs using LangChain agents and vector similarity search.

**Original Project Concept** (for reference): The initial guideline proposed a banking web application, but the current implementation focuses on the NBS degree advisor as a practical demonstration of agentic AI capabilities.

**Key Features Implemented**:
- RAG-powered chatbot for NBS program information
- Agentic AI with tool use (search, compare, FAQ)
- Vector similarity search using Supabase pgvector
- Conversation history and context management
- Program comparison capabilities
- Modern responsive UI with NBS branding

## Technology Stack (Current Implementation)

**Frontend**: React 18 + Vite + Tailwind CSS
**Backend**: FastAPI (Python 3.11+)
**Database**: Supabase (PostgreSQL + pgvector extension)
**Vector Store**: Supabase pgvector for RAG
**AI Models**:
- GPT-4o for conversational AI
- text-embedding-3-small (1536 dimensions) for embeddings
**Agent Framework**: LangChain for agentic capabilities

## Project Structure (Current)

```
/backend          - FastAPI application with LangChain agents
  /app
    /api/routes   - REST API endpoints (chat, programs)
    /agents       - LangChain agent and tools (RAG, compare, FAQ)
    /rag          - RAG pipeline (embeddings, retriever, ingestion)
    /db           - Supabase client and utilities
  /data/scraped   - Scraped NBS program data
/frontend         - React + Vite application
  /src
    /components   - React components (Chat, Layout, Messages)
    /hooks        - Custom React hooks (useChat)
    /services     - API client
/scripts          - Utility scripts (scraping, ingestion, DB setup)
/data/scraped     - Primary scraped content (all_programs.json)
```

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
- **Chat Model**: GPT-4o (configurable in `backend/app/config.py`)

## Version Control

Use Git for collaborative development:
- Create feature branches for each major feature
- Use descriptive commit messages
- Keep commits atomic and focused
- **CRITICAL**: Never commit `backend/.env` or API keys

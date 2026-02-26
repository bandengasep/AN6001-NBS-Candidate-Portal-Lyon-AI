# NBS Candidate Portal

An AI-powered candidate portal for Nanyang Business School that demonstrates advanced RAG (Retrieval-Augmented Generation) and agentic AI capabilities. This project showcases practical applications of large language models in educational contexts.

**AN6001 AI and Big Data Group Project** | Nanyang Technological University

**Live at**: https://nbs-candidate-portal.vercel.app

## Overview

The NBS Graduate Candidate Portal is a multi-page web application that helps prospective students explore NBS graduate degree programmes. It features an AI-powered recommendation wizard, a chatbot advisor (Lyon), and a programme browser. Scoped to the 11 programmes managed by the NBS Graduate Studies Office, it uses vector similarity search, LangChain agents, and GPT-5.2 to deliver contextually relevant information through natural conversation.

## Key Features

- **Programme Recommendation Wizard**: Upload your CV + take a branching quiz (experience → track → interest) to get matched programmes with rationale
- **Lyon AI Chatbot**: NTU's lion mascot as your NBS degree advisor, with professional conversational responses, file upload support (PDF/JPG/PNG), and advisor hand-off
- **Programme Browser**: Browse all 11 NBS graduate programmes with filter tabs and direct links
- **Agentic AI Architecture**: Autonomous tool selection and multi-step reasoning using LangChain agents
- **RAG Pipeline**: Retrieval-augmented generation with vector embeddings for accurate, grounded responses
- **Programme Comparison**: Side-by-side analysis of degree options via the chatbot
- **Modern Stack**: FastAPI backend, React frontend, Supabase vector database, Vercel deployment

## Pages

| Route | Page | Description |
|-------|------|-------------|
| `/` | Splash Page | NTU-styled landing page with hero, programme grid, Lyon teaser |
| `/recommend` | Recommendation Wizard | CV upload + branching quiz → matched programmes |
| `/chat` | Lyon Chatbot | AI chatbot with file upload support |
| `/programmes` | Programme Browser | All 11 graduate programmes with filter tabs |

## Architecture

> Full diagram: [`docs/architecture.excalidraw`](docs/architecture.excalidraw) (open with [excalidraw.com](https://excalidraw.com) or VS Code Excalidraw extension)

```
Candidates → Frontend (React + Vite) → Backend (FastAPI) → LangChain Agent
                                                               ├─ RAG Search
                                                               ├─ Compare
                                                               ├─ FAQ Lookup
                                                               └─ Advisor Hand-off
                                                                    │
                                                          ┌────────┴────────┐
                                                          ▼                 ▼
                                                     OpenAI GPT-5.2   Supabase pgvector
```

## Technology Stack

> Full diagram: [`docs/tech-stack.excalidraw`](docs/tech-stack.excalidraw) (open with [excalidraw.com](https://excalidraw.com) or VS Code Excalidraw extension)

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 18 • Vite • Tailwind CSS • React Router |
| **Backend / API** | FastAPI • Python 3.12 • Pydantic |
| **AI & Agents** | LangChain • LangGraph • GPT-5.2 • text-embedding-3-small (1536d) |
| **Database** | Supabase • PostgreSQL • pgvector |
| **Deployment** | Vercel (Serverless Functions) • GitHub |

## Getting Started

**Prerequisites**: Python 3.11+, Node.js 18+, Supabase account, OpenAI API key

See `CLAUDE.md` for detailed setup instructions, environment configuration, and development commands.

**URLs**:
- **Production**: https://nbs-candidate-portal.vercel.app
- **Local Frontend**: `http://localhost:5173`
- **Local Backend**: `http://localhost:8000` (API docs at `/docs`)

## Project Structure

```
├── api/                 Vercel serverless entry point
│   └── index.py         FastAPI app loader
├── backend/             FastAPI application with LangChain agents
│   ├── app/
│   │   ├── agents/      Agent orchestration and tool definitions
│   │   ├── rag/         RAG pipeline (embeddings, retrieval)
│   │   ├── api/routes/  REST API endpoints (chat, programs, recommend)
│   │   └── db/          Database models and utilities
│
├── frontend/            React application
│   └── src/
│       ├── pages/       Route pages (Splash, Recommend, Chat, Programmes)
│       ├── components/  UI components (Chat, Charts, Layout, Recommend)
│       ├── hooks/       Custom React hooks
│       └── services/    API integration (chat, programs, recommend)
│
├── scripts/             Utility scripts
│   ├── deep_scrape.py   Deep web scraping (all sub-pages + PDFs)
│   ├── scrape_nbs.py    Legacy web scraping
│   ├── ingest_data.py   Vector database ingestion
│   └── supabase_setup.sql  Database schema
│
├── data/scraped/        Source programme data
├── static/              Frontend build output (served by FastAPI on Vercel)
└── vercel.json          Vercel deployment configuration
```

## Core Capabilities

**RAG Pipeline**
- ~1,100 vector-embedded chunks from 11 NBS graduate programmes (landing pages, sub-pages)
- Semantic search via Supabase pgvector with tuned IVFFlat index for high recall
- Covers tuition fees, admissions, curriculum, career outcomes, scholarships

**Agentic AI**
- LangChain agent with autonomous tool selection and multi-step reasoning
- Tools: knowledge search, programme comparison, FAQ lookup, advisor hand-off
- Conversational drip-feed responses with GPT-5.2 verbosity control
- Advisor hand-off: inline scheduling form when Lyon can't answer or user requests
- Topic-fenced system prompt with prompt injection protection
- Cost control (6 LLM calls max) + recursion limit (25 steps) for multi-tool workflows

**API Design**
- RESTful endpoints for chat, conversation history, programme data retrieval
- Full OpenAPI documentation at `/docs`

## Use Cases

- **Prospective Students**: Explore programmes via recommendation wizard or chat with Lyon
- **Programme Comparison**: Side-by-side degree analysis
- **CV-Based Matching**: Upload CV for personalised recommendations
- **Educational Demo**: RAG, agentic AI, and embedding-based matching showcase

## Academic Context

This project was developed as part of the AN6001 AI and Big Data course at Nanyang Business School, demonstrating practical applications of:
- Large language model integration
- Vector databases and semantic search
- Agentic AI architectures
- Modern full-stack development practices

## License

Educational project for AN6001 course at Nanyang Technological University.

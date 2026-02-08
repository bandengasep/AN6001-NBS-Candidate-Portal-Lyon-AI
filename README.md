# NBS Candidate Portal

An AI-powered candidate portal for Nanyang Business School that demonstrates advanced RAG (Retrieval-Augmented Generation) and agentic AI capabilities. This project showcases practical applications of large language models in educational contexts.

**AN6001 AI and Big Data Group Project** | Nanyang Technological University

**Live at**: https://nbs-candidate-portal.vercel.app

## Overview

The NBS Candidate Portal is a multi-page web application that helps prospective students explore NBS degree programmes. It features an AI-powered recommendation wizard, a chatbot advisor (Lyon), and a programme browser. Using vector similarity search, LangChain agents, and GPT-5.2, it delivers contextually relevant information through natural conversation.

## Key Features

- **Programme Recommendation Wizard**: Upload your CV + answer a 7-question quiz to get personalised programme matches with a spider chart profile comparison
- **Lyon AI Chatbot**: NTU's lion mascot as your NBS degree advisor, with file upload support (PDF/JPG/PNG)
- **Programme Browser**: Browse all 22 NBS programmes with filter tabs and direct links
- **Agentic AI Architecture**: Autonomous tool selection and multi-step reasoning using LangChain agents
- **RAG Pipeline**: Retrieval-augmented generation with vector embeddings for accurate, grounded responses
- **Programme Comparison**: Side-by-side analysis of degree options via the chatbot
- **Modern Stack**: FastAPI backend, React frontend, Supabase vector database, Vercel deployment

## Pages

| Route | Page | Description |
|-------|------|-------------|
| `/` | Splash Page | NTU-styled landing page with hero, programme grid, Lyon teaser |
| `/recommend` | Recommendation Wizard | CV upload + 7-question quiz + spider chart results |
| `/chat` | Lyon Chatbot | AI chatbot with file upload support |
| `/programmes` | Programme Browser | All 22 programmes with filter tabs |

## Architecture

```
┌─────────────────────────────────────┐
│   Frontend (React + Vite + Tailwind)│
│   • Splash Page & Programme Grid    │
│   • Recommendation Wizard           │
│   • Lyon Chatbot (file upload)      │
│   • Programme Browser               │
└────────────┬────────────────────────┘
             │ REST API
             ▼
┌─────────────────────────────────────┐
│   Backend (FastAPI)                 │
│   ┌───────────────────────┐        │
│   │  LangChain Agent      │        │
│   │  • RAG Search Tool    │        │
│   │  • Compare Tool       │        │
│   │  • FAQ Tool           │        │
│   └───────────────────────┘        │
│   ┌───────────────────────┐        │
│   │  Recommendation Engine│        │
│   │  • CV Parser (GPT)    │        │
│   │  • Embedding Matching │        │
│   │  • Spider Chart Scores│        │
│   └───────────────────────┘        │
│             │                      │
│   ┌─────────┴─────────┐           │
│   │  Data Layer       │            │
│   │  • Supabase       │            │
│   │  • OpenAI API     │            │
│   └───────────────────┘            │
└─────────────────────────────────────┘
```

## Technology Stack

**Backend**
- FastAPI for high-performance async API
- LangChain for agentic workflow orchestration
- OpenAI GPT-5.2 for language generation and CV parsing
- text-embedding-3-small for semantic search (1536 dimensions)

**Frontend**
- React 18 with react-router-dom
- Vite for fast development and optimized builds
- Tailwind CSS for responsive UI
- chart.js for spider chart visualisation

**Data Layer**
- Supabase (PostgreSQL + pgvector extension)
- Vector similarity search for RAG retrieval
- Structured programme data with profile scores

**Deployment**
- Vercel (static frontend + serverless Python backend)
- Frontend served from FastAPI via StaticFiles mount

## Getting Started

Detailed setup instructions are available in `CLAUDE.md` for development purposes. At a high level:

1. **Prerequisites**: Python 3.11+, Node.js 18+, Supabase account, OpenAI API key
2. **Environment Setup**: Configure credentials in `backend/.env`
3. **Database Initialization**: Run SQL setup script and ingest program data
4. **Launch Services**: Start FastAPI backend and React frontend

The application runs on:
- **Production**: https://nbs-candidate-portal.vercel.app
- **Local Frontend**: `http://localhost:5173`
- **Local Backend API**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`

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
│   ├── scrape_nbs.py    Web scraping for programme data
│   ├── ingest_data.py   Vector database ingestion
│   └── supabase_setup.sql  Database schema
│
├── data/scraped/        Source programme data
├── static/              Frontend build output (served by FastAPI on Vercel)
└── vercel.json          Vercel deployment configuration
```

## Core Capabilities

### RAG (Retrieval-Augmented Generation)
- Semantic search over NBS program data using vector embeddings
- Context-aware responses grounded in official program information
- Configurable similarity thresholds for retrieval precision

### Agentic AI
- LangChain-based agent with autonomous tool selection
- Multi-step reasoning for complex queries
- Tools: knowledge search, program comparison, FAQ lookup

### API Design
The REST API provides endpoints for chat interaction, conversation history, and program data retrieval. Full API documentation is available via FastAPI's automatic OpenAPI interface.

## Use Cases

- **Prospective Students**: Explore NBS programmes through the recommendation wizard or natural conversation with Lyon
- **Programme Comparison**: Side-by-side analysis of degree options via the chatbot
- **CV-Based Matching**: Upload a CV to get personalised programme recommendations
- **FAQ Automation**: Instant answers to common admissions questions
- **Educational Demo**: Showcase practical applications of RAG, agentic AI, and embedding-based matching

## Development

The project follows a modular architecture with clear separation between frontend, backend, and data layers. See `CLAUDE.md` for detailed development guidelines and setup instructions.

## Academic Context

This project was developed as part of the AN6001 AI and Big Data course at Nanyang Business School, demonstrating practical applications of:
- Large language model integration
- Vector databases and semantic search
- Agentic AI architectures
- Modern full-stack development practices

## License

Educational project for AN6001 course at Nanyang Technological University.

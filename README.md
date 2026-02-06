# NBS Degree Advisor Chatbot

An AI-powered conversational agent for Nanyang Business School that demonstrates advanced RAG (Retrieval-Augmented Generation) and agentic AI capabilities. This project showcases practical applications of large language models in educational contexts.

**AN6001 AI and Big Data Group Project** | Nanyang Technological University

## Overview

This chatbot provides intelligent assistance to prospective students exploring NBS degree programs. Using a combination of vector similarity search, LangChain agents, and GPT-4o, it delivers contextually relevant information through natural conversation.

## Key Features

- **Agentic AI Architecture**: Autonomous tool selection and multi-step reasoning using LangChain agents
- **RAG Pipeline**: Retrieval-augmented generation with vector embeddings for accurate, grounded responses
- **Program Intelligence**: Compare degree programs, answer FAQs, and provide detailed program information
- **Conversation Management**: Stateful dialogue with context preservation across sessions
- **Modern Stack**: FastAPI backend, React frontend, Supabase vector database

## Architecture

```
┌─────────────────────────────────┐
│   Frontend (React + Vite)       │
│   • Chat Interface              │
│   • Program Explorer            │
└────────────┬────────────────────┘
             │ REST API
             ▼
┌─────────────────────────────────┐
│   Backend (FastAPI)             │
│   ┌───────────────────────┐     │
│   │  LangChain Agent      │     │
│   │  • RAG Tool           │     │
│   │  • Compare Tool       │     │
│   │  • FAQ Tool           │     │
│   └───────────────────────┘     │
│             │                   │
│   ┌─────────┴─────────┐         │
│   │  Data Layer       │         │
│   │  • Supabase       │         │
│   │  • OpenAI API     │         │
│   └───────────────────┘         │
└─────────────────────────────────┘
```

## Technology Stack

**Backend**
- FastAPI for high-performance async API
- LangChain for agentic workflow orchestration
- OpenAI GPT-4o for language generation
- text-embedding-3-small for semantic search (1536 dimensions)

**Frontend**
- React 18 with modern hooks
- Vite for fast development and optimized builds
- Tailwind CSS for responsive UI

**Data Layer**
- Supabase (PostgreSQL + pgvector extension)
- Vector similarity search for RAG retrieval
- Structured program data storage

## Getting Started

Detailed setup instructions are available in `CLAUDE.md` for development purposes. At a high level:

1. **Prerequisites**: Python 3.11+, Node.js 18+, Supabase account, OpenAI API key
2. **Environment Setup**: Configure credentials in `backend/.env`
3. **Database Initialization**: Run SQL setup script and ingest program data
4. **Launch Services**: Start FastAPI backend and React frontend

The application runs on:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`

## Project Structure

```
├── backend/              FastAPI application with LangChain agents
│   ├── app/
│   │   ├── agents/      Agent orchestration and tool definitions
│   │   ├── rag/         RAG pipeline (embeddings, retrieval)
│   │   ├── api/routes/  REST API endpoints
│   │   └── db/          Database models and utilities
│
├── frontend/            React application
│   └── src/
│       ├── components/  UI components
│       ├── hooks/       Custom React hooks
│       └── services/    API integration
│
├── scripts/             Utility scripts
│   ├── scrape_nbs.py   Web scraping for program data
│   ├── ingest_data.py  Vector database ingestion
│   └── supabase_setup.sql  Database schema
│
└── data/scraped/        Source program data
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

- **Prospective Students**: Explore NBS programs through natural conversation
- **Program Comparison**: Side-by-side analysis of degree options
- **FAQ Automation**: Instant answers to common admissions questions
- **Educational Demo**: Showcase practical applications of RAG and agentic AI

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

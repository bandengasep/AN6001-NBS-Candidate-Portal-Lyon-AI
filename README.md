# NBS Degree Advisor Chatbot

AI-powered chatbot for Nanyang Business School that provides information about degree programs using RAG (Retrieval-Augmented Generation) and agentic AI capabilities.

**AN6001 AI and Big Data Group Project** | Nanyang Technological University

## Features

- **AI-Powered Chat**: Conversational interface powered by GPT-4o
- **RAG (Retrieval-Augmented Generation)**: Answers grounded in NBS program data
- **Program Comparison**: Compare different NBS programs
- **FAQ Support**: Quick answers to common questions
- **Conversation History**: Maintains context across messages
- **Modern UI**: Responsive React frontend with NBS branding

## Architecture

```
Frontend (React + Vite + Tailwind)
         │
         │ REST API
         ▼
Backend (FastAPI)
         │
         ├── LangChain Agent
         │   ├── RAG Tool (search knowledge base)
         │   ├── Compare Tool (compare programs)
         │   └── FAQ Tool (common questions)
         │
         └── Data Layer
             ├── Supabase (pgvector for RAG)
             └── OpenAI API (GPT-4o, embeddings)
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- Supabase account
- OpenAI API key

## Setup

### 1. Clone and Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 2. Set Up Supabase

1. Create a new Supabase project
2. Run the SQL setup script in `scripts/supabase_setup.sql`
3. Get your project URL and keys from Settings > API

### 3. Configure Environment

```bash
# Copy example env file
cp backend/.env.example backend/.env

# Edit .env with your credentials
OPENAI_API_KEY=sk-...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...
```

### 4. Ingest Data

**CRITICAL STEP**: The chatbot requires data to be ingested into the vector store to function properly.

```bash
# Use the nbs-msba conda environment for Python operations
# Scrape NBS website (optional - sample data already included in data/scraped/)
"/mnt/c/Users/User/anaconda3/envs/nbs-msba/python.exe" scripts/scrape_nbs.py

# Ingest data into vector store (REQUIRED)
"/mnt/c/Users/User/anaconda3/envs/nbs-msba/python.exe" scripts/ingest_data.py
```

**Expected Output**:
```
Starting data ingestion...
==================================================
Ingesting Nanyang MBA...
  -> Ingested 4 document chunks
...
==================================================
Ingestion complete! Total documents: 36
```

If you see errors or 0 documents ingested, check:
- Supabase credentials in `backend/.env`
- OpenAI API key is valid
- `data/scraped/all_programs.json` exists

### 5. Run the Application

```bash
# Terminal 1: Start backend (using conda environment)
cd backend
"/mnt/c/Users/User/anaconda3/envs/nbs-msba/python.exe" -m uvicorn app.main:app --reload --port 8000

# Or if conda environment is activated:
uvicorn app.main:app --reload --port 8000

# Terminal 2: Start frontend
cd frontend
npm run dev
```

Visit **http://localhost:5173** to use the chatbot.

Backend API docs: **http://localhost:8000/docs**

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/chat/` | POST | Send chat message |
| `/api/chat/history/{id}` | GET | Get conversation history |
| `/api/programs/` | GET | List all programs |
| `/api/programs/{id}` | GET | Get program by ID |
| `/api/programs/type/{type}` | GET | Get programs by type |

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Configuration
│   │   ├── api/routes/          # API endpoints
│   │   ├── agents/              # LangChain agent
│   │   ├── rag/                 # RAG pipeline
│   │   └── db/                  # Database models
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── hooks/               # Custom hooks
│   │   └── services/            # API client
│   └── package.json
│
├── scripts/
│   ├── scrape_nbs.py           # Web scraper
│   ├── ingest_data.py          # Data ingestion
│   └── supabase_setup.sql      # Database setup
│
└── data/scraped/               # Scraped content
```

## Technologies

- **Backend**: FastAPI, LangChain, OpenAI
- **Frontend**: React 18, Vite, Tailwind CSS
- **Database**: Supabase (PostgreSQL + pgvector)
- **AI**: GPT-4o, text-embedding-3-small

## Development

### Backend Development

```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Troubleshooting: Rollup Module Error (Windows)

If you see `Error: Cannot find module @rollup/rollup-win32-x64-msvc`:

```cmd
cd frontend
rmdir /s /q node_modules
del package-lock.json
npm cache clean --force
npm install
npm run dev
```

**Note:** Run all npm commands from the same environment (Windows CMD or WSL, not mixed).

### Testing the API

```bash
# Health check
curl http://localhost:8000/health

# Send chat message
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What MBA programs does NBS offer?"}'
```

## Recent Updates

### February 1, 2026

**Fixed Empty/Generic Chatbot Responses**:
- ✅ Ingested 36 document chunks from 9 NBS programs into vector database
- ✅ Enhanced `backend/app/rag/ingestion.py` to process program "sections" field
- ✅ Lowered similarity threshold from 0.7 → 0.5 for better retrieval
- ✅ Updated admissions link to `https://www.ntu.edu.sg/business/admissions`

**How the Fix Works**:
1. The chatbot uses RAG (Retrieval-Augmented Generation) to find relevant program information
2. Previously, the vector database was empty, causing generic "I can't answer" responses
3. After running `scripts/ingest_data.py`, 36 document chunks are now searchable
4. The lowered threshold allows more relevant results to be retrieved

## Troubleshooting

### Chatbot Returns Generic Answers

**Symptom**: Chatbot says "I'm sorry I can't answer" or gives vague responses

**Solution**:
1. Check if data has been ingested: Run `scripts/ingest_data.py`
2. Verify Supabase connection: Check `backend/.env` credentials
3. Restart backend server after ingestion

### Empty Search Results

**Cause**: Similarity threshold too high or no matching documents

**Fix**: Threshold is now 0.5 (was 0.7) in `backend/app/rag/retriever.py:11`

## License

This project is for educational purposes as part of the AN6001 course at Nanyang Business School.

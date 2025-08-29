# Marketing Content Generator

AI-powered marketing content generator with FastAPI backend and React frontend.

## Features

- **Backend**: FastAPI with LangGraph multi-agent workflow
- **Frontend**: React + TypeScript + Tailwind CSS
- **AI Integration**: OpenAI GPT-4o-mini for content generation
- **File Processing**: CSV and PDF upload support
- **Sentiment Analysis**: Built-in content sentiment analysis
- **Marketing Trends**: Current marketing trends integration

## Quick Start

### Backend
```bash
cd backend
source venv/bin/activate
python run.py
```

### Frontend
```bash
cd contentgen-ai
npm install --legacy-peer-deps
npm run dev
```

## API Endpoints

- `POST /api/v1/content/generate` - Generate marketing content
- `GET /api/v1/trends` - Get marketing trends
- `POST /api/v1/analysis` - Analyze content sentiment

## Tech Stack

- **Backend**: FastAPI, Python 3.10+, LangGraph, LangChain
- **Frontend**: React 19, TypeScript, Tailwind CSS, shadcn/ui
- **AI**: OpenAI GPT-4o-mini
- **Database**: In-memory (LangGraph checkpoints)

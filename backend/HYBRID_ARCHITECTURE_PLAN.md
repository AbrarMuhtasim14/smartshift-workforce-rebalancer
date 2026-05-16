# SmartShift Hybrid Architecture Plan
## Python Backend (FastAPI) + Next.js Frontend

---

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│              Next.js Frontend (Vercel)                   │
│  - React UI Components                                   │
│  - Tailwind CSS Styling                                  │
│  - API Client (fetch/axios)                              │
│  - Deployed on Vercel (Free Tier)                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTP/REST API
                     │ (CORS enabled)
                     │
┌────────────────────▼────────────────────────────────────┐
│         Python FastAPI Backend (Railway/Render)          │
│  ┌────────────────────────────────────────────────┐     │
│  │  FastAPI Routes                                 │     │
│  │  - GET  /api/workers                            │     │
│  │  - POST /api/search                             │     │
│  │  - POST /api/recommendations                    │     │
│  └────────────────────────────────────────────────┘     │
│                     │                                    │
│  ┌────────────────────────────────────────────────┐     │
│  │  Existing Python Logic (Keep 90% of code!)     │     │
│  │  - CrewAI Agents (agents.py)                    │     │
│  │  - OpenRouter LLM (config.py - updated)        │     │
│  │  - ChromaDB Vector Store (vector_store.py)     │     │
│  │  - Data Loader (data_loader.py)                │     │
│  │  - Tools (tools.py)                             │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  Deployed on Railway/Render (Free Tier)                 │
└──────────────────────────────────────────────────────────┘
```

---

## 📋 What Changes vs What Stays

### ✅ Files That Stay (Minimal/No Changes)
- ✅ [`agents.py`](agents.py:1) - Keep as is
- ✅ [`tasks.py`](tasks.py:1) - Keep as is
- ✅ [`tools.py`](tools.py:1) - Keep as is
- ✅ [`vector_store.py`](vector_store.py:1) - Keep as is
- ✅ [`data_loader.py`](data_loader.py:1) - Keep as is
- ✅ [`workers.csv`](workers.csv:1) - Keep as is
- ✅ [`requirements.txt`](requirements.txt:1) - Add FastAPI dependencies

### 🔄 Files That Need Updates
- 🔄 [`config.py`](config.py:1) - Update LLM to use OpenRouter
- 🔄 [`app.py`](app.py:1) - Convert from Streamlit to FastAPI
- 🔄 [`.env`](.env:1) - Update environment variables

### ➕ New Files to Create
- ➕ `api.py` - FastAPI application (or rename app.py)
- ➕ `frontend/` - Next.js project directory
- ➕ `Procfile` - For Railway/Render deployment
- ➕ `railway.json` or `render.yaml` - Deployment config

---

## 🔧 Implementation Steps

### Phase 1: Update Python Backend (30-60 minutes)

#### Step 1.1: Update config.py for OpenRouter
```python
# config.py (UPDATED)
import os
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

# OpenRouter Configuration
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "qwen/qwen-2.5-72b-instruct"

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY must be set in .env file")

# Initialize LLM with OpenRouter
llm = LLM(
    model=MODEL_NAME,
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
    max_tokens=2000,
    temperature=0.7
)

# ChromaDB Configuration (unchanged)
CHROMA_PERSIST_DIR = "./chroma_store"
CHROMA_COLLECTION_NAME = "warehouse_workers"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
```

#### Step 1.2: Update .env file
```env
# .env (UPDATED)
# OpenRouter Configuration
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# App Configuration
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
```

#### Step 1.3: Update requirements.txt
```txt
# requirements.txt (ADD THESE)
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6
```

#### Step 1.4: Create FastAPI Backend (api.py)
```python
# api.py (NEW FILE)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from crewai import Crew, Process

from data_loader import load_workers, get_worker_by_id
from tools import initialize_tools
from tasks import create_crew_tasks
from agents import skill_matcher_agent, shift_planner_agent

# Initialize FastAPI
app = FastAPI(title="SmartShift API", version="2.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
workers_df = None
tools_initialized = False

# Pydantic Models
class RecommendationRequest(BaseModel):
    manager_input: str

class SearchRequest(BaseModel):
    query: str
    exclude_zone: Optional[str] = None

# Startup event
@app.on_event("startup")
async def startup_event():
    global workers_df, tools_initialized
    workers_df = load_workers("workers.csv")
    initialize_tools()
    tools_initialized = True
    print("✅ SmartShift API initialized successfully")

# Health check
@app.get("/")
async def root():
    return {
        "message": "SmartShift API",
        "status": "running",
        "version": "2.0"
    }

# Get all workers
@app.get("/api/workers")
async def get_workers():
    if workers_df is None:
        raise HTTPException(status_code=500, detail="Workers data not loaded")
    return workers_df.to_dict(orient="records")

# Get worker by ID
@app.get("/api/workers/{worker_id}")
async def get_worker(worker_id: str):
    if workers_df is None:
        raise HTTPException(status_code=500, detail="Workers data not loaded")
    
    worker = get_worker_by_id(workers_df, worker_id)
    if worker is None:
        raise HTTPException(status_code=404, detail=f"Worker {worker_id} not found")
    
    return worker

# Get zone statistics
@app.get("/api/zones/{zone}")
async def get_zone_stats(zone: str):
    if workers_df is None:
        raise HTTPException(status_code=500, detail="Workers data not loaded")
    
    zone_workers = workers_df[workers_df['current_zone'] == zone]
    
    if zone_workers.empty:
        raise HTTPException(status_code=404, detail=f"No workers found in {zone}")
    
    stats = {
        "zone": zone,
        "total_workers": len(zone_workers),
        "available_workers": len(zone_workers[zone_workers['available'] == 'Yes']),
        "unavailable_workers": len(zone_workers[zone_workers['available'] == 'No']),
        "load_distribution": {
            "low": len(zone_workers[zone_workers['load_status'] == 'Low']),
            "medium": len(zone_workers[zone_workers['load_status'] == 'Medium']),
            "high": len(zone_workers[zone_workers['load_status'] == 'High'])
        },
        "average_load_percentage": float(zone_workers['load_percentage'].mean())
    }
    
    return stats

# Search workers
@app.post("/api/search")
async def search_workers(request: SearchRequest):
    if not tools_initialized:
        raise HTTPException(status_code=500, detail="Tools not initialized")
    
    from tools import search_workers_tool
    
    result = search_workers_tool(
        query=request.query,
        exclude_zone=request.exclude_zone
    )
    
    return {"result": result}

# Get AI recommendations
@app.post("/api/recommendations")
async def get_recommendations(request: RecommendationRequest):
    if not tools_initialized:
        raise HTTPException(status_code=500, detail="Tools not initialized")
    
    try:
        # Create tasks
        tasks = create_crew_tasks(request.manager_input)
        
        # Create crew
        crew = Crew(
            agents=[skill_matcher_agent, shift_planner_agent],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Execute crew
        result = crew.kickoff()
        
        return {
            "status": "success",
            "recommendations": str(result),
            "input": request.manager_input
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

### Phase 2: Create Next.js Frontend (2-3 hours)

#### Step 2.1: Create Next.js Project
```bash
# In your Desktop or preferred location
cd ~/Desktop
npx create-next-app@latest smartshift-frontend --typescript --tailwind --app --eslint
cd smartshift-frontend
```

#### Step 2.2: Install Dependencies
```bash
npm install axios date-fns
npm install -D @types/node
```

#### Step 2.3: Create Environment Variables
```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Step 2.4: Create API Client
```typescript
// lib/api.ts
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Worker {
  worker_id: string;
  name: string;
  age: number;
  primary_skill: string;
  transferable_skills: string;
  education: string;
  physicality: string;
  current_zone: string;
  zone_function: string;
  shift: string;
  shift_hours: string;
  load_status: string;
  load_percentage: number;
  available: string;
}

export const workersApi = {
  getAll: () => api.get<Worker[]>('/api/workers'),
  getById: (id: string) => api.get<Worker>(`/api/workers/${id}`),
  getZoneStats: (zone: string) => api.get(`/api/zones/${zone}`),
  search: (query: string, excludeZone?: string) => 
    api.post('/api/search', { query, exclude_zone: excludeZone }),
  getRecommendations: (managerInput: string) => 
    api.post('/api/recommendations', { manager_input: managerInput }),
};
```

#### Step 2.5: Create Main Dashboard Page
```typescript
// app/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { workersApi, Worker } from '@/lib/api';
import WorkforceOverview from '@/components/WorkforceOverview';
import WorkerTable from '@/components/WorkerTable';
import OverloadForm from '@/components/OverloadForm';
import RecommendationDisplay from '@/components/RecommendationDisplay';

export default function Home() {
  const [workers, setWorkers] = useState<Worker[]>([]);
  const [loading, setLoading] = useState(true);
  const [recommendations, setRecommendations] = useState<string | null>(null);

  useEffect(() => {
    loadWorkers();
  }, []);

  const loadWorkers = async () => {
    try {
      const response = await workersApi.getAll();
      setWorkers(response.data);
    } catch (error) {
      console.error('Error loading workers:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGetRecommendations = async (input: string) => {
    try {
      setLoading(true);
      const response = await workersApi.getRecommendations(input);
      setRecommendations(response.data.recommendations);
    } catch (error) {
      console.error('Error getting recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Loading SmartShift...</div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-2">🏭 SmartShift</h1>
        <p className="text-gray-600 mb-8">AI-Powered Warehouse Workforce Rebalancing</p>
        
        <WorkforceOverview workers={workers} />
        
        <div className="mt-8">
          <WorkerTable workers={workers} />
        </div>
        
        <div className="mt-8">
          <OverloadForm onSubmit={handleGetRecommendations} loading={loading} />
        </div>
        
        {recommendations && (
          <div className="mt-8">
            <RecommendationDisplay recommendations={recommendations} />
          </div>
        )}
      </div>
    </main>
  );
}
```

---

### Phase 3: Deployment

#### Backend Deployment (Railway - Recommended)

1. **Create Railway Account**: https://railway.app
2. **Create New Project**: "New Project" → "Deploy from GitHub"
3. **Add Environment Variables**:
   ```
   OPENROUTER_API_KEY=your-key
   PORT=8000
   ```
4. **Create Procfile**:
   ```
   web: uvicorn api:app --host 0.0.0.0 --port $PORT
   ```
5. **Deploy**: Railway auto-deploys on git push

#### Frontend Deployment (Vercel)

1. **Push to GitHub**: Commit and push your Next.js project
2. **Import to Vercel**: https://vercel.com/new
3. **Add Environment Variable**:
   ```
   NEXT_PUBLIC_API_URL=https://your-railway-app.railway.app
   ```
4. **Deploy**: Vercel auto-deploys

---

## 📊 Comparison: Before vs After

| Aspect | Before | After |
|--------|--------|-------|
| **LLM** | IBM Watson/Granite | OpenRouter (Qwen 3.6-27B) |
| **Frontend** | Streamlit (Python) | Next.js (React/TypeScript) |
| **Backend** | Streamlit | FastAPI (Python) |
| **Agents** | CrewAI ✅ | CrewAI ✅ (kept!) |
| **Vector Store** | ChromaDB ✅ | ChromaDB ✅ (kept!) |
| **Data** | CSV ✅ | CSV ✅ (kept!) |
| **Deployment** | Local only | Railway + Vercel |
| **Code Reuse** | - | 90% of Python code kept! |

---

## 💰 Cost Estimate

- **OpenRouter**: $5-20/month (pay per use)
- **Railway**: Free tier (500 hours/month)
- **Vercel**: Free tier (hobby projects)
- **Total**: $5-20/month

---

## ✅ Benefits of This Approach

1. **Keep 90% of existing code** - Only update config and add API layer
2. **Keep CrewAI** - No need to learn LangChain.js
3. **Keep ChromaDB** - No need to migrate to Pinecone
4. **Modern UI** - Professional React interface
5. **Scalable** - Separate frontend/backend can scale independently
6. **Free deployment** - Both Railway and Vercel have free tiers

---

## 🚀 Quick Start Commands

### Backend
```bash
# Update config.py and create api.py
# Install new dependencies
pip install fastapi uvicorn python-multipart

# Run locally
uvicorn api:app --reload --port 8000
```

### Frontend
```bash
# Create Next.js project
npx create-next-app@latest smartshift-frontend --typescript --tailwind --app

# Install dependencies
cd smartshift-frontend
npm install axios date-fns

# Run locally
npm run dev
```

### Test Full Stack
1. Start backend: `uvicorn api:app --reload` (port 8000)
2. Start frontend: `npm run dev` (port 3000)
3. Open http://localhost:3000

---

## 📝 Next Steps

1. ✅ Update [`config.py`](config.py:1) with OpenRouter
2. ✅ Create `api.py` with FastAPI routes
3. ✅ Test backend API endpoints
4. ✅ Create Next.js frontend
5. ✅ Build React components
6. ✅ Test full stack locally
7. ✅ Deploy backend to Railway
8. ✅ Deploy frontend to Vercel

**Ready to implement? Switch to Code mode!**
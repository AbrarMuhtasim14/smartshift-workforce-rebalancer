# SmartShift Migration Plan
## From Streamlit + IBM Watson → Next.js + OpenRouter (Qwen 3.6-27B)

---

## 📋 Overview

This document outlines the complete migration strategy for SmartShift from:
- **Current Stack**: Streamlit UI + IBM Watson/Granite LLM + Python backend
- **Target Stack**: Next.js (React) + OpenRouter (Qwen 3.6-27B) + Vercel deployment

---

## 🎯 Migration Goals

1. Replace IBM Watson with OpenRouter's Qwen 3.6-27B model
2. Convert Streamlit UI to Next.js React application
3. Migrate Python backend to Next.js API routes
4. Deploy to Vercel instead of running locally
5. Maintain all existing functionality (AI agents, vector search, worker management)

---

## 🏗️ Architecture Comparison

### Current Architecture (Streamlit)
```
┌─────────────────────────────────────┐
│     Streamlit Frontend (Python)     │
│  - app.py (316 lines)               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Python Backend                  │
│  - CrewAI Agents                    │
│  - IBM Watson/Granite LLM           │
│  - ChromaDB Vector Store            │
│  - Pandas Data Processing           │
└─────────────────────────────────────┘
```

### Target Architecture (Next.js + Vercel)
```
┌─────────────────────────────────────┐
│   Next.js Frontend (React/TSX)      │
│  - React Components                 │
│  - Tailwind CSS Styling             │
│  - Client-side State Management     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Next.js API Routes (Serverless)   │
│  - /api/workers (GET, POST)         │
│  - /api/search (POST)               │
│  - /api/recommendations (POST)      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Backend Services                │
│  - LangChain.js (Agent framework)   │
│  - OpenRouter API (Qwen 3.6-27B)    │
│  - Vector Store (Pinecone/Supabase) │
│  - CSV Data Processing              │
└─────────────────────────────────────┘
```

---

## 🔄 Key Changes Required

### 1. LLM Provider Migration
**From**: IBM Watson/Granite
```python
# config.py (OLD)
from crewai import LLM
llm = LLM(
    model="watsonx/ibm/granite-13b-chat-v2",
    base_url="https://eu-de.ml.cloud.ibm.com",
    project_id=WATSONX_PROJECT_ID,
    max_tokens=2000,
    temperature=0.7
)
```

**To**: OpenRouter with Qwen 3.6-27B
```typescript
// lib/llm.ts (NEW)
import { ChatOpenAI } from "@langchain/openai";

export const llm = new ChatOpenAI({
  modelName: "qwen/qwen-2.5-72b-instruct",
  openAIApiKey: process.env.OPENROUTER_API_KEY,
  configuration: {
    baseURL: "https://openrouter.ai/api/v1",
  },
  temperature: 0.7,
  maxTokens: 2000,
});
```

### 2. Vector Store Migration
**Challenge**: ChromaDB is Python-based and doesn't work well in serverless environments.

**Options**:
1. **Pinecone** (Recommended) - Serverless vector database, excellent for Vercel
2. **Supabase pgvector** - PostgreSQL with vector support, free tier available
3. **Upstash Vector** - Redis-based, serverless-friendly
4. **Keep ChromaDB** - Run as separate microservice (more complex)

**Recommendation**: Use **Pinecone** for simplicity and Vercel compatibility.

### 3. Agent Framework Migration
**From**: CrewAI (Python)
```python
# agents.py (OLD)
from crewai import Agent, Crew, Process

skill_matcher_agent = Agent(
    role="Warehouse Skill Search Specialist",
    goal="Search ChromaDB to find workers...",
    tools=[search_workers_tool],
    llm=llm
)
```

**To**: LangChain.js (TypeScript)
```typescript
// lib/agents.ts (NEW)
import { ChatOpenAI } from "@langchain/openai";
import { AgentExecutor, createOpenAIFunctionsAgent } from "langchain/agents";

export const createSkillMatcherAgent = async () => {
  const agent = await createOpenAIFunctionsAgent({
    llm,
    tools: [searchWorkersTool],
    prompt: skillMatcherPrompt,
  });
  
  return new AgentExecutor({
    agent,
    tools: [searchWorkersTool],
  });
};
```

### 4. UI Migration
**From**: Streamlit (Python)
- Automatic UI generation
- Built-in components (st.dataframe, st.button, etc.)
- Session state management

**To**: Next.js + React + Tailwind CSS
- Custom React components
- Manual UI design with Tailwind
- React state management (useState, useContext)

---

## 📦 New Project Structure

```
smartshift-nextjs/
├── app/                          # Next.js 14 App Router
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Home page (dashboard)
│   ├── api/                     # API routes
│   │   ├── workers/
│   │   │   └── route.ts        # GET/POST workers
│   │   ├── search/
│   │   │   └── route.ts        # POST search workers
│   │   └── recommendations/
│   │       └── route.ts        # POST get AI recommendations
│   └── globals.css              # Global styles
│
├── components/                   # React components
│   ├── WorkforceOverview.tsx    # Dashboard overview
│   ├── WorkerTable.tsx          # Worker data table
│   ├── OverloadForm.tsx         # Report overload form
│   ├── RecommendationCard.tsx   # AI recommendation display
│   └── ZoneStatistics.tsx       # Zone stats display
│
├── lib/                         # Utility functions
│   ├── llm.ts                   # OpenRouter LLM setup
│   ├── agents.ts                # LangChain agents
│   ├── vectorStore.ts           # Pinecone integration
│   ├── dataLoader.ts            # CSV data loading
│   └── tools.ts                 # Agent tools
│
├── public/
│   └── workers.csv              # Worker data
│
├── types/
│   └── worker.ts                # TypeScript types
│
├── .env.local                   # Environment variables
├── next.config.js               # Next.js configuration
├── package.json                 # Dependencies
├── tailwind.config.js           # Tailwind CSS config
├── tsconfig.json                # TypeScript config
└── vercel.json                  # Vercel deployment config
```

---

## 🔧 Implementation Steps

### Phase 1: Project Setup (Day 1)
1. ✅ Create Next.js project with TypeScript
   ```bash
   npx create-next-app@latest smartshift-nextjs --typescript --tailwind --app
   ```

2. ✅ Install dependencies
   ```bash
   npm install @langchain/openai langchain @pinecone-database/pinecone
   npm install papaparse date-fns
   npm install -D @types/papaparse
   ```

3. ✅ Set up environment variables
   ```env
   OPENROUTER_API_KEY=your_openrouter_key
   PINECONE_API_KEY=your_pinecone_key
   PINECONE_ENVIRONMENT=your_environment
   PINECONE_INDEX=smartshift-workers
   ```

### Phase 2: Backend Migration (Day 2-3)
1. ✅ Migrate data loader to TypeScript
   - Convert `data_loader.py` → `lib/dataLoader.ts`
   - Use `papaparse` for CSV parsing
   - Create TypeScript interfaces for Worker type

2. ✅ Set up Pinecone vector store
   - Create Pinecone index
   - Migrate embedding logic from ChromaDB
   - Implement search functionality

3. ✅ Configure OpenRouter LLM
   - Set up LangChain.js with OpenRouter
   - Test Qwen 3.6-27B model connection
   - Configure parameters (temperature, max_tokens)

4. ✅ Migrate agents to LangChain.js
   - Convert `agents.py` → `lib/agents.ts`
   - Recreate Skill Matcher Agent
   - Recreate Shift Planner Agent

5. ✅ Create agent tools
   - Convert `tools.py` → `lib/tools.ts`
   - Implement search_workers_tool
   - Implement get_worker_details_tool
   - Implement get_zone_statistics_tool

### Phase 3: API Routes (Day 3-4)
1. ✅ Create `/api/workers` endpoint
   - GET: Return all workers
   - POST: Update worker data

2. ✅ Create `/api/search` endpoint
   - POST: Search workers by skill
   - Integrate with Pinecone

3. ✅ Create `/api/recommendations` endpoint
   - POST: Get AI recommendations
   - Run agent workflow
   - Return formatted results

### Phase 4: Frontend Development (Day 4-6)
1. ✅ Create layout and navigation
   - Header with app title
   - Sidebar for controls
   - Responsive design

2. ✅ Build WorkforceOverview component
   - Display worker statistics
   - Zone distribution cards
   - Load status indicators

3. ✅ Build WorkerTable component
   - Sortable columns
   - Filters (zone, load, availability)
   - Export to CSV functionality

4. ✅ Build OverloadForm component
   - Text input for overload description
   - Quick example buttons
   - Submit button with loading state

5. ✅ Build RecommendationCard component
   - Display AI recommendations
   - Show worker details
   - Explanation text
   - Action buttons

6. ✅ Implement state management
   - React Context for global state
   - Loading states
   - Error handling

### Phase 5: Testing & Deployment (Day 7)
1. ✅ Local testing
   - Test all API endpoints
   - Test UI components
   - Test agent workflow end-to-end

2. ✅ Configure Vercel deployment
   - Create `vercel.json`
   - Set environment variables in Vercel dashboard
   - Configure build settings

3. ✅ Deploy to Vercel
   - Connect GitHub repository
   - Deploy and test production build
   - Verify all functionality

4. ✅ Update documentation
   - Update README.md
   - Create deployment guide
   - Document API endpoints

---

## 🔑 Environment Variables

### Required for Development
```env
# OpenRouter Configuration
OPENROUTER_API_KEY=sk-or-v1-xxxxx

# Pinecone Configuration
PINECONE_API_KEY=xxxxx
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX=smartshift-workers

# Next.js Configuration
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Required for Vercel Production
Same as above, but set in Vercel dashboard under Project Settings → Environment Variables

---

## 📊 Feature Parity Checklist

Ensure all current features are maintained:

- [ ] Load worker data from CSV
- [ ] Display workforce overview with statistics
- [ ] Show zone distribution
- [ ] Filter workers by zone, load, availability
- [ ] Natural language overload input
- [ ] AI-powered skill matching
- [ ] AI-powered shift recommendations
- [ ] Display detailed recommendations with explanations
- [ ] Export data to CSV
- [ ] Responsive UI design

---

## ⚠️ Challenges & Solutions

### Challenge 1: ChromaDB in Serverless
**Problem**: ChromaDB requires persistent storage, not ideal for Vercel serverless functions.
**Solution**: Migrate to Pinecone (cloud-based vector database).

### Challenge 2: CrewAI Framework
**Problem**: CrewAI is Python-only, no JavaScript equivalent.
**Solution**: Use LangChain.js with custom agent implementation.

### Challenge 3: CSV Data Storage
**Problem**: Vercel serverless functions are stateless.
**Solution**: 
- Option 1: Store CSV in public folder (read-only)
- Option 2: Use Vercel Postgres or Supabase for dynamic data
- **Recommended**: Start with Option 1, migrate to Option 2 if needed

### Challenge 4: Real-time Updates
**Problem**: Streamlit has built-in session state.
**Solution**: Use React state management + API polling or WebSockets.

---

## 💰 Cost Considerations

### OpenRouter (Qwen 3.6-27B)
- **Pricing**: ~$0.18 per 1M input tokens, ~$0.18 per 1M output tokens
- **Estimated Monthly Cost**: $5-20 (depending on usage)

### Pinecone
- **Free Tier**: 1 index, 100K vectors, sufficient for 28 workers
- **Paid Tier**: $70/month (if scaling needed)

### Vercel
- **Hobby Plan**: Free (sufficient for development/demo)
- **Pro Plan**: $20/month (for production with custom domain)

**Total Estimated Cost**: $0-25/month (using free tiers)

---

## 🚀 Quick Start Commands

### 1. Create New Next.js Project
```bash
npx create-next-app@latest smartshift-nextjs --typescript --tailwind --app
cd smartshift-nextjs
```

### 2. Install Dependencies
```bash
npm install @langchain/openai langchain @pinecone-database/pinecone papaparse date-fns
npm install -D @types/papaparse
```

### 3. Copy Worker Data
```bash
cp ../smartshift_v2/workers.csv ./public/
```

### 4. Set Up Environment Variables
```bash
cp .env.example .env.local
# Edit .env.local with your API keys
```

### 5. Run Development Server
```bash
npm run dev
```

### 6. Deploy to Vercel
```bash
npm install -g vercel
vercel
```

---

## 📚 Resources

### Documentation
- [Next.js Documentation](https://nextjs.org/docs)
- [LangChain.js Documentation](https://js.langchain.com/docs)
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [Vercel Documentation](https://vercel.com/docs)

### Tutorials
- [Next.js App Router Tutorial](https://nextjs.org/learn)
- [LangChain.js Agents](https://js.langchain.com/docs/modules/agents/)
- [Pinecone Quickstart](https://docs.pinecone.io/docs/quickstart)

---

## 🎯 Success Criteria

Migration is complete when:
1. ✅ All 28 workers are indexed in Pinecone
2. ✅ OpenRouter API successfully responds with Qwen 3.6-27B
3. ✅ Both agents (Skill Matcher, Shift Planner) work correctly
4. ✅ UI displays all worker data and statistics
5. ✅ Natural language input generates accurate recommendations
6. ✅ Application is deployed and accessible on Vercel
7. ✅ All original features are functional
8. ✅ Documentation is updated

---

## 📝 Next Steps

1. **Review this plan** with stakeholders
2. **Set up OpenRouter account** and get API key
3. **Set up Pinecone account** and create index
4. **Create Next.js project** following Phase 1
5. **Begin backend migration** following Phase 2
6. **Switch to Code mode** to start implementation

---

**Ready to proceed?** Switch to Code mode to begin implementation!
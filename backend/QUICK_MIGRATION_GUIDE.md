# Quick Migration Guide - SmartShift to Next.js + Vercel

## 🎯 What You Need to Do Now

### Step 1: Get API Keys (15 minutes)

#### OpenRouter Setup
1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for an account
3. Navigate to "Keys" section
4. Create a new API key
5. Copy the key (starts with `sk-or-v1-`)
6. **Model to use**: `qwen/qwen-2.5-72b-instruct` (or `qwen/qwen-3.6-27b` if available)

#### Pinecone Setup (for Vector Store)
1. Go to [Pinecone.io](https://www.pinecone.io/)
2. Sign up for free account
3. Create a new index:
   - **Name**: `smartshift-workers`
   - **Dimensions**: `384` (for all-MiniLM-L6-v2 embeddings)
   - **Metric**: `cosine`
   - **Environment**: Choose closest region
4. Copy your API key from dashboard

### Step 2: Create Next.js Project (10 minutes)

```bash
# Navigate to your desktop or preferred location
cd ~/Desktop

# Create new Next.js project
npx create-next-app@latest smartshift-nextjs --typescript --tailwind --app --eslint

# When prompted, choose:
# ✓ Would you like to use TypeScript? Yes
# ✓ Would you like to use ESLint? Yes
# ✓ Would you like to use Tailwind CSS? Yes
# ✓ Would you like to use `src/` directory? No
# ✓ Would you like to use App Router? Yes
# ✓ Would you like to customize the default import alias? No

# Navigate into project
cd smartshift-nextjs

# Install required dependencies
npm install @langchain/openai langchain @pinecone-database/pinecone
npm install papaparse date-fns zod
npm install -D @types/papaparse
```

### Step 3: Set Up Environment Variables (5 minutes)

Create `.env.local` file in project root:

```env
# OpenRouter Configuration
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Pinecone Configuration
PINECONE_API_KEY=your-pinecone-key-here
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX=smartshift-workers

# App Configuration
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Step 4: Copy Worker Data (2 minutes)

```bash
# Copy workers.csv from old project to new project
cp ../smartshift_v2/workers.csv ./public/workers.csv
```

### Step 5: Project Structure Setup (5 minutes)

Create the following folder structure:

```bash
# Create directories
mkdir -p app/api/workers
mkdir -p app/api/search
mkdir -p app/api/recommendations
mkdir -p components
mkdir -p lib
mkdir -p types

# Create placeholder files
touch types/worker.ts
touch lib/llm.ts
touch lib/vectorStore.ts
touch lib/dataLoader.ts
touch lib/agents.ts
touch lib/tools.ts
```

### Step 6: Test Development Server (2 minutes)

```bash
# Start development server
npm run dev

# Open browser to http://localhost:3000
# You should see the default Next.js welcome page
```

---

## 📋 What Needs to Be Built

### Priority 1: Core Backend (Start Here)
1. **types/worker.ts** - TypeScript interfaces for Worker data
2. **lib/dataLoader.ts** - Load and parse workers.csv
3. **lib/llm.ts** - Configure OpenRouter with Qwen model
4. **lib/vectorStore.ts** - Set up Pinecone vector store
5. **lib/tools.ts** - Agent tools (search, get details, stats)
6. **lib/agents.ts** - LangChain agents (Skill Matcher, Shift Planner)

### Priority 2: API Routes
1. **app/api/workers/route.ts** - GET all workers
2. **app/api/search/route.ts** - POST search workers by skill
3. **app/api/recommendations/route.ts** - POST get AI recommendations

### Priority 3: Frontend Components
1. **components/WorkforceOverview.tsx** - Dashboard with stats
2. **components/WorkerTable.tsx** - Sortable/filterable table
3. **components/OverloadForm.tsx** - Input form for overload reports
4. **components/RecommendationCard.tsx** - Display AI recommendations
5. **app/page.tsx** - Main page combining all components

### Priority 4: Deployment
1. **vercel.json** - Vercel configuration
2. Push to GitHub
3. Connect to Vercel
4. Set environment variables in Vercel dashboard
5. Deploy!

---

## 🔄 Migration Mapping

### Python → TypeScript Equivalents

| Python File | TypeScript File | Purpose |
|------------|----------------|---------|
| `config.py` | `lib/llm.ts` | LLM configuration |
| `data_loader.py` | `lib/dataLoader.ts` | CSV data loading |
| `vector_store.py` | `lib/vectorStore.ts` | Vector search |
| `tools.py` | `lib/tools.ts` | Agent tools |
| `agents.py` | `lib/agents.ts` | AI agents |
| `tasks.py` | `lib/agents.ts` | Agent workflows |
| `app.py` | `app/page.tsx` + components | UI |

### Key Technology Changes

| Old | New | Reason |
|-----|-----|--------|
| IBM Watson/Granite | OpenRouter (Qwen 3.6-27B) | Your preference |
| CrewAI | LangChain.js | JavaScript equivalent |
| ChromaDB | Pinecone | Serverless-friendly |
| Streamlit | Next.js + React | Vercel deployment |
| Python | TypeScript | Web standard |

---

## 🚨 Important Notes

### Vector Store Migration
- **ChromaDB uses 384-dimensional embeddings** (all-MiniLM-L6-v2)
- **Pinecone index must be created with dimension=384**
- You'll need to re-index all 28 workers in Pinecone
- Embeddings will be generated using the same model for consistency

### Agent Framework Differences
- **CrewAI**: High-level, automatic agent orchestration
- **LangChain.js**: More manual, but flexible
- You'll need to implement the sequential workflow manually
- Agent communication will be handled through function calls

### Serverless Limitations
- **No persistent file system** on Vercel
- Workers.csv must be in `/public` folder (read-only)
- Vector store must be cloud-based (Pinecone)
- Each API route is a separate serverless function

### Cost Optimization
- Use Pinecone free tier (sufficient for 28 workers)
- OpenRouter charges per token (~$0.18/1M tokens)
- Vercel Hobby plan is free (good for demo/development)
- Estimated total: $0-10/month

---

## 🎬 Ready to Start?

### Option 1: Do It Yourself
Follow the steps above and use the detailed MIGRATION_PLAN.md as reference.

### Option 2: Get Help from Code Mode
Switch to Code mode and I'll help you build each component step by step.

**Recommended approach**: Start with Step 1-4 above, then switch to Code mode for implementation.

---

## 📞 Need Help?

If you encounter issues:
1. Check the detailed MIGRATION_PLAN.md
2. Review Next.js documentation
3. Check LangChain.js examples
4. Switch to Code mode for hands-on assistance

---

## ✅ Checklist Before Starting

- [ ] OpenRouter account created and API key obtained
- [ ] Pinecone account created and index set up (dimension=384)
- [ ] Next.js project created successfully
- [ ] Dependencies installed
- [ ] Environment variables configured
- [ ] workers.csv copied to public folder
- [ ] Development server runs without errors

**Once all checked, you're ready to start building!** 🚀
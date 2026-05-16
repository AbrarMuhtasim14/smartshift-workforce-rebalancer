# 🏭 SmartShift v2.0 - Hybrid Architecture
## AI-Powered Warehouse Workforce Rebalancing

SmartShift is an intelligent workforce management system that uses AI agents to automatically recommend optimal worker shifts when warehouse zones become overloaded.

**New in v2.0**: Hybrid architecture with Python FastAPI backend + Next.js frontend, deployed on Railway + Vercel.

---

## 🌟 Features

- **🤖 AI-Powered Recommendations**: Two specialized AI agents (CrewAI) work together
- **🔍 Semantic Skill Matching**: ChromaDB vector store for intelligent worker search
- **📊 Real-Time Analytics**: Visual dashboard with zone distribution and load status
- **⚖️ Smart Load Balancing**: Considers workload, skills, education, and physical capabilities
- **💬 Natural Language Input**: Managers describe overload situations in plain English
- **🎯 Detailed Explanations**: Clear reasoning for each recommendation
- **🌐 Modern Web UI**: Responsive Next.js frontend with Tailwind CSS
- **🚀 Cloud Deployed**: Backend on Railway, Frontend on Vercel

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Next.js Frontend (Vercel)                   │
│  - React Components                                      │
│  - Tailwind CSS Styling                                  │
│  - Responsive Design                                     │
│  - https://your-app.vercel.app                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ REST API (HTTP/JSON)
                     │
┌────────────────────▼────────────────────────────────────┐
│         Python FastAPI Backend (Railway)                 │
│  ┌────────────────────────────────────────────────┐     │
│  │  API Endpoints                                  │     │
│  │  - GET  /api/workers                            │     │
│  │  - GET  /api/zones/{zone}                       │     │
│  │  - POST /api/search                             │     │
│  │  - POST /api/recommendations                    │     │
│  └────────────────────────────────────────────────┘     │
│                     │                                    │
│  ┌────────────────────────────────────────────────┐     │
│  │  AI & Data Layer                                │     │
│  │  - CrewAI Agents (Skill Matcher, Planner)      │     │
│  │  - OpenRouter LLM (Qwen 2.5 72B)               │     │
│  │  - ChromaDB Vector Store                        │     │
│  │  - Worker Data (CSV)                            │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  https://your-api.railway.app                           │
└──────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- OpenRouter API key (get from https://openrouter.ai/)

### Backend Setup

1. **Clone and navigate to project**:
   ```bash
   git clone <repository-url>
   cd smartshift_v2
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENROUTER_API_KEY
   ```

4. **Run the backend**:
   ```bash
   python api.py
   ```
   
   Backend will start at http://localhost:8000

5. **Test the API**:
   ```bash
   python test_api.py
   ```

### Frontend Setup

1. **Create Next.js project** (in a separate directory):
   ```bash
   cd ~/Desktop
   npx create-next-app@latest smartshift-frontend --typescript --tailwind --app
   cd smartshift-frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install axios date-fns
   ```

3. **Configure environment**:
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   ```

4. **Copy frontend code** (from DEPLOYMENT_GUIDE.md)

5. **Run the frontend**:
   ```bash
   npm run dev
   ```
   
   Frontend will start at http://localhost:3000

---

## 📦 Technology Stack

### Backend
- **Framework**: FastAPI
- **AI Agents**: CrewAI
- **LLM**: OpenRouter (Qwen 2.5 72B Instruct)
- **Vector Store**: ChromaDB
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Data**: Pandas + CSV

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **UI Components**: React

### Deployment
- **Backend**: Railway (Python)
- **Frontend**: Vercel (Next.js)
- **Database**: ChromaDB (embedded)

---

## 📊 API Endpoints

### Health Check
```bash
GET /
```

### Get All Workers
```bash
GET /api/workers
```

### Get Zone Statistics
```bash
GET /api/zones/{zone}
# Example: GET /api/zones/Zone%20A
```

### Search Workers
```bash
POST /api/search
Content-Type: application/json

{
  "query": "forklift operator",
  "exclude_zone": "Zone A"
}
```

### Get AI Recommendations
```bash
POST /api/recommendations
Content-Type: application/json

{
  "manager_input": "Zone A dispatch is overloaded, need forklift help"
}
```

---

## 🧪 Testing

### Test Backend API
```bash
# Start backend
python api.py

# In another terminal, run tests
python test_api.py
```

### Test Frontend
```bash
cd smartshift-frontend
npm run dev
# Visit http://localhost:3000
```

---

## 🚀 Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

### Quick Deploy

**Backend to Railway**:
1. Push code to GitHub
2. Connect Railway to your repository
3. Add `OPENROUTER_API_KEY` environment variable
4. Deploy automatically

**Frontend to Vercel**:
1. Push frontend code to GitHub
2. Import project in Vercel
3. Add `NEXT_PUBLIC_API_URL` environment variable
4. Deploy automatically

---

## 📁 Project Structure

```
smartshift_v2/
├── api.py                      # FastAPI backend (NEW)
├── config.py                   # LLM configuration (UPDATED)
├── agents.py                   # CrewAI agents
├── tasks.py                    # Agent tasks
├── tools.py                    # Agent tools
├── vector_store.py             # ChromaDB integration
├── data_loader.py              # CSV data management
├── workers.csv                 # Worker database
├── requirements.txt            # Python dependencies (UPDATED)
├── .env                        # Environment variables (UPDATED)
├── Procfile                    # Railway deployment (NEW)
├── railway.json                # Railway config (NEW)
├── test_api.py                 # API test suite (NEW)
├── DEPLOYMENT_GUIDE.md         # Deployment instructions (NEW)
├── HYBRID_ARCHITECTURE_PLAN.md # Architecture docs (NEW)
└── README_HYBRID.md            # This file (NEW)
```

---

## 🔧 Configuration

### Backend Environment Variables (.env)
```env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
```

### Frontend Environment Variables (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 💰 Cost Estimate

- **OpenRouter**: ~$5-20/month (pay per use)
- **Railway**: Free tier (500 hours/month)
- **Vercel**: Free tier (unlimited deployments)
- **Total**: $5-20/month

---

## 🔄 Migration from v1.0

If you're upgrading from the Streamlit version:

1. **What Changed**:
   - ❌ Removed: IBM Watson/Granite LLM
   - ❌ Removed: Streamlit UI
   - ✅ Added: OpenRouter (Qwen 2.5 72B)
   - ✅ Added: FastAPI backend
   - ✅ Added: Next.js frontend
   - ✅ Kept: CrewAI agents (90% of code unchanged!)
   - ✅ Kept: ChromaDB vector store
   - ✅ Kept: All worker data and logic

2. **Migration Steps**:
   - Update `config.py` for OpenRouter
   - Install FastAPI dependencies
   - Create Next.js frontend
   - Deploy to Railway + Vercel

See [HYBRID_ARCHITECTURE_PLAN.md](HYBRID_ARCHITECTURE_PLAN.md) for detailed migration guide.

---

## 📖 Documentation

- [HYBRID_ARCHITECTURE_PLAN.md](HYBRID_ARCHITECTURE_PLAN.md) - Architecture overview
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Deployment instructions
- [MIGRATION_PLAN.md](MIGRATION_PLAN.md) - Original migration plan
- [QUICK_MIGRATION_GUIDE.md](QUICK_MIGRATION_GUIDE.md) - Quick reference

---

## 🧪 Example Usage

### 1. Start Backend
```bash
python api.py
```

### 2. Test API
```bash
curl http://localhost:8000/api/workers
```

### 3. Get Recommendations
```bash
curl -X POST http://localhost:8000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"manager_input": "Zone A needs forklift help"}'
```

---

## 🐛 Troubleshooting

### Backend Issues

**"OPENROUTER_API_KEY not set"**
- Add your API key to `.env` file

**"Workers data not loaded"**
- Ensure `workers.csv` is in the project root

**"ChromaDB initialization failed"**
- Delete `chroma_store/` folder and restart

### Frontend Issues

**"Network Error"**
- Check backend is running on port 8000
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`

**CORS errors**
- Backend CORS is configured for localhost:3000
- Check `api.py` CORS settings

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📝 License

This project is part of the IBM watsonx.ai Call for Code challenge.

---

## 🎯 Roadmap

- [x] Migrate from IBM Watson to OpenRouter
- [x] Convert Streamlit to FastAPI
- [x] Create Next.js frontend
- [x] Deploy to Railway + Vercel
- [ ] Add authentication
- [ ] Add worker preference system
- [ ] Historical analytics dashboard
- [ ] Mobile app
- [ ] Integration with WMS systems

---

## 📧 Support

For issues and questions:
- Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- Review [HYBRID_ARCHITECTURE_PLAN.md](HYBRID_ARCHITECTURE_PLAN.md)
- Create an issue on GitHub

---

**Built with ❤️ for efficient warehouse operations**

**v2.0 - Hybrid Architecture Edition**
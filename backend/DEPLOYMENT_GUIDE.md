# SmartShift Deployment Guide
## Hybrid Architecture: Python Backend + Next.js Frontend

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────┐
│   Next.js Frontend (Vercel)     │
│   https://your-app.vercel.app   │
└────────────┬────────────────────┘
             │ HTTP/REST API
┌────────────▼────────────────────┐
│  Python Backend (Railway)       │
│  https://your-api.railway.app   │
│  - FastAPI                      │
│  - CrewAI + OpenRouter          │
│  - ChromaDB                     │
└─────────────────────────────────┘
```

---

## 📋 Prerequisites

### Required Accounts
1. **OpenRouter** - https://openrouter.ai/ (for LLM API)
2. **Railway** - https://railway.app/ (for Python backend)
3. **Vercel** - https://vercel.com/ (for Next.js frontend)
4. **GitHub** - https://github.com/ (for code hosting)

### Required Tools
- Python 3.10+
- Node.js 18+
- Git

---

## 🚀 Part 1: Backend Deployment (Railway)

### Step 1: Prepare Backend

1. **Install dependencies locally** (test first):
   ```bash
   pip install -r requirements.txt
   ```

2. **Test backend locally**:
   ```bash
   # Make sure you have OPENROUTER_API_KEY in .env
   python api.py
   ```
   
   Visit http://localhost:8000 - you should see:
   ```json
   {
     "message": "SmartShift API",
     "status": "running",
     "version": "2.0"
   }
   ```

### Step 2: Push to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Add FastAPI backend with OpenRouter"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/smartshift.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Railway

1. **Sign up at Railway**: https://railway.app/

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your smartshift repository
   - Railway will auto-detect Python and use Nixpacks

3. **Add Environment Variables**:
   - Go to your project → Variables tab
   - Add these variables:
     ```
     OPENROUTER_API_KEY=sk-or-v1-your-key-here
     PORT=8000
     ```

4. **Deploy**:
   - Railway will automatically build and deploy
   - Wait for deployment to complete (2-5 minutes)
   - You'll get a URL like: `https://smartshift-production.up.railway.app`

5. **Test Deployment**:
   ```bash
   curl https://your-railway-url.railway.app/
   ```

### Step 4: Verify Backend Endpoints

Test these endpoints:
- `GET /` - Health check
- `GET /api/workers` - Get all workers
- `GET /api/zones/Zone%20A` - Get zone stats
- `POST /api/recommendations` - Get AI recommendations

Example test:
```bash
curl -X POST https://your-railway-url.railway.app/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"manager_input": "Zone A needs forklift help"}'
```

---

## 🎨 Part 2: Frontend Setup (Next.js)

### Step 1: Create Next.js Project

```bash
# Navigate to your desktop or preferred location
cd ~/Desktop

# Create new Next.js project
npx create-next-app@latest smartshift-frontend --typescript --tailwind --app --eslint

# Navigate into project
cd smartshift-frontend
```

When prompted:
- ✓ TypeScript? **Yes**
- ✓ ESLint? **Yes**
- ✓ Tailwind CSS? **Yes**
- ✓ `src/` directory? **No**
- ✓ App Router? **Yes**
- ✓ Import alias? **No**

### Step 2: Install Dependencies

```bash
npm install axios date-fns
npm install -D @types/node
```

### Step 3: Create Environment Variables

Create `.env.local`:
```env
NEXT_PUBLIC_API_URL=https://your-railway-url.railway.app
```

### Step 4: Create API Client

Create `lib/api.ts`:
```typescript
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

### Step 5: Create Components

I'll provide the key components structure. Create these files:

**components/WorkforceOverview.tsx** - Dashboard stats
**components/WorkerTable.tsx** - Worker data table
**components/OverloadForm.tsx** - Input form
**components/RecommendationDisplay.tsx** - AI results

### Step 6: Update Main Page

Update `app/page.tsx` to use the components and API client.

### Step 7: Test Locally

```bash
npm run dev
```

Visit http://localhost:3000

---

## 🌐 Part 3: Frontend Deployment (Vercel)

### Step 1: Push Frontend to GitHub

```bash
cd smartshift-frontend

git init
git add .
git commit -m "Initial Next.js frontend"

# Create new GitHub repository for frontend
git remote add origin https://github.com/yourusername/smartshift-frontend.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Vercel

1. **Sign up at Vercel**: https://vercel.com/

2. **Import Project**:
   - Click "Add New..." → "Project"
   - Import your `smartshift-frontend` repository
   - Vercel will auto-detect Next.js

3. **Configure Environment Variables**:
   - Before deploying, add environment variable:
     ```
     NEXT_PUBLIC_API_URL=https://your-railway-url.railway.app
     ```

4. **Deploy**:
   - Click "Deploy"
   - Wait for build to complete (2-3 minutes)
   - You'll get a URL like: `https://smartshift-frontend.vercel.app`

5. **Test Deployment**:
   - Visit your Vercel URL
   - Test all features:
     - View workers
     - Filter by zone
     - Submit overload request
     - View AI recommendations

---

## 🔧 Configuration Summary

### Backend (.env on Railway)
```env
OPENROUTER_API_KEY=sk-or-v1-xxxxx
PORT=8000
```

### Frontend (.env.local for Vercel)
```env
NEXT_PUBLIC_API_URL=https://your-railway-url.railway.app
```

---

## 🧪 Testing Checklist

### Backend Tests
- [ ] Health check endpoint works
- [ ] Can fetch all workers
- [ ] Can get zone statistics
- [ ] Can search workers
- [ ] Can get AI recommendations
- [ ] CORS allows frontend domain

### Frontend Tests
- [ ] Page loads successfully
- [ ] Workers data displays
- [ ] Zone statistics show correctly
- [ ] Can filter workers
- [ ] Can submit overload form
- [ ] AI recommendations display
- [ ] No CORS errors in console

### Integration Tests
- [ ] Frontend can connect to backend
- [ ] API calls return data
- [ ] AI recommendations work end-to-end
- [ ] Error handling works

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: "OPENROUTER_API_KEY not set"
- **Solution**: Add environment variable in Railway dashboard

**Problem**: "Workers data not loaded"
- **Solution**: Ensure `workers.csv` is in repository root

**Problem**: "ChromaDB initialization failed"
- **Solution**: Check Railway logs, may need to increase memory

### Frontend Issues

**Problem**: "Network Error" or CORS error
- **Solution**: Check `NEXT_PUBLIC_API_URL` is correct
- **Solution**: Verify backend CORS settings allow your domain

**Problem**: "API_URL is undefined"
- **Solution**: Environment variable must start with `NEXT_PUBLIC_`

**Problem**: Build fails on Vercel
- **Solution**: Check all dependencies are in `package.json`

---

## 💰 Cost Breakdown

### Free Tier Limits
- **Railway**: 500 hours/month, $5 credit
- **Vercel**: Unlimited deployments, 100GB bandwidth
- **OpenRouter**: Pay per use (~$0.18/1M tokens)

### Expected Monthly Cost
- **Development**: $0 (all free tiers)
- **Light Production**: $5-10 (OpenRouter usage)
- **Heavy Production**: $20-50 (may need Railway Pro)

---

## 🔄 Continuous Deployment

### Auto-Deploy on Git Push

**Railway** (Backend):
- Automatically deploys on push to `main` branch
- No configuration needed

**Vercel** (Frontend):
- Automatically deploys on push to `main` branch
- Preview deployments for pull requests

### Manual Deployment

**Railway**:
```bash
# Push to GitHub
git push origin main
# Railway auto-deploys
```

**Vercel**:
```bash
# Push to GitHub
git push origin main
# Vercel auto-deploys
```

---

## 📊 Monitoring

### Railway Dashboard
- View logs: Project → Deployments → Logs
- Monitor metrics: CPU, Memory, Network
- Check build status

### Vercel Dashboard
- View deployments: Project → Deployments
- Check analytics: Project → Analytics
- Monitor performance

---

## 🔐 Security Best Practices

1. **Never commit `.env` files**
2. **Use environment variables for all secrets**
3. **Restrict CORS in production** (update `api.py`)
4. **Use HTTPS only** (both platforms provide this)
5. **Rotate API keys regularly**

---

## 📝 Next Steps After Deployment

1. **Custom Domain** (Optional):
   - Railway: Add custom domain in settings
   - Vercel: Add custom domain in project settings

2. **Monitoring** (Optional):
   - Set up error tracking (Sentry)
   - Add analytics (Vercel Analytics)

3. **Scaling** (If needed):
   - Railway: Upgrade to Pro plan
   - Vercel: Automatic scaling included

---

## 🎉 Success!

Your SmartShift application is now deployed:
- **Backend**: https://your-app.railway.app
- **Frontend**: https://your-app.vercel.app

Users can access the full application through the Vercel URL!

---

## 📞 Support

- **Railway Docs**: https://docs.railway.app/
- **Vercel Docs**: https://vercel.com/docs
- **OpenRouter Docs**: https://openrouter.ai/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Next.js Docs**: https://nextjs.org/docs
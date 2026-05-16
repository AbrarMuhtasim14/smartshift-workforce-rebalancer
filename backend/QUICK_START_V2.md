# SmartShift v2.0 - Quick Start Guide
## Get Up and Running in 15 Minutes

---

## 🚀 Backend Setup (5 minutes)

### 1. Get OpenRouter API Key
```
1. Visit: https://openrouter.ai/
2. Sign up for free account
3. Go to "Keys" section
4. Create new API key
5. Copy the key (starts with sk-or-v1-)
```

### 2. Configure Environment
```bash
# Edit .env file
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### 3. Install & Run
```bash
# Install dependencies
pip install -r requirements.txt

# Start backend
python api.py
```

Backend runs at: **http://localhost:8000**

### 4. Test Backend
```bash
# In another terminal
python test_api.py
```

You should see: **5/5 tests passed** ✅

---

## 🎨 Frontend Setup (10 minutes)

### 1. Create Next.js Project
```bash
cd ~/Desktop
npx create-next-app@latest smartshift-frontend --typescript --tailwind --app
cd smartshift-frontend
```

### 2. Install Dependencies
```bash
npm install axios date-fns
```

### 3. Configure Environment
```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

### 4. Create API Client
Create `lib/api.ts` - Copy from DEPLOYMENT_GUIDE.md section 2.4

### 5. Create Components
Create these files (copy from DEPLOYMENT_GUIDE.md):
- `components/WorkforceOverview.tsx`
- `components/WorkerTable.tsx`
- `components/OverloadForm.tsx`
- `components/RecommendationDisplay.tsx`

### 6. Update Main Page
Update `app/page.tsx` - Copy from DEPLOYMENT_GUIDE.md section 2.5

### 7. Run Frontend
```bash
npm run dev
```

Frontend runs at: **http://localhost:3000**

---

## ✅ Verification Checklist

### Backend
- [ ] Backend starts without errors
- [ ] Visit http://localhost:8000 shows API info
- [ ] `python test_api.py` passes all tests
- [ ] Can see workers at http://localhost:8000/api/workers

### Frontend
- [ ] Frontend starts without errors
- [ ] Visit http://localhost:3000 shows dashboard
- [ ] Workers data loads and displays
- [ ] Can submit overload form
- [ ] AI recommendations appear

---

## 🚀 Deploy to Production (30 minutes)

### Backend → Railway

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add FastAPI backend"
   git push origin main
   ```

2. **Deploy on Railway**
   - Visit https://railway.app/
   - New Project → Deploy from GitHub
   - Select your repository
   - Add environment variable: `OPENROUTER_API_KEY`
   - Deploy automatically

3. **Get URL**
   - Copy your Railway URL (e.g., `https://smartshift.railway.app`)

### Frontend → Vercel

1. **Push to GitHub**
   ```bash
   cd smartshift-frontend
   git init
   git add .
   git commit -m "Initial frontend"
   git push origin main
   ```

2. **Deploy on Vercel**
   - Visit https://vercel.com/
   - Import Project → Select repository
   - Add environment variable: `NEXT_PUBLIC_API_URL=https://your-railway-url.railway.app`
   - Deploy

3. **Access App**
   - Your app is live at: `https://smartshift.vercel.app`

---

## 📊 API Endpoints Reference

```bash
# Health Check
curl http://localhost:8000/

# Get All Workers
curl http://localhost:8000/api/workers

# Get Zone Stats
curl http://localhost:8000/api/zones/Zone%20A

# Search Workers
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "forklift", "exclude_zone": "Zone A"}'

# Get AI Recommendations
curl -X POST http://localhost:8000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"manager_input": "Zone A needs forklift help"}'
```

---

## 🐛 Quick Troubleshooting

### "OPENROUTER_API_KEY not set"
→ Add your API key to `.env` file

### "Module not found"
→ Run `pip install -r requirements.txt`

### "Workers data not loaded"
→ Ensure `workers.csv` is in project root

### "CORS error"
→ Check backend is running and CORS is configured

### "Network Error" in frontend
→ Verify `NEXT_PUBLIC_API_URL` in `.env.local`

---

## 📚 Full Documentation

- **Architecture**: [HYBRID_ARCHITECTURE_PLAN.md](HYBRID_ARCHITECTURE_PLAN.md)
- **Deployment**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Overview**: [README_HYBRID.md](README_HYBRID.md)
- **Summary**: [IMPLEMENTATION_SUMMARY_V2.md](IMPLEMENTATION_SUMMARY_V2.md)

---

## 💡 Pro Tips

1. **Test backend first** before building frontend
2. **Use test_api.py** to verify all endpoints work
3. **Check Railway logs** if deployment fails
4. **Use Vercel preview** deployments for testing
5. **Keep API keys secret** - never commit to git

---

## 🎯 Success Metrics

### Backend Working ✅
- API responds at http://localhost:8000
- All 5 tests pass
- Can get AI recommendations

### Frontend Working ✅
- UI loads at http://localhost:3000
- Workers display correctly
- Can submit forms
- Recommendations appear

### Deployed ✅
- Backend live on Railway
- Frontend live on Vercel
- Full app accessible online

---

## ⏱️ Time Estimates

- Backend setup: **5 minutes**
- Backend testing: **2 minutes**
- Frontend setup: **10 minutes**
- Frontend testing: **3 minutes**
- Deployment: **30 minutes**

**Total: ~50 minutes** from zero to production! 🚀

---

## 🆘 Need Help?

1. Check the error message
2. Review relevant documentation
3. Check Railway/Vercel logs
4. Verify environment variables
5. Test API endpoints individually

---

**Ready? Start with Backend Setup above!** ⬆️
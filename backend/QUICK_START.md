# 🚀 SmartShift Quick Start Guide

## Prerequisites Checklist
- [ ] Python 3.10 or higher installed
- [ ] IBM Cloud account created
- [ ] watsonx.ai access enabled
- [ ] API Key and Project ID obtained

---

## 5-Minute Setup

### Step 1: Install Dependencies (2 minutes)
```bash
cd smartshift_v2
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### Step 2: Configure Credentials (1 minute)
```bash
# Copy the template
cp .env.example .env

# Edit .env file and add your credentials:
# WATSONX_API_KEY=your_actual_api_key
# WATSONX_PROJECT_ID=your_actual_project_id
```

### Step 3: Run Application (1 minute)
```bash
streamlit run app.py
```

### Step 4: Initialize System (1 minute)
1. Open browser to `http://localhost:8501`
2. Click **"🔄 Load/Reload Data"** in sidebar
3. Click **"🚀 Initialize System"** in sidebar
4. Wait for "System initialized successfully!" message

---

## First Test Run

### Try This Example:
1. In the text area, enter:
   ```
   Zone A dispatch is overloaded, need forklift help
   ```

2. Click **"🤖 Get AI Recommendations"**

3. Wait 30-60 seconds for AI analysis

4. Review the recommendations showing:
   - Worker names and IDs
   - Skill matches
   - Current load status
   - Detailed reasoning

---

## Common Commands

### Start Application
```bash
streamlit run app.py
```

### Stop Application
Press `Ctrl+C` in terminal

### Reinstall Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Clear Vector Store
Delete the `chroma_store` folder and reinitialize

---

## Test Queries

Copy and paste these into the application:

### Query 1: Forklift Operator
```
Zone A dispatch is overloaded, need forklift help
```

### Query 2: Packing Specialist
```
Zone C needs packing help for afternoon shift
```

### Query 3: Quality Inspector
```
Zone B is at 90% capacity, need quality inspector
```

### Query 4: Heavy Equipment
```
Zone D receiving needs heavy equipment operator urgently
```

---

## Troubleshooting

### Issue: "WATSONX_API_KEY not set"
**Fix**: Create `.env` file with your credentials

### Issue: "Collection not initialized"
**Fix**: Click "Initialize System" in sidebar

### Issue: "Module not found"
**Fix**: Run `pip install -r requirements.txt`

### Issue: Application won't start
**Fix**: Check Python version with `python --version` (need 3.10+)

---

## Getting IBM watsonx.ai Credentials

1. Go to https://cloud.ibm.com/
2. Sign up or log in
3. Navigate to watsonx.ai
4. Create a project
5. Copy your Project ID
6. Generate an API key from IBM Cloud
7. Add both to `.env` file

---

## File Structure Overview

```
smartshift_v2/
├── app.py              ← Main application (run this)
├── config.py           ← LLM configuration
├── workers.csv         ← Worker database
├── .env                ← Your credentials (create this)
├── requirements.txt    ← Dependencies
└── README.md           ← Full documentation
```

---

## Next Steps After Setup

1. ✅ Test with sample queries
2. ✅ Explore the workforce dashboard
3. ✅ Try different overload scenarios
4. ✅ Review AI recommendations
5. ✅ Read full README.md for advanced features

---

## Support

- 📖 Full documentation: `README.md`
- 🔧 Technical details: `TECHNICAL_IMPLEMENTATION_GUIDE.md`
- ✅ Implementation status: `IMPLEMENTATION_COMPLETE.md`

---

**Ready to go? Run `streamlit run app.py` and start optimizing your warehouse workforce!** 🎉
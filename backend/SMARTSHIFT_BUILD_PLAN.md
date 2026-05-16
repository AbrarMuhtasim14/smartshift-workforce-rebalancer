# SmartShift - Complete Build Plan
## AI Warehouse Workforce Optimizer - IBM Dev Day Bob Hackathon 2026

---

## 📋 Project Overview

**Goal**: Build a Python application that helps warehouse managers optimize workforce shifts using AI-powered recommendations.

**Key Technologies**:
- Language: Python 3.10+
- Agent Framework: CrewAI
- LLM: IBM Granite via watsonx.ai
- Vector Database: ChromaDB (local)
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- UI: Streamlit
- Data: CSV file with 28 workers

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit Frontend                     │
│         (Worker Registry + Overload Input Form)          │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  CrewAI Workflow                         │
│         (Skill Matcher → Shift Planner)                  │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼────────┐ ┌▼──────────────┐
│  ChromaDB    │ │  IBM      │ │  Data Loader  │
│  Vector      │ │  Granite  │ │  (CSV)        │
│  Store       │ │  LLM      │ │               │
└──────────────┘ └───────────┘ └───────────────┘
```

---

## 📁 Project Structure

```
smartshift/
│
├── app.py                  # Streamlit UI main file
├── agents.py               # CrewAI agents definition
├── tasks.py                # CrewAI tasks definition
├── vector_store.py         # ChromaDB setup and search
├── data_loader.py          # Load and prep CSV data
├── config.py               # LLM and env config
├── workers.csv             # Worker dataset (28 workers)
├── requirements.txt        # All dependencies
├── .env.example            # Env variable template
├── .bobignore              # Ignore .env and secrets
├── bob_sessions/           # Folder for Bob exports
└── README.md               # Setup instructions
```

---

## 📊 Data Model - workers.csv

### Columns:
- **worker_id**: Unique ID (W001, W002, etc.)
- **name**: Full name (diverse, realistic)
- **age**: Integer (22-58 years)
- **primary_skill**: Main job skill
- **transferable_skills**: Comma-separated list
- **education**: Qualifications + certifications
- **physicality**: Physical capability description
- **current_zone**: Zone A/B/C/D
- **zone_function**: Receiving/Packing/Dispatch/Storage
- **shift**: Morning/Afternoon/Evening
- **shift_hours**: e.g., 6AM-2PM
- **load_status**: Low/Medium/High
- **load_percentage**: Integer (0-100)
- **available**: Yes/No

### Zone Distribution:
- Zone A (Receiving): 7 workers
- Zone B (Packing): 7 workers
- Zone C (Dispatch): 7 workers
- Zone D (Storage): 7 workers

### Shift Distribution:
- Morning (6AM-2PM): 9-10 workers
- Afternoon (2PM-10PM): 9-10 workers
- Evening (10PM-6AM): 8-9 workers

### Skills to Include:
- Forklift Operator
- Packing Specialist
- Quality Inspector
- Loading Bay Operator
- Inventory Manager
- Heavy Equipment Operator
- Order Picker
- Shipping Coordinator
- Warehouse Supervisor
- Material Handler

---

## 🤖 CrewAI Agent Design

### Agent 1: Skill Matcher Agent

**Configuration**:
```python
role = "Warehouse Skill Search Specialist"
goal = "Search ChromaDB to find workers whose primary or transferable skills match the overload requirement. Filter out workers already in the overloaded zone and those unavailable."
backstory = "You are an expert in warehouse workforce management. You understand that skills like 'forklift' and 'heavy equipment' are related, and you find the best available talent efficiently."
tools = [search_workers_tool]
```

**Responsibilities**:
- Parse manager's natural language input
- Extract skill requirements
- Query ChromaDB vector store
- Filter by zone and availability
- Return shortlist of 3-5 candidates

### Agent 2: Shift Planner Agent

**Configuration**:
```python
role = "Warehouse Shift Planning Specialist"
goal = "Take candidates from Skill Matcher and decide the top 2-3 best workers to recommend. Consider education, physicality, current load, and transferable skill relevance."
backstory = "You are a seasoned warehouse operations manager. You make fair, efficient staffing decisions based on worker capability and current workload. You always explain your decisions clearly."
tools = []  # Reasoning only
```

**Responsibilities**:
- Analyze candidate profiles
- Rank by multiple criteria
- Select top 2-3 recommendations
- Generate plain English explanations
- Create updated shift plan

---

## 🔧 Component Specifications

### 1. config.py

**Purpose**: Configure IBM Granite LLM and environment variables

**Key Code**:
```python
import os
from crewai import LLM

WATSONX_URL = "https://eu-de.ml.cloud.ibm.com"
WATSONX_API_KEY = os.environ.get("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.environ.get("WATSONX_PROJECT_ID")
WATSONX_MODEL_ID = "watsonx/ibm/granite-13b-chat-v2"

os.environ["WATSONX_URL"] = WATSONX_URL
os.environ["WATSONX_APIKEY"] = WATSONX_API_KEY
os.environ["WATSONX_PROJECT_ID"] = WATSONX_PROJECT_ID

llm = LLM(
    model=WATSONX_MODEL_ID,
    base_url=WATSONX_URL,
    project_id=WATSONX_PROJECT_ID,
    max_tokens=2000,
    temperature=0.7
)
```

### 2. data_loader.py

**Purpose**: Load and validate worker CSV data

**Key Functions**:
- `load_workers()`: Read CSV into pandas DataFrame
- `validate_workers()`: Check data integrity
- `get_worker_by_id()`: Retrieve specific worker
- `get_workers_by_zone()`: Filter by zone
- `get_available_workers()`: Filter by availability

### 3. vector_store.py

**Purpose**: ChromaDB integration for semantic search

**Key Functions**:
- `initialize_chromadb()`: Create persistent ChromaDB client
- `create_collection()`: Set up "warehouse_workers" collection
- `index_workers()`: Embed and store all workers
- `search_workers()`: Semantic search with filters
- `create_worker_document()`: Format worker profile for embedding

**Document Format**:
```
"Worker Ahmed Hassan. Primary skill: Forklift Operator. 
Transferable skills: Packing, Loading, Heavy Equipment. 
Education: Certified Forklift Technician. 
Physicality: Fit, heavy lifting certified. 
Zone: Zone B. Available: Yes."
```

### 4. agents.py

**Purpose**: Define two CrewAI agents

**Structure**:
```python
from crewai import Agent
from config import llm
from tools import search_workers_tool

skill_matcher_agent = Agent(
    role="Warehouse Skill Search Specialist",
    goal="...",
    backstory="...",
    tools=[search_workers_tool],
    llm=llm,
    verbose=True
)

shift_planner_agent = Agent(
    role="Warehouse Shift Planning Specialist",
    goal="...",
    backstory="...",
    tools=[],
    llm=llm,
    verbose=True
)
```

### 5. tasks.py

**Purpose**: Define CrewAI tasks

**Task 1: skill_search_task**
```python
Task(
    description="Given '{manager_input}', identify the skill needed and search ChromaDB for matching workers. Return shortlist with full profiles.",
    agent=skill_matcher_agent,
    expected_output="List of 3-5 candidate worker profiles"
)
```

**Task 2: shift_planning_task**
```python
Task(
    description="Review candidates and pick top 2-3 workers. Explain why each is a good fit, their skill match, current zone/load, and relevant qualifications.",
    agent=shift_planner_agent,
    expected_output="Ranked recommendations with explanations + updated shift plan"
)
```

### 6. app.py

**Purpose**: Streamlit UI with 4 main sections

**Section 1: Current Workforce Overview**
- Display workers.csv as clean table
- Show: Name, Zone, Primary Skill, Transferable Skills, Shift, Load Status, Available

**Section 2: Report Overload**
- Text input: "Describe the overload situation..."
- Button: "Find Best Workers"

**Section 3: AI Recommendations**
- Loading spinner during agent execution
- Recommendation cards for each worker:
  - Worker Name
  - Current Zone → Recommended Move To
  - Skill Match
  - AI Explanation
  - Current Load %
- Updated shift plan table

**Section 4: Confirm & Export**
- Button: "Confirm Shift Change"
- Button: "Download Updated Shift Plan (CSV)"

---

## 📦 Dependencies (requirements.txt)

```
crewai
chromadb
sentence-transformers
streamlit
pandas
python-dotenv
ibm-watsonx-ai
```

---

## 🔒 Security Files

### .env.example
```
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://eu-de.ml.cloud.ibm.com
```

### .bobignore
```
.env
*.key
secrets/
config/credentials.json
__pycache__/
chroma_store/
```

---

## 🧪 Test Scenario

**Input**:
```
"Zone A dispatch is overloaded. I need someone who can operate a forklift. Zone A currently at 90% load."
```

**Expected Output**:
- 2-3 worker recommendations
- Each with:
  - Name and ID
  - Current zone and load
  - Skill match explanation
  - Why they're a good fit
- Updated shift plan showing the move

---

## 📝 Implementation Sequence

1. ✅ Generate workers.csv (28 workers)
2. ✅ Build config.py (LLM setup)
3. ✅ Build data_loader.py (CSV reader)
4. ✅ Build vector_store.py (ChromaDB)
5. ✅ Create custom tools for agents
6. ✅ Build agents.py (2 agents)
7. ✅ Build tasks.py (2 tasks)
8. ✅ Build app.py (Streamlit UI)
9. ✅ Create requirements.txt
10. ✅ Create .env.example and .bobignore
11. ✅ Write README.md
12. ✅ Test end-to-end
13. ✅ Export Bob session reports

---

## 🎯 Success Criteria

- ✅ All files created and working
- ✅ ChromaDB successfully indexes 28 workers
- ✅ Agents can process natural language input
- ✅ Recommendations are relevant and explained
- ✅ UI is clean and functional
- ✅ No hardcoded credentials
- ✅ Complete documentation

---

**Status**: Ready to implement
**Next Step**: Generate workers.csv with 28 realistic workers
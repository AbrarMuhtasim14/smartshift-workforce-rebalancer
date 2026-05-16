# 🏭 SmartShift - AI-Powered Warehouse Workforce Rebalancing

SmartShift is an intelligent workforce management system that uses AI agents to automatically recommend optimal worker shifts when warehouse zones become overloaded. Built with CrewAI, IBM Granite LLM, ChromaDB, and Streamlit.

## 🌟 Features

- **🤖 AI-Powered Recommendations**: Two specialized AI agents work together to find and recommend the best workers for shift changes
- **🔍 Semantic Skill Matching**: Uses ChromaDB vector store to find workers with matching skills (primary or transferable)
- **📊 Real-Time Workforce Analytics**: Visual dashboard showing zone distribution, load status, and worker availability
- **⚖️ Load Balancing**: Considers current workload, skills, education, and physical capabilities
- **💬 Natural Language Input**: Managers describe overload situations in plain English
- **🎯 Detailed Explanations**: Clear reasoning for each recommendation

## 🏗️ Architecture

### System Components

```
SmartShift/
├── app.py                 # Streamlit UI
├── config.py              # LLM and system configuration
├── data_loader.py         # CSV data management
├── vector_store.py        # ChromaDB integration
├── tools.py               # Custom CrewAI tools
├── agents.py              # AI agent definitions
├── tasks.py               # Workflow task definitions
├── workers.csv            # Worker database (28 workers)
├── chroma_store/          # Vector database storage
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

### AI Agents

1. **Skill Matcher Agent**: Searches ChromaDB for workers with matching skills
2. **Shift Planner Agent**: Analyzes candidates and recommends top 2-3 workers

### Technology Stack

- **Frontend**: Streamlit
- **AI Framework**: CrewAI
- **LLM**: IBM Granite 13B Chat v2 (via watsonx.ai)
- **Vector Store**: ChromaDB
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Data**: Pandas

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- IBM Cloud account with watsonx.ai access
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smartshift_v2
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your credentials
   # WATSONX_API_KEY=your_api_key_here
   # WATSONX_PROJECT_ID=your_project_id_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the application**
   - Open your browser to `http://localhost:8501`
   - Click "Load/Reload Data" in the sidebar
   - Click "Initialize System" to set up the vector store

## 📖 Usage Guide

### Step 1: Load Data
Click the "🔄 Load/Reload Data" button in the sidebar to load the worker database.

### Step 2: Initialize System
Click "🚀 Initialize System" to initialize the AI agents and vector store.

### Step 3: Report Overload
Describe the overload situation in natural language, for example:
- "Zone A dispatch is overloaded, need forklift help"
- "Zone C needs packing help for afternoon shift"
- "Zone B is at 90% capacity, need quality inspector"

### Step 4: Review Recommendations
The AI agents will analyze the situation and provide 2-3 worker recommendations with detailed explanations.

### Step 5: Take Action
Review the recommendations and approve, modify, or reject them.

## 🧪 Test Cases

### Test Case 1: Basic Forklift Request
**Input**: "Zone A dispatch is overloaded, need forklift help"

**Expected Output**: Workers with forklift or heavy equipment skills from other zones

### Test Case 2: Transferable Skills
**Input**: "Zone C needs packing help for afternoon shift"

**Expected Output**: Workers with packing as primary or transferable skill, afternoon shift

### Test Case 3: Load Balancing
**Input**: "Zone B is at 90% capacity, need quality inspector"

**Expected Output**: Quality inspectors from low-load zones

## 📊 Worker Database

The system includes 28 workers distributed across 4 zones:
- **Zone A**: Dispatch (7 workers)
- **Zone B**: Packing (7 workers)
- **Zone C**: Storage (7 workers)
- **Zone D**: Receiving (7 workers)

Each worker has:
- Primary skill
- 2-4 transferable skills
- Education and certifications
- Physical capabilities
- Current load status (Low/Medium/High)
- Shift assignment (Morning/Afternoon)
- Availability status

## 🔧 Configuration

### IBM watsonx.ai Setup

1. Create an IBM Cloud account at https://cloud.ibm.com/
2. Set up watsonx.ai service
3. Create a project and get your Project ID
4. Generate an API key
5. Add credentials to `.env` file

### ChromaDB Configuration

The vector store is automatically initialized with:
- **Collection**: warehouse_workers
- **Embedding Model**: all-MiniLM-L6-v2
- **Storage**: ./chroma_store/

### LLM Configuration

Default settings in `config.py`:
- **Model**: IBM Granite 13B Chat v2
- **Max Tokens**: 2000
- **Temperature**: 0.7

## 🛠️ Development

### Project Structure

```python
# config.py - System configuration
llm = LLM(model="watsonx/ibm/granite-13b-chat-v2", ...)

# data_loader.py - Data management
load_workers() -> DataFrame
get_worker_by_id() -> Dict
get_available_workers() -> DataFrame

# vector_store.py - Semantic search
WorkerVectorStore.search_workers() -> List[Dict]
WorkerVectorStore.index_workers() -> None

# tools.py - CrewAI tools
@tool search_workers_tool(query, exclude_zone) -> str
@tool get_worker_details_tool(worker_id) -> str

# agents.py - AI agents
skill_matcher_agent: Searches for matching workers
shift_planner_agent: Recommends best candidates

# tasks.py - Workflow tasks
create_skill_search_task() -> Task
create_shift_planning_task() -> Task

# app.py - Streamlit UI
main() -> None
```

### Adding New Features

1. **New Skills**: Add to workers.csv and re-index
2. **New Zones**: Update workers.csv with new zone assignments
3. **New Tools**: Add to tools.py and update agent definitions
4. **Custom Agents**: Define in agents.py with specific roles

## 🐛 Troubleshooting

### Common Issues

**Issue**: "WATSONX_API_KEY not set"
- **Solution**: Create `.env` file with your credentials

**Issue**: "Collection not initialized"
- **Solution**: Click "Initialize System" in the sidebar

**Issue**: "No workers found"
- **Solution**: Ensure workers.csv is in the correct location

**Issue**: Import errors
- **Solution**: Reinstall dependencies: `pip install -r requirements.txt`

### Debug Mode

Enable verbose logging by setting `verbose=True` in agent definitions.

## 📝 License

This project is part of the IBM watsonx.ai Call for Code challenge.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the technical implementation guide

## 🎯 Roadmap

- [ ] Multi-shift planning
- [ ] Historical analytics
- [ ] Mobile app interface
- [ ] Integration with existing WMS systems
- [ ] Advanced load prediction
- [ ] Worker preference consideration

## 🏆 Acknowledgments

- IBM watsonx.ai for LLM capabilities
- CrewAI for agent framework
- ChromaDB for vector storage
- Streamlit for UI framework

---

**Built with ❤️ for efficient warehouse operations**
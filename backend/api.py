"""
SmartShift FastAPI Backend
Provides REST API endpoints for the Next.js frontend.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from crewai import Crew, Process
import json

from data_loader import load_workers, get_worker_by_id
from tools import initialize_tools, search_workers_tool
from tasks import create_crew_tasks
from agents import skill_matcher_agent, shift_planner_agent

# Initialize FastAPI
app = FastAPI(
    title="SmartShift API",
    version="2.0",
    description="AI-Powered Warehouse Workforce Rebalancing System"
)

# CORS Configuration - Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app",
        "*"  # For development - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
workers_df: Optional[pd.DataFrame] = None
tools_initialized = False


# Pydantic Models for Request/Response
class RecommendationRequest(BaseModel):
    manager_input: str


class SearchRequest(BaseModel):
    query: str
    exclude_zone: Optional[str] = None


class Worker(BaseModel):
    worker_id: str
    name: str
    age: int
    primary_skill: str
    transferable_skills: str
    education: str
    physicality: str
    current_zone: str
    zone_function: str
    shift: str
    shift_hours: str
    load_status: str
    load_percentage: int
    available: str


# Startup event - Initialize system
@app.on_event("startup")
async def startup_event():
    """Initialize the system on startup."""
    global workers_df, tools_initialized
    
    try:
        print("🚀 Starting SmartShift API...")
        

        # Load workers data using absolute positioning
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        workers_df = load_workers(os.path.join(base_dir, "workers.csv"))
        
        # Initialize tools and vector store
        initialize_tools()
        tools_initialized = True
        print("✅ Tools and vector store initialized")
        
        print("✅ SmartShift API is ready!")
        
    except Exception as e:
        print(f"❌ Error during startup: {str(e)}")
        raise


# Root endpoint - Health check
@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "SmartShift API",
        "status": "running",
        "version": "2.0",
        "workers_loaded": workers_df is not None,
        "tools_initialized": tools_initialized
    }


# Get all workers
@app.get("/api/workers")
async def get_workers():
    """Get all workers from the database."""
    if workers_df is None:
        raise HTTPException(status_code=500, detail="Workers data not loaded")
    
    return workers_df.to_dict(orient="records")


# Get worker by ID
@app.get("/api/workers/{worker_id}")
async def get_worker(worker_id: str):
    """Get a specific worker by ID."""
    if workers_df is None:
        raise HTTPException(status_code=500, detail="Workers data not loaded")
    
    worker = get_worker_by_id(workers_df, worker_id)
    if worker is None:
        raise HTTPException(status_code=404, detail=f"Worker {worker_id} not found")
    
    return worker


# Get zone statistics
@app.get("/api/zones/{zone}")
async def get_zone_stats(zone: str):
    """Get statistics for a specific zone."""
    if workers_df is None:
        raise HTTPException(status_code=500, detail="Workers data not loaded")
    
    zone_workers = workers_df[workers_df['current_zone'] == zone]
    
    if zone_workers.empty:
        raise HTTPException(status_code=404, detail=f"No workers found in {zone}")
    
    stats = {
        "zone": zone,
        "total_workers": int(len(zone_workers)),
        "available_workers": int(len(zone_workers[zone_workers['available'] == 'Yes'])),
        "unavailable_workers": int(len(zone_workers[zone_workers['available'] == 'No'])),
        "load_distribution": {
            "low": int(len(zone_workers[zone_workers['load_status'] == 'Low'])),
            "medium": int(len(zone_workers[zone_workers['load_status'] == 'Medium'])),
            "high": int(len(zone_workers[zone_workers['load_status'] == 'High']))
        },
        "average_load_percentage": float(zone_workers['load_percentage'].mean()),
        "shifts": {
            "morning": int(len(zone_workers[zone_workers['shift'] == 'Morning'])),
            "afternoon": int(len(zone_workers[zone_workers['shift'] == 'Afternoon']))
        }
    }
    
    return stats


# Get all zones statistics
@app.get("/api/zones")
async def get_all_zones_stats():
    """Get statistics for all zones."""
    if workers_df is None:
        raise HTTPException(status_code=500, detail="Workers data not loaded")
    
    zones = ['Zone A', 'Zone B', 'Zone C', 'Zone D']
    all_stats = {}
    
    for zone in zones:
        zone_workers = workers_df[workers_df['current_zone'] == zone]
        if not zone_workers.empty:
            all_stats[zone] = {
                "total_workers": int(len(zone_workers)),
                "available_workers": int(len(zone_workers[zone_workers['available'] == 'Yes'])),
                "average_load_percentage": float(zone_workers['load_percentage'].mean())
            }
    
    return all_stats


# Search workers
@app.post("/api/search")
async def search_workers(request: SearchRequest):
    """Search for workers matching the skill query."""
    if not tools_initialized:
        raise HTTPException(status_code=500, detail="Tools not initialized")
    
    try:
        # Prepare the tool input payload dictionary
        tool_input = {"query": request.query}
        if request.exclude_zone:
            tool_input["exclude_zone"] = request.exclude_zone
            
        # Execute the CrewAI tool using the proper .run() interface
        result = search_workers_tool.run(tool_input)
        
        # If the tool natively returns parsed structures, yield them directly
        if isinstance(result, (dict, list)):
            return result
            
        return json.loads(result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching workers: {str(e)}")


# Get AI recommendations
@app.post("/api/recommendations")
async def get_recommendations(request: RecommendationRequest):
    """Get AI-powered worker recommendations for overload situation."""
    if not tools_initialized:
        raise HTTPException(status_code=500, detail="Tools not initialized")
    
    try:
        print(f"📝 Processing request: {request.manager_input}")
        
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
        print("🤖 Running AI agents...")
        result = crew.kickoff()
        print("✅ AI analysis complete")
        
        return {
            "status": "success",
            "recommendations": str(result),
            "input": request.manager_input
        }
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )


# System status endpoint
@app.get("/api/status")
async def get_status():
    """Get system status."""
    return {
        "workers_loaded": workers_df is not None,
        "total_workers": len(workers_df) if workers_df is not None else 0,
        "tools_initialized": tools_initialized,
        "api_version": "2.0"
    }


if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.getenv("BACKEND_PORT", 8000))
    
    print(f"🚀 Starting SmartShift API on port {port}...")
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )

# Made with Bob

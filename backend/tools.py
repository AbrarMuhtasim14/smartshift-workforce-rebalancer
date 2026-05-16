"""
Custom tools for CrewAI agents in SmartShift.
Provides tools for searching workers and getting worker details.
"""
from crewai.tools import tool
from vector_store import WorkerVectorStore
from data_loader import load_workers, get_worker_by_id
import json

# Initialize vector store and load workers
vector_store = WorkerVectorStore()
workers_df = None


def initialize_tools():
    """Initialize tools by loading workers and setting up vector store."""
    global workers_df, vector_store
    
    # Load workers
    workers_df = load_workers("workers.csv")
    print(f"Loaded {len(workers_df)} workers from CSV")
    
    # Initialize and index in vector store
    vector_store.initialize_collection()
    vector_store.index_workers(workers_df)
    print("Tools initialized successfully")


@tool("Search Workers Tool")
def search_workers_tool(query: str, exclude_zone: str = None) -> str:
    """
    Search for workers matching the skill query using semantic search.
    
    This tool searches the ChromaDB vector store to find workers whose skills
    match the query. It considers both primary and transferable skills.
    
    Args:
        query: Natural language description of needed skill (e.g., "forklift operator", 
               "packing specialist", "heavy equipment")
        exclude_zone: Zone to exclude from results (e.g., "Zone A", "Zone B"). 
                     Use this to exclude workers from the overloaded zone.
    
    Returns:
        JSON string containing list of matching workers with their full profiles
    
    Example:
        search_workers_tool("forklift operator", "Zone A")
        Returns workers with forklift skills who are NOT in Zone A
    """
    try:
        # Search for workers
        results = vector_store.search_workers(
            query=query, 
            exclude_zone=exclude_zone,
            n_results=5
        )
        
        if not results:
            return json.dumps({
                "status": "no_results",
                "message": f"No available workers found matching '{query}'",
                "workers": []
            })
        
        # Format results
        formatted_results = {
            "status": "success",
            "query": query,
            "excluded_zone": exclude_zone,
            "count": len(results),
            "workers": results
        }
        
        return json.dumps(formatted_results, indent=2)
    
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error searching workers: {str(e)}",
            "workers": []
        })


@tool("Get Worker Details Tool")
def get_worker_details_tool(worker_id: str) -> str:
    """
    Get full details of a specific worker by their ID.
    
    Use this tool when you need detailed information about a specific worker
    that was found in a search result.
    
    Args:
        worker_id: Worker ID (e.g., "W001", "W015")
    
    Returns:
        JSON string containing complete worker details
    
    Example:
        get_worker_details_tool("W001")
        Returns all details for worker W001
    """
    try:
        global workers_df
        
        if workers_df is None:
            return json.dumps({
                "status": "error",
                "message": "Workers data not loaded"
            })
        
        worker = get_worker_by_id(workers_df, worker_id)
        
        if worker is None:
            return json.dumps({
                "status": "not_found",
                "message": f"Worker {worker_id} not found"
            })
        
        return json.dumps({
            "status": "success",
            "worker": worker
        }, indent=2)
    
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error getting worker details: {str(e)}"
        })


@tool("Get Zone Statistics Tool")
def get_zone_statistics_tool(zone: str) -> str:
    """
    Get statistics about workers in a specific zone.
    
    Provides information about worker count, load distribution, and availability
    in the specified zone.
    
    Args:
        zone: Zone name (e.g., "Zone A", "Zone B", "Zone C", "Zone D")
    
    Returns:
        JSON string containing zone statistics
    
    Example:
        get_zone_statistics_tool("Zone A")
        Returns statistics for Zone A
    """
    try:
        global workers_df
        
        if workers_df is None:
            return json.dumps({
                "status": "error",
                "message": "Workers data not loaded"
            })
        
        zone_workers = workers_df[workers_df['current_zone'] == zone]
        
        if zone_workers.empty:
            return json.dumps({
                "status": "not_found",
                "message": f"No workers found in {zone}"
            })
        
        stats = {
            "status": "success",
            "zone": zone,
            "total_workers": len(zone_workers),
            "available_workers": len(zone_workers[zone_workers['available'] == 'Yes']),
            "unavailable_workers": len(zone_workers[zone_workers['available'] == 'No']),
            "load_distribution": {
                "low": len(zone_workers[zone_workers['load_status'] == 'Low']),
                "medium": len(zone_workers[zone_workers['load_status'] == 'Medium']),
                "high": len(zone_workers[zone_workers['load_status'] == 'High'])
            },
            "average_load_percentage": float(zone_workers['load_percentage'].mean()),
            "shifts": {
                "morning": len(zone_workers[zone_workers['shift'] == 'Morning']),
                "afternoon": len(zone_workers[zone_workers['shift'] == 'Afternoon'])
            }
        }
        
        return json.dumps(stats, indent=2)
    
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error getting zone statistics: {str(e)}"
        })

# Made with Bob

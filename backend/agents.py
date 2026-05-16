"""
CrewAI agents for SmartShift.
Defines the Skill Matcher Agent and Shift Planner Agent.
"""
from crewai import Agent
from config import llm
from tools import search_workers_tool, get_worker_details_tool, get_zone_statistics_tool


# Agent 1: Skill Matcher Agent
skill_matcher_agent = Agent(
    role="Warehouse Skill Search Specialist",
    goal="""Search the ChromaDB vector store to find workers whose primary or 
    transferable skills match the overload requirement. Filter out workers 
    already in the overloaded zone and those unavailable. Return 3-5 best 
    candidates with complete profiles.""",
    backstory="""You are an expert in warehouse workforce management with 10 years 
    of experience. You understand that skills like 'forklift' and 'heavy equipment' 
    are related, and 'packing' relates to 'order picking'. You excel at finding 
    the best available talent efficiently by considering both primary and 
    transferable skills. You always prioritize workers who are available and 
    not already overloaded. You understand the importance of matching the right 
    skill set to the zone's needs.""",
    tools=[search_workers_tool, get_worker_details_tool, get_zone_statistics_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=10
)


# Agent 2: Shift Planner Agent
shift_planner_agent = Agent(
    role="Warehouse Shift Planning Specialist",
    goal="""Take the candidates from Skill Matcher Agent and decide the top 2-3 
    best workers to recommend for rebalancing. Consider their education, 
    physicality, current load, transferable skill relevance, and impact on 
    their current zone. Produce clear, actionable recommendations with detailed 
    reasoning.""",
    backstory="""You are a seasoned warehouse operations manager with 15 years 
    of experience in workforce optimization. You make fair, efficient staffing 
    decisions based on multiple factors: worker capability, current workload, 
    skill match quality, physical fitness, and the impact on both source and 
    destination zones. You always explain your decisions clearly to floor 
    managers, providing specific reasons why each worker is recommended. You 
    consider the human element - ensuring workers aren't overworked and that 
    moves make operational sense. You prioritize workers with lower current 
    loads and strong skill matches.""",
    tools=[get_worker_details_tool, get_zone_statistics_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=10
)


def get_skill_matcher_agent() -> Agent:
    """
    Get the Skill Matcher Agent instance.
    
    Returns:
        Configured Skill Matcher Agent
    """
    return skill_matcher_agent


def get_shift_planner_agent() -> Agent:
    """
    Get the Shift Planner Agent instance.
    
    Returns:
        Configured Shift Planner Agent
    """
    return shift_planner_agent

# Made with Bob

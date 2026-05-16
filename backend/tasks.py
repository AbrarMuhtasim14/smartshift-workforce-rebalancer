"""
CrewAI tasks for SmartShift.
Defines the workflow tasks for skill search and shift planning.
"""
from crewai import Task
from agents import skill_matcher_agent, shift_planner_agent


def create_skill_search_task(manager_input: str) -> Task:
    """
    Create skill search task for finding matching workers.
    
    Args:
        manager_input: Natural language input from the manager describing the overload
        
    Returns:
        Configured Task for skill searching
    """
    return Task(
        description=f"""Given the manager input: '{manager_input}', 
        identify the skill needed and search ChromaDB for workers who match.
        
        Your task is to:
        1. Parse the input to identify the overloaded zone (e.g., "Zone A", "Zone B")
        2. Extract the skill requirement (e.g., "forklift", "packing", "quality inspector")
        3. Use the search_workers_tool to find matching workers
           - Search for workers with the required skill (primary or transferable)
           - Exclude workers from the overloaded zone
           - Only consider available workers
        4. Review the search results and select 3-5 best candidates
        5. For each candidate, gather their complete profile including:
           - Worker ID and name
           - Primary skill and transferable skills
           - Current zone and function
           - Load status and percentage
           - Education and physicality
           - Shift information
        
        Return a detailed list of 3-5 candidate worker profiles with all their 
        information. Focus on workers who:
        - Have the required skill (primary or transferable)
        - Are currently available
        - Are NOT in the overloaded zone
        - Have reasonable current workload (prefer Low or Medium load)
        
        Format your output as a structured list with complete worker details.""",
        agent=skill_matcher_agent,
        expected_output="""A detailed list of 3-5 candidate worker profiles including:
        - Worker ID and full name
        - Primary skill and all transferable skills
        - Current zone and zone function
        - Load status (Low/Medium/High) and load percentage
        - Education and certifications
        - Physical fitness and restrictions
        - Current shift and hours
        - Availability status
        
        Each candidate should be clearly numbered and include all relevant details 
        that will help the Shift Planner make informed decisions."""
    )


def create_shift_planning_task() -> Task:
    """
    Create shift planning task for selecting best workers.
    
    Returns:
        Configured Task for shift planning
    """
    return Task(
        description="""Review the shortlisted candidates from the Skill Matcher Agent.
        Your task is to select the top 2-3 best workers to recommend for the shift change.
        
        For each candidate, analyze:
        1. Skill Match Quality:
           - Is the required skill their primary skill or transferable skill?
           - How relevant is their experience?
           - Do they have related certifications?
        
        2. Current Workload:
           - What is their current load status (Low/Medium/High)?
           - What is their load percentage?
           - Can they handle additional work?
        
        3. Physical Capability:
           - Does their physicality match the job requirements?
           - Are there any restrictions?
           - Do they have necessary certifications (forklift, heavy lifting, etc.)?
        
        4. Education and Experience:
           - What is their education level?
           - Do they have relevant certifications?
           - What does their experience suggest?
        
        5. Impact Analysis:
           - What zone are they currently in?
           - What is their current function?
           - How will moving them affect their current zone?
        
        Rank the candidates and select the top 2-3 workers. For each recommendation, 
        provide:
        - Worker ID and name
        - Clear explanation of why they are recommended
        - Specific skill match details (primary or transferable)
        - Current zone and load status
        - Education and physicality highlights
        - Impact assessment on both zones
        - Any concerns or considerations
        
        Write your recommendations in clear, plain English that a warehouse floor 
        manager can understand and act upon immediately. Be specific and actionable.
        
        Format your final output as:
        RECOMMENDATION 1: [Worker ID - Name]
        - Why recommended: [clear explanation]
        - Skill match: [details]
        - Current status: [zone, load, availability]
        - Key qualifications: [education, physicality]
        - Impact: [effect on current and target zones]
        
        RECOMMENDATION 2: [Worker ID - Name]
        [same structure]
        
        RECOMMENDATION 3: [Worker ID - Name] (if applicable)
        [same structure]
        
        SUMMARY:
        [Brief summary of the recommended shift changes and expected outcomes]""",
        agent=shift_planner_agent,
        expected_output="""Top 2-3 ranked worker recommendations with detailed explanations.
        
        Each recommendation must include:
        1. Worker identification (ID and name)
        2. Clear reasoning for selection
        3. Skill match analysis (primary vs transferable)
        4. Current zone and workload status
        5. Relevant qualifications (education, certifications, physicality)
        6. Impact assessment on both source and destination zones
        7. Any concerns or special considerations
        
        The output should be formatted as numbered recommendations with clear sections,
        followed by a summary of the proposed shift changes and expected benefits.
        
        The language should be professional but accessible, suitable for immediate
        action by warehouse floor managers.""",
        context=[create_skill_search_task("placeholder")]  # Will be replaced with actual task
    )


def create_crew_tasks(manager_input: str) -> list:
    """
    Create the complete list of tasks for the crew.
    
    Args:
        manager_input: Natural language input from the manager
        
    Returns:
        List of configured tasks in execution order
    """
    skill_search_task = create_skill_search_task(manager_input)
    shift_planning_task = create_shift_planning_task()
    
    # Set context for shift planning task
    shift_planning_task.context = [skill_search_task]
    
    return [skill_search_task, shift_planning_task]

# Made with Bob

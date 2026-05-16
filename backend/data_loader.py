"""
Data loader module for SmartShift.
Handles CSV data management and worker data operations.
"""
import pandas as pd
from typing import List, Dict, Optional


def load_workers(csv_path: str = "workers.csv") -> pd.DataFrame:
    """
    Load workers from CSV file.
    
    Args:
        csv_path: Path to the workers CSV file
        
    Returns:
        DataFrame containing worker data
    """
    df = pd.read_csv(csv_path)
    return df


def validate_workers(df: pd.DataFrame) -> bool:
    """
    Validate worker data integrity.
    
    Args:
        df: DataFrame containing worker data
        
    Returns:
        True if all required columns are present, False otherwise
    """
    required_columns = [
        'worker_id', 'name', 'age', 'primary_skill',
        'transferable_skills', 'education', 'physicality',
        'current_zone', 'zone_function', 'shift', 'shift_hours',
        'load_status', 'load_percentage', 'available'
    ]
    return all(col in df.columns for col in required_columns)


def get_worker_by_id(df: pd.DataFrame, worker_id: str) -> Optional[Dict]:
    """
    Get worker by ID.
    
    Args:
        df: DataFrame containing worker data
        worker_id: Worker ID to search for
        
    Returns:
        Dictionary containing worker data or None if not found
    """
    worker = df[df['worker_id'] == worker_id]
    if not worker.empty:
        return worker.iloc[0].to_dict()
    return None


def get_workers_by_zone(df: pd.DataFrame, zone: str) -> pd.DataFrame:
    """
    Filter workers by zone.
    
    Args:
        df: DataFrame containing worker data
        zone: Zone to filter by (e.g., "Zone A")
        
    Returns:
        DataFrame containing workers in the specified zone
    """
    return df[df['current_zone'] == zone]


def get_available_workers(df: pd.DataFrame, exclude_zone: str = None) -> pd.DataFrame:
    """
    Get available workers, optionally excluding a zone.
    
    Args:
        df: DataFrame containing worker data
        exclude_zone: Zone to exclude from results (optional)
        
    Returns:
        DataFrame containing available workers
    """
    available = df[df['available'] == 'Yes']
    if exclude_zone:
        available = available[available['current_zone'] != exclude_zone]
    return available


def parse_transferable_skills(skills_str: str) -> List[str]:
    """
    Parse comma-separated transferable skills.
    
    Args:
        skills_str: Comma-separated string of skills
        
    Returns:
        List of individual skills
    """
    return [s.strip() for s in skills_str.split(',')]


def get_workers_by_skill(df: pd.DataFrame, skill: str) -> pd.DataFrame:
    """
    Get workers who have a specific skill (primary or transferable).
    
    Args:
        df: DataFrame containing worker data
        skill: Skill to search for
        
    Returns:
        DataFrame containing workers with the specified skill
    """
    # Search in primary skill
    primary_match = df[df['primary_skill'].str.contains(skill, case=False, na=False)]
    
    # Search in transferable skills
    transferable_match = df[df['transferable_skills'].str.contains(skill, case=False, na=False)]
    
    # Combine and remove duplicates
    combined = pd.concat([primary_match, transferable_match]).drop_duplicates()
    return combined


def get_low_load_workers(df: pd.DataFrame, max_load: int = 50) -> pd.DataFrame:
    """
    Get workers with load percentage below threshold.
    
    Args:
        df: DataFrame containing worker data
        max_load: Maximum load percentage threshold
        
    Returns:
        DataFrame containing workers with low load
    """
    return df[df['load_percentage'] <= max_load]


def update_worker_zone(df: pd.DataFrame, worker_id: str, new_zone: str, new_function: str) -> pd.DataFrame:
    """
    Update a worker's zone and function.
    
    Args:
        df: DataFrame containing worker data
        worker_id: Worker ID to update
        new_zone: New zone assignment
        new_function: New zone function
        
    Returns:
        Updated DataFrame
    """
    df.loc[df['worker_id'] == worker_id, 'current_zone'] = new_zone
    df.loc[df['worker_id'] == worker_id, 'zone_function'] = new_function
    return df


def save_workers(df: pd.DataFrame, csv_path: str = "workers.csv") -> None:
    """
    Save workers DataFrame to CSV file.
    
    Args:
        df: DataFrame containing worker data
        csv_path: Path to save the CSV file
    """
    df.to_csv(csv_path, index=False)

# Made with Bob

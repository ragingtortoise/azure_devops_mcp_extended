"""
Work item state transition functions.
"""

from typing import Any, Dict, List, Optional

from .client import AzureDevOpsClient
from .config import Config


# DEPRECATED: Hardcoded state mappings
# This dict is no longer used by the library - states are now discovered dynamically.
# Kept for backward compatibility reference only.
WORK_ITEM_STATES = {
    "Bug": ["New", "Development", "Released", "Not a Bug"],
    "Epic": ["New", "Active", "Closed", "Removed"],
    "Feature": ["Ideation", "New", "Development", "Released", "Removed"],
    "User Story": ["New", "Development", "Released", "Removed"],
    "Task": ["New", "Active", "Done", "Removed"],
    "Issue": ["Active", "Closed"],
}


def transition_to_new(
    work_item_id: int,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Transition work item to 'New' state.
    
    Convenience wrapper for transition_state(). For dynamic state discovery,
    use get_available_states() first to check valid states.
    
    Args:
        work_item_id: Work item ID
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(work_item_id, {"System.State": "New"})


def transition_to_active(
    work_item_id: int,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Transition work item to 'Active' state.
    
    Convenience wrapper for transition_state(). For dynamic state discovery,
    use get_available_states() first to check valid states.
    
    Args:
        work_item_id: Work item ID
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(work_item_id, {"System.State": "Active"})


def transition_to_development(
    work_item_id: int,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Transition work item to 'Development' state.
    
    Convenience wrapper for transition_state(). For dynamic state discovery,
    use get_available_states() first to check valid states.
    
    Args:
        work_item_id: Work item ID
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(work_item_id, {"System.State": "Development"})


def transition_to_ideation(
    work_item_id: int,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Transition work item to 'Ideation' state (Features only).
    
    Convenience wrapper for transition_state(). For dynamic state discovery,
    use get_available_states() first to check valid states.
    
    Args:
        work_item_id: Work item ID
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(work_item_id, {"System.State": "Ideation"})


def transition_to_resolved(
    work_item_id: int,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Transition work item to 'Resolved' state.
    
    Convenience wrapper for transition_state(). For dynamic state discovery,
    use get_available_states() first to check valid states.
    
    Args:
        work_item_id: Work item ID
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(work_item_id, {"System.State": "Resolved"})


def transition_to_released(
    work_item_id: int,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Transition work item to 'Released' state.
    
    Convenience wrapper for transition_state(). For dynamic state discovery,
    use get_available_states() first to check valid states.
    
    Args:
        work_item_id: Work item ID
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(work_item_id, {"System.State": "Released"})


def transition_to_done(
    work_item_id: int,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Transition work item to 'Done' state (Tasks only).
    
    Convenience wrapper for transition_state(). For dynamic state discovery,
    use get_available_states() first to check valid states.
    
    Args:
        work_item_id: Work item ID
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(work_item_id, {"System.State": "Done"})


def transition_to_not_a_bug(
    work_item_id: int,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Transition work item to 'Not a Bug' state (Bugs only).
    
    Convenience wrapper for transition_state(). For dynamic state discovery,
    use get_available_states() first to check valid states.
    
    Args:
        work_item_id: Work item ID
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(work_item_id, {"System.State": "Not a Bug"})


def transition_to_closed(
    work_item_id: int,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Transition work item to 'Closed' state.
    
    Convenience wrapper for transition_state(). For dynamic state discovery,
    use get_available_states() first to check valid states.
    
    Args:
        work_item_id: Work item ID
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(work_item_id, {"System.State": "Closed"})


def transition_to_removed(
    work_item_id: int,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Transition work item to 'Removed' state.
    
    Convenience wrapper for transition_state(). For dynamic state discovery,
    use get_available_states() first to check valid states.
    
    Args:
        work_item_id: Work item ID
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(work_item_id, {"System.State": "Removed"})


def transition_state(
    work_item_id: int,
    state: str,
    config: Optional[Config] = None,
    validate: bool = True,
) -> Dict[str, Any]:
    """
    Transition work item to a specific state with optional validation.
    
    Args:
        work_item_id: Work item ID
        state: Target state name
        config: Optional Config instance
        validate: Whether to validate state exists for work item type (default: True)
        
    Returns:
        Updated work item data
        
    Raises:
        ValueError: If state is invalid for the work item type (when validate=True)
    """
    client = AzureDevOpsClient(config)
    
    # Validate state if requested
    if validate:
        available = get_available_states(work_item_id, config)
        if state not in available:
            # Get work item type for better error message
            work_item = client.get_work_item(work_item_id, fields=["System.WorkItemType"])
            work_item_type = work_item["fields"]["System.WorkItemType"]
            
            available_str = ", ".join(available)
            raise ValueError(
                f"Invalid state '{state}' for {work_item_type}. "
                f"Available states: {available_str}"
            )
    
    return client.update_work_item(work_item_id, {"System.State": state})


def get_available_states(
    work_item_id: int,
    config: Optional[Config] = None,
) -> List[str]:
    """
    Get available states for a work item based on its type.
    
    Args:
        work_item_id: Work item ID
        config: Optional Config instance
        
    Returns:
        List of available state names
    """
    client = AzureDevOpsClient(config)
    
    # Get the work item to find its type
    work_item = client.get_work_item(work_item_id, fields=["System.WorkItemType"])
    work_item_type = work_item["fields"]["System.WorkItemType"]
    
    # Get states from the work item type definition
    try:
        states = client.get_work_item_type_states(work_item_type)
        return [state["name"] for state in states]
    except Exception:
        # Fallback to generic states if API call fails
        return ["New", "Active", "Resolved", "Closed", "Removed"]


def get_available_states_for_type(
    work_item_type: str,
    config: Optional[Config] = None,
) -> List[str]:
    """
    Get available states for a specific work item type.
    
    Args:
        work_item_type: Work item type name (e.g., "User Story", "Bug", "Task")
        config: Optional Config instance
        
    Returns:
        List of available state names
    """
    client = AzureDevOpsClient(config)
    
    try:
        states = client.get_work_item_type_states(work_item_type)
        return [state["name"] for state in states]
    except Exception:
        # Fallback to generic states if API call fails
        return ["New", "Active", "Resolved", "Closed", "Removed"]

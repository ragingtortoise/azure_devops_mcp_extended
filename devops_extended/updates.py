"""
Work item update functions.
"""

from typing import Any, Dict, Optional

from .client import AzureDevOpsClient
from .config import Config


def _format_html_text(text: str) -> str:
    """
    Convert plain text with newlines to HTML format.
    
    If text already contains HTML tags, return as-is.
    Otherwise, convert newlines to <br> tags for proper rendering.
    Double newlines become paragraph breaks.
    
    Args:
        text: Input text (plain or HTML)
        
    Returns:
        HTML-formatted text
    """
    if not text:
        return text
    
    # Check if text already contains HTML tags
    if '<' in text and '>' in text:
        return text
    
    # Convert newlines to HTML breaks
    # Single newline → <br><br> (visible break)
    # Double newline → <br><br><br><br> (paragraph break)
    text = text.replace('\n\n', '<br><br><br><br>')
    text = text.replace('\n', '<br><br>')
    
    return text


def update_work_item(
    work_item_id: int,
    fields: Dict[str, Any],
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Update multiple fields of a work item.
    
    Args:
        work_item_id: Work item ID
        fields: Dictionary of field updates (e.g., {"System.Title": "New Title"})
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(work_item_id, fields)


def update_title(
    work_item_id: int,
    title: str,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Update the title of a work item.
    
    Args:
        work_item_id: Work item ID
        title: New title
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(work_item_id, {"System.Title": title})


def update_description(
    work_item_id: int,
    description: str,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Update the description of a work item.
    
    Args:
        work_item_id: Work item ID
        description: New description (HTML supported, newlines auto-converted)
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(work_item_id, {"System.Description": _format_html_text(description)})


def assign_work_item(
    work_item_id: int,
    assigned_to: str,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Assign a work item to a user.
    
    Args:
        work_item_id: Work item ID
        assigned_to: Email or display name of assignee
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(work_item_id, {"System.AssignedTo": assigned_to})


def update_priority(
    work_item_id: int,
    priority: int,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Update the priority of a work item.
    
    Args:
        work_item_id: Work item ID
        priority: Priority value (1-4, where 1 is highest)
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(
        work_item_id,
        {"Microsoft.VSTS.Common.Priority": priority}
    )


def update_effort(
    work_item_id: int,
    effort: int,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Update the effort/story points of a work item.
    
    Args:
        work_item_id: Work item ID
        effort: Effort/story points
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(
        work_item_id,
        {"Microsoft.VSTS.Scheduling.Effort": effort}
    )


def update_tags(
    work_item_id: int,
    tags: str,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Update the tags of a work item.
    
    Args:
        work_item_id: Work item ID
        tags: Comma-separated tags
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(work_item_id, {"System.Tags": tags})


def update_area_path(
    work_item_id: int,
    area_path: str,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Update the area path of a work item.
    
    Args:
        work_item_id: Work item ID
        area_path: Area path (e.g., "ProjectName\\Area")
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(work_item_id, {"System.AreaPath": area_path})


def update_iteration_path(
    work_item_id: int,
    iteration_path: str,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Update the iteration path of a work item.
    
    Args:
        work_item_id: Work item ID
        iteration_path: Iteration path (e.g., "ProjectName\\Sprint 1")
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.update_work_item(
        work_item_id,
        {"System.IterationPath": iteration_path}
    )


def add_comment(
    work_item_id: int,
    comment: str,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Add a comment to a work item.
    
    Args:
        work_item_id: Work item ID
        comment: Comment text
        config: Optional Config instance
        
    Returns:
        Comment data
    """
    client = AzureDevOpsClient(config)
    return client.add_comment(work_item_id, comment)


def add_parent_link(
    child_id: int,
    parent_id: int,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Add a parent link to a work item.
    
    Args:
        child_id: Child work item ID
        parent_id: Parent work item ID
        config: Optional Config instance
        
    Returns:
        Updated work item data
    """
    client = AzureDevOpsClient(config)
    return client.add_parent_link(child_id, parent_id)

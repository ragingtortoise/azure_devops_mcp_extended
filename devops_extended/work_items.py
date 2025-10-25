"""
Work item creation functions for various work item types.
"""

from typing import Any, Dict, Optional, Union

from .client import AzureDevOpsClient
from .config import Config
from .type_resolver import get_resolver


def create_work_item(
    work_item_type: str,
    title: str,
    description: Optional[str] = None,
    assigned_to: Optional[str] = None,
    area_path: Optional[str] = None,
    iteration_path: Optional[str] = None,
    priority: Optional[int] = None,
    tags: Optional[str] = None,
    parent_id: Optional[int] = None,
    state: Optional[str] = None,
    # Common backlog item fields
    effort: Optional[int] = None,
    story_points: Optional[int] = None,
    value_area: Optional[str] = None,
    # Bug-specific fields
    repro_steps: Optional[str] = None,
    system_info: Optional[str] = None,
    severity: Optional[str] = None,
    # Task-specific fields
    activity: Optional[str] = None,
    remaining_work: Optional[float] = None,
    original_estimate: Optional[float] = None,
    # Feature/Epic fields
    target_date: Optional[str] = None,
    start_date: Optional[str] = None,
    # Team assignment
    team: Optional[str] = None,
    # Additional custom fields
    custom_fields: Optional[Dict[str, Any]] = None,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Create a work item of any type.
    
    This is a unified creation function that works with any work item type
    (Bug, User Story, Task, Feature, Epic, or custom types).
    
    Args:
        work_item_type: Work item type name (e.g., "Bug", "User Story", "Task", "MyCustomType")
        title: Work item title
        description: Detailed description (HTML supported)
        assigned_to: Email or display name of assignee
        area_path: Area path (e.g., "ProjectName\\Area")
        iteration_path: Iteration path (e.g., "ProjectName\\Sprint 1")
        priority: Priority (1-4, where 1 is highest)
        tags: Comma-separated tags
        parent_id: Parent work item ID for hierarchical linking
        state: Initial state (e.g., "New", "Active", "Ideation")
        effort: Story points/effort estimate (for backlog items)
        story_points: Story points (alternative to effort)
        value_area: Business or Architectural
        repro_steps: Steps to reproduce (for bugs)
        system_info: System information (for bugs)
        severity: Bug severity (1-4, where 1 is critical)
        activity: Activity type (for tasks, e.g., "Development", "Testing")
        remaining_work: Remaining work in hours (for tasks)
        original_estimate: Original estimate in hours (for tasks)
        target_date: Target date in ISO format (YYYY-MM-DD)
        start_date: Start date in ISO format (YYYY-MM-DD)
        team: Team key to assign to team's board
        custom_fields: Dictionary of custom field reference names to values (e.g., {"Custom.FieldName": "value"})
        config: Optional Config instance
        
    Returns:
        Created work item data including ID and URL
        
    Example:
        # Create a bug
        create_work_item("Bug", "Login fails", severity="1", repro_steps="Click login button")
        
        # Create a user story
        create_work_item("User Story", "Add search", effort=5, priority=1)
        
        # Create a custom type
        create_work_item("Custom Requirement", "My requirement", custom_fields={"Custom.Field": "value"})
    """
    client = AzureDevOpsClient(config)
    
    fields: Dict[str, Union[str, int, float]] = {
        "System.Title": title,
    }
    
    # Core fields
    if description:
        fields["System.Description"] = _format_html_text(description)
    if assigned_to:
        fields["System.AssignedTo"] = assigned_to
    if priority:
        fields["Microsoft.VSTS.Common.Priority"] = priority
    if tags:
        fields["System.Tags"] = tags
    if state:
        fields["System.State"] = state
    
    # Area path with team support
    if area_path:
        fields["System.AreaPath"] = area_path
    elif team and client.config.project:
        fields["System.AreaPath"] = client.config.project
    
    if iteration_path:
        fields["System.IterationPath"] = iteration_path
    
    # Backlog item fields
    if effort:
        fields["Microsoft.VSTS.Scheduling.Effort"] = effort
    if story_points:
        fields["Microsoft.VSTS.Scheduling.StoryPoints"] = story_points
    if value_area:
        fields["Microsoft.VSTS.Common.ValueArea"] = value_area
    
    # Bug fields
    if repro_steps:
        fields["Microsoft.VSTS.TCM.ReproSteps"] = _format_html_text(repro_steps)
    if system_info:
        fields["Microsoft.VSTS.TCM.SystemInfo"] = _format_html_text(system_info)
    if severity:
        # Convert severity to Azure DevOps format if it's a number
        severity_map = {
            "1": "1 - Critical",
            "2": "2 - High",
            "3": "3 - Medium",
            "4": "4 - Low",
            1: "1 - Critical",
            2: "2 - High",
            3: "3 - Medium",
            4: "4 - Low"
        }
        fields["Microsoft.VSTS.Common.Severity"] = severity_map.get(severity, severity)
    
    # Task fields
    if activity:
        fields["Microsoft.VSTS.Common.Activity"] = activity
    if remaining_work is not None:
        fields["Microsoft.VSTS.Scheduling.RemainingWork"] = remaining_work
    if original_estimate is not None:
        fields["Microsoft.VSTS.Scheduling.OriginalEstimate"] = original_estimate
    
    # Feature/Epic fields
    if target_date:
        fields["Microsoft.VSTS.Scheduling.TargetDate"] = target_date
    if start_date:
        fields["Microsoft.VSTS.Scheduling.StartDate"] = start_date
    
    # Custom fields
    if custom_fields:
        fields.update(custom_fields)
    
    # Create the work item
    result = client.create_work_item(work_item_type, fields)
    
    # Add parent link if specified
    if parent_id:
        client.add_parent_link(result["id"], parent_id)
    
    return result


def _format_html_text(text: str) -> str:
    """
    Convert plain text with newlines to HTML format.
    
    If text already contains HTML block-level tags, return as-is.
    Otherwise, convert newlines to <br> tags for proper rendering.
    Double newlines become paragraph breaks.
    
    Args:
        text: Input text (plain or HTML)
        
    Returns:
        HTML-formatted text
    """
    if not text:
        return text
    
    # Check if text already contains HTML block-level tags (not just <br>)
    html_block_tags = ['<div', '<p>', '<ul', '<ol', '<table', '<h1', '<h2', '<h3', '<h4', '<h5', '<h6']
    if any(tag in text.lower() for tag in html_block_tags):
        return text
    
    # Convert newlines to HTML breaks
    # Single newline → <br><br> (visible break)
    # Double newline → <br><br><br><br> (paragraph break)
    text = text.replace('\n\n', '<br><br><br><br>')
    text = text.replace('\n', '<br><br>')
    
    return text


def create_pbi(
    title: str,
    description: Optional[str] = None,
    priority: Optional[int] = None,
    effort: Optional[int] = None,
    value_area: Optional[str] = None,
    tags: Optional[str] = None,
    assigned_to: Optional[str] = None,
    area_path: Optional[str] = None,
    iteration_path: Optional[str] = None,
    parent_id: Optional[int] = None,
    work_item_type: Optional[str] = None,
    team: Optional[str] = None,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Create a Product Backlog Item (PBI/User Story/Issue).
    
    Auto-detects the correct work item type based on your project's process template:
    - Scrum: "Product Backlog Item"
    - Agile: "User Story"
    - Basic: "Issue"
    - CMMI: "Requirement"
    
    Args:
        title: PBI title
        description: Detailed description (HTML supported)
        priority: Priority (1-4, where 1 is highest)
        effort: Story points/effort estimate
        value_area: Business or Architectural
        tags: Comma-separated tags
        assigned_to: Email or display name of assignee
        area_path: Area path (e.g., "ProjectName\\Area") - overrides team
        iteration_path: Iteration path (e.g., "ProjectName\\Sprint 1")
        parent_id: Optional parent work item ID (e.g., Epic or Feature ID)
        work_item_type: Optional explicit type name to override auto-detection
        team: Team/board key (e.g., "frontend", "backend", "mobile") - auto-sets area_path
        config: Optional Config instance
        
    Returns:
        Created PBI data including ID and URL
    """
    client = AzureDevOpsClient(config)
    resolver = get_resolver(config)
    
    # Resolve the actual work item type name
    resolved_type = resolver.resolve_backlog_item(prefer=work_item_type)
    
    fields: Dict[str, Union[str, int, float]] = {
        "System.Title": title,
    }
    
    if description:
        fields["System.Description"] = _format_html_text(description)
    if priority:
        fields["Microsoft.VSTS.Common.Priority"] = priority
    if effort:
        fields["Microsoft.VSTS.Scheduling.Effort"] = effort
    if value_area:
        fields["Microsoft.VSTS.Common.ValueArea"] = value_area
    if tags:
        fields["System.Tags"] = tags
    if assigned_to:
        fields["System.AssignedTo"] = assigned_to
    
    # Handle area path with team support
    if area_path:
        # Explicit area path takes precedence
        fields["System.AreaPath"] = area_path
    elif team and client.config.project:
        # Team parameter provided but not mapped - use project root
        # For custom team mapping, set area_path explicitly
        fields["System.AreaPath"] = client.config.project
    
    if iteration_path:
        fields["System.IterationPath"] = iteration_path
    
    # Create the work item
    result = client.create_work_item(resolved_type, fields)
    
    # Add parent link if specified
    if parent_id:
        client.add_parent_link(result["id"], parent_id)
    
    return result


def create_bug(
    title: str,
    repro_steps: Optional[str] = None,
    system_info: Optional[str] = None,
    severity: Optional[str] = None,
    priority: Optional[int] = None,
    tags: Optional[str] = None,
    assigned_to: Optional[str] = None,
    area_path: Optional[str] = None,
    iteration_path: Optional[str] = None,
    parent_id: Optional[int] = None,
    work_item_type: Optional[str] = None,
    team: Optional[str] = None,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Create a Bug work item.
    
    Args:
        title: Bug title
        repro_steps: Steps to reproduce (HTML supported)
        system_info: System information where bug occurs
        severity: Bug severity (1 - Critical, 2 - High, 3 - Medium, 4 - Low)
        priority: Priority (1-4, where 1 is highest)
        tags: Comma-separated tags
        assigned_to: Email or display name of assignee
        area_path: Area path
        iteration_path: Iteration path
        parent_id: Optional parent work item ID
        work_item_type: Optional explicit type name to override auto-detection
        config: Optional Config instance
        
    Returns:
        Created Bug data including ID and URL
    """
    client = AzureDevOpsClient(config)
    resolver = get_resolver(config)
    
    # Resolve the actual work item type name
    resolved_type = resolver.resolve_bug(prefer=work_item_type)
    
    fields: Dict[str, Union[str, int, float]] = {
        "System.Title": title,
    }
    
    if repro_steps:
        fields["Microsoft.VSTS.TCM.ReproSteps"] = _format_html_text(repro_steps)
    if system_info:
        fields["Microsoft.VSTS.TCM.SystemInfo"] = _format_html_text(system_info)
    if severity:
        # Convert severity to Azure DevOps format if it's a number
        severity_map = {
            "1": "1 - Critical",
            "2": "2 - High",
            "3": "3 - Medium",
            "4": "4 - Low",
            1: "1 - Critical",
            2: "2 - High",
            3: "3 - Medium",
            4: "4 - Low"
        }
        fields["Microsoft.VSTS.Common.Severity"] = severity_map.get(severity, severity)
    if priority:
        fields["Microsoft.VSTS.Common.Priority"] = priority
    if tags:
        fields["System.Tags"] = tags
    if assigned_to:
        fields["System.AssignedTo"] = assigned_to
    
    # Handle area path with team support
    if area_path:
        # Explicit area path takes precedence
        fields["System.AreaPath"] = area_path
    elif team and client.config.project:
        # Team parameter provided but not mapped - use project root
        # For custom team mapping, set area_path explicitly
        fields["System.AreaPath"] = client.config.project
    
    if iteration_path:
        fields["System.IterationPath"] = iteration_path
    
    # Create the work item
    result = client.create_work_item(resolved_type, fields)
    
    # Add parent link if specified
    if parent_id:
        client.add_parent_link(result["id"], parent_id)
    
    return result


def create_task(
    title: str,
    description: Optional[str] = None,
    activity: Optional[str] = None,
    remaining_work: Optional[float] = None,
    original_estimate: Optional[float] = None,
    tags: Optional[str] = None,
    assigned_to: Optional[str] = None,
    area_path: Optional[str] = None,
    iteration_path: Optional[str] = None,
    parent_id: Optional[int] = None,
    work_item_type: Optional[str] = None,
    team: Optional[str] = None,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Create a Task work item.
    
    Args:
        title: Task title
        description: Task description (HTML supported)
        activity: Activity type (e.g., "Development", "Testing", "Documentation")
        remaining_work: Remaining work in hours
        original_estimate: Original estimate in hours
        tags: Comma-separated tags
        assigned_to: Email or display name of assignee
        area_path: Area path
        iteration_path: Iteration path
        parent_id: Optional parent work item ID
        work_item_type: Optional explicit type name to override auto-detection
        team: Optional team key (e.g., "frontend", "backend", "mobile") to assign work item to team's board
        config: Optional Config instance
        
    Returns:
        Created Task data including ID and URL
    """
    client = AzureDevOpsClient(config)
    resolver = get_resolver(config)
    
    # Resolve the actual work item type name
    resolved_type = resolver.resolve_task(prefer=work_item_type)
    
    fields: Dict[str, Union[str, int, float]] = {
        "System.Title": title,
    }
    
    if description:
        fields["System.Description"] = _format_html_text(description)
    if activity:
        fields["Microsoft.VSTS.Common.Activity"] = activity
    if remaining_work is not None:
        fields["Microsoft.VSTS.Scheduling.RemainingWork"] = remaining_work
    if original_estimate is not None:
        fields["Microsoft.VSTS.Scheduling.OriginalEstimate"] = original_estimate
    if tags:
        fields["System.Tags"] = tags
    if assigned_to:
        fields["System.AssignedTo"] = assigned_to
    
    # Handle area path with team support
    if area_path:
        # Explicit area path takes precedence
        fields["System.AreaPath"] = area_path
    elif team and client.config.project:
        # Team parameter provided but not mapped - use project root
        # For custom team mapping, set area_path explicitly
        fields["System.AreaPath"] = client.config.project
    
    if iteration_path:
        fields["System.IterationPath"] = iteration_path
    
    # Create the work item
    result = client.create_work_item(resolved_type, fields)
    
    # Add parent link if specified
    if parent_id:
        client.add_parent_link(result["id"], parent_id)
    
    return result


def create_feature(
    title: str,
    description: Optional[str] = None,
    priority: Optional[int] = None,
    value_area: Optional[str] = None,
    target_date: Optional[str] = None,
    tags: Optional[str] = None,
    assigned_to: Optional[str] = None,
    area_path: Optional[str] = None,
    iteration_path: Optional[str] = None,
    parent_id: Optional[int] = None,
    work_item_type: Optional[str] = None,
    team: Optional[str] = None,
    ideation: bool = False,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Create a Feature work item.
    
    Args:
        title: Feature title
        description: Feature description (HTML supported)
        priority: Priority (1-4, where 1 is highest)
        value_area: Value area (Business/Architectural)
        target_date: Target date in ISO format (YYYY-MM-DD)
        tags: Comma-separated tags
        assigned_to: Email or display name of assignee
        area_path: Area path
        iteration_path: Iteration path
        parent_id: Optional parent work item ID (e.g., Epic ID)
        work_item_type: Optional explicit type name to override auto-detection
        team: Optional team key (e.g., "frontend", "backend", "mobile") to assign work item to team's board
        ideation: If True, create in "Ideation" state (for quick ideas/notes). Otherwise creates in "New" state.
        config: Optional Config instance
        
    Returns:
        Created Feature data including ID and URL
    """
    client = AzureDevOpsClient(config)
    resolver = get_resolver(config)
    
    # Resolve the actual work item type name
    resolved_type = resolver.resolve_feature(prefer=work_item_type)
    
    fields: Dict[str, Union[str, int, float]] = {
        "System.Title": title,
    }
    
    # Set initial state based on ideation flag
    if ideation:
        fields["System.State"] = "Ideation"
    
    if description:
        fields["System.Description"] = _format_html_text(description)
    if priority:
        fields["Microsoft.VSTS.Common.Priority"] = priority
    if value_area:
        fields["Microsoft.VSTS.Common.ValueArea"] = value_area
    if target_date:
        fields["Microsoft.VSTS.Scheduling.TargetDate"] = target_date
    if tags:
        fields["System.Tags"] = tags
    if assigned_to:
        fields["System.AssignedTo"] = assigned_to
    
    # Handle area path with team support
    if area_path:
        # Explicit area path takes precedence
        fields["System.AreaPath"] = area_path
    elif team and client.config.project:
        # Team parameter provided but not mapped - use project root
        # For custom team mapping, set area_path explicitly
        fields["System.AreaPath"] = client.config.project
    
    if iteration_path:
        fields["System.IterationPath"] = iteration_path
    
    # Create the work item
    result = client.create_work_item(resolved_type, fields)
    
    # Add parent link if specified
    if parent_id:
        client.add_parent_link(result["id"], parent_id)
    
    return result


def create_epic(
    title: str,
    description: Optional[str] = None,
    priority: Optional[int] = None,
    value_area: Optional[str] = None,
    start_date: Optional[str] = None,
    target_date: Optional[str] = None,
    tags: Optional[str] = None,
    assigned_to: Optional[str] = None,
    area_path: Optional[str] = None,
    iteration_path: Optional[str] = None,
    work_item_type: Optional[str] = None,
    team: Optional[str] = None,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Create an Epic work item.
    
    Args:
        title: Epic title
        description: Epic description (HTML supported)
        priority: Priority (1-4, where 1 is highest)
        value_area: Value area (Business/Architectural)
        start_date: Start date in ISO format (YYYY-MM-DD)
        target_date: Target date in ISO format (YYYY-MM-DD)
        tags: Comma-separated tags
        assigned_to: Email or display name of assignee
        area_path: Area path
        iteration_path: Iteration path
        work_item_type: Optional explicit type name to override auto-detection
        team: Optional team key (e.g., "frontend", "backend", "mobile") to assign work item to team's board
        config: Optional Config instance
        
    Returns:
        Created Epic data including ID and URL
    """
    client = AzureDevOpsClient(config)
    resolver = get_resolver(config)
    
    # Resolve the actual work item type name
    resolved_type = resolver.resolve_epic(prefer=work_item_type)
    
    fields: Dict[str, Union[str, int, float]] = {
        "System.Title": title,
    }
    
    if description:
        fields["System.Description"] = _format_html_text(description)
    if priority:
        fields["Microsoft.VSTS.Common.Priority"] = priority
    if value_area:
        fields["Microsoft.VSTS.Common.ValueArea"] = value_area
    if start_date:
        fields["Microsoft.VSTS.Scheduling.StartDate"] = start_date
    if target_date:
        fields["Microsoft.VSTS.Scheduling.TargetDate"] = target_date
    if tags:
        fields["System.Tags"] = tags
    if assigned_to:
        fields["System.AssignedTo"] = assigned_to
    
    # Handle area path with team support
    if area_path:
        # Explicit area path takes precedence
        fields["System.AreaPath"] = area_path
    elif team and client.config.project:
        # Team parameter provided but not mapped - use project root
        # For custom team mapping, set area_path explicitly
        fields["System.AreaPath"] = client.config.project
    
    if iteration_path:
        fields["System.IterationPath"] = iteration_path
    
    # Create the work item
    result = client.create_work_item(resolved_type, fields)
    
    return result


def get_work_item(
    work_item_id: int,
    config: Optional[Config] = None,
) -> Dict[str, Any]:
    """
    Get a work item by ID.
    
    Args:
        work_item_id: Work item ID
        config: Optional Config instance
        
    Returns:
        Work item data
    """
    client = AzureDevOpsClient(config)
    return client.get_work_item(work_item_id, expand="all")


def delete_work_item(
    work_item_id: int,
    permanent: bool = False,
    config: Optional[Config] = None,
) -> None:
    """
    Delete a work item.
    
    Args:
        work_item_id: Work item ID
        permanent: If True, permanently delete. If False, move to recycle bin.
        config: Optional Config instance
    """
    client = AzureDevOpsClient(config)
    client.delete_work_item(work_item_id, destroy=permanent)

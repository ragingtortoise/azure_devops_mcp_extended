"""
Work item type detection and mapping for different Azure DevOps process templates.
"""

from typing import Dict, List, Optional, Set
from .client import AzureDevOpsClient
from .config import Config


# Work item type mappings for different process templates
WORK_ITEM_TYPE_MAPPINGS = {
    # Backlog item types (ordered by preference)
    "backlog_item": [
        "Product Backlog Item",  # Scrum
        "User Story",            # Agile
        "Issue",                 # Basic
        "Requirement",           # CMMI
    ],
    # Bug types
    "bug": [
        "Bug",
        "Defect",
    ],
    # Task types
    "task": [
        "Task",
    ],
    # Feature types
    "feature": [
        "Feature",
    ],
    # Epic types
    "epic": [
        "Epic",
    ],
    # Test case types
    "test_case": [
        "Test Case",
    ],
}


class WorkItemTypeResolver:
    """
    Resolves work item type names based on what's available in the project.
    Caches results to avoid repeated API calls.
    """
    
    def __init__(self, config: Optional[Config] = None):
        self.client = AzureDevOpsClient(config)
        self._available_types: Optional[Set[str]] = None
        self._type_cache: Dict[str, str] = {}
    
    def get_available_types(self) -> Set[str]:
        """
        Get all available work item types in the project.
        
        Returns:
            Set of available work item type names
        """
        if self._available_types is None:
            types = self.client.get_work_item_types()
            self._available_types = {wit["name"] for wit in types}
        
        return self._available_types
    
    def resolve_type(self, category: str, prefer: Optional[str] = None) -> str:
        """
        Resolve a work item type name based on category and what's available.
        
        Args:
            category: Category key (e.g., "backlog_item", "bug", "task")
            prefer: Optional preferred type name to try first
            
        Returns:
            Resolved work item type name
            
        Raises:
            ValueError: If no suitable type is found
        """
        # Check cache first
        cache_key = f"{category}:{prefer or ''}"
        if cache_key in self._type_cache:
            return self._type_cache[cache_key]
        
        available = self.get_available_types()
        
        # If a preferred type is specified and available, use it
        if prefer and prefer in available:
            self._type_cache[cache_key] = prefer
            return prefer
        
        # Try to find a matching type from the category mappings
        if category in WORK_ITEM_TYPE_MAPPINGS:
            candidates = WORK_ITEM_TYPE_MAPPINGS[category]
            
            for candidate in candidates:
                if candidate in available:
                    self._type_cache[cache_key] = candidate
                    return candidate
        
        # If nothing found, raise an error with helpful information
        available_list = ", ".join(sorted(available))
        raise ValueError(
            f"Cannot find suitable work item type for category '{category}'. "
            f"Available types in this project: {available_list}. "
            f"Use the --type parameter to specify a custom type."
        )
    
    def resolve_backlog_item(self, prefer: Optional[str] = None) -> str:
        """Resolve the backlog item type (PBI/User Story/Issue)."""
        return self.resolve_type("backlog_item", prefer)
    
    def resolve_bug(self, prefer: Optional[str] = None) -> str:
        """Resolve the bug/defect type."""
        return self.resolve_type("bug", prefer)
    
    def resolve_task(self, prefer: Optional[str] = None) -> str:
        """Resolve the task type."""
        return self.resolve_type("task", prefer)
    
    def resolve_feature(self, prefer: Optional[str] = None) -> str:
        """Resolve the feature type."""
        return self.resolve_type("feature", prefer)
    
    def resolve_epic(self, prefer: Optional[str] = None) -> str:
        """Resolve the epic type."""
        return self.resolve_type("epic", prefer)
    
    def get_process_template_info(self) -> Dict[str, str]:
        """
        Determine process template information based on available types.
        
        Returns:
            Dictionary with template info
        """
        available = self.get_available_types()
        
        # Detect process template
        if "Product Backlog Item" in available:
            template = "Scrum"
        elif "User Story" in available:
            template = "Agile"
        elif "Issue" in available:
            template = "Basic"
        elif "Requirement" in available:
            template = "CMMI"
        else:
            template = "Unknown/Custom"
        
        # Find backlog item type
        backlog_type = None
        for candidate in WORK_ITEM_TYPE_MAPPINGS["backlog_item"]:
            if candidate in available:
                backlog_type = candidate
                break
        
        return {
            "template": template,
            "backlog_item_type": backlog_type or "Unknown",
            "available_types": ", ".join(sorted(available)),
        }


def get_resolver(config: Optional[Config] = None) -> WorkItemTypeResolver:
    """
    Get a WorkItemTypeResolver instance.
    
    Args:
        config: Optional Config instance
        
    Returns:
        WorkItemTypeResolver instance
    """
    return WorkItemTypeResolver(config)

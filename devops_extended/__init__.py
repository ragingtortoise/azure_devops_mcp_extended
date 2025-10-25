"""
Azure DevOps Extended - Azure DevOps REST API Interface
A Python package for managing Azure DevOps work items programmatically.
"""

from .client import AzureDevOpsClient
from .work_items import (
    create_pbi,
    create_bug,
    create_task,
    create_feature,
    create_epic,
    get_work_item,
    delete_work_item,
)
from .updates import (
    update_work_item,
    update_title,
    update_description,
    assign_work_item,
    add_comment,
)
from .states import (
    transition_to_new,
    transition_to_active,
    transition_to_resolved,
    transition_to_closed,
    transition_to_removed,
    get_available_states,
)
from .type_resolver import WorkItemTypeResolver, get_resolver

__version__ = "0.2.0"
__all__ = [
    "AzureDevOpsClient",
    # Work item creation
    "create_pbi",
    "create_bug",
    "create_task",
    "create_feature",
    "create_epic",
    "get_work_item",
    "delete_work_item",
    # Updates
    "update_work_item",
    "update_title",
    "update_description",
    "assign_work_item",
    "add_comment",
    # State transitions
    "transition_to_new",
    "transition_to_active",
    "transition_to_resolved",
    "transition_to_closed",
    "transition_to_removed",
    "get_available_states",
    # Type resolution
    "WorkItemTypeResolver",
    "get_resolver",
]

"""
Azure DevOps MCP Server - Model Context Protocol server for Azure DevOps.
Provides tools for creating, updating, and managing Azure DevOps work items.
"""

import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from . import work_items, updates, states
from .config import get_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize server
app = Server("devops-extended-mcp")

# Global variable for domain filtering (set by main())
SELECTED_DOMAINS: set[str] | None = None

# Tool categorization by domain
TOOL_DOMAINS = {
    # Creation domain - tools that create new work items
    "creation": {
        "create_pbi",
        "create_bug",
        "create_task",
        "create_feature",
        "create_epic",
    },
    # Updates domain - tools that modify existing work items
    "updates": {
        "update_work_item_title",
        "assign_work_item",
        "add_comment",
        "transition_state",
        "add_parent_link",
    },
    # Queries domain - tools that retrieve work item data
    "queries": {
        "get_work_item",
        "delete_work_item",
    },
    # Metadata domain - tools that discover schema/types/states
    "metadata": {
        "get_work_item_types",
        "get_available_states",
        "get_work_item_type_schema",
        "get_work_item_fields",
        "get_work_item_available_states",
    },
    # Composite domains for convenience
    "core": {  # Essential operations (create + get)
        "create_pbi",
        "create_bug",
        "create_task",
        "get_work_item",
    },
    "work-items": {  # All work item operations (creation + updates + queries)
        "create_pbi",
        "create_bug",
        "create_task",
        "create_feature",
        "create_epic",
        "update_work_item_title",
        "assign_work_item",
        "add_comment",
        "transition_state",
        "add_parent_link",
        "get_work_item",
        "delete_work_item",
    },
}

# Validate configuration on startup
try:
    config = get_config()
    logger.info(f"Azure DevOps MCP Server initialized for organization: {config.organization}")
except Exception as e:
    logger.error(f"Failed to initialize configuration: {e}")
    raise


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available Azure DevOps tools (with optional domain filtering)."""
    all_tools = [
        Tool(
            name="create_pbi",
            description="Create a Product Backlog Item (or User Story/Issue depending on process template). Auto-detects correct work item type.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Work item title"},
                    "description": {"type": "string", "description": "Work item description (HTML supported)"},
                    "priority": {"type": "integer", "description": "Priority (1-4, where 1 is highest)", "minimum": 1, "maximum": 4},
                    "effort": {"type": "integer", "description": "Story points/effort estimate"},
                    "value_area": {"type": "string", "description": "Value area (Business/Architectural)"},
                    "tags": {"type": "string", "description": "Comma-separated tags"},
                    "assigned_to": {"type": "string", "description": "Assignee email or display name"},
                    "area_path": {"type": "string", "description": "Area path (e.g., 'ProjectName\\Area')"},
                    "iteration_path": {"type": "string", "description": "Iteration path (e.g., 'ProjectName\\Sprint 1')"},
                    "parent_id": {"type": "integer", "description": "Parent work item ID (e.g., Epic or Feature ID)"},
                    "team": {"type": "string", "description": "Team key (e.g., 'frontend', 'backend', 'mobile') to assign to team's board"},
                },
                "required": ["title"],
            },
        ),
        Tool(
            name="create_bug",
            description="Create a Bug work item.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Bug title"},
                    "repro_steps": {"type": "string", "description": "Steps to reproduce"},
                    "system_info": {"type": "string", "description": "System information"},
                    "severity": {"type": "string", "description": "Severity (1-4, where 1 is critical)"},
                    "priority": {"type": "integer", "description": "Priority (1-4)", "minimum": 1, "maximum": 4},
                    "tags": {"type": "string", "description": "Comma-separated tags"},
                    "assigned_to": {"type": "string", "description": "Assignee email or display name"},
                    "area_path": {"type": "string", "description": "Area path"},
                    "iteration_path": {"type": "string", "description": "Iteration path"},
                    "parent_id": {"type": "integer", "description": "Parent work item ID"},
                    "team": {"type": "string", "description": "Team key to assign to team's board"},
                },
                "required": ["title"],
            },
        ),
        Tool(
            name="create_task",
            description="Create a Task work item.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description"},
                    "activity": {"type": "string", "description": "Activity type (Development, Testing, etc.)"},
                    "remaining_work": {"type": "number", "description": "Remaining work in hours"},
                    "original_estimate": {"type": "number", "description": "Original estimate in hours"},
                    "tags": {"type": "string", "description": "Comma-separated tags"},
                    "assigned_to": {"type": "string", "description": "Assignee email or display name"},
                    "area_path": {"type": "string", "description": "Area path"},
                    "iteration_path": {"type": "string", "description": "Iteration path"},
                    "parent_id": {"type": "integer", "description": "Parent work item ID (e.g., PBI or Feature)"},
                    "team": {"type": "string", "description": "Team key to assign to team's board"},
                },
                "required": ["title"],
            },
        ),
        Tool(
            name="create_feature",
            description="Create a Feature work item.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Feature title"},
                    "description": {"type": "string", "description": "Feature description"},
                    "priority": {"type": "integer", "description": "Priority (1-4)", "minimum": 1, "maximum": 4},
                    "value_area": {"type": "string", "description": "Value area (Business/Architectural)"},
                    "target_date": {"type": "string", "description": "Target date (YYYY-MM-DD)"},
                    "tags": {"type": "string", "description": "Comma-separated tags"},
                    "assigned_to": {"type": "string", "description": "Assignee email or display name"},
                    "area_path": {"type": "string", "description": "Area path"},
                    "iteration_path": {"type": "string", "description": "Iteration path"},
                    "parent_id": {"type": "integer", "description": "Parent work item ID (e.g., Epic)"},
                    "team": {"type": "string", "description": "Team key to assign to team's board"},
                    "ideation": {"type": "boolean", "description": "Create in 'Ideation' state (for quick ideas/notes)"},
                },
                "required": ["title"],
            },
        ),
        Tool(
            name="create_epic",
            description="Create an Epic work item.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Epic title"},
                    "description": {"type": "string", "description": "Epic description"},
                    "priority": {"type": "integer", "description": "Priority (1-4)", "minimum": 1, "maximum": 4},
                    "value_area": {"type": "string", "description": "Value area (Business/Architectural)"},
                    "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                    "target_date": {"type": "string", "description": "Target date (YYYY-MM-DD)"},
                    "tags": {"type": "string", "description": "Comma-separated tags"},
                    "assigned_to": {"type": "string", "description": "Assignee email or display name"},
                    "area_path": {"type": "string", "description": "Area path"},
                    "iteration_path": {"type": "string", "description": "Iteration path"},
                    "team": {"type": "string", "description": "Team key to assign to team's board"},
                },
                "required": ["title"],
            },
        ),
        Tool(
            name="get_work_item",
            description="Get a work item by ID with all details.",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_item_id": {"type": "integer", "description": "Work item ID"},
                },
                "required": ["work_item_id"],
            },
        ),
        Tool(
            name="update_work_item_title",
            description="Update the title of a work item.",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_item_id": {"type": "integer", "description": "Work item ID"},
                    "title": {"type": "string", "description": "New title"},
                },
                "required": ["work_item_id", "title"],
            },
        ),
        Tool(
            name="assign_work_item",
            description="Assign a work item to a user.",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_item_id": {"type": "integer", "description": "Work item ID"},
                    "assigned_to": {"type": "string", "description": "User email or display name"},
                },
                "required": ["work_item_id", "assigned_to"],
            },
        ),
        Tool(
            name="add_comment",
            description="Add a comment to a work item.",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_item_id": {"type": "integer", "description": "Work item ID"},
                    "comment": {"type": "string", "description": "Comment text"},
                },
                "required": ["work_item_id", "comment"],
            },
        ),
        Tool(
            name="transition_state",
            description="Change the state of a work item (new, active, development, ideation, resolved, released, done, not-a-bug, closed, removed).",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_item_id": {"type": "integer", "description": "Work item ID"},
                    "state": {
                        "type": "string",
                        "description": "Target state",
                        "enum": ["new", "active", "development", "ideation", "resolved", "released", "done", "not-a-bug", "closed", "removed"],
                    },
                },
                "required": ["work_item_id", "state"],
            },
        ),
        Tool(
            name="add_parent_link",
            description="Add a parent link to a work item (creates hierarchical relationship).",
            inputSchema={
                "type": "object",
                "properties": {
                    "child_id": {"type": "integer", "description": "Child work item ID"},
                    "parent_id": {"type": "integer", "description": "Parent work item ID"},
                },
                "required": ["child_id", "parent_id"],
            },
        ),
        Tool(
            name="delete_work_item",
            description="Delete a work item (moves to recycle bin by default).",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_item_id": {"type": "integer", "description": "Work item ID"},
                    "permanent": {"type": "boolean", "description": "Permanently delete (default: false)"},
                },
                "required": ["work_item_id"],
            },
        ),
        Tool(
            name="get_work_item_types",
            description="Get all available work item types in the project (e.g., User Story, Bug, Task, Feature, Epic). Returns process template information.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_available_states",
            description="Get available states for a specific work item type (e.g., New, Active, Development, Released). Use this to discover valid states before transitions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_item_type": {"type": "string", "description": "Work item type name (e.g., 'User Story', 'Bug', 'Task')"},
                },
                "required": ["work_item_type"],
            },
        ),
        Tool(
            name="get_work_item_type_schema",
            description="Get full schema for a work item type including states, fields, and metadata. Use this to understand what fields are available and required.",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_item_type": {"type": "string", "description": "Work item type name (e.g., 'User Story', 'Bug', 'Task')"},
                },
                "required": ["work_item_type"],
            },
        ),
        Tool(
            name="get_work_item_fields",
            description="Get all available fields in the project with their types, reference names, and metadata. Useful for understanding what custom fields exist.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_work_item_available_states",
            description="Get available states for a specific work item based on its type. Use this before attempting state transitions to see what states are valid.",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_item_id": {"type": "integer", "description": "Work item ID"},
                },
                "required": ["work_item_id"],
            },
        ),
    ]
    
    # Apply domain filtering if specified
    if SELECTED_DOMAINS is None:
        # No filtering - return all tools
        return all_tools
    
    # Build set of enabled tool names based on selected domains
    enabled_tools = set()
    for domain in SELECTED_DOMAINS:
        if domain in TOOL_DOMAINS:
            enabled_tools.update(TOOL_DOMAINS[domain])
        else:
            logger.warning(f"Unknown domain: {domain}")
    
    # Filter tools by name
    filtered_tools = [tool for tool in all_tools if tool.name in enabled_tools]
    
    logger.info(f"Filtered tools: {len(filtered_tools)}/{len(all_tools)} tools enabled")
    return filtered_tools


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "create_pbi":
            result = work_items.create_pbi(**arguments)
        elif name == "create_bug":
            result = work_items.create_bug(**arguments)
        elif name == "create_task":
            result = work_items.create_task(**arguments)
        elif name == "create_feature":
            result = work_items.create_feature(**arguments)
        elif name == "create_epic":
            result = work_items.create_epic(**arguments)
        elif name == "get_work_item":
            result = work_items.get_work_item(arguments["work_item_id"])
        elif name == "update_work_item_title":
            result = updates.update_title(arguments["work_item_id"], arguments["title"])
        elif name == "assign_work_item":
            result = updates.assign_work_item(arguments["work_item_id"], arguments["assigned_to"])
        elif name == "add_comment":
            result = updates.add_comment(arguments["work_item_id"], arguments["comment"])
        elif name == "transition_state":
            # Map lowercase to proper case
            state_map = {
                "new": "New",
                "active": "Active",
                "resolved": "Resolved",
                "closed": "Closed",
                "removed": "Removed",
                "development": "Development",
                "released": "Released",
                "done": "Done",
                "not-a-bug": "Not a Bug",
                "ideation": "Ideation",
            }
            state_input: str = arguments.get("state", "New")
            state = state_map.get(state_input.lower(), state_input)
            result = states.transition_state(arguments["work_item_id"], state)
        elif name == "add_parent_link":
            result = updates.add_parent_link(arguments["child_id"], arguments["parent_id"])
        elif name == "delete_work_item":
            permanent = arguments.get("permanent", False)
            work_items.delete_work_item(arguments["work_item_id"], permanent=permanent)
            result = {"success": True, "message": f"Work item {arguments['work_item_id']} deleted"}
        elif name == "get_work_item_types":
            from .type_resolver import get_resolver
            resolver = get_resolver()
            info = resolver.get_process_template_info()
            available = list(resolver.get_available_types())
            result = {
                "process_template": info["template"],
                "backlog_item_type": info["backlog_item_type"],
                "available_types": sorted(available)
            }
        elif name == "get_available_states":
            result = {
                "work_item_type": arguments["work_item_type"],
                "states": states.get_available_states_for_type(arguments["work_item_type"])
            }
        elif name == "get_work_item_type_schema":
            from .client import AzureDevOpsClient
            client = AzureDevOpsClient()
            schema = client.get_work_item_type_definition(arguments["work_item_type"])
            # Simplify schema for AI consumption
            result = {
                "name": schema.get("name"),
                "description": schema.get("description"),
                "states": [{"name": s["name"], "color": s.get("color")} for s in schema.get("states", [])],
                "fields": [{"name": f.get("name"), "referenceName": f.get("referenceName"), "type": f.get("type")} for f in schema.get("fields", [])]
            }
        elif name == "get_work_item_fields":
            from .client import AzureDevOpsClient
            client = AzureDevOpsClient()
            all_fields = client.get_work_item_fields()
            # Simplify for AI consumption - show most relevant fields
            result = {
                "total_fields": len(all_fields),
                "fields": [
                    {
                        "name": f.get("name"),
                        "referenceName": f.get("referenceName"),
                        "type": f.get("type"),
                        "isIdentity": f.get("isIdentity", False),
                        "isPicklist": f.get("isPicklist", False),
                    }
                    for f in all_fields
                ]
            }
        elif name == "get_work_item_available_states":
            available_states = states.get_available_states(arguments["work_item_id"])
            result = {
                "work_item_id": arguments["work_item_id"],
                "available_states": available_states
            }
        else:
            raise ValueError(f"Unknown tool: {name}")

        # Format response
        return [TextContent(type="text", text=str(result))]

    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Main entry point for MCP server."""
    import argparse
    global SELECTED_DOMAINS
    
    parser = argparse.ArgumentParser(
        description="Azure DevOps MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-d", "--domains",
        nargs="*",
        default=None,
        help="Domains to enable (default: all). Options: creation, updates, queries, metadata, core, work-items",
    )
    
    args = parser.parse_args()
    
    # Store domains globally for filtering
    if args.domains:
        SELECTED_DOMAINS = set(args.domains)
        logger.info(f"Domain filtering enabled: {SELECTED_DOMAINS}")
    else:
        SELECTED_DOMAINS = None  # None means all domains
        logger.info("All domains enabled (no filtering)")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

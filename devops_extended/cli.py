"""
Command-line interface for Azure DevOps Extended.
"""

import argparse
import json
import sys
from typing import Optional

from . import work_items, updates, states


def format_output(data: dict, verbose: bool = False) -> str:
    """Format work item data for output."""
    if verbose:
        return json.dumps(data, indent=2)
    
    # Extract key information
    work_item_id = data.get("id", "N/A")
    title = data.get("fields", {}).get("System.Title", "N/A")
    state = data.get("fields", {}).get("System.State", "N/A")
    work_item_type = data.get("fields", {}).get("System.WorkItemType", "N/A")
    url = data.get("_links", {}).get("html", {}).get("href", "N/A")
    
    return (
        f"Work Item Created/Updated:\n"
        f"  ID: {work_item_id}\n"
        f"  Type: {work_item_type}\n"
        f"  Title: {title}\n"
        f"  State: {state}\n"
        f"  URL: {url}"
    )


def create_pbi_command(args):
    """Handle create-pbi command."""
    result = work_items.create_pbi(
        title=args.title,
        description=args.description,
        priority=args.priority,
        effort=args.effort,
        value_area=args.value_area,
        tags=args.tags,
        assigned_to=args.assigned_to,
        area_path=args.area_path,
        iteration_path=args.iteration_path,
        parent_id=args.parent,
        work_item_type=args.type,
        team=args.team,
    )
    print(format_output(result, args.verbose))


def create_bug_command(args):
    """Handle create-bug command."""
    result = work_items.create_bug(
        title=args.title,
        repro_steps=args.repro_steps,
        system_info=args.system_info,
        severity=args.severity,
        priority=args.priority,
        tags=args.tags,
        assigned_to=args.assigned_to,
        area_path=args.area_path,
        iteration_path=args.iteration_path,
        parent_id=args.parent,
        work_item_type=args.type,
        team=args.team,
    )
    print(format_output(result, args.verbose))


def create_task_command(args):
    """Handle create-task command."""
    result = work_items.create_task(
        title=args.title,
        description=args.description,
        activity=args.activity,
        remaining_work=args.remaining_work,
        original_estimate=args.original_estimate,
        tags=args.tags,
        assigned_to=args.assigned_to,
        area_path=args.area_path,
        iteration_path=args.iteration_path,
        parent_id=args.parent,
        work_item_type=args.type,
        team=args.team,
    )
    print(format_output(result, args.verbose))


def create_feature_command(args):
    """Handle create-feature command."""
    result = work_items.create_feature(
        title=args.title,
        description=args.description,
        priority=args.priority,
        value_area=args.value_area,
        target_date=args.target_date,
        tags=args.tags,
        assigned_to=args.assigned_to,
        area_path=args.area_path,
        iteration_path=args.iteration_path,
        parent_id=args.parent,
        work_item_type=args.type,
        team=args.team,
        ideation=args.ideation,
    )
    print(format_output(result, args.verbose))


def create_epic_command(args):
    """Handle create-epic command."""
    result = work_items.create_epic(
        title=args.title,
        description=args.description,
        priority=args.priority,
        value_area=args.value_area,
        start_date=args.start_date,
        target_date=args.target_date,
        tags=args.tags,
        assigned_to=args.assigned_to,
        area_path=args.area_path,
        iteration_path=args.iteration_path,
        work_item_type=args.type,
        team=args.team,
    )
    print(format_output(result, args.verbose))


def get_command(args):
    """Handle get command."""
    result = work_items.get_work_item(args.id)
    print(format_output(result, args.verbose))


def update_command(args):
    """Handle update command."""
    result = updates.update_work_item(args.id, json.loads(args.fields))
    print(format_output(result, args.verbose))


def update_title_command(args):
    """Handle update-title command."""
    result = updates.update_title(args.id, args.title)
    print(format_output(result, args.verbose))


def update_description_command(args):
    """Handle update-description command."""
    result = updates.update_description(args.id, args.description)
    print(format_output(result, args.verbose))


def assign_command(args):
    """Handle assign command."""
    result = updates.assign_work_item(args.id, args.user)
    print(format_output(result, args.verbose))


def comment_command(args):
    """Handle comment command."""
    result = updates.add_comment(args.id, args.comment)
    if args.verbose:
        print(json.dumps(result, indent=2))
    else:
        print(f"Comment added to work item {args.id}")


def add_parent_command(args):
    """Handle add-parent command."""
    result = updates.add_parent_link(args.child_id, args.parent_id)
    print(format_output(result, args.verbose))


def state_command(args):
    """Handle state command."""
    # Map lowercase input to proper case-sensitive state names
    state_map = {
        # Common states (base Azure DevOps)
        "new": "New",
        "active": "Active",
        "resolved": "Resolved",
        "closed": "Closed",
        "removed": "Removed",
        
        # Extended states (process template specific)
        "development": "Development",
        "released": "Released",
        "done": "Done",
        "not-a-bug": "Not a Bug",
        "ideation": "Ideation",
    }

    # Get the proper cased state name
    state_input = args.state if args.state else "new"
    state_to_set = state_map.get(state_input.lower(), state_input)
    
    # Use the generic transition function with proper casing
    result = states.transition_state(args.id, state_to_set)

    print(format_output(result, args.verbose))


def delete_command(args):
    """Handle delete command."""
    work_items.delete_work_item(args.id, permanent=args.permanent)
    print(f"Work item {args.id} deleted {'permanently' if args.permanent else '(moved to recycle bin)'}")


def types_command(args):
    """Handle the types command."""
    from .type_resolver import get_resolver
    
    resolver = get_resolver()
    info = resolver.get_process_template_info()
    available = resolver.get_available_types()
    
    print("=" * 60)
    print("Azure DevOps Work Item Types")
    print("=" * 60)
    print(f"\nProcess Template: {info['template']}")
    print(f"Backlog Item Type: {info['backlog_item_type']}")
    print(f"\nAvailable Work Item Types:")
    for wit_type in sorted(available):
        print(f"  - {wit_type}")
    print("\n" + "=" * 60)


def states_command(args):
    """Handle the states command."""
    from .states import get_available_states_for_type
    
    try:
        states = get_available_states_for_type(args.type)
        
        print("=" * 60)
        print(f"Available States for '{args.type}'")
        print("=" * 60)
        for state in states:
            print(f"  - {state}")
        print("\n" + "=" * 60)
    except Exception as e:
        print(f"Error getting states for '{args.type}': {e}", file=sys.stderr)
        sys.exit(1)


def fields_command(args):
    """Handle the fields command."""
    from .client import AzureDevOpsClient
    
    try:
        client = AzureDevOpsClient()
        
        if args.type:
            # Get fields for specific work item type
            fields = client.get_work_item_type_fields(args.type)
            print("=" * 60)
            print(f"Available Fields for '{args.type}'")
            print("=" * 60)
        else:
            # Get all fields
            fields = client.get_work_item_fields()
            print("=" * 60)
            print(f"All Available Fields ({len(fields)} total)")
            print("=" * 60)
        
        for field in fields:
            name = field.get("name", "Unknown")
            ref_name = field.get("referenceName", "")
            field_type = field.get("type", "")
            print(f"  - {name}")
            if args.verbose:
                print(f"    Reference: {ref_name}")
                print(f"    Type: {field_type}")
        
        print("\n" + "=" * 60)
    except Exception as e:
        print(f"Error getting fields: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Azure DevOps Extended - Azure DevOps Work Item Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show verbose output (full JSON response)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create PBI
    pbi_parser = subparsers.add_parser("create-pbi", help="Create a Product Backlog Item (auto-detects: PBI/User Story/Issue)")
    pbi_parser.add_argument("title", help="PBI title")
    pbi_parser.add_argument("-d", "--description", help="PBI description")
    pbi_parser.add_argument("-p", "--priority", type=int, help="Priority (1-4)")
    pbi_parser.add_argument("-e", "--effort", type=int, help="Story points/effort")
    pbi_parser.add_argument("--value-area", help="Value area (Business/Architectural)")
    pbi_parser.add_argument("-t", "--tags", help="Comma-separated tags")
    pbi_parser.add_argument("-a", "--assigned-to", help="Assignee email/name")
    pbi_parser.add_argument("--area-path", help="Area path")
    pbi_parser.add_argument("--iteration-path", help="Iteration path")
    pbi_parser.add_argument("--parent", type=int, help="Parent work item ID (e.g., Epic or Feature)")
    pbi_parser.add_argument("--type", help="Override work item type name")
    pbi_parser.add_argument("--team", help="Team key (e.g., 'frontend', 'backend', 'mobile') to assign to team's board")
    pbi_parser.set_defaults(func=create_pbi_command)
    
    # Create Bug
    bug_parser = subparsers.add_parser("create-bug", help="Create a Bug")
    bug_parser.add_argument("title", help="Bug title")
    bug_parser.add_argument("-r", "--repro-steps", help="Steps to reproduce")
    bug_parser.add_argument("-s", "--system-info", help="System information")
    bug_parser.add_argument("--severity", help="Severity (1-4)")
    bug_parser.add_argument("-p", "--priority", type=int, help="Priority (1-4)")
    bug_parser.add_argument("-t", "--tags", help="Comma-separated tags")
    bug_parser.add_argument("-a", "--assigned-to", help="Assignee email/name")
    bug_parser.add_argument("--area-path", help="Area path")
    bug_parser.add_argument("--iteration-path", help="Iteration path")
    bug_parser.add_argument("--parent", type=int, help="Parent work item ID")
    bug_parser.add_argument("--type", help="Override work item type name")
    bug_parser.add_argument("--team", help="Team key (e.g., 'frontend', 'backend', 'mobile') to assign to team's board")
    bug_parser.set_defaults(func=create_bug_command)
    
    # Create Task
    task_parser = subparsers.add_parser("create-task", help="Create a Task")
    task_parser.add_argument("title", help="Task title")
    task_parser.add_argument("-d", "--description", help="Task description")
    task_parser.add_argument("--activity", help="Activity type")
    task_parser.add_argument("-r", "--remaining-work", type=float, help="Remaining work (hours)")
    task_parser.add_argument("-o", "--original-estimate", type=float, help="Original estimate (hours)")
    task_parser.add_argument("-t", "--tags", help="Comma-separated tags")
    task_parser.add_argument("-a", "--assigned-to", help="Assignee email/name")
    task_parser.add_argument("--area-path", help="Area path")
    task_parser.add_argument("--iteration-path", help="Iteration path")
    task_parser.add_argument("--parent", type=int, help="Parent work item ID (e.g., PBI or Feature)")
    task_parser.add_argument("--type", help="Override work item type name")
    task_parser.add_argument("--team", help="Team key (e.g., 'frontend', 'backend', 'mobile') to assign to team's board")
    task_parser.set_defaults(func=create_task_command)
    
    # Create Feature
    feature_parser = subparsers.add_parser("create-feature", help="Create a Feature")
    feature_parser.add_argument("title", help="Feature title")
    feature_parser.add_argument("-d", "--description", help="Feature description")
    feature_parser.add_argument("-p", "--priority", type=int, help="Priority (1-4)")
    feature_parser.add_argument("--value-area", help="Value area (Business/Architectural)")
    feature_parser.add_argument("--target-date", help="Target date (YYYY-MM-DD)")
    feature_parser.add_argument("-t", "--tags", help="Comma-separated tags")
    feature_parser.add_argument("-a", "--assigned-to", help="Assignee email/name")
    feature_parser.add_argument("--area-path", help="Area path")
    feature_parser.add_argument("--iteration-path", help="Iteration path")
    feature_parser.add_argument("--parent", type=int, help="Parent work item ID (e.g., Epic)")
    feature_parser.add_argument("--type", help="Override work item type name")
    feature_parser.add_argument("--team", help="Team key (e.g., 'frontend', 'backend', 'mobile') to assign to team's board")
    feature_parser.add_argument("--ideation", action="store_true", help="Create in 'Ideation' state (quick ideas/notes)")
    feature_parser.set_defaults(func=create_feature_command)
    
    # Create Epic
    epic_parser = subparsers.add_parser("create-epic", help="Create an Epic")
    epic_parser.add_argument("title", help="Epic title")
    epic_parser.add_argument("-d", "--description", help="Epic description")
    epic_parser.add_argument("-p", "--priority", type=int, help="Priority (1-4)")
    epic_parser.add_argument("--value-area", help="Value area (Business/Architectural)")
    epic_parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    epic_parser.add_argument("--target-date", help="Target date (YYYY-MM-DD)")
    epic_parser.add_argument("-t", "--tags", help="Comma-separated tags")
    epic_parser.add_argument("-a", "--assigned-to", help="Assignee email/name")
    epic_parser.add_argument("--area-path", help="Area path")
    epic_parser.add_argument("--iteration-path", help="Iteration path")
    epic_parser.add_argument("--type", help="Override work item type name")
    epic_parser.add_argument("--team", help="Team key (e.g., 'frontend', 'backend', 'mobile') to assign to team's board")
    epic_parser.set_defaults(func=create_epic_command)
    
    # Get work item
    get_parser = subparsers.add_parser("get", help="Get a work item by ID")
    get_parser.add_argument("id", type=int, help="Work item ID")
    get_parser.add_argument("-v", "--verbose", action="store_true", help="Show full JSON output")
    get_parser.set_defaults(func=get_command)
    
    # Update work item
    update_parser = subparsers.add_parser("update", help="Update work item fields")
    update_parser.add_argument("id", type=int, help="Work item ID")
    update_parser.add_argument("fields", help='JSON fields to update (e.g., \'{"System.Title": "New"}\')')
    update_parser.set_defaults(func=update_command)
    
    # Update title
    title_parser = subparsers.add_parser("update-title", help="Update work item title")
    title_parser.add_argument("id", type=int, help="Work item ID")
    title_parser.add_argument("title", help="New title")
    title_parser.set_defaults(func=update_title_command)
    
    # Update description
    desc_parser = subparsers.add_parser("update-description", help="Update work item description")
    desc_parser.add_argument("id", type=int, help="Work item ID")
    desc_parser.add_argument("description", help="New description")
    desc_parser.set_defaults(func=update_description_command)
    
    # Assign
    assign_parser = subparsers.add_parser("assign", help="Assign work item to user")
    assign_parser.add_argument("id", type=int, help="Work item ID")
    assign_parser.add_argument("user", help="User email or display name")
    assign_parser.set_defaults(func=assign_command)
    
    # Add comment
    comment_parser = subparsers.add_parser("comment", help="Add comment to work item")
    comment_parser.add_argument("id", type=int, help="Work item ID")
    comment_parser.add_argument("comment", help="Comment text")
    comment_parser.set_defaults(func=comment_command)
    
    # Add parent link
    parent_parser = subparsers.add_parser("add-parent", help="Add parent link to work item")
    parent_parser.add_argument("child_id", type=int, help="Child work item ID")
    parent_parser.add_argument("parent_id", type=int, help="Parent work item ID")
    parent_parser.set_defaults(func=add_parent_command)
    
    # Change state
    state_parser = subparsers.add_parser("state", help="Change work item state")
    state_parser.add_argument("id", type=int, help="Work item ID")
    state_parser.add_argument(
        "state",
        help="Target state: new, active, development, ideation, resolved, released, done, not-a-bug, closed, removed"
    )
    state_parser.set_defaults(func=state_command)
    
    # Delete
    delete_parser = subparsers.add_parser("delete", help="Delete work item")
    delete_parser.add_argument("id", type=int, help="Work item ID")
    delete_parser.add_argument(
        "--permanent",
        action="store_true",
        help="Permanently delete (otherwise moves to recycle bin)"
    )
    delete_parser.set_defaults(func=delete_command)
    
    # Show work item types
    types_parser = subparsers.add_parser("types", help="Show available work item types")
    types_parser.set_defaults(func=types_command)
    
    # Show available states
    states_parser = subparsers.add_parser("states", help="Show available states for a work item type")
    states_parser.add_argument("type", help="Work item type name (e.g., 'User Story', 'Bug', 'Task')")
    states_parser.set_defaults(func=states_command)
    
    # Show available fields
    fields_parser = subparsers.add_parser("fields", help="Show available fields (all or for a specific work item type)")
    fields_parser.add_argument("--type", help="Work item type name to filter fields (optional)")
    fields_parser.set_defaults(func=fields_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

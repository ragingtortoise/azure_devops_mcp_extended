"""
Example usage of devops_extended package.

This demonstrates how to use the package programmatically.
"""

from devops_extended import (
    create_pbi,
    create_bug,
    create_task,
    get_work_item,
    update_title,
    assign_work_item,
    add_comment,
    transition_to_active,
    transition_to_closed,
)


def example_create_pbi():
    """Example: Create a Product Backlog Item."""
    print("Creating a PBI...")
    
    pbi = create_pbi(
        title="Implement user authentication system",
        description="<p>Add OAuth2 authentication with support for:</p><ul><li>Google</li><li>Microsoft</li><li>GitHub</li></ul>",
        priority=1,
        effort=13,
        value_area="Business",
        tags="authentication,security,priority",
    )
    
    print(f"✅ Created PBI #{pbi['id']}: {pbi['fields']['System.Title']}")
    print(f"   URL: {pbi['_links']['html']['href']}")
    
    return pbi['id']


def example_create_bug():
    """Example: Create a Bug."""
    print("\nCreating a bug...")
    
    bug = create_bug(
        title="Login button doesn't respond on mobile",
        repro_steps=(
            "<ol>"
            "<li>Open app on mobile device (iOS/Android)</li>"
            "<li>Navigate to login screen</li>"
            "<li>Tap the login button</li>"
            "<li>Nothing happens</li>"
            "</ol>"
        ),
        system_info="iOS 17.0, iPhone 14 Pro",
        severity="2",  # High
        priority=1,
        tags="mobile,login,ui",
    )
    
    print(f"✅ Created Bug #{bug['id']}: {bug['fields']['System.Title']}")
    
    return bug['id']


def example_create_task():
    """Example: Create a Task."""
    print("\nCreating a task...")
    
    task = create_task(
        title="Write unit tests for authentication module",
        description="Cover all authentication scenarios including edge cases",
        activity="Testing",
        remaining_work=8.0,
        original_estimate=8.0,
        tags="testing,unit-tests",
    )
    
    print(f"✅ Created Task #{task['id']}: {task['fields']['System.Title']}")
    
    return task['id']


def example_workflow(work_item_id: int):
    """Example: Complete workflow - update, assign, transition."""
    print(f"\n--- Starting workflow for work item {work_item_id} ---")
    
    # Get current state
    print("\n1. Getting work item details...")
    item = get_work_item(work_item_id)
    print(f"   Current state: {item['fields']['System.State']}")
    
    # Update title
    print("\n2. Updating title...")
    update_title(work_item_id, f"{item['fields']['System.Title']} [Updated]")
    print("   ✅ Title updated")
    
    # Assign to someone
    print("\n3. Assigning work item...")
    # Replace with actual user email
    assign_work_item(work_item_id, "user@example.com")
    print("   ✅ Assigned")
    
    # Add comment
    print("\n4. Adding comment...")
    add_comment(work_item_id, "Starting work on this item")
    print("   ✅ Comment added")
    
    # Transition to Active
    print("\n5. Moving to Active state...")
    transition_to_active(work_item_id)
    print("   ✅ Transitioned to Active")
    
    # Add progress comment
    print("\n6. Adding progress update...")
    add_comment(work_item_id, "Work in progress - 50% complete")
    print("   ✅ Progress updated")
    
    # Close the work item
    print("\n7. Closing work item...")
    transition_to_closed(work_item_id)
    print("   ✅ Transitioned to Closed")
    
    print(f"\n--- Workflow completed for work item {work_item_id} ---")


def main():
    """Run all examples."""
    print("=" * 60)
    print("Azure DevOps Extended - Usage Examples")
    print("=" * 60)
    
    try:
        # Create different work item types
        pbi_id = example_create_pbi()
        bug_id = example_create_bug()
        task_id = example_create_task()
        
        # Demonstrate workflow on the PBI
        example_workflow(pbi_id)
        
        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print(f"\nCreated work items:")
        print(f"  - PBI: {pbi_id}")
        print(f"  - Bug: {bug_id}")
        print(f"  - Task: {task_id}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have set the environment variables:")
        print("  - AZDO_ORGANIZATION")
        print("  - AZDO_PROJECT")
        print("  - AZDO_PAT")


if __name__ == "__main__":
    main()

"""
Integration tests for Azure DevOps Extended.

This script validates your setup by testing all major functionality:
- Work item creation (PBI/User Story, Bug, Task, Feature, Epic)
- Work item type auto-detection
- Parent/child linking (hierarchies)
- Field updates (title, description, assignments, estimates)
- State transitions (New → Active → Closed)
- Advanced scenarios (reparenting, bulk operations)

REQUIREMENTS:
- Azure DevOps organization, project, and PAT configured in environment variables
- See .env.example for required variables (AZDO_ORGANIZATION, AZDO_PROJECT, AZDO_PAT)
- Package installed: pip install -e .

USAGE:
    python integration_tests.py

CLEANUP:
    All created work items will be listed at the end with delete commands.
    WARNING: This script creates real work items in your Azure DevOps project!

OPTIONAL CONFIGURATION:
    Set TEST_TEAM environment variable to assign work items to a specific team/area:
        export TEST_TEAM=MyTeam  # Unix
        $env:TEST_TEAM="MyTeam"  # PowerShell
    
    Set TEST_USER environment variable for work item assignments:
        export TEST_USER=user@example.com  # Unix
        $env:TEST_USER="user@example.com"  # PowerShell
"""

import os
import sys
from devops_extended import work_items, updates, states

# Optional test configuration from environment variables
TEST_TEAM = os.getenv("TEST_TEAM")  # Optional: assign to specific team/area
TEST_USER = os.getenv("TEST_USER")  # Optional: assign work items to user

def test_section(title):
    """Print test section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_result(test_name, work_item_id, area_path=None):
    """Print test result."""
    status = "✓" if work_item_id else "✗"
    msg = f"{status} {test_name}: ID {work_item_id}"
    if area_path:
        msg += f" (Area: {area_path})"
    print(msg)
    return work_item_id

# Track created work items for cleanup
created_ids = []

try:
    test_section("1. BASIC WORK ITEM CREATION TESTS")
    
    # Test PBI/User Story creation
    pbi1 = work_items.create_pbi(
        "Test: User Authentication Feature",
        description="Implement user authentication system",
        team=TEST_TEAM,
        effort=8,
        priority=1,
        tags="test,authentication"
    )
    created_ids.append(test_result("PBI/User Story", pbi1["id"], pbi1["fields"]["System.AreaPath"]))
    
    # Test with different effort values
    pbi2 = work_items.create_pbi(
        "Test: Data Import Functionality",
        description="Import data from external sources",
        team=TEST_TEAM,
        effort=5,
        priority=2,
        tags="test,import"
    )
    created_ids.append(test_result("PBI with medium effort", pbi2["id"], pbi2["fields"]["System.AreaPath"]))
    
    # Test with low priority
    pbi3 = work_items.create_pbi(
        "Test: Search Optimization",
        description="Optimize search performance",
        team=TEST_TEAM,
        effort=3,
        priority=3,
        tags="test,performance"
    )
    created_ids.append(test_result("PBI with low priority", pbi3["id"], pbi3["fields"]["System.AreaPath"]))
    
    # Test without team assignment (default project area)
    pbi4 = work_items.create_pbi(
        "Test: Template Support",
        description="Add template support for common patterns",
        effort=5,
        priority=2,
        tags="test,templates"
    )
    created_ids.append(test_result("PBI without team", pbi4["id"], pbi4["fields"]["System.AreaPath"]))
    
    test_section("2. HIERARCHICAL LINKING TESTS")
    
    # Create Epic
    epic = work_items.create_epic(
        "Test: Platform Modernization Initiative",
        description="Major platform upgrades and improvements",
        team=TEST_TEAM,
        priority=1,
        start_date="2024-10-01",
        target_date="2024-12-31"
    )
    created_ids.append(test_result("Epic created", epic["id"]))
    
    # Create Feature under Epic
    feature = work_items.create_feature(
        "Test: Service Infrastructure Upgrade",
        description="Upgrade service infrastructure to latest standards",
        team=TEST_TEAM,
        parent_id=epic["id"],
        priority=1,
        target_date="2024-11-30"
    )
    created_ids.append(test_result("Feature under Epic", feature["id"]))
    
    # Create PBI under Feature
    pbi_child = work_items.create_pbi(
        "Test: Implement Token Management",
        description="Add automatic token refresh mechanism",
        team=TEST_TEAM,
        parent_id=feature["id"],
        effort=5,
        priority=1
    )
    created_ids.append(test_result("PBI under Feature", pbi_child["id"]))
    
    # Create Tasks under PBI
    task1 = work_items.create_task(
        "Test: Design Token Logic",
        description="Design the token management architecture",
        team=TEST_TEAM,
        parent_id=pbi_child["id"],
        activity="Design",
        remaining_work=4.0,
        original_estimate=4.0
    )
    created_ids.append(test_result("Task 1 under PBI", task1["id"]))
    
    task2 = work_items.create_task(
        "Test: Implement Token Management",
        description="Code implementation of token management",
        team=TEST_TEAM,
        parent_id=pbi_child["id"],
        activity="Development",
        remaining_work=8.0,
        original_estimate=8.0
    )
    created_ids.append(test_result("Task 2 under PBI", task2["id"]))
    
    task3 = work_items.create_task(
        "Test: Write Unit Tests",
        description="Test token management functionality",
        team=TEST_TEAM,
        parent_id=pbi_child["id"],
        activity="Testing",
        remaining_work=4.0,
        original_estimate=4.0
    )
    created_ids.append(test_result("Task 3 under PBI", task3["id"]))
    
    test_section("3. FIELD UPDATE TESTS")
    
    # Update title
    updates.update_title(task2["id"], "Test: Implement Token Management with Caching")
    print(f"✓ Updated task {task2['id']} title")
    
    # Update description
    updates.update_description(task2["id"], "Implement token management with cache storage")
    print(f"✓ Updated task {task2['id']} description")
    
    # Assign to user (if TEST_USER is set)
    if TEST_USER:
        updates.assign_work_item(task2["id"], TEST_USER)
        print(f"✓ Assigned task {task2['id']} to {TEST_USER}")
    else:
        print(f"ℹ Skipped assignment (set TEST_USER env var to test)")
    
    # Update remaining work (simulating progress)
    updates.update_work_item(task2["id"], {
        "Microsoft.VSTS.Scheduling.RemainingWork": 3.0,
        "Microsoft.VSTS.Scheduling.CompletedWork": 5.0
    })
    print(f"✓ Updated task {task2['id']} work estimates (5h completed, 3h remaining)")
    
    test_section("4. STATE TRANSITION TESTS")
    
    # Start working on task
    states.transition_to_active(task1["id"])
    print(f"✓ Task {task1['id']}: New → Active")
    
    # Complete task
    states.transition_to_closed(task1["id"])
    print(f"✓ Task {task1['id']}: Active → Closed")
    
    # Start another task
    states.transition_to_active(task2["id"])
    print(f"✓ Task {task2['id']}: New → Active")
    
    # Activate PBI
    states.transition_to_active(pbi_child["id"])
    print(f"✓ PBI {pbi_child['id']}: New → Active")
    
    test_section("5. ADVANCED SCENARIOS")
    
    # Scenario 1: Create bug and link to PBI
    bug = work_items.create_bug(
        "Test: System fails with expired tokens",
        repro_steps="1. Let token expire\n2. Try to make API call\n3. Observe error",
        team=TEST_TEAM,
        parent_id=pbi_child["id"],
        priority=1,
        tags="test,bug,high-priority"
    )
    created_ids.append(test_result("Bug linked to PBI", bug["id"]))
    
    # Scenario 2: Create orphan PBI, then reparent it to existing feature
    orphan_pbi = work_items.create_pbi(
        "Test: Add Provider Configuration",
        description="Allow dynamic provider configuration",
        team=TEST_TEAM,
        effort=3,
        priority=2
    )
    created_ids.append(test_result("Orphan PBI created", orphan_pbi["id"]))
    
    # Reparent the orphan PBI to the feature
    from devops_extended.client import AzureDevOpsClient
    client = AzureDevOpsClient()
    client.add_parent_link(orphan_pbi["id"], feature["id"])
    print(f"✓ Reparented PBI {orphan_pbi['id']} under Feature {feature['id']}")
    
    # Scenario 3: Bulk update - mark multiple items with same tag
    bulk_tag = "test-sprint-1"
    for item_id in [pbi_child["id"], task2["id"], task3["id"]]:
        current = work_items.get_work_item(item_id)
        existing_tags = current["fields"].get("System.Tags", "")
        new_tags = f"{existing_tags}; {bulk_tag}" if existing_tags else bulk_tag
        updates.update_work_item(item_id, {"System.Tags": new_tags})
    print(f"✓ Bulk tagged 3 work items with '{bulk_tag}'")
    
    # Scenario 4: Update effort after refinement
    original_effort = pbi_child["fields"]["Microsoft.VSTS.Scheduling.Effort"]
    updates.update_work_item(pbi_child["id"], {
        "Microsoft.VSTS.Scheduling.Effort": 8
    })
    print(f"✓ Updated PBI {pbi_child['id']} effort: {original_effort} → 8 story points")
    
    # Scenario 5: Create another PBI to demonstrate relationships
    related_pbi = work_items.create_pbi(
        "Test: Implement External API Integration",
        description="Integration with external services",
        team=TEST_TEAM,
        effort=5,
        priority=2,
        tags="test,integration"
    )
    created_ids.append(test_result("Related PBI", related_pbi["id"]))
    print(f"✓ Created related PBI {related_pbi['id']} for demonstration")
    
    test_section("6. TYPE AUTO-DETECTION TEST")
    
    # This will auto-detect "User Story" for Agile/Scrum or "Product Backlog Item" for other templates
    auto_pbi = work_items.create_pbi(
        "Test: Auto-Detection Validation",
        description="Testing automatic work item type detection",
        team=TEST_TEAM,
        effort=1
    )
    created_ids.append(auto_pbi["id"])
    detected_type = auto_pbi["fields"]["System.WorkItemType"]
    print(f"✓ Auto-detected work item type: {detected_type}")
    
    test_section("7. SUMMARY")
    
    print(f"\n✓ Successfully created {len(created_ids)} work items")
    print(f"✓ Created full hierarchy: Epic → Feature → PBI → Tasks")
    print(f"✓ Tested field updates, state transitions, and reparenting")
    print(f"✓ All integration tests passed!")
    
    print("\n" + "=" * 70)
    print("  CREATED WORK ITEMS")
    print("=" * 70)
    for item_id in created_ids:
        item = work_items.get_work_item(item_id)
        title = item["fields"]["System.Title"]
        wi_type = item["fields"]["System.WorkItemType"]
        area = item["fields"]["System.AreaPath"]
        state = item["fields"]["System.State"]
        print(f"  [{item_id:3d}] {wi_type:12s} | {state:8s} | {area:30s} | {title}")
    
    print("\n" + "=" * 70)
    print("  CLEANUP COMMANDS")
    print("=" * 70)
    print("  Run these commands to delete created work items:")
    print()
    for item_id in created_ids:
        print(f"  python -m devops_extended delete {item_id}")
    print()
    print("  Or use this one-liner (PowerShell):")
    ids_str = ",".join(str(id) for id in created_ids)
    print(f"  {ids_str} -split ',' | ForEach-Object {{ python -m devops_extended delete $_ }}")
    print()
    print("  Or (Bash):")
    print(f"  for id in {' '.join(str(id) for id in created_ids)}; do python -m devops_extended delete $id; done")
    print("=" * 70)

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

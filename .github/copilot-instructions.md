# Azure DevOps Work Item Management with MCP

This project uses the **Azure DevOps Extended MCP Server** for work item management directly from VS Code via GitHub Copilot.

## Available MCP Tools

Always check if the Azure DevOps MCP server has a relevant tool before suggesting manual actions or web browser navigation.

### Domain Filtering

The server supports **selective tool loading** via domain filtering to optimize performance and respect client tool limits.

**Available Domains:**
- `creation` - 5 tools for creating work items (create_pbi, create_bug, create_task, create_feature, create_epic)
- `updates` - 5 tools for modifying work items (update_work_item_title, assign_work_item, add_comment, transition_state, add_parent_link)
- `queries` - 2 tools for retrieving work items (get_work_item, delete_work_item)
- `metadata` - 5 tools for discovering schema/types/states (get_work_item_types, get_available_states, get_work_item_type_schema, get_work_item_fields, get_work_item_available_states)
- `core` - 4 essential tools (create_pbi, create_bug, create_task, get_work_item)
- `work-items` - 12 tools for all work item operations (creation + updates + queries)

**Configuration Examples:**
```jsonc
// Load only core tools (4 tools)
"args": ["-m", "devops_extended.mcp", "-d", "core"]

// Load multiple domains (10 tools)
"args": ["-m", "devops_extended.mcp", "-d", "creation", "metadata"]

// Load all tools (no filtering, 17 tools)
"args": ["-m", "devops_extended.mcp"]
```

See `examples/mcp-with-domain-filtering.json` for complete examples.

### Work Item Creation
- `create_pbi` - Create Product Backlog Items/User Stories
- `create_bug` - Create Bugs with priority and severity
- `create_task` - Create Tasks with effort estimates
- `create_feature` - Create Features
- `create_epic` - Create Epics

### Work Item Operations
- `get_work_item` - Retrieve work item details by ID
- `update_work_item_title` - Update work item titles
- `assign_work_item` - Assign work items to users
- `add_comment` - Add comments to work items
- `transition_state` - Change work item states (with validation)
- `add_parent_link` - Create hierarchical relationships
- `delete_work_item` - Delete work items

### Metadata Discovery (Dynamic)
- `get_work_item_types` - List all available work item types
- `get_available_states` - Get valid states for a work item type
- `get_work_item_type_schema` - Full schema with fields and metadata
- `get_work_item_fields` - Get all fields with types and constraints
- `get_work_item_available_states` - Get valid states for a specific work item

## Best Practices

### Always Use Dynamic Discovery
This MCP server supports **any Azure DevOps process template** (Agile, Scrum, CMMI, Basic, Custom) through dynamic metadata discovery.

**Before creating work items:**
- Use `get_work_item_types` to see available types
- Use `get_work_item_type_schema` to understand required fields

**Before transitioning states:**
- Use `get_available_states` to see valid states for the work item type
- Use `get_work_item_available_states` to see valid states for a specific work item
- The server validates state transitions automatically

**When exploring fields:**
- Use `get_work_item_fields` to discover all available fields
- Check field metadata for type, required status, and allowed values

### State Transitions
State transitions are **validated automatically** with helpful error messages:
- Invalid state: `"Invalid state 'InvalidState' for User Story. Available states: New, Active, Resolved, Closed"`
- Use validation to guide users to correct states

### Performance
The server uses **thread-safe TTL-based caching** (1 hour default) for:
- Work item types
- Work item type schemas
- Field metadata

Repeated queries are fast and don't hit Azure DevOps API unnecessarily.

### Example Prompts

**Good prompts (use MCP tools):**
- "What work item types are available?"
- "Show me available states for User Story"
- "Create a bug for the login timeout issue with priority 1"
- "Get work item 123"
- "What states can work item 456 transition to?"
- "Mark work item 789 as Resolved"
- "Show me all fields available for Bug work items"

**Avoid manual approaches:**
- ❌ "Open the Azure DevOps web page to create a bug"
- ❌ "You'll need to manually update the work item in the browser"
- ❌ "Check the Azure DevOps documentation for valid states"

### Authentication
This MCP server uses **PAT token authentication** configured via environment variables:
- `AZDO_ORGANIZATION` - Organization name
- `AZDO_PROJECT` - Project name
- `AZDO_PAT` - Personal Access Token

## Process Template Support

Unlike hardcoded implementations, this server works with:
- ✅ **Agile** (Microsoft standard)
- ✅ **Scrum** (Microsoft standard)
- ✅ **CMMI** (Microsoft standard)
- ✅ **Basic** (Microsoft standard)
- ✅ **Custom process templates**

All states, fields, and work item types are discovered dynamically at runtime.

## Key Differentiators

This MCP server provides advantages over other Azure DevOps integrations:

1. **Dynamic Metadata Discovery** - No hardcoded assumptions about process templates
2. **State Validation** - Prevents invalid transitions with helpful error messages
3. **Smart Caching** - Performance optimization without staleness
4. **PAT Authentication** - Works in all environments including CI/CD
5. **Developer-Friendly** - Python-based, easy to extend and customize

## When to Use These Tools

Use Azure DevOps MCP tools for:
- Creating work items during conversations
- Checking work item status
- Transitioning work item states
- Adding comments and updates
- Exploring project metadata
- Validating state transitions

The tools handle all API communication, authentication, and error handling automatically.


# Azure DevOps Extended

A Python package and **Model Context Protocol (MCP) server** for managing Azure DevOps work items (for now). Use it as a CLI tool, Python API, or integrate with AI assistants like Claude, Cline, and GitHub Copilot via MCP.

## 🎯 Why This Exists

The official Azure DevOps MCP server doesn't support PAT authentication. This one does, plus it's built from battle-tested CLI tools that actually work.

## Features

- ✅ **MCP Server** - Works with Claude Desktop, VS Code, and any MCP-compatible client
- ✅ **PAT Authentication** - Use Personal Access Tokens
- ✅ Create work items (PBIs, Bugs, Tasks, Features, Epics)
- ✅ Update work items (title, description, fields)
- ✅ State transitions (dynamic state discovery with validation)
- ✅ Feature ideation mode (`--ideation` flag for quick ideas/notes)
- ✅ Multi-team board support (6 teams with auto-assignment)
- ✅ Assign work items
- ✅ Add comments
- ✅ Delete work items
- ✅ Hierarchical linking (parent-child relationships)
- ✅ Dynamic work item type detection (Scrum/Agile/Basic/CMMI/custom)
- ✅ Hybrid CLI + Python API + MCP interface
- ✅ Type-safe with type hints
- ✅ Environment-based configuration
- ✅ Real-time state tracking for AI agents

## Installation

```bash
# Clone the repository
git clone https://github.com/ragingtortoise/azure_devops_mcp_extended
cd azure_devops_mcp_extended

# Install dependencies
pip install -r requirements.txt

# Or install the package
pip install -e .
```

## Configuration

### Environment Variables

Set the following environment variables (or create a `.env` file):

```bash
AZDO_ORGANIZATION=your-organization
AZDO_PROJECT=your-project
AZDO_PAT=your-personal-access-token
```

To get a Personal Access Token (PAT):
1. Go to `https://dev.azure.com/YOUR_ORG/_usersSettings/tokens`
2. Create a new token with **Work Items (Read, Write)** scope
3. Copy the token and set it as `AZDO_PAT`

## 🚀 Quick Start

**Get started in 5 minutes:** See **[QUICKSTART.md](QUICKSTART.md)**

The Quick Start guide covers:
- MCP Server setup for AI assistants (VS Code, Claude Desktop)
- Command-line interface usage
- Common workflows and use cases

## MCP Server for AI Assistants

Model Context Protocol (MCP) lets AI assistants interact with Azure DevOps.

**Minimal setup:**
1. `pip install -e .`
2. Create `.vscode/mcp.json` (see examples in `examples/` folder)
3. Set environment variables: `AZDO_ORGANIZATION`, `AZDO_PROJECT`, `AZDO_PAT`  
4. Reload VS Code

###Available MCP Tools (17 total)

**1. Create `.vscode/mcp.json` in your project:**

```json
{
  "servers": {
    "devops-extended": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "devops_extended.mcp"]
    }
  }
}
```

**2. Create `.github/copilot-instructions.md`:**

```markdown
This project uses the Azure DevOps Extended MCP Server. Always check if the Azure DevOps MCP server has a relevant tool before suggesting manual actions.
```

**3. Reload VS Code** (`Ctrl+Shift+P` → "Developer: Reload Window")

**4. In GitHub Copilot Chat**, switch to Agent Mode and select the Azure DevOps tools.

> **Note:** The server uses environment variables for authentication (`AZDO_ORGANIZATION`, `AZDO_PROJECT`, `AZDO_PAT`). If you don't have these set, add an `env` section to your `mcp.json` - see examples in the `examples/` folder.

### Alternative: User Settings Configuration
If you prefer user-level configuration, add to your VS Code `settings.json`:

```json
{
  "mcp.servers": {
    "devops-extended": {
      "command": "python",
      "args": ["-m", "devops_extended.mcp"],
      "env": {
        "AZDO_ORGANIZATION": "your-org",
        "AZDO_PROJECT": "your-project",
        "AZDO_PAT": "your-pat-token"
      }
    }
  }
}
```

### Claude Desktop Configuration
Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "devops-extended": {
      "command": "python",
      "args": ["-m", "devops_extended.mcp"],
      "env": {
        "AZDO_ORGANIZATION": "your-org",
        "AZDO_PROJECT": "your-project",
        "AZDO_PAT": "your-pat-token"
      }
    }
  }
}
```

### Currently Available MCP Tools (17 total) - Extending Fast

Once configured, AI assistants can:

**Work Item Creation (5 tools):**
- `create_pbi` - Create Product Backlog Items/User Stories
- `create_bug` - Create Bugs
- `create_task` - Create Tasks
- `create_feature` - Create Features
- `create_epic` - Create Epics

**Work Item Operations (5 tools):**
- `update_work_item_title` - Update titles
- `assign_work_item` - Assign to users
- `add_comment` - Add comments
- `transition_state` - Change work item states (with validation!)
- `add_parent_link` - Create hierarchical relationships

**Work Item Queries (2 tools):**
- `get_work_item` - Retrieve work item details
- `delete_work_item` - Delete work items

**Metadata Discovery (5 tools):**
- `get_work_item_types` - List all available work item types
- `get_available_states` - Get valid states for a work item type
- `get_work_item_type_schema` - Full schema with fields and metadata
- `get_work_item_fields` - Get all fields with types and constraints
- `get_work_item_available_states` - Get valid states for a specific work item

### Domain Filtering (NEW)

**Reduce tool count** by loading only needed domains:

```jsonc
// Load only core tools (4 tools)
{
  "servers": {
    "devops-extended": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "devops_extended.mcp", "-d", "core"]
    }
  }
}

// Load multiple domains (10 tools)
{
  "servers": {
    "devops-extended": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "devops_extended.mcp", "-d", "creation", "metadata"]
    }
  }
}
```

**Available domains:**
- `creation` - 5 tools (create_pbi, create_bug, create_task, create_feature, create_epic)
- `updates` - 5 tools (update_work_item_title, assign_work_item, add_comment, transition_state, add_parent_link)
- `queries` - 2 tools (get_work_item, delete_work_item)
- `metadata` - 5 tools (get_work_item_types, get_available_states, get_work_item_type_schema, get_work_item_fields, get_work_item_available_states)
- `core` - 4 tools (create_pbi, create_bug, create_task, get_work_item)
- `work-items` - 12 tools (creation + updates + queries)

See `examples/mcp-with-domain-filtering.json` for complete examples.

> **🎯 Key Features:**
> - ✅ Dynamic metadata discovery - works with ANY process template (Agile, Scrum, CMMI, Basic, Custom)
> - ✅ State validation - prevents invalid transitions with helpful error messages
> - ✅ Smart caching - thread-safe TTL-based cache for performance
> - ✅ PAT authentication - works in all environments including CI/CD
> - ✅ Domain filtering - load only the tools you need (4-17 tools)


### Testing the MCP Server
Following steps will allow you to test the MCP server if you wish to extend it locally.

```bash
# Test the server directly
python -m devops_extended.mcp

# Test with domain filtering
python -m devops_extended.mcp -d core
python -m devops_extended.mcp -d creation metadata

# It will communicate via stdio (standard input/output)
# Press Ctrl+C to stop
```

### Validating Your Setup

Two validation tools are provided:

**1. Basic Setup Validation** - Quick diagnostic check:
```bash
python validate_setup.py
```
This checks:
- Package imports
- Environment variables
- CLI module
- Dependencies
- Basic functionality

**2. Integration Tests** - Comprehensive end-to-end testing:
```bash
python integration_tests.py
```
This validates:
- Work item creation (PBI, Bug, Task, Feature, Epic)
- Hierarchical linking (Epic → Feature → PBI → Tasks)
- Field updates and state transitions
- Advanced scenarios (reparenting, bulk operations)

⚠️ **WARNING:** Integration tests create real work items in your Azure DevOps project! Cleanup commands are provided at the end.

**Optional Configuration:**
```bash
# Assign to specific team/area
export TEST_TEAM=MyTeam  # Unix
$env:TEST_TEAM="MyTeam"  # PowerShell

# Assign to specific user
export TEST_USER=user@example.com  # Unix
$env:TEST_USER="user@example.com"  # PowerShell
```


## Usage

### Command-Line Interface

The package can be used via CLI in multiple ways:

```bash
# As a module
python -m devops_extended <command> [options]

# After pip install (console script)
devops-extended <command> [options]
```

#### Examples

**Create a PBI:**
```bash
python -m devops_extended create-pbi "Implement user authentication" \
    -d "Add OAuth2 authentication flow" \
    -p 1 \
    -e 5 \
    -t "authentication,security"
```

**Create a Bug:**
```bash
python -m devops_extended create-bug "Login button not responding" \
    -r "1. Go to login page\n2. Click login\n3. Nothing happens" \
    --severity 2 \
    -p 1
```

**Create a Task:**
```bash
python -m devops_extended create-task "Write unit tests for auth module" \
    -d "Cover all authentication scenarios" \
    --activity "Testing" \
    -r 8 \
    -o 8
```

**Update work item:**
```bash
python -m devops_extended update-title 123 "New title"
python -m devops_extended assign 123 "user@example.com"
python -m devops_extended comment 123 "Work in progress"
```

**Change state:**
```bash
python -m devops_extended state 123 active
python -m devops_extended state 123 resolved
python -m devops_extended state 123 removed
```

**Get work item:**
```bash
python -m devops_extended get 123
python -m devops_extended get 123 -v  # Verbose JSON output
```

**Delete work item:**
```bash
python -m devops_extended delete 123
python -m devops_extended delete 123 --permanent
```

### Programmatic Usage

```python
from devops_extended import (
    create_pbi,
    create_bug,
    update_work_item,
    transition_to_active,
    add_comment,
)

# Create a PBI
pbi = create_pbi(
    title="Implement new feature",
    description="Detailed description here",
    priority=1,
    effort=8,
    tags="feature,priority"
)
print(f"Created PBI #{pbi['id']}")

# Create a bug
bug = create_bug(
    title="Fix critical issue",
    repro_steps="Steps to reproduce...",
    severity="1",
    priority=1
)

# Update and transition
transition_to_active(pbi['id'])
add_comment(pbi['id'], "Starting work on this")

# Update multiple fields
update_work_item(pbi['id'], {
    "System.Title": "Updated title",
    "Microsoft.VSTS.Scheduling.Effort": 13
})
```

## AI Agent Integration

This package is designed to work with AI agents (like GitHub Copilot). Add instructions to your Copilot configuration:

```markdown
## Azure DevOps Integration

When the user asks to create or manage Azure DevOps work items:

1. Clone the repository if not present: `git clone <repo-url>`
2. Use the `devops_extended` package
3. Run commands via terminal using `python -m devops_extended`

Examples:
- "Create a PBI for <feature>": Use `create-pbi` command
- "Create bugs for these issues": Use `create-bug` command  
- "Mark work item as done": Use `state <id> closed` command
- "Update PBI description": Use `update-description` command
```

## Available Commands

### Work Item Creation
- `create-pbi` - Create Product Backlog Item
- `create-bug` - Create Bug
- `create-task` - Create Task
- `create-feature` - Create Feature
- `create-epic` - Create Epic

### Work Item Operations
- `get` - Get work item by ID
- `update` - Update work item fields (JSON)
- `update-title` - Update work item title
- `update-description` - Update work item description
- `assign` - Assign work item to user
- `comment` - Add comment to work item
- `state` - Change work item state
- `delete` - Delete work item

### State Transitions
- `new` - Move to New state
- `active` - Move to Active state
- `resolved` - Move to Resolved state
- `closed` - Move to Closed state
- `removed` - Move to Removed state

## Common Options

- `-v, --verbose` - Show full JSON response
- `-d, --description` - Item description
- `-p, --priority` - Priority (1-4, where 1 is highest)
- `-t, --tags` - Comma-separated tags
- `-a, --assigned-to` - Assignee email/name
- `--area-path` - Area path
- `--iteration-path` - Iteration path

## Work Item Fields

### PBI Fields
- Title, Description, Priority, Effort (story points), Value Area, Tags

### Bug Fields
- Title, Repro Steps, System Info, Severity, Priority, Tags

### Task Fields
- Title, Description, Activity, Remaining Work, Original Estimate, Tags

### Feature/Epic Fields
- Title, Description, Priority, Value Area, Start/Target Date, Tags

## Error Handling

The package will raise clear errors for:
- Missing environment variables
- Invalid work item IDs
- API authentication failures
- Network issues

Use `--verbose` flag for detailed error information.

## Development

```bash
# Install in development mode
pip install -e .

# Run tests (when added)
pytest

# Type checking
mypy devops_extended
```

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes (MCP + CLI setup)
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - AI assistant integration guide

## License

MIT License

## Author

RagingTortoise 🐢

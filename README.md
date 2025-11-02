# Azure DevOps Extended

A Python package and **Model Context Protocol (MCP) server** for managing Azure DevOps work items — designed to go beyond Microsoft’s official implementation.

Integrate it with **AI assistants** like Claude, Cline, and GitHub Copilot via MCP, or use it as a **CLI tool**, or as **Python API**.

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()

---

## At a Glance

| Interface | Supported | Description |
|------------|------------|-------------|
| 💻 CLI Tool | ✅ | Automate DevOps work items from terminal |
| 🐍 Python API | ✅ | Use in scripts and AI workflows |
| 🤖 MCP Server | ✅ | Integrate with Claude, Cline, Copilot, VS Code |

---

## 🎯 Why This Exists

This repository originated as an individual tool designed to fill the functional gaps in the [official Azure DevOps MCP Server](https://github.com/microsoft/azure-devops-mcp). Over time, it evolved into its current state, incorporating broader capabilities and improved maintainability.

**Azure DevOps Extended** fills those gaps with:
- ✅ PAT Authentication support
- ✅ Dynamic metadata discovery for all process templates (Agile, Scrum, CMMI, Basic, or custom)
- ✅ Validated state transitions
- ✅ Hybrid architecture (MCP + CLI + Python API)

---

## 🚀 Features

### 🧩 Core Features
- Full work item CRUD support (PBIs, Bugs, Tasks, Features, Epics)
- PAT-based authentication
- Hierarchical linking (parent-child)
- Commenting and assignment
- Multi-team support with auto-assignment
- Real-time state tracking for AI agents

### 🧠 MCP Features
- 13 available MCP tools (creation, updates, queries, metadata), many more on the way
- Generic field update tool for maximum flexibility
- Domain filtering (`-d` flag) — load only the tools you need
- Dynamic metadata and schema discovery
- Process template agnostic
- Works seamlessly with Claude, Cline, GitHub Copilot, and VS Code

### 👨‍💻 Developer Features
- CLI and Python API
- Type-safe with complete type hints
- Environment-based configuration
- Smart caching with TTL
- Integrated validation tools and tests
- Extensible architecture for new MCP tools

---

## ⚙️ Installation

```bash
# Clone repository
git clone https://github.com/ragingtortoise/azure_devops_mcp_extended
cd azure_devops_mcp_extended

# Install dependencies
pip install -r requirements.txt

# Or install as package
pip install -e .
```

---

## 🔧 Configuration

### Environment Variables
Set the following or create a `.env` file:

```bash
AZDO_ORGANIZATION=your-organization
AZDO_PROJECT=your-project
AZDO_PAT=your-personal-access-token
```

To get a PAT:
1. Go to `https://dev.azure.com/YOUR_ORG/_usersSettings/tokens`
2. Create a token with **Work Items (Read, Write)** scope
3. Copy it and set `AZDO_PAT`

---

## ⚡ Quick Start

**Get started in under 5 minutes:**  
See [QUICKSTART.md](QUICKSTART.md) for complete MCP + CLI setup.

### Example (minimal MCP config for VS Code)

```json
{
  "servers": {
    "devops-extended": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "devops_extended.mcp"],
      "env": {
        "AZDO_ORGANIZATION": "your-org",
        "AZDO_PROJECT": "your-project",
        "AZDO_PAT": "your-token"
      }
    }
  }
}
```

### Claude Desktop Configuration
Add to:
- macOS → `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows → `%APPDATA%\\Claude\\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "devops-extended": {
      "command": "python",
      "args": ["-m", "devops_extended.mcp"],
      "env": {
        "AZDO_ORGANIZATION": "your-org",
        "AZDO_PROJECT": "your-project",
        "AZDO_PAT": "your-pat"
      }
    }
  }
}
```

---

## 🧩 MCP Tools Overview

| Domain | Tools | Description |
|---------|-------|-------------|
| `creation` | 1 | Create work items (unified tool for all types) |
| `updates` | 6 | Update any fields, titles, assign, add comments, transition, link |
| `queries` | 2 | Get or delete work items |
| `metadata` | 5 | Work item types, fields, states, schemas |
| `core` | 2 | Minimal loadout for fast startup (create + get) |
| `work-items` | 9 | All creation + update + query tools |

### New in v0.3.0 ✨
- **Generic `update_work_item` tool**: Update any work item field using field reference names (e.g., `System.AreaPath`, `System.IterationPath`)
- **Area path support in work item creation**: Specify area paths directly when creating work items

Example domain filtering:
```json
{
  "args": ["-m", "devops_extended.mcp", "-d", "creation", "metadata"]
}
```

See `examples/mcp-with-domain-filtering.json` for more.

---

## 🧪 Testing & Validation

**Basic Setup Validation**
```bash
python validate_setup.py
```

Checks:
- Imports, environment, dependencies, and CLI module.

**Integration Tests**
```bash
python integration_tests.py
```

Validates:
- Work item creation and linking
- Field updates & state transitions
- Advanced scenarios (bulk ops, reparenting)

> ⚠️ Creates real work items. Cleanup commands included.

Optional test configuration:
```bash
export TEST_TEAM=MyTeam
export TEST_USER=user@example.com
```

---

## 💻 Command-Line Usage

```bash
python -m devops_extended <command> [options]
# or
devops-extended <command> [options]
```

### Examples
```bash
# Create PBI
python -m devops_extended create-pbi "Implement OAuth2" -d "Add login flow" -p 1 -e 5 -t "auth,security"

# Create Bug
python -m devops_extended create-bug "Login button unresponsive" -r "Steps..." --severity 2 -p 1

# Update & assign
python -m devops_extended update-title 123 "New title"
python -m devops_extended assign 123 "user@example.com"
python -m devops_extended comment 123 "Work in progress"

# Change state
python -m devops_extended state 123 active
```

---

## 🐍 Programmatic Usage

```python
from devops_extended import create_work_item, update_work_item, transition_state, add_comment

# Create any type of work item
bug = create_work_item("Bug", "Login fails", severity="1", priority=1, repro_steps="Click login")
story = create_work_item("User Story", "Add search", effort=5, priority=1, value_area="Business")
task = create_work_item("Task", "Write tests", activity="Testing", remaining_work=4)
custom = create_work_item("Custom Type", "My item", custom_fields={"Custom.Field": "value"})

# Update and transition
transition_state(bug['id'], "Active")
add_comment(bug['id'], "Started investigation")
update_work_item(bug['id'], {"System.Title": "Updated title"})
```

---

## 🤖 AI Assistant Integration

Add to `.github/copilot-instructions.md`:

```markdown
## Azure DevOps Integration

When asked to manage Azure DevOps work items:
- Use the `devops_extended` package
- Run commands via `python -m devops_extended`
- Check for matching MCP tools before manual steps
```

---

## 🧭 Roadmap

- [ ] WIQL query support  
- [ ] Pull request / repository operations  
- [ ] Work item analytics and summaries  
- [ ] AI-assisted work item ideation  
- [ ] Optional REST API layer  

See [docs/ROADMAP.md](docs/ROADMAP.md) for detailed roadmap and version history.

---

## ⚙️ Development

```bash
pip install -e .
pytest
mypy devops_extended
```

---

## 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) – setup in under 5 minutes  
- [.github/copilot-instructions.md](.github/copilot-instructions.md) – AI integration guide  
- [examples/](examples/) – MCP, domain filtering, and config examples  

---


## 🪪 License
MIT License © RagingTortoise (Selim S. Balci)
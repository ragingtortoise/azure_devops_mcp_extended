# Quick Start Guide

Get started with the Azure DevOps Extended tool quickly.

## Installation Options

### Option 1: MCP Server for AI Assistants (Recommended)

**Best for:** Using with GitHub Copilot, Claude, or other AI assistants

**1. Install the package:**
```powershell
pip install -e .
```

**2. Create `.vscode/mcp.json` in your project:**
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

> **Domain Filtering (NEW):** Load only needed tools:
> ```json
> "args": ["-m", "devops_extended.mcp", "-d", "core"]
> ```
> See `examples/mcp-with-domain-filtering.json` for more options.

**3. Create `.github/copilot-instructions.md`:**
```markdown
This project uses the Azure DevOps Extended MCP Server. Always check if the Azure DevOps MCP server has a relevant tool before suggesting manual actions.
```

**4. Set environment variables:**
```powershell
$env:AZDO_ORGANIZATION = "your-organization"
$env:AZDO_PROJECT = "your-project"
$env:AZDO_PAT = "your-personal-access-token"
```

**5. Reload VS Code** (`Ctrl+Shift+P` → "Developer: Reload Window")

**6. Try it:** In GitHub Copilot Chat, ask:
- "What work item types are available?"
- "Create a bug for the login issue"
- "Show me available states for User Story"

**See:** `VSCODE_MCP_SETUP_GUIDE.md` for detailed setup instructions.

---

### Option 2: Command-Line Interface

**Best for:** Scripting, automation, CI/CD pipelines

## Step 1: Set Up Environment Variables

Create a `.env` file or set environment variables:

```powershell
# PowerShell
$env:AZDO_ORGANIZATION = "your-organization"
$env:AZDO_PROJECT = "your-project"
$env:AZDO_PAT = "your-personal-access-token"
```

**Get your PAT:**
1. Go to https://dev.azure.com/YOUR_ORG/_usersSettings/tokens
2. Click "New Token"
3. Name: "DevOps Tools"
4. Scopes: Select "Work Items" → "Read & Write"
5. Click "Create" and copy the token

## Step 2: Install Dependencies

```powershell
pip install -r requirements.txt
```

## Step 3: Validate Setup

```powershell
python validate_setup.py
```

You should see all checks pass ✅

## Step 4: Create Your First Work Item

```powershell
# Create a PBI
python -m devops_extended create-pbi "My First PBI" -d "Testing the tool" -p 2 -e 3

# Create a Bug
python -m devops_extended create-bug "Test Bug" -r "Just testing" --severity 3 -p 3

# Create a Task
python -m devops_extended create-task "My Task" -d "Task description" --activity "Development"
```

## Step 5: Manage Work Items

```powershell
# Get a work item (replace 123 with your work item ID)
python -m devops_extended get 123

# Update title
python -m devops_extended update-title 123 "Updated Title"

# Assign to someone
python -m devops_extended assign 123 "user@example.com"

# Add a comment
python -m devops_extended comment 123 "This is a comment"

# Change state
python -m devops_extended state 123 active
python -m devops_extended state 123 resolved
python -m devops_extended state 123 closed
```

## Common Use Cases

### Scenario: Create a Feature with Tasks

```powershell
# 1. Create a Feature
python -m devops_extended create-feature "User Authentication" `
    -d "Implement OAuth2 authentication" `
    -p 1 `
    --target-date "2024-12-31"

# 2. Create related tasks (note the feature ID from step 1)
python -m devops_extended create-task "Set up OAuth provider" -d "Configure OAuth2" --activity "Development"
python -m devops_extended create-task "Write auth tests" -d "Unit tests for auth" --activity "Testing"
```

### Scenario: Bug Workflow

```powershell
# 1. Create bug
python -m devops_extended create-bug "Login fails on Safari" `
    -r "1. Open Safari\n2. Try to login\n3. Error appears" `
    --severity 2 `
    -p 1 `
    -t "bug,browser,critical"

# Output will show: Work Item Created: ID: 456

# 2. Assign to developer
python -m devops_extended assign 456 "dev@example.com"

# 3. Move to active
python -m devops_extended state 456 active

# 4. Add progress updates
python -m devops_extended comment 456 "Found the issue - fixing now"

# 5. Mark as resolved
python -m devops_extended state 456 resolved

# 6. Close after verification
python -m devops_extended state 456 closed
```

### Scenario: Bulk Create PBIs from List

```powershell
# Create multiple PBIs
python -m devops_extended create-pbi "Implement user profile page" -p 2 -e 5
python -m devops_extended create-pbi "Add search functionality" -p 1 -e 8
python -m devops_extended create-pbi "Improve performance" -p 3 -e 3
python -m devops_extended create-pbi "Add export to CSV" -p 2 -e 5
```

## Pro Tips 💡

1. **Use `-v` for details**: Add `-v` flag to see full JSON response
   ```powershell
   python -m devops_extended get 123 -v
   ```

2. **Rich descriptions**: Descriptions support HTML
   ```powershell
   python -m devops_extended create-pbi "Feature" `
       -d "<h2>Overview</h2><p>Details here</p><ul><li>Item 1</li><li>Item 2</li></ul>"
   ```

3. **Tag everything**: Tags help with organization
   ```powershell
   -t "priority,frontend,sprint-1"
   ```

4. **Check state transitions**: Not all transitions are valid
   ```
   new → active → resolved → closed ✅
   new → closed (might require intermediate states)
   ```

## Troubleshooting

### Error: "Invalid configuration"
- Check environment variables are set
- Verify organization and project names are correct

### Error: "401 Unauthorized"
- PAT might be expired - generate a new one
- PAT needs "Work Items (Read, Write)" permissions

### Error: "Work item not found"
- Double-check the work item ID
- Ensure you're in the correct project

### Error: "Invalid state transition"
- Check available states with current work item type
- Some transitions require intermediate states

## Next Steps

- Read the full [README.md](README.md) for all features
- Check [examples/example_usage.py](examples/example_usage.py) for programmatic usage
- See [.github/copilot-instructions.md](.github/copilot-instructions.md) for AI agent integration

## Need Help?

- Check work item in browser: `https://dev.azure.com/YOUR_ORG/YOUR_PROJECT/_workitems/edit/ID`
- Use `--help` flag: `python -m devops_extended --help`
- Use `-v` for verbose output to debug issues

---

Happy work item managing! 🐢✨


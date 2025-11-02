# Changelog

All notable changes to Azure DevOps Extended will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-11-02

### Added
- **Generic `update_work_item` MCP tool** (#535): Update any work item field using field reference names
  - Accepts dictionary of field updates (e.g., `{"System.AreaPath": "Project\\Area", "Microsoft.VSTS.Common.Priority": 1}`)
  - Eliminates need for REST API workarounds when updating fields beyond title/assignee/state
  - Use `get_work_item_fields` tool to discover available field reference names
- **Area path support in work item creation** (#534): Specify area paths directly when creating work items via the `area_path` parameter
  - Works with `create_work_item` and all type-specific creation functions
  - Supports format like `"ProjectName\\Area\\SubArea"`
  - No longer creates work items at project root by default when area path is specified

### Changed
- Updated tool count documentation (13 tools total after consolidation in v0.2.0)
- Improved README documentation with clearer tool categories and counts
- Updated ROADMAP to reflect completed Phase 2 features

### Fixed
- Clarified area path behavior in documentation

## [0.2.0] - 2025-10-26

### Added
- Unified `create_work_item` tool supporting all work item types including custom types
- Custom fields support via `custom_fields` parameter
- Domain filtering for selective tool loading
- Thread-safe TTL-based metadata caching
- Dynamic work item type detection
- Comprehensive integration tests
- Example configurations for VS Code and Claude Desktop

### Changed
- Refactored from 5 separate creation tools to unified `create_work_item` tool
- Reduced total tool count from 17 → 13 tools
- Improved error handling with detailed Azure DevOps responses
- Updated documentation structure

### Fixed
- URL encoding bugs in work item type names
- State transition validation edge cases

## [0.1.0] - 2025-10-24

### Added
- Initial release with MCP server implementation
- PAT authentication support
- Core work item operations (create, read, update, delete)
- State transitions with validation
- Comment system
- Parent-child linking
- CLI interface
- Python API
- Basic documentation

[0.3.0]: https://github.com/ragingtortoise/azure_devops_mcp_extended/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/ragingtortoise/azure_devops_mcp_extended/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/ragingtortoise/azure_devops_mcp_extended/releases/tag/v0.1.0

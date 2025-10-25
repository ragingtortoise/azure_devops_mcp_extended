# Azure DevOps Extended - Roadmap

This document outlines the planned development phases for Azure DevOps Extended, an MCP server and CLI tool for Azure DevOps work item management.

**Last Updated:** October 25, 2025  
**Current Version:** 0.2.0  
**Status:** Public Release

---

## Phase 1: Foundation & Stability ✅ (COMPLETED)

**Status:** Released as v0.2.0

### Completed Features
- [x] Core work item creation (unified create_work_item tool)
- [x] Support for all work item types including custom types
- [x] Dynamic work item type detection (Agile/Scrum/CMMI/Basic/Custom)
- [x] Work item updates (title, description, fields)
- [x] State transitions with validation
- [x] Comment system
- [x] Parent-child linking (hierarchical relationships)
- [x] MCP server implementation with 13 tools
- [x] Domain filtering for selective tool loading
- [x] PAT authentication
- [x] CLI interface with console script
- [x] Python API for programmatic usage
- [x] Thread-safe TTL-based metadata caching
- [x] Comprehensive documentation (README, QUICKSTART)
- [x] Example configurations for VS Code and Claude Desktop
- [x] Integration tests and validation scripts

### Recent Changes (v0.2.0)
- [x] Refactored to unified create_work_item tool (from 5 separate tools)
- [x] Added custom fields support
- [x] Improved error handling with detailed Azure DevOps responses
- [x] Fixed URL encoding bugs
- [x] Reduced total tool count from 17 → 13 tools

---

## Phase 2: Enhanced Query & Search 🔄 (IN PROGRESS)

**Focus:** Improve work item discovery and batch operations

### Planned Features
- [ ] **Query Builder**
  - [ ] WIQL (Work Item Query Language) support
  - [ ] Predefined query templates (My Work, Recent Items, etc.)
  - [ ] Custom query creation via MCP tools
  
- [ ] **Batch Operations**
  - [ ] Bulk work item creation from CSV/JSON
  - [ ] Bulk state transitions
  - [ ] Bulk field updates
  - [ ] Batch tagging operations

- [ ] **Search & Filter**
  - [ ] Full-text search across work items
  - [ ] Advanced filtering by multiple criteria
  - [ ] Saved search configurations
  - [ ] Search within specific iterations/sprints

- [ ] **Work Item Lists**
  - [ ] Get work items by iteration
  - [ ] Get work items by area path
  - [ ] Get child work items for a parent
  - [ ] Get related work items

---

## Phase 3: Rich Content & Attachments 📎

**Focus:** Handle work item attachments and rich content

### Planned Features
- [ ] **Attachment Management**
  - [ ] Upload attachments to work items
  - [ ] Download attachments from work items
  - [ ] List all attachments for a work item
  - [ ] Delete attachments

- [ ] **Rich Text Editing**
  - [ ] Markdown to HTML conversion
  - [ ] HTML sanitization for security
  - [ ] Image embedding in descriptions
  - [ ] Code block formatting

- [ ] **Links & Relations**
  - [ ] Create custom link types (Related, Duplicate, etc.)
  - [ ] Bi-directional link management
  - [ ] Link visualization in CLI output
  - [ ] Dependency tracking

---

## Phase 4: Team & Sprint Management 🏃

**Focus:** Sprint planning and team collaboration features

### Planned Features
- [ ] **Sprint/Iteration Management**
  - [ ] Create and manage sprints
  - [ ] Sprint capacity planning
  - [ ] Sprint burndown tracking
  - [ ] Move work items between sprints

- [ ] **Team Configuration**
  - [ ] List team members
  - [ ] Team capacity management
  - [ ] Team velocity tracking
  - [ ] Assign work to teams via area paths

- [ ] **Board Management**
  - [ ] Get board columns and swimlanes
  - [ ] Move work items on board
  - [ ] Board configuration queries
  - [ ] Kanban board support

- [ ] **Notifications**
  - [ ] Watch/unwatch work items
  - [ ] Mention users in comments (@mentions)
  - [ ] Subscribe to work item changes

---

## Phase 5: Reporting & Analytics 📊

**Focus:** Insights and metrics for project tracking

### Planned Features
- [ ] **Metrics & Reports**
  - [ ] Work item statistics (count by type, state)
  - [ ] Velocity calculations
  - [ ] Cycle time analysis
  - [ ] Lead time tracking

- [ ] **Visualization**
  - [ ] ASCII/Unicode charts in CLI
  - [ ] Burndown chart data export
  - [ ] Cumulative flow diagram data
  - [ ] Export data for external visualization tools

- [ ] **Custom Reports**
  - [ ] Report templates
  - [ ] Scheduled report generation
  - [ ] Export to CSV/JSON/Markdown
  - [ ] Email report summaries

---

## Phase 6: Advanced Features & Integrations 🔌

**Target:** 2027  
**Focus:** Extend capabilities and integrate with other tools

### Planned Features
- [ ] **Git Integration**
  - [ ] Link commits to work items
  - [ ] Create branches from work items
  - [ ] Pull request linking
  - [ ] Commit message parsing for auto-linking

- [ ] **Pipeline Integration**
  - [ ] Link builds/deployments to work items
  - [ ] Auto-transition on successful deployment
  - [ ] Release notes generation from work items

- [ ] **External Tool Integration**
  - [ ] Slack notifications
  - [ ] Microsoft Teams webhooks
  - [ ] Jira import/export
  - [ ] GitHub Issues sync

- [ ] **AI Enhancements**
  - [ ] Auto-tagging based on content
  - [ ] Work item similarity detection
  - [ ] Effort estimation suggestions
  - [ ] Natural language query processing

- [ ] **Templates & Automation**
  - [ ] Work item templates
  - [ ] Automation rules (if-then conditions)
  - [ ] Auto-assignment based on rules
  - [ ] Scheduled work item creation

---

## Phase 7: Enterprise & Scale 🏢

**Focus:** Enterprise features and scalability

### Planned Features
- [ ] **Multi-Organization Support**
  - [ ] Switch between organizations
  - [ ] Cross-organization work item references
  - [ ] Consolidated reporting across orgs

- [ ] **Performance Optimization**
  - [ ] Parallel API calls for batch operations
  - [ ] Response pagination for large datasets
  - [ ] Enhanced caching strategies
  - [ ] GraphQL API support (if available)

- [ ] **Security & Compliance**
  - [ ] Audit logging
  - [ ] Field-level permissions
  - [ ] Data encryption at rest
  - [ ] GDPR compliance features

- [ ] **Admin Features**
  - [ ] Process template customization
  - [ ] Field schema management
  - [ ] Work item type customization
  - [ ] State workflow configuration

---

## Continuous Improvements 🔧

These items are ongoing throughout all phases:

### Code Quality
- [ ] Expand test coverage to 90%+
- [ ] Performance benchmarking
- [ ] Memory profiling and optimization
- [ ] Code quality metrics (complexity, maintainability)

### Documentation
- [ ] API reference documentation
- [ ] Video tutorials
- [ ] Best practices guide
- [ ] Troubleshooting guide
- [ ] Migration guides for version upgrades

### Developer Experience
- [ ] VS Code extension for direct integration
- [ ] PyPI package publishing
- [ ] Docker container for easy deployment
- [ ] GitHub Actions workflows
- [ ] Contribution guidelines

### Community
- [ ] Issue templates
- [ ] Feature request process
- [ ] Community plugins/extensions
- [ ] Regular release cadence
- [ ] Changelog maintenance

---

## Feature Requests & Community Input 💡

We welcome community feedback! To request a feature:

1. Check if it's already on the roadmap
2. Search existing GitHub issues
3. Create a new issue with the `feature-request` label
4. Provide use case and expected behavior

**Priority Criteria:**
- **High:** Critical functionality, affects many users, aligns with core mission
- **Medium:** Useful feature, moderate impact, nice-to-have
- **Low:** Edge case, workaround exists, specialized use case

---

## Contributing

Want to help implement features from this roadmap?

1. Check the roadmap for unassigned items
2. Comment on relevant GitHub issues
3. Fork the repository
4. Submit a pull request
5. Follow the contribution guidelines

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

---

## Feedback & Updates

This roadmap is a living document and will evolve based on:
- Community feedback
- Technical feasibility
- Azure DevOps API changes
- MCP protocol updates
- User needs and priorities

**Have questions or suggestions?** Open an issue on GitHub!

---

**Note:** Features may be added, removed, or reprioritized based on community needs and development resources.

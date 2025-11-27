# NewsSummary Documentation Index

**Status**: Planned
**Priority**: 5
**Last Updated**: 2025-11-27

---

## 📂 Quick Start

**When Starting Work on NewsSummary:**

1. **Read first**:
   - Project-level `README.md` - Complete setup guide and documentation
   - `Tasks/current-sprint.md` - Active work items
   - This .agent/README.md - Documentation overview

2. **Reference as needed**:
   - `System/tech-stack.md` - Technologies and architecture
   - `System/integrations.md` - RSS feeds and external services
   - Project files: `config.yaml`, `frequency_words.txt`, `RSS-Feeds-Configuration.md`

---

## 📋 Current Tasks & Work Items

**Task System**: Legacy System (current-sprint.md)

**Active Work**: See `Tasks/current-sprint.md`
**Future Features**: See `Tasks/backlog.md`

**Quick Status:**
- Configuration complete and ready for deployment
- Fork TrendRadar repository
- Deploy configuration to GitHub
- Test and optimize delivery schedule

---

## 🎯 Project Quick Reference

### Project Overview
- **Purpose**: Personalized news aggregation system with twice-daily email delivery (5 AM & 7 PM)
- **Platform**: TrendRadar (GitHub-based, free tier)
- **Status**: Configuration ready for deployment
- **Start Date**: 2025-11-23
- **Completion**: Configuration phase 100%, Deployment phase 0%

### Tech Stack Summary
- **Frontend**: GitHub Pages (web dashboard)
- **Backend**: GitHub Actions (automated workflows)
- **Aggregation**: TrendRadar platform
- **Email**: SMTP (Gmail app password)
- **Notifications**: Telegram bot (optional)
- **Key Dependencies**: TrendRadar, RSS feeds (25 sources)

### Key Metrics & Goals
- Deliver 2 curated digests per day (5 AM & 7 PM)
- Filter ~200-300 raw articles down to ~40-50 curated articles
- <5 Telegram alerts per day for breaking news
- 85% noise reduction, 90% signal retention
- Save 2+ hours per day vs manual news browsing

### News Sources Configured (25 RSS Feeds)
- **Financial (6)**: ZeroHedge, Reuters Business, Financial Times, NPR Business, BBC Business, Politico Economy
- **Political (7)**: Politico, Politico Congress, The Federalist, NPR Politics, The Hill, BBC World News, BBC US & Canada
- **Technology (4)**: TechCrunch AI, TechCrunch Startups, BBC Technology, NPR Technology
- **Sports (4)**: LA Times Sports, ESPN NFL, ESPN NBA, ESPN MLB
- **General (2)**: Axios, NPR National News
- **Built-in (2)**: HackerNews, GitHub Trending

### Related Projects
- None currently (standalone news aggregation project)

---

## 🗂️ Documentation Structure

### Tasks/ - What Needs to Be Done

**Purpose**: Track work items using legacy single-file system

**Files:**
- `current-sprint.md` - Active work with checkboxes
- `backlog.md` - Future features, ideas, optimizations

**When to Update**: After each work session, when tasks complete, when new work identified

### System/ - Current State of Project

**Purpose**: Document architecture, integrations, and technical implementation

**Files:**
- `tech-stack.md` - TrendRadar platform, GitHub Actions, RSS architecture
- `integrations.md` - 25 RSS feeds, email SMTP, Telegram bot, GitHub Pages

**When to Update**: After adding RSS feeds, changing configuration, deployment setup

### SOPs/ - How to Do Common Tasks

**Purpose**: Step-by-step procedures for repeatable operations

**Examples:**
- How to add a new RSS feed
- How to adjust keyword filters
- How to change delivery schedule
- How to troubleshoot email delivery
- How to optimize feed weights

**Note**: SOPs/ will be built as we discover common maintenance patterns

### Design/ - Not Applicable

This project has no frontend UI component (email-based delivery only), so Design/ documentation is not needed.

---

## 🔄 Maintaining This Documentation

### After Implementation Work

**What to Update:**
1. **System/integrations.md** - If RSS feeds are added/removed
2. **Tasks/** - Mark completed deployment steps, add optimization tasks
3. **SOPs/** - Create procedures for common maintenance operations
4. **README.md** - Update status and completion percentage

### Update Frequency Guidelines

- **README.md**: When deployment status changes
- **Tasks/**: After each work session
- **System/**: After adding feeds or changing configuration
- **SOPs/**: When repeatable processes are discovered

### Documentation Quality Checklist

- [x] README.md has accurate status and priority
- [x] Tasks/current-sprint.md exists
- [x] System/tech-stack.md created
- [x] System/integrations.md created
- [x] All placeholder text replaced
- [x] Last Updated date is current
- [x] Quick Start section has relevant file references
- [x] Task system clearly identified (legacy)

---

## 🔑 Connection Info & Credentials

**Location**: Project-level `CLAUDE.md` file (to be created during deployment)

**Will Contain**:
- GitHub Secrets configuration (EMAIL_*, TELEGRAM_*)
- Gmail app-specific password setup
- Telegram bot token and chat ID
- GitHub repository details

**Security Note**: Credentials will be stored in GitHub Secrets (encrypted), not in project files

---

## 📖 Product Requirements

**Location**: Project-level `README.md` (comprehensive documentation)

**Key Requirements**:
- Twice-daily email delivery (5 AM & 7 PM)
- 25+ RSS sources across 5 categories
- Keyword filtering to reduce noise by 60-70%
- Telegram alerts for breaking news only (<5/day)
- Web dashboard with 7-day searchable archive
- Zero-cost infrastructure (GitHub only)

---

## 🔗 Cross-References

**Workspace Documentation:**
- Main CLAUDE.md: `/home/cpbjr/Documents/AI_Automation/CLAUDE.md`
- .agent Template: `/home/cpbjr/Documents/AI_Automation/docs/.agent-template/`

**Project Documentation:**
- Main README: `../README.md` (comprehensive guide)
- TrendRadar Analysis: `../TrendRadar-Analysis.md` (17 KB setup guide)
- RSS Feeds Configuration: `../RSS-Feeds-Configuration.md` (30+ feed URLs)
- Config File: `../config.yaml` (ready-to-deploy configuration)
- Keyword Filters: `../frequency_words.txt` (filtering rules)

**External Resources:**
- TrendRadar Repository: https://github.com/sansan0/TrendRadar
- GitHub Actions Docs: https://docs.github.com/en/actions
- GitHub Pages Docs: https://docs.github.com/en/pages

---

## 📝 Template Information

**Template Version**: 2.0
**Created**: 2025-11-27
**Customized For**: NewsSummary project
**Source**: `/home/cpbjr/Documents/AI_Automation/docs/.agent-template/README.md`

---

**🎯 Remember**: This documentation exists to save future Claude Code sessions (and you!) time by preserving context. Keep it current, keep it concise, keep it useful.

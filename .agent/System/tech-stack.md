# NewsSummary Tech Stack

**Last Updated**: 2025-11-27

---

## Platform Architecture

### Core Platform
- **TrendRadar**: GitHub-based news aggregation platform
  - Repository: https://github.com/sansan0/TrendRadar
  - License: Open source
  - Deployment: Fork and customize

### Infrastructure
- **GitHub Actions**: Workflow automation (free tier: 2,000 minutes/month)
- **GitHub Pages**: Web dashboard hosting (static site)
- **GitHub Secrets**: Encrypted credential storage

---

## News Aggregation System

### RSS Feed Processing
- **Feed Sources**: 25 custom RSS feeds + 2 built-in platforms
- **Update Frequency**: Every digest generation (twice daily)
- **Parser**: TrendRadar RSS parser (XML processing)
- **Deduplication**: 85% similarity threshold within 24-hour window

### Ranking Algorithm
**Composite scoring system:**
- Platform rank: 50% weight
- Cross-platform frequency: 40% weight
- Stability: 10% weight

**Configurable via**: `config.yaml` → `weights:` section

### Filtering System
- **Keyword filtering**: `frequency_words.txt`
- **Category limits**: Tech (15), Finance (12), Politics (10), Sports (8), General (10), World (8)
- **Quality filters**: Min 100 chars, English only
- **Deduplication**: Title similarity + time window

---

## Delivery Channels

### 1. Email (Primary)
- **Protocol**: SMTP over TLS
- **Provider**: Gmail (app-specific password)
- **Port**: 587
- **Format**: HTML with platform icons, ranking scores, links
- **Schedule**: 5 AM & 7 PM (timezone configurable)
- **Max Articles**: 50 per digest

### 2. Web Dashboard (Secondary)
- **Platform**: GitHub Pages
- **URL Pattern**: `username.github.io/TrendRadar`
- **Update Frequency**: Hourly
- **Features**:
  - Search last 7 days
  - Filter by platform, keyword, date
  - Trending topics visualization
  - CSV export

### 3. Telegram Alerts (Optional)
- **Bot API**: Telegram Bot API
- **Trigger**: Keyword-based (`@urgent:` patterns)
- **Window**: 6 AM - 10 PM (configurable)
- **Target**: <5 alerts per day

---

## Configuration Files

### config.yaml (13 KB)
**Purpose**: Main TrendRadar configuration

**Key Sections**:
- `custom_sources:` - 25 RSS feeds with weights
- `platforms:` - Built-in sources (HackerNews, GitHub Trending)
- `delivery:` - Schedule and channel configuration
- `weights:` - Ranking algorithm parameters
- `filtering:` - Deduplication and quality settings
- `advanced:` - Category limits and source overrides

### frequency_words.txt (10 KB)
**Purpose**: Keyword filtering and categorization

**Syntax**:
- `+keyword` - Mandatory term
- `!keyword` - Exclusion
- `@category:N` - Quantity limit
- `@urgent:+term1+term2` - Telegram alert trigger

---

## Technology Decisions & Rationale

### Why TrendRadar?
- ✅ Free forever (GitHub only)
- ✅ No server maintenance
- ✅ Open source (customizable)
- ✅ Multi-channel delivery
- ✅ Built-in ranking algorithm

### Why GitHub Actions?
- ✅ 2,000 free minutes/month
- ✅ Reliable cron scheduling
- ✅ Secrets management
- ✅ Integrated with Pages hosting

### Why RSS over Web Scraping?
- ✅ Publisher-provided (legal, reliable)
- ✅ Standardized format
- ✅ No maintenance burden
- ✅ Respectful of publisher bandwidth

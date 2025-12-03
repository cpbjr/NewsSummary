# TrendRadar News Feed System - Complete Analysis & Setup Guide

**Created:** 2025-11-23
**Purpose:** Custom news aggregation with twice-daily email delivery (5 AM & 7 PM)
**Repository:** https://github.com/sansan0/TrendRadar

---

## Table of Contents

1. [What is TrendRadar](#what-is-trendradar)
2. [Key Features](#key-features)
3. [Technology Stack](#technology-stack)
4. [Your Custom Configuration](#your-custom-configuration)
5. [Installation Steps](#installation-steps)
6. [Customization Guide](#customization-guide)
7. [Multi-Channel Workflow](#multi-channel-workflow)
8. [Advanced Features](#advanced-features)
9. [Maintenance & Optimization](#maintenance--optimization)

---

## What is TrendRadar

**TrendRadar** is a lightweight trend monitoring tool that aggregates hot topics from 35+ platforms and custom RSS feeds, delivering intelligent news filtering through multiple channels (email, Telegram, web dashboard).

### Core Concept
Think of it as your personal news curator that:
- Monitors dozens of platforms simultaneously
- Filters content through customizable keyword rules
- Ranks stories using composite algorithm (platform rank + cross-platform frequency + stability)
- Delivers through multiple channels based on priority

### Why It Works
- **Zero maintenance** - Runs entirely on free GitHub infrastructure (Actions + Pages)
- **Composite algorithm** - Weights trending content by: 60% platform ranking + 30% cross-platform frequency + 10% ranking stability
- **MCP-powered AI layer** - v3.0+ enables natural language queries against news data

---

## Key Features

### 1. Content Aggregation
- **Built-in platforms:** 35+ sources (TikTok, Reddit, HackerNews, Zhihu, Bilibili, financial news)
- **Custom RSS feeds:** Add any RSS/Atom feed (Politico, ZeroHedge, LA Times, etc.)
- **Real-time monitoring:** Continuous collection and ranking

### 2. Smart Delivery Modes

| Mode | Best For | Description |
|------|----------|-------------|
| **Daily Summary** | Executives, information consumers | Digest of top stories at scheduled times |
| **Current Rankings** | Content creators | Live trending topics, refreshed hourly |
| **Incremental Updates** | Traders, researchers | Zero duplicates, only new stories |

### 3. Intelligent Filtering

**Four keyword syntax types:**

```
Basic matching           → AI, automation
Mandatory terms (+)      → +Claude, +breaking
Exclusions (!)           → !celebrity, !opinion
Quantity limits (@)      → @tech:15, @finance:10
```

**Thematic groups:** Use line breaks to organize keywords into categories

### 4. Multi-Channel Delivery
- **Email** - Daily digests with formatted summaries
- **Telegram** - Real-time alerts for critical keywords
- **Web Dashboard** - Searchable archive with 7-day history
- **Enterprise WeChat, Feishu, DingTalk** - Team notifications

### 5. AI-Powered Analysis (v3.0+)

**13 analytical tools via Model Context Protocol:**
- "Show me AI trends from the last week"
- "Compare sentiment across platforms for 'climate change'"
- "What topics are trending on both TikTok and HackerNews?"

**Cost:** ~$0.10-0.50/day for LLM API calls (optional feature)

---

## Technology Stack

- **Backend:** Python
- **Data Sources:** newsnow API + custom RSS feeds
- **Deployment:** GitHub Actions (2,000 free minutes/month)
- **Frontend:** GitHub Pages (static HTML/CSS)
- **Storage:** Git repository (unlimited)
- **Notifications:** SMTP (email), Telegram Bot API, webhook integrations

---

## Your Custom Configuration

### Delivery Schedule
- **5:00 AM** - Morning digest (overnight news + early market updates)
- **7:00 PM** - Evening digest (day's events + closing market news)

### Platform Mix
- **Tech news:** HackerNews, GitHub Trending, Reddit r/programming
- **Financial:** Bloomberg, Reuters, ZeroHedge
- **Political:** Politico, The Federalist, NPR, BBC News, The Hill
- **Sports:** LA Times Sports, ESPN
- **General:** Axios, AP News

### Multi-Channel Strategy
1. **Email (Primary)** - Twice daily full digests
2. **Web Dashboard** - On-demand browsing and search
3. **Telegram (Selective)** - Breaking news alerts only (6 AM - 10 PM window)

---

## Installation Steps

### Step 1: Fork Repository (2 minutes)

1. Go to https://github.com/sansan0/TrendRadar
2. Click **Fork** (top right)
3. Keep repository name or rename to `news-feed`

### Step 2: Configure Secrets (5 minutes)

Go to **Settings → Secrets and variables → Actions → New repository secret**

**Email Configuration:**
```
EMAIL_HOST = smtp.gmail.com (or your provider)
EMAIL_PORT = 587
EMAIL_USER = your-email@gmail.com
EMAIL_PASS = your-app-password (not regular password!)
EMAIL_TO = your-email@gmail.com
```

**Telegram Configuration (Optional):**
```
TELEGRAM_BOT_TOKEN = get from @BotFather
TELEGRAM_CHAT_ID = your chat ID
```

**AI Analysis (Optional):**
```
OPENAI_API_KEY = sk-... (for AI features)
```

### Step 3: Add Configuration Files (10 minutes)

**Replace `config.yaml`** with your custom configuration (see `config.yaml` in this directory)

**Replace `frequency_words.txt`** with your keyword filters (see `frequency_words.txt` in this directory)

**Add custom RSS feeds** to `config.yaml` (see RSS-Feeds-Configuration.md)

### Step 4: Enable GitHub Actions (1 minute)

1. Go to **Actions** tab
2. Click **"I understand my workflows, go ahead and enable them"**
3. Workflows will run at 5 AM and 7 PM daily (based on config.yaml)

### Step 5: Enable GitHub Pages (2 minutes)

1. **Settings → Pages**
2. **Source:** Deploy from branch
3. **Branch:** `gh-pages` (will be created automatically after first run)
4. **Access dashboard at:** `https://yourusername.github.io/TrendRadar`

### Step 6: Test Setup (5 minutes)

**Manual trigger:**
1. Go to **Actions** tab
2. Select workflow **"TrendRadar Daily Digest"**
3. Click **"Run workflow"** → Run on main branch
4. Check your email in ~2-5 minutes

---

## Customization Guide

### Keyword Filtering (`frequency_words.txt`)

**Strategy:** Organize by thematic groups using line breaks

```
# === TECH & AI GROUP ===
+AI
+LLM
+Claude
+ChatGPT
automation
machine learning
!tutorial          # Exclude beginner content

# === FINANCIAL GROUP ===
+Federal Reserve
+interest rate
+earnings
stocks
bonds
market
!prediction        # Facts only, no speculation
!opinion

# === POLITICAL GROUP ===
+election
+Congress
+White House
legislation
policy
!Twitter           # Exclude social media drama

# === SPORTS GROUP ===
+Lakers
+Dodgers
NFL
NBA
!rumors           # Exclude unverified reports

# === TELEGRAM ALERTS (High Priority) ===
@urgent:+breaking
@urgent:+acquisition
@urgent:+security breach
@urgent:+Fed announcement

# === QUANTITY LIMITS ===
@tech:15          # Max 15 tech articles per digest
@finance:12       # Max 12 financial articles
@politics:10      # Max 10 political articles
@sports:8         # Max 8 sports articles
```

### Platform Weighting

**Adjust algorithm in `config.yaml`:**

```yaml
weights:
  platform_rank: 50      # Official rankings (default: 60)
  cross_platform: 40     # Viral velocity (default: 30)
  stability: 10          # Consistency (default: 10)
```

**Use cases:**
- **Want viral content?** Increase `cross_platform` to 50%
- **Trust official rankings?** Keep `platform_rank` at 60%
- **Value consistency?** Increase `stability` to 20%

### Email Scheduling

**Two approaches:**

**Option 1: GitHub Actions Cron (config.yaml)**
```yaml
delivery:
  schedule:
    - time: "05:00"
      timezone: "America/New_York"
    - time: "19:00"
      timezone: "America/New_York"
```

**Option 2: Workflow File (.github/workflows/daily-digest.yml)**
```yaml
on:
  schedule:
    - cron: '0 5,19 * * *'  # 5 AM and 7 PM UTC (adjust for timezone)
```

**Important:** GitHub Actions uses UTC time. Convert your timezone:
- PST (UTC-8): 5 AM PST = 13:00 UTC, 7 PM PST = 03:00 UTC (next day)
- EST (UTC-5): 5 AM EST = 10:00 UTC, 7 PM EST = 00:00 UTC (next day)
- MST (UTC-7): 5 AM MST = 12:00 UTC, 7 PM MST = 02:00 UTC (next day)

### Telegram Push Windows

**Limit alerts to waking hours:**

```yaml
push_window:
  start: "06:00"
  end: "22:00"
  timezone: "America/New_York"
```

**Why this matters:** Prevents 3 AM breaking news alerts

---

## Multi-Channel Workflow

### Morning Routine (5 AM)

**Email arrives with:**
- Overnight tech developments (HackerNews, GitHub)
- Asian market updates (ZeroHedge, Reuters)
- Early political news (Politico, The Hill)
- Grouped by platform with ranking scores

**Typical structure:**
```
=== TECH NEWS (15 stories) ===
1. [HackerNews #1] New AI breakthrough in reasoning
2. [GitHub Trending #3] Open source LLM framework
...

=== FINANCIAL NEWS (12 stories) ===
1. [ZeroHedge] Fed signals rate decision
2. [Reuters] Asian markets rally on trade news
...

=== POLITICAL NEWS (10 stories) ===
1. [Politico] Congressional bill advances
...
```

### Throughout the Day (6 AM - 10 PM)

**Telegram fires for critical keywords:**
- `+breaking` + `Fed` → Immediate notification
- `+acquisition` + `tech company` → Immediate notification
- Regular news → Waits for 7 PM digest

**Example alert:**
```
🚨 BREAKING: Fed Announces Emergency Rate Cut

Source: ZeroHedge (Cross-platform: 8 sources)
Ranking: #1 Financial News
Time: 2:34 PM EST

[Link to article]
```

### Evening Routine (7 PM)

**Email arrives with:**
- Day's tech developments
- Market close analysis
- Political day recap
- Sports scores and highlights

**Incremental mode:** Only stories NOT in 5 AM digest

### On-Demand Research

**Web Dashboard** (`https://yourusername.github.io/TrendRadar`):
- Search last 7 days of collected news
- Filter by platform, keyword, or date range
- Export to CSV for analysis
- View trending topics visualization

---

## Advanced Features

### 1. Custom RSS Feed Integration

**See `RSS-Feeds-Configuration.md` for complete feed list**

**Basic integration (config.yaml):**
```yaml
custom_sources:
  - name: "Politico Politics"
    type: rss
    url: "https://rss.politico.com/politics-news.xml"
    weight: 1.5
    category: "politics"

  - name: "ZeroHedge"
    type: rss
    url: "https://www.zerohedge.com/feeds/all"
    weight: 1.2
    category: "finance"

  - name: "LA Times Sports"
    type: rss
    url: "https://www.latimes.com/sports/rss2.0.xml"
    weight: 1.0
    category: "sports"
```

### 2. Sentiment-Based Filtering

**Add to custom logic (requires code modification):**

```python
# In sources.py or custom_filters.py
def filter_by_sentiment(article):
    sentiment = analyze_sentiment(article.title + article.description)

    # Filter out negative news (optional)
    if sentiment['score'] < 0.3:
        return False

    # Boost positive financial news
    if article.category == 'finance' and sentiment['score'] > 0.7:
        article.weight *= 1.3

    return True
```

### 3. Cross-Platform Correlation

**Find stories mentioned across multiple sources:**

```
# frequency_words.txt
@correlation:AI+regulation        # Only if both topics appear
@correlation:Fed+interest+rate    # Must have all three terms
```

### 4. Time-Based Priorities

**Emphasize certain topics during specific hours:**

```yaml
# config.yaml
priority_hours:
  market_hours:
    start: "09:30"
    end: "16:00"
    boost_categories: ["finance", "economics"]
    weight_multiplier: 1.5

  political_hours:
    start: "08:00"
    end: "20:00"
    boost_categories: ["politics", "policy"]
    weight_multiplier: 1.2
```

### 5. Duplicate Detection

**TrendRadar automatically deduplicates:**
- Same story from multiple RSS feeds
- Similar headlines (using fuzzy matching)
- URL canonicalization

**Tune sensitivity in config.yaml:**
```yaml
deduplication:
  title_similarity_threshold: 0.85  # 85% similar = duplicate
  time_window_hours: 24             # Consider duplicates within 24h
```

---

## Maintenance & Optimization

### Weekly Review (15 minutes)

**Check email digest quality:**
- Too many articles? Reduce `@category:N` limits
- Missing important stories? Relax keyword filters
- Too much noise? Add `!exclusion` keywords

**Review Telegram alerts:**
- Goal: <5 alerts per day
- Too many? Tighten `@urgent:` conditions
- Too few? Add more `+mandatory` terms

**Platform performance:**
- Which sources provide best signal-to-noise?
- Remove low-value feeds
- Add new RSS sources as discovered

### Monthly Optimization (30 minutes)

**Analyze trends over 30 days:**

1. **Export dashboard data** to CSV
2. **Identify patterns:**
   - Which platforms break news first?
   - Which keywords generate most matches?
   - Which categories exceed quantity limits most often?

3. **Adjust weights:**
   ```yaml
   # If ZeroHedge is too sensational
   custom_sources:
     - name: "ZeroHedge"
       weight: 0.8  # Reduce from 1.2 to 0.8
   ```

4. **Refine keywords:**
   - Remove low-value broad terms
   - Add newly discovered topics
   - Update `!exclusions` based on noise patterns

### GitHub Actions Monitoring

**Check workflow runs:**
1. Go to **Actions** tab
2. Review recent runs for errors
3. Common issues:
   - API rate limits (reduce polling frequency)
   - Email delivery failures (check SMTP credentials)
   - RSS feed timeouts (remove slow feeds)

**Resource usage:**
- Free tier: 2,000 minutes/month
- Typical usage: ~5-10 minutes/day = 150-300 minutes/month
- Plenty of headroom for twice-daily runs

---

## Troubleshooting

### Email Not Arriving

**Check:**
1. GitHub Secrets configured correctly? (EMAIL_HOST, EMAIL_USER, EMAIL_PASS)
2. Using app-specific password? (not regular account password)
3. SMTP port correct? (587 for TLS, 465 for SSL)
4. Check spam folder
5. Review Actions log for SMTP errors

**Gmail users:**
- Enable 2-factor authentication
- Create app-specific password: https://myaccount.google.com/apppasswords
- Use `smtp.gmail.com` port `587`

### Telegram Alerts Not Working

**Check:**
1. Bot token valid? (test with `https://api.telegram.org/bot<TOKEN>/getMe`)
2. Chat ID correct? (send message to bot, check `https://api.telegram.org/bot<TOKEN>/getUpdates`)
3. Bot added to group/channel?
4. Telegram secrets in GitHub Actions?

### GitHub Pages Dashboard Not Loading

**Common issues:**
1. Wait 5-10 minutes after first workflow run
2. Check **Settings → Pages** shows `gh-pages` branch
3. Verify workflow created `gh-pages` branch (check branches list)
4. Clear browser cache

### No News Items in Digest

**Possible causes:**
1. **Keyword filters too strict** - Try removing `!exclusions` temporarily
2. **Quantity limits too low** - Increase `@category:N` values
3. **RSS feeds not responding** - Check Actions log for feed errors
4. **Time zone mismatch** - Verify cron schedule matches your timezone

---

## Cost Analysis

### Free Tier (100% GitHub)

**Costs:** $0/month

**Limitations:**
- 2,000 GitHub Actions minutes/month (sufficient for twice-daily runs)
- No AI analysis features
- Basic keyword filtering only

**What you get:**
- Unlimited RSS feeds
- Unlimited email delivery
- Unlimited web dashboard access
- Telegram notifications

### AI-Enabled Tier

**Costs:** ~$3-15/month (OpenAI/Anthropic API usage)

**Breakdown:**
- Daily digest AI summaries: ~$0.10-0.30/day
- Natural language queries: ~$0.05-0.20/query
- Sentiment analysis: ~$0.02-0.05/article

**Estimated monthly:**
- Light usage (AI summaries only): $3-9/month
- Heavy usage (queries + summaries): $10-15/month

**What you get additionally:**
- Natural language queries against news data
- AI-generated summaries in email
- Sentiment analysis
- Topic clustering
- Cross-platform trend analysis

---

## Next Steps

1. **Read `RSS-Feeds-Configuration.md`** for complete feed URLs
2. **Review sample `config.yaml`** and customize for your timezone
3. **Edit `frequency_words.txt`** with your keyword preferences
4. **Fork TrendRadar repository** and add secrets
5. **Test with manual workflow run** before relying on schedule
6. **Monitor first week** and adjust filters based on results
7. **Optional:** Enable AI features for enhanced analysis

---

## Resources

- **TrendRadar Repository:** https://github.com/sansan0/TrendRadar
- **Documentation:** See repository README.md
- **RSS Feed Directory:** `RSS-Feeds-Configuration.md` in this directory
- **Sample Config:** `config.yaml` in this directory
- **Sample Keywords:** `frequency_words.txt` in this directory

---

## FAQ

**Q: Can I run this locally instead of GitHub Actions?**
A: Yes, use Docker or Python virtual environment. See repository docs for local setup.

**Q: How do I add a paywall-protected source (WSJ, NYT)?**
A: TrendRadar can't bypass paywalls. Use RSS feeds (usually free) or integrate with services like RSS Bridge.

**Q: Can I share the dashboard with my team?**
A: Yes, GitHub Pages is public by default. Make repository private for restricted access.

**Q: What happens if an RSS feed goes down?**
A: TrendRadar skips failed feeds and logs error. Other sources continue normally.

**Q: Can I get notifications in Slack instead of Telegram?**
A: Yes, modify notification handler to use Slack webhook instead of Telegram API.

**Q: How do I backup my news data?**
A: Export from web dashboard to CSV, or access raw data in `gh-pages` branch JSON files.

---

**Last Updated:** 2025-11-23
**Version:** 1.0

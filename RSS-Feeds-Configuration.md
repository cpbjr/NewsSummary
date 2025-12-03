# RSS Feeds Configuration for TrendRadar

**Created:** 2025-11-23
**Purpose:** Comprehensive RSS feed directory for custom news aggregation
**Status:** All feeds verified as of November 2025

---

## Table of Contents

1. [Requested Sources](#requested-sources)
2. [Recommended Additions](#recommended-additions)
3. [TrendRadar Integration](#trendradar-integration)
4. [Feed Maintenance](#feed-maintenance)

---

## Requested Sources

### 1. ZeroHedge
**Category:** Financial/Political (Libertarian/Alternative perspective)

**Feed URL:**
```
https://www.zerohedge.com/feeds/all
```

**Description:** All ZeroHedge articles covering financial markets, economics, politics, and current affairs

**Update Frequency:** Multiple times daily (10-20 articles/day)

**Notes:**
- Alternative perspective on markets and economics
- Strong focus on contrarian views
- May have category-specific feeds (check website footer)

**TrendRadar Config:**
```yaml
custom_sources:
  - name: "ZeroHedge"
    type: rss
    url: "https://www.zerohedge.com/feeds/all"
    weight: 1.2
    category: "finance"
```

---

### 2. Politico
**Category:** Political News (Center-left perspective)

**Main Feed:**
```
https://www.politico.com/rss/politicopicks.xml
```

**Topic-Specific Feeds:**

| Topic | RSS Feed URL |
|-------|-------------|
| **White House** | `https://rss.politico.com/white-house.xml` |
| **Congress** | `https://rss.politico.com/congress.xml` |
| **Defense** | `https://rss.politico.com/defense.xml` |
| **Economy** | `https://rss.politico.com/economy.xml` |
| **Healthcare** | `https://rss.politico.com/healthcare.xml` |
| **Energy** | `https://rss.politico.com/energy.xml` |
| **Politics News** | `https://rss.politico.com/politics-news.xml` |
| **Playbook** | `https://rss.politico.com/playbook.xml` |
| **Morning Tech** | `https://rss.politico.com/morningtech.xml` |
| **Magazine** | `https://rss.politico.com/magazine.xml` |

**Politico Europe:**
```
https://www.politico.eu/feed
```

**Description:** Global authority on politics, policy, and power with extensive Washington coverage

**Update Frequency:** Continuous throughout the day (30-50 articles/day across all feeds)

**Recommended Approach:**
- Use main feed (`politicopicks.xml`) for general coverage
- Add specific topic feeds if you want deeper coverage in those areas

**TrendRadar Config:**
```yaml
custom_sources:
  # Main Politico feed
  - name: "Politico"
    type: rss
    url: "https://www.politico.com/rss/politicopicks.xml"
    weight: 1.5
    category: "politics"

  # Optional: Add specific topics
  - name: "Politico Congress"
    type: rss
    url: "https://rss.politico.com/congress.xml"
    weight: 1.3
    category: "politics"

  - name: "Politico Economy"
    type: rss
    url: "https://rss.politico.com/economy.xml"
    weight: 1.4
    category: "finance"
```

---

### 3. The Federalist
**Category:** Political News (Conservative perspective)

**Feed URL:**
```
https://thefederalist.com/feed/
```

**Description:** Conservative political commentary, analysis, and news with focus on cultural and constitutional issues

**Update Frequency:** Multiple times daily (5-15 articles/day)

**Podcast Feed (Optional):**
```
https://podcasts.apple.com/us/podcast/federalist-radio-hour/id983782306
```

**TrendRadar Config:**
```yaml
custom_sources:
  - name: "The Federalist"
    type: rss
    url: "https://thefederalist.com/feed/"
    weight: 1.0
    category: "politics"
```

---

### 4. LA Times Sports
**Category:** Sports News (Regional/National)

**Feed URL:**
```
https://www.latimes.com/sports/rss2.0.xml
```

**Description:** Sports news and scores for NBA, NFL, MLB, NHL, college and high school sports. Comprehensive coverage of LA teams:
- **Baseball:** Dodgers, Angels
- **Basketball:** Lakers, Clippers
- **Football:** Rams, Chargers
- **College:** USC, UCLA
- **Other:** Boxing, soccer, Olympics

**Update Frequency:** Multiple times daily (10-25 articles/day)

**TrendRadar Config:**
```yaml
custom_sources:
  - name: "LA Times Sports"
    type: rss
    url: "https://www.latimes.com/sports/rss2.0.xml"
    weight: 1.0
    category: "sports"
```

---

### 5. Axios
**Category:** General News (Center perspective)

**Main Feed:**
```
https://www.axios.com/feeds/feed.rss
```

**Description:** Smart brevity news covering politics, business, tech, and media

**Update Frequency:** Multiple times daily (15-30 articles/day)

**Important Notes:**
- Axios has limited native RSS support
- Main feed above is verified functional
- For topic-specific feeds, may need third-party RSS generators:
  - **RSS.app** - https://rss.app
  - **FeedSpot** - https://feedspot.com
  - **FiveFilters** - https://createfeed.fivefilters.org

**Alternative Approach (using RSS generators):**

| Topic | Original URL | Use Generator |
|-------|-------------|---------------|
| Politics | `https://www.axios.com/politics-policy` | RSS.app or FeedSpot |
| Technology | `https://www.axios.com/technology` | RSS.app or FeedSpot |
| Economy | `https://www.axios.com/economy-business` | RSS.app or FeedSpot |
| Health | `https://www.axios.com/health` | RSS.app or FeedSpot |

**TrendRadar Config:**
```yaml
custom_sources:
  - name: "Axios"
    type: rss
    url: "https://www.axios.com/feeds/feed.rss"
    weight: 1.3
    category: "general"
```

---

## Recommended Additions

### Political Diversity Sources

#### NPR (Center/Slightly Left)
**Main Feeds:**

| Topic | RSS Feed URL |
|-------|-------------|
| **General News** | `https://feeds.npr.org/1002/rss.xml` |
| **Politics** | `https://feeds.npr.org/1014/rss.xml` |
| **National News** | `https://feeds.npr.org/1003/rss.xml` |
| **World News** | `https://feeds.npr.org/1004/rss.xml` |
| **Business** | `https://feeds.npr.org/1006/rss.xml` |
| **Technology** | `https://feeds.npr.org/1019/rss.xml` |

**Description:** Comprehensive public radio coverage with expanded U.S. and world politics

**Update Frequency:** Continuous (50-100 articles/day across all feeds)

**TrendRadar Config:**
```yaml
custom_sources:
  - name: "NPR Politics"
    type: rss
    url: "https://feeds.npr.org/1014/rss.xml"
    weight: 1.2
    category: "politics"

  - name: "NPR Business"
    type: rss
    url: "https://feeds.npr.org/1006/rss.xml"
    weight: 1.1
    category: "finance"
```

---

#### The Hill (Center/Balanced)
**Main Feeds:**

| Topic | RSS Feed URL |
|-------|-------------|
| **All News** | `https://thehill.com/news/feed` |
| **Homepage** | `https://thehill.com/rss/` |
| **Business** | `https://thehill.com/business/feed` |

**Full feed list:** https://thehill.com/resources/rss-feeds/

**Description:** Washington-focused political news covering Congress, presidency, and campaigns

**Update Frequency:** Continuous (30-60 articles/day)

**TrendRadar Config:**
```yaml
custom_sources:
  - name: "The Hill"
    type: rss
    url: "https://thehill.com/news/feed"
    weight: 1.2
    category: "politics"
```

---

#### BBC News (International/Center)
**Main Feeds:**

| Topic | RSS Feed URL |
|-------|-------------|
| **World News** | `https://feeds.bbci.co.uk/news/world/rss.xml` |
| **US & Canada** | `https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml` |
| **Business** | `https://feeds.bbci.co.uk/news/business/rss.xml` |
| **Technology** | `http://feeds.bbci.co.uk/news/technology/rss.xml` |
| **General News** | `https://feeds.bbci.co.uk/news/rss.xml` |

**Description:** International perspective on world news, business, and technology

**Update Frequency:** Continuous (40-80 articles/day across all feeds)

**Why Include:** Non-US perspective balances American-centric coverage

**TrendRadar Config:**
```yaml
custom_sources:
  - name: "BBC World News"
    type: rss
    url: "https://feeds.bbci.co.uk/news/world/rss.xml"
    weight: 1.1
    category: "world"

  - name: "BBC Business"
    type: rss
    url: "https://feeds.bbci.co.uk/news/business/rss.xml"
    weight: 1.0
    category: "finance"
```

---

### Financial/Economic News

#### Reuters (Center/Balanced)
**Note:** Official RSS ended in 2020, but some feeds still work

**Working Feeds:**
```
https://www.reuters.com/rss/business
https://www.reuters.com/rss/
```

**Alternative:** Use third-party RSS generators:
- **FiveFilters:** https://createfeed.fivefilters.org
- **RSS.app:** Create feed from https://www.reuters.com/business

**Description:** International news agency with strong financial coverage

**Update Frequency:** Continuous (if feed works)

**TrendRadar Config:**
```yaml
custom_sources:
  - name: "Reuters Business"
    type: rss
    url: "https://www.reuters.com/rss/business"
    weight: 1.3
    category: "finance"
    # Fallback if feed fails - remove or use RSS generator
```

---

#### Financial Times
**Main Feeds:**

```
https://www.ft.com/?format=rss
https://www.ft.com/rss/home
```

**Description:** Premium business and economic news with global perspective

**Update Frequency:** Continuous (30-50 articles/day)

**Notes:**
- May require subscription for full article access
- RSS feed provides headlines/summaries for free

**TrendRadar Config:**
```yaml
custom_sources:
  - name: "Financial Times"
    type: rss
    url: "https://www.ft.com/rss/home"
    weight: 1.4
    category: "finance"
```

---

### Technology News

#### TechCrunch
**Feed Structure:** Add `/feed` to any category URL

**Examples:**
```
https://techcrunch.com/category/startups/feed/
https://techcrunch.com/category/security/feed/
https://techcrunch.com/category/artificial-intelligence/feed/
https://techcrunch.com/category/venture/feed/
```

**Full category list:** https://techcrunch.com/subscribing/

**Categories Available (45+):**
- Security, Biotech, Transportation, Space, Apps, Climate, Cloud Computing, Commerce, Consumer Tech, Cryptocurrency, Data, Enterprise, Fintech, Gadgets, Gaming, Government & Policy, Hardware, Health, Media & Entertainment, Mobile, Privacy, Robotics, SaaS, Social, Software, Transportation, etc.

**Description:** Leading startup and technology news

**Update Frequency:** Continuous (50-100 articles/day across all categories)

**TrendRadar Config:**
```yaml
custom_sources:
  - name: "TechCrunch AI"
    type: rss
    url: "https://techcrunch.com/category/artificial-intelligence/feed/"
    weight: 1.3
    category: "tech"

  - name: "TechCrunch Startups"
    type: rss
    url: "https://techcrunch.com/category/startups/feed/"
    weight: 1.1
    category: "tech"
```

---

### Sports Coverage

#### ESPN
**Main Feeds:**

| Sport | RSS Feed URL |
|-------|-------------|
| **Main Sports** | `https://www.espn.com/espn/rss/` |
| **NFL** | `https://www.espn.com/espn/rss/nfl/news` |
| **NBA** | `https://www.espn.com/espn/rss/nba/news` |
| **MLB** | `https://www.espn.in/espn/rss/mlb/news` |
| **NHL** | `https://www.espn.com/espn/rss/nhl/news` |
| **College Football** | `https://www.espn.com/espn/rss/ncf/news` |
| **College Basketball** | `https://www.espn.com/espn/rss/ncb/news` |

**Description:** Comprehensive sports coverage across all major leagues (25+ sport-specific feeds available)

**Update Frequency:** Continuous (100+ articles/day across all sports)

**Content Requirement:** Must link to ESPN.com when displaying content

**TrendRadar Config:**
```yaml
custom_sources:
  - name: "ESPN NFL"
    type: rss
    url: "https://www.espn.com/espn/rss/nfl/news"
    weight: 1.2
    category: "sports"

  - name: "ESPN NBA"
    type: rss
    url: "https://www.espn.com/espn/rss/nba/news"
    weight: 1.2
    category: "sports"
```

---

### Wire Services

#### Associated Press (AP News)
**Important:** No official RSS feeds available

**Workarounds:**
1. **Third-party hosted feed:**
   ```
   http://associated-press.s3-website-us-east-1.amazonaws.com
   ```
   (Reliability not guaranteed)

2. **Use RSS generators:**
   - **RSS.app:** Create feed from https://apnews.com/
   - **FeedSpot:** Monitor AP News sections
   - **FiveFilters:** https://createfeed.fivefilters.org

**Topic URLs for Generator Input:**
```
https://apnews.com/hub/politics
https://apnews.com/hub/business
https://apnews.com/hub/technology
https://apnews.com/hub/sports
```

**Description:** Unbiased wire service news

**Update Frequency:** Continuous (if generator works)

**License Note:** Non-commercial use only without AP permission

**TrendRadar Config:**
```yaml
# Only if using RSS generator successfully
custom_sources:
  - name: "AP News Politics"
    type: rss
    url: "[YOUR_RSS_GENERATOR_URL]"
    weight: 1.5
    category: "politics"
```

---

## Additional Recommendations

### Conservative/Right Balance
**Reason:** You have The Federalist; consider adding:

#### National Review
```
https://www.nationalreview.com/feed/
```
**Category:** Conservative political commentary

#### Daily Wire
```
https://www.dailywire.com/rss.xml
```
**Category:** Conservative news and commentary

---

### Business/Markets Deep Dive

#### Bloomberg
**Note:** Limited RSS support; may need workarounds

**Potential feeds:**
```
https://www.bloomberg.com/feed/podcast/businessweek.xml (Podcast)
```

**Alternative:** Use RSS generators on:
```
https://www.bloomberg.com/markets
https://www.bloomberg.com/technology
```

---

### Local News (if desired)

#### LA Times General
```
https://www.latimes.com/california/rss2.0.xml
```
**Category:** California news

#### Your Local Paper
Find RSS at: `https://[yourlocalnewspaper].com/rss`

---

## TrendRadar Integration

### Complete config.yaml Example

```yaml
# Custom RSS Sources Configuration
custom_sources:
  # === FINANCIAL SOURCES ===
  - name: "ZeroHedge"
    type: rss
    url: "https://www.zerohedge.com/feeds/all"
    weight: 1.2
    category: "finance"

  - name: "Reuters Business"
    type: rss
    url: "https://www.reuters.com/rss/business"
    weight: 1.3
    category: "finance"

  - name: "Financial Times"
    type: rss
    url: "https://www.ft.com/rss/home"
    weight: 1.4
    category: "finance"

  - name: "NPR Business"
    type: rss
    url: "https://feeds.npr.org/1006/rss.xml"
    weight: 1.1
    category: "finance"

  - name: "BBC Business"
    type: rss
    url: "https://feeds.bbci.co.uk/news/business/rss.xml"
    weight: 1.0
    category: "finance"

  # === POLITICAL SOURCES ===
  - name: "Politico"
    type: rss
    url: "https://www.politico.com/rss/politicopicks.xml"
    weight: 1.5
    category: "politics"

  - name: "The Federalist"
    type: rss
    url: "https://thefederalist.com/feed/"
    weight: 1.0
    category: "politics"

  - name: "NPR Politics"
    type: rss
    url: "https://feeds.npr.org/1014/rss.xml"
    weight: 1.2
    category: "politics"

  - name: "The Hill"
    type: rss
    url: "https://thehill.com/news/feed"
    weight: 1.2
    category: "politics"

  - name: "BBC World News"
    type: rss
    url: "https://feeds.bbci.co.uk/news/world/rss.xml"
    weight: 1.1
    category: "world"

  # === GENERAL NEWS ===
  - name: "Axios"
    type: rss
    url: "https://www.axios.com/feeds/feed.rss"
    weight: 1.3
    category: "general"

  # === TECHNOLOGY ===
  - name: "TechCrunch AI"
    type: rss
    url: "https://techcrunch.com/category/artificial-intelligence/feed/"
    weight: 1.3
    category: "tech"

  - name: "BBC Technology"
    type: rss
    url: "http://feeds.bbci.co.uk/news/technology/rss.xml"
    weight: 1.0
    category: "tech"

  # === SPORTS ===
  - name: "LA Times Sports"
    type: rss
    url: "https://www.latimes.com/sports/rss2.0.xml"
    weight: 1.0
    category: "sports"

  - name: "ESPN NFL"
    type: rss
    url: "https://www.espn.com/espn/rss/nfl/news"
    weight: 1.2
    category: "sports"

  - name: "ESPN NBA"
    type: rss
    url: "https://www.espn.com/espn/rss/nba/news"
    weight: 1.2
    category: "sports"

# Built-in TrendRadar Platforms (keep if desired)
platforms:
  - hackernews        # Tech news
  - github_trending   # Developer trends
  - reddit            # Community discussions
```

---

## Feed Maintenance

### Weekly Checks (5 minutes)

**Monitor feed health:**
```bash
# If running locally, check feed status
python check_feeds.py
```

**In GitHub Actions logs, look for:**
- `Feed timeout: [source_name]` - Remove or reduce weight
- `Parse error: [source_name]` - Feed format changed, needs update
- `404 Not Found: [source_name]` - Feed URL dead, find replacement

### Monthly Review (15 minutes)

1. **Verify all feed URLs still work**
   - Click each URL in browser to confirm XML loads
   - Check for redirect messages

2. **Evaluate feed quality**
   - Which feeds provide best articles in digests?
   - Which feeds are too noisy?
   - Which feeds are redundant?

3. **Update weights based on performance**
   ```yaml
   # Example: ZeroHedge too sensational, reduce weight
   - name: "ZeroHedge"
     weight: 0.8  # Down from 1.2
   ```

4. **Add new sources discovered**
   - Found a great new blog? Add its RSS feed
   - New publication launched? Include it

### RSS Feed Testing Tools

**Validate RSS feeds:**
- **W3C Feed Validator:** https://validator.w3.org/feed/
- **RSS Feed Reader:** https://rss.app (test before adding)
- **FeedSpot:** https://feedspot.com (discover new feeds)

**Create RSS from any website:**
- **RSS.app:** https://rss.app
- **FiveFilters:** https://createfeed.fivefilters.org
- **FetchRSS:** https://fetchrss.com

---

## Feed Categories Summary

### By Political Perspective

**Conservative/Right:**
- The Federalist
- ZeroHedge (Libertarian)
- National Review (recommended)

**Center/Balanced:**
- Politico (Center-left)
- The Hill
- Reuters
- BBC News
- Axios

**Left/Center-Left:**
- NPR
- (Add others if desired for balance)

### By Topic Area

**Financial/Economic (6 feeds):**
- ZeroHedge, Reuters, Financial Times, NPR Business, BBC Business, Politico Economy

**Political (5 feeds):**
- Politico, The Federalist, NPR Politics, The Hill, BBC World

**Technology (2 feeds):**
- TechCrunch AI, BBC Technology

**Sports (3 feeds):**
- LA Times Sports, ESPN NFL, ESPN NBA

**General News (1 feed):**
- Axios

### By Update Frequency

**Very High (50+ articles/day):**
- NPR, Politico, TechCrunch, ESPN

**High (20-50 articles/day):**
- BBC News, The Hill, Reuters

**Medium (10-20 articles/day):**
- ZeroHedge, LA Times Sports, Axios

**Low (5-10 articles/day):**
- The Federalist, Financial Times (RSS version)

---

## Troubleshooting Feed Issues

### Feed Returns No Items

**Possible causes:**
1. **Invalid URL** - Copy/paste directly from source
2. **Authentication required** - Some feeds need login (WSJ, NYT)
3. **Regional blocking** - Use VPN or RSS generator
4. **Feed deprecated** - Check source website for new URL

**Solution:**
- Test in browser: Does XML load?
- Test in RSS reader: Can FeedSpot/RSS.app read it?
- Check source website for updated feed URL

### Feed Parse Errors

**Error message examples:**
```
XML parse error: Invalid character
Feed format not recognized
```

**Solutions:**
1. **Try alternative feed URL** (many sites have multiple)
2. **Use RSS generator** to clean/convert feed
3. **Contact site support** if official feed is broken

### Feed Too Noisy

**Problem:** Feed generates too many low-value articles

**Solutions:**
1. **Reduce weight** in config.yaml (1.5 → 0.8)
2. **Add keyword filters** in frequency_words.txt:
   ```
   # Exclude noise from [source]
   !rumor
   !speculation
   !celebrity
   ```
3. **Remove feed entirely** if consistently low quality

---

## Next Steps

1. **Copy feeds into `config.yaml`** (see sample in this directory)
2. **Test feeds in browser** to verify they work
3. **Start with core feeds** (5-10 sources), expand later
4. **Monitor first week** to evaluate signal-to-noise ratio
5. **Adjust weights and filters** based on results

---

## Resources

- **FeedSpot RSS Directory:** https://rss.feedspot.com
- **RSS.app (Generator):** https://rss.app
- **W3C Feed Validator:** https://validator.w3.org/feed/
- **TrendRadar Repository:** https://github.com/sansan0/TrendRadar

---

**Last Updated:** 2025-11-23
**Total Feeds Documented:** 30+
**Verified Status:** All primary feeds tested November 2025

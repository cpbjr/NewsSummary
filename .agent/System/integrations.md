# NewsSummary Integrations

**Last Updated**: 2025-11-27

---

## RSS Feed Sources (25 total)

### Financial Sources (6)
1. **ZeroHedge** - `https://www.zerohedge.com/feeds/all` (weight: 1.2)
2. **Reuters Business** - `https://www.reuters.com/rss/business` (weight: 1.3)
3. **Financial Times** - `https://www.ft.com/rss/home` (weight: 1.4)
4. **NPR Business** - `https://feeds.npr.org/1006/rss.xml` (weight: 1.1)
5. **BBC Business** - `https://feeds.bbci.co.uk/news/business/rss.xml` (weight: 1.0)
6. **Politico Economy** - `https://rss.politico.com/economy.xml` (weight: 1.3)

### Political Sources (7)
7. **Politico** - `https://www.politico.com/rss/politicopicks.xml` (weight: 1.5)
8. **Politico Congress** - `https://rss.politico.com/congress.xml` (weight: 1.3)
9. **The Federalist** - `https://thefederalist.com/feed/` (weight: 1.0)
10. **NPR Politics** - `https://feeds.npr.org/1014/rss.xml` (weight: 1.2)
11. **The Hill** - `https://thehill.com/news/feed` (weight: 1.2)
12. **BBC World News** - `https://feeds.bbci.co.uk/news/world/rss.xml` (weight: 1.1)
13. **BBC US & Canada** - `https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml` (weight: 1.0)

### Technology Sources (4)
14. **TechCrunch AI** - `https://techcrunch.com/category/artificial-intelligence/feed/` (weight: 1.4)
15. **TechCrunch Startups** - `https://techcrunch.com/category/startups/feed/` (weight: 1.1)
16. **BBC Technology** - `http://feeds.bbci.co.uk/news/technology/rss.xml` (weight: 1.0)
17. **NPR Technology** - `https://feeds.npr.org/1019/rss.xml` (weight: 0.9)

### Sports Sources (4)
18. **LA Times Sports** - `https://www.latimes.com/sports/rss2.0.xml` (weight: 1.0)
19. **ESPN NFL** - `https://www.espn.com/espn/rss/nfl/news` (weight: 1.2)
20. **ESPN NBA** - `https://www.espn.com/espn/rss/nba/news` (weight: 1.2)
21. **ESPN MLB** - `https://www.espn.in/espn/rss/mlb/news` (weight: 1.0)

### General News (2)
22. **Axios** - `https://www.axios.com/feeds/feed.rss` (weight: 1.3)
23. **NPR National** - `https://feeds.npr.org/1003/rss.xml` (weight: 1.2)

### Built-in Platforms (2)
24. **HackerNews** - TrendRadar built-in platform
25. **GitHub Trending** - TrendRadar built-in platform

---

## Email Integration (Gmail SMTP)

**Service**: Gmail SMTP server
**Protocol**: SMTP over TLS

**GitHub Secrets Required**:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=xxxx-xxxx-xxxx-xxxx  # App-specific password
EMAIL_TO=your-email@gmail.com
```

**Setup**: Generate app password at https://myaccount.google.com/apppasswords

---

## Telegram Integration (Optional)

**GitHub Secrets Required**:
```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxyz
TELEGRAM_CHAT_ID=123456789
```

**Setup**:
1. Message @BotFather → Create new bot → Copy token
2. Message your bot
3. Visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`
4. Extract chat ID

**Alert Triggers**: Defined in `frequency_words.txt` with `@urgent:` prefix

---

## GitHub Pages

**URL**: `username.github.io/TrendRadar`
**Features**: 7-day searchable archive, category filtering, CSV export
**Update**: Automatic on workflow completion

---

## Adding New RSS Feeds

1. Validate feed: `curl https://example.com/feed.rss`
2. Add to `config.yaml` under `custom_sources:`
3. Test with manual workflow run
4. Adjust weight (0.8-1.5) based on quality

**Find feeds**: Check website footer for RSS links or try `/feed`, `/rss`, `/atom`

#!/usr/bin/env python3
"""
RSS News Aggregator
Fetches RSS feeds, filters by keywords, deduplicates, and sends email digest.
"""

import os
import re
import sys
import yaml
import hashlib
import smtplib
import requests
import feedparser
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from difflib import SequenceMatcher
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

# Load environment variables from .env if it exists
load_dotenv()


def load_config(config_path: str = "feeds.yaml") -> dict:
    """Load configuration from YAML file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def fetch_feed(feed_config: dict) -> list:
    """Fetch and parse a single RSS feed."""
    try:
        parsed = feedparser.parse(feed_config["url"])
        articles = []

        for entry in parsed.entries[:20]:  # Limit per feed
            article = {
                "title": entry.get("title", "").strip(),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", entry.get("description", ""))[:500],
                "published": entry.get("published", entry.get("updated", "")),
                "source": feed_config["name"],
                "category": feed_config.get("category", "general"),
            }

            # Parse date
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                article["date"] = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                article["date"] = datetime(*entry.updated_parsed[:6])
            else:
                article["date"] = datetime.utcnow()

            # Image extraction
            image_url = None
            
            # 1. Try enclosures
            if hasattr(entry, "links"):
                for link in entry.links:
                    if link.get("rel") == "enclosure" and "image" in link.get("type", ""):
                        image_url = link.get("href")
                        break
            
            # 2. Try media:content
            if not image_url and "media_content" in entry:
                image_url = entry["media_content"][0].get("url")
            
            # 3. Try media:thumbnail
            if not image_url and "media_thumbnail" in entry:
                image_url = entry["media_thumbnail"][0].get("url")
            
            # 4. Fallback to extracting from summary/description
            if not image_url:
                img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', article["summary"])
                if img_match:
                    image_url = img_match.group(1)
            
            article["image_url"] = image_url
            articles.append(article)

        return articles
    except Exception as e:
        print(f"Error fetching {feed_config['name']}: {e}")
        return []


def fetch_all_feeds(feeds: list) -> list:
    """Fetch all feeds in parallel."""
    all_articles = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_feed, feed): feed for feed in feeds}

        for future in as_completed(futures):
            articles = future.result()
            all_articles.extend(articles)

    return all_articles


def similarity(a: str, b: str) -> float:
    """Calculate string similarity ratio."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def deduplicate(articles: list, threshold: float = 0.85) -> list:
    """Remove duplicate articles based on title similarity."""
    unique = []

    for article in articles:
        is_dup = False
        for existing in unique:
            if similarity(article["title"], existing["title"]) > threshold:
                is_dup = True
                break

        if not is_dup:
            unique.append(article)

    return unique


def filter_articles(articles: list, keywords: dict) -> list:
    """Filter articles based on keyword rules and recategorize based on keywords."""
    filtered = []

    exclude_patterns = [re.compile(re.escape(kw), re.IGNORECASE)
                        for kw in keywords.get("exclude", [])]
    interest_patterns = [re.compile(re.escape(kw), re.IGNORECASE)
                         for kw in keywords.get("interests", [])]
    priority_patterns = [re.compile(re.escape(kw), re.IGNORECASE)
                         for kw in keywords.get("priority", [])]

    # Special keyword-based categories
    dodgers_pattern = re.compile(r'dodgers?', re.IGNORECASE)
    josh_allen_pattern = re.compile(r'josh allen', re.IGNORECASE)

    for article in articles:
        text = f"{article['title']} {article['summary']}"

        # Skip if matches exclusion
        if any(p.search(text) for p in exclude_patterns):
            continue

        # Recategorize based on special keywords
        if dodgers_pattern.search(text):
            article["category"] = "dodgers"
        elif josh_allen_pattern.search(text):
            article["category"] = "josh_allen"

        # Update score - preserve higher existing scores (like from Search API)
        score = 0
        if any(p.search(text) for p in priority_patterns):
            score += 100
        if any(p.search(text) for p in interest_patterns):
            score += 50

        article["score"] = max(article.get("score", 0), score)
        filtered.append(article)

    return filtered


def search_news(query: str, limit: int = 5) -> list:
    """Fetch news from Serper.dev News API."""
    api_key = os.environ.get("SERPER_API_KEY")
    if not api_key:
        print("SERPER_API_KEY not found. Skipping news search.")
        return []

    url = "https://google.serper.dev/news"
    payload = {
        "q": query,
        "num": limit,
        "tbs": "qdr:d"  # Published in the last 24 hours
    }
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        results = response.json().get("news", [])
        
        articles = []
        for entry in results[:limit]:
            # Convert Serper date (e.g. "3 hours ago" or "Jan 1, 2024")
            # For simplicity, we'll use current time if it's relative
            date_str = entry.get("date", "")
            if "hour" in date_str or "minute" in date_str or "moment" in date_str:
                date = datetime.utcnow()
            else:
                try:
                    # Very basic date parsing if needed, but Serper usually gives relative
                    date = datetime.utcnow() 
                except:
                    date = datetime.utcnow()

            article = {
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("snippet", ""),
                "source": entry.get("source", "Google News Search"),
                "category": "josh_allen",
                "date": date,
                "score": 200, # High priority
                "image_url": entry.get("imageUrl")
            }
            articles.append(article)
        
        return articles
    except Exception as e:
        print(f"Error searching news for '{query}': {e}")
        return []


def group_by_category(articles: list, default_limit: int = 12, category_limits: dict = None) -> dict:
    """Group articles by category with individual limits."""
    groups = defaultdict(list)
    limits = category_limits or {}

    for article in articles:
        cat = article["category"]
        limit = limits.get(cat, default_limit)
        if len(groups[cat]) < limit:
            groups[cat].append(article)

    return dict(groups)


def fetch_trending_topics() -> list:
    """Fetch current trending topics on X/Twitter via Serper Search."""
    api_key = os.environ.get("SERPER_API_KEY")
    if not api_key:
        return []

    url = "https://google.serper.dev/search"
    payload = {"q": "trending on twitter now USA", "num": 5}
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        data = response.json()
        snippet = data.get("organic", [{}])[0].get("snippet", "")
        
        # Extract trends (usually looks like "Trends: #Trend1, #Trend2...")
        if ":" in snippet:
            trends_part = snippet.split(":", 1)[1]
            # Split by comma or space and clean up
            trends = [t.strip().rstrip(".").rstrip(",") for t in re.split(r",|\s", trends_part)]
            return [t for t in trends if t and len(t) > 2][:10]
        return []
    except:
        return []


def format_html_digest(grouped: dict, digest_name: str, trends: list = None) -> str:
    """Format articles as HTML email."""
    trends = trends or []
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; max-width: 700px; margin: 0 auto; padding: 20px; background: #f8fafc; color: #1e293b; }}
        .header {{ background: #0f172a; color: white; padding: 40px 20px; border-radius: 12px 12px 0 0; text-align: center; border-bottom: 4px solid #3b82f6; }}
        .header h1 {{ margin: 0; font-family: 'Playfair Display', serif; font-size: 32px; letter-spacing: -0.02em; }}
        .header p {{ margin: 10px 0 0; opacity: 0.7; font-size: 13px; text-transform: uppercase; letter-spacing: 0.2em; font-weight: 600; }}
        
        .content {{ background: white; padding: 30px; border-radius: 0 0 12px 12px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }}
        
        .category {{ margin-top: 40px; }}
        .category:first-child {{ margin-top: 0; }}
        .category h2 {{ 
            color: #0f172a; 
            font-family: 'Playfair Display', serif; 
            font-size: 20px; 
            border-bottom: 1px solid #e2e8f0; 
            padding-bottom: 12px; 
            margin-bottom: 25px;
            font-variant: small-caps;
            letter-spacing: 0.05em;
        }}
        
        .article {{ margin-bottom: 30px; padding-bottom: 25px; border-bottom: 1px solid #f1f5f9; }}
        .article:last-child {{ border-bottom: none; }}
        
        .article-image {{ 
            width: 100%; 
            max-height: 300px; 
            object-fit: cover; 
            border-radius: 8px; 
            margin-bottom: 15px;
            border: 1px solid #e2e8f0;
        }}
        
        .article h3 {{ margin: 0 0 8px; font-family: 'Playfair Display', serif; font-size: 19px; line-height: 1.3; }}
        .article h3 a {{ color: #0f172a; text-decoration: none; transition: color 0.2s; }}
        .article h3 a:hover {{ color: #3b82f6; }}
        
        .article .meta {{ 
            font-size: 11px; 
            color: #64748b; 
            margin-bottom: 10px; 
            text-transform: uppercase; 
            letter-spacing: 0.1em; 
            font-weight: 600;
        }}
        
        .article .summary {{ font-size: 14px; color: #475569; line-height: 1.6; }}

        /* Trending Section */
        .trends-container {{ margin-top: 40px; padding-top: 25px; border-top: 2px solid #f1f5f9; }}
        .trends-title {{ 
            font-family: 'Playfair Display', serif; 
            font-size: 16px; 
            color: #0f172a; 
            margin-bottom: 15px; 
            font-variant: small-caps; 
            letter-spacing: 0.05em;
        }}
        .trends-list {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .trend-pill {{ 
            background: #f1f5f9; 
            color: #475569; 
            padding: 6px 12px; 
            border-radius: 20px; 
            font-size: 12px; 
            font-weight: 600;
            white-space: nowrap;
            text-decoration: none;
            transition: background 0.2s;
        }}
        .trend-pill:hover {{ background: #e2e8f0; color: #0f172a; }}
        
        .footer {{ text-align: center; padding: 40px 20px; font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Christopher's News Summary</h1>
        <p>{digest_name} &bull; {datetime.now().strftime('%A, %B %d, %Y')}</p>
    </div>
    <div class="content">
"""

    category_labels = {
        "zerohedge": "ZeroHedge",
        "federalist": "The Federalist",
        "dodgers": "Dodgers Nation",
        "finance": "Finance & Markets",
        "politics": "Politics",
        "tech": "Technology",
        "sports": "Sports",
        "opinion": "Opinion & Commentary",
        "josh_allen": "Josh Allen Updates",
        "special": "Special Interest",
        "general": "General News",
        "world": "World News",
    }

    # Sort categories
    # Order: News -> Sports -> Dodgers -> Josh Allen -> Special Search
    cat_order = ["zerohedge", "federalist", "general", "finance", "politics", "tech", "world", "sports", "dodgers", "josh_allen", "special"]
    
    # Add any remaining categories not explicitly in the order
    remaining_cats = sorted([c for c in grouped.keys() if c not in cat_order])
    full_order = cat_order + remaining_cats

    for cat in full_order:
        if cat not in grouped:
            continue
        articles = grouped[cat]
        label = category_labels.get(cat, cat.title())

        html += f'<div class="category"><h2>{label} ({len(articles)})</h2>'

        for article in articles:
            clean_summary = re.sub(r'<[^>]+>', '', article.get("summary", ""))[:200]
            if len(article.get("summary", "")) > 200:
                clean_summary += "..."

            img_tag = ""
            if article.get("image_url"):
                img_tag = f'<img src="{article["image_url"]}" class="article-image" onerror="this.style.display=\'none\';">'

            html += f'''
            <div class="article">
                {img_tag}
                <div class="meta">{article['source']} &bull; {article['date'].strftime('%I:%M %p')}</div>
                <h3><a href="{article['link']}">{article['title']}</a></h3>
                <div class="summary">{clean_summary}</div>
            </div>
            '''

        html += '</div>'

    # Add Trending Section at the bottom if available
    if trends:
        html += '<div class="trends-container"><div class="trends-title">Trending on X</div><div class="trends-list">'
        for trend in trends:
            # URL encode the trend for the link
            encoded_trend = trend.replace("#", "%23").replace(" ", "%20")
            html += f'<a href="https://x.com/search?q={encoded_trend}" class="trend-pill">{trend}</a>'
        html += '</div></div>'

    total = sum(len(v) for v in grouped.values())
    html += f"""
    </div>
    <div class="footer">
        <p>{total} articles from {len(grouped)} categories</p>
        <p>Generated by NewsSummary</p>
    </div>
</body>
</html>
"""
    return html


def send_email(html: str, subject: str):
    """Send email digest via SMTP."""
    # Get credentials from environment
    smtp_host = os.environ.get("EMAIL_HOST", "smtp.mail.me.com")
    smtp_port = int(os.environ.get("EMAIL_PORT", "587"))
    smtp_user = os.environ.get("EMAIL_USER")
    smtp_pass = os.environ.get("EMAIL_PASS")
    email_to = os.environ.get("EMAIL_TO")

    if not all([smtp_user, smtp_pass, email_to]):
        print("Missing email credentials. Set EMAIL_USER, EMAIL_PASS, EMAIL_TO")
        # Save to file instead
        with open("digest.html", "w") as f:
            f.write(html)
        print("Saved digest to digest.html")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = email_to

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, email_to.split(","), msg.as_string())
        print(f"Email sent to {email_to}")
    except Exception as e:
        print(f"Error sending email: {e}")
        with open("digest.html", "w") as f:
            f.write(html)
        print("Saved digest to digest.html")


def main():
    """Main entry point."""
    # Determine digest type from args or time
    # Use Mountain Time (America/Denver) for hour check
    # UTC-7 (no DST correction for simplicity, or use offset)
    # Better: check if we are in GitHub or local and adjust
    
    # Load config for timezone setting
    config = load_config()
    settings = config.get("settings", {})
    tz_name = settings.get("timezone", "America/Denver")
    
    # For simplicity without pytz, we estimate Mountain Time offset (-7)
    # A more robust way is to use the environment variable TZ if on Linux
    try:
        import time
        if hasattr(time, 'tzset'):
            os.environ['TZ'] = tz_name
            time.tzset()
    except:
        pass

    now = datetime.utcnow()
    hour = now.hour
    
    if len(sys.argv) > 1:
        digest_type = sys.argv[1].lower()
    elif hour >= 11 and hour < 14:  # 5a-8a MT is roughly 12-15 UTC
        # This detection is tricky without knowing the exact cron trigger relation
        # but if we are running at 13 UTC (6 AM MT), 19 UTC (12 PM MT), 1 UTC (6 PM MT)
        # 13 UTC: morning
        # 19 UTC: noon
        # 1 UTC: evening
        digest_type = "morning" if hour == 13 else ("noon" if hour == 19 else "evening")
    else:
        # Fallback based on UTC hours
        if hour >= 11 and hour < 16: digest_type = "morning"
        elif hour >= 16 and hour < 22: digest_type = "noon"
        else: digest_type = "evening"

    names = {
        "morning": "Morning",
        "noon": "Noon",
        "afternoon": "Afternoon",
        "evening": "Evening"
    }
    digest_name = names.get(digest_type, "News Digest")

    print(f"Generating {digest_name}...")

    # Load config
    config = load_config()
    settings = config.get("settings", {})

    # Fetch feeds
    print(f"Fetching {len(config['feeds'])} feeds...")
    articles = fetch_all_feeds(config["feeds"])
    
    # NEW: Fetch Josh Allen via Search API
    print("Searching for Josh Allen updates via API...")
    search_articles = search_news("Josh Allen", limit=5)
    print(f"Search API returned {len(search_articles)} articles")
    articles.extend(search_articles)

    # NEW: Fetch Special Search
    print("Searching for Special Interest...")
    special_articles = search_news("thick OR thicc latinas", limit=3)
    for a in special_articles: a["category"] = "special"
    print(f"Special Search returned {len(special_articles)} articles")
    articles.extend(special_articles)

    # NEW: Fetch Twitter Trends
    print("Fetching Twitter Trends...")
    trends = fetch_trending_topics()
    print(f"Fetched {len(trends)} trends")

    print(f"Total fetched {len(articles)} articles")

    # Filter by recent (dynamic window)
    # Morning: 12h (6pm-6am), Noon: 6h (6am-12pm), Evening: 6h (12pm-6pm)
    hours_back = 12 if digest_type == "morning" else 6
    cutoff = datetime.utcnow() - timedelta(hours=hours_back)
    articles = [a for a in articles if a["date"] > cutoff]
    print(f"Recent articles (last {hours_back}h): {len(articles)}")

    # Filter by keywords
    articles = filter_articles(articles, config.get("keywords", {}))
    print(f"After keyword filter: {len(articles)}")

    # Deduplicate
    articles = deduplicate(articles, settings.get("dedup_similarity", 0.85))
    print(f"After dedup: {len(articles)}")

    # Sort by score then date (highest score first, then newest date)
    articles.sort(key=lambda x: (x.get("score", 0), x["date"]), reverse=True)

    # Group and limit
    grouped = group_by_category(
        articles, 
        settings.get("max_per_category", 12),
        settings.get("category_limits", {})
    )
    
    # Print summary for debug
    print("\n--- Digest Summary ---")
    josh_count = len(grouped.get("josh_allen", []))
    print(f"Josh Allen Articles: {josh_count}")
    
    for cat, items in grouped.items():
        if cat != "josh_allen":
            print(f"Category '{cat}': {len(items)} articles")
    print("----------------------\n")

    # Format HTML
    html = format_html_digest(grouped, digest_name, trends=locals().get('trends', []))

    # Send email
    subject = f"{digest_name} News Summary - {datetime.now().strftime('%b %d, %Y')}"
    send_email(html, subject)

    print("Done!")


if __name__ == "__main__":
    main()

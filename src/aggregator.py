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
import feedparser
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from difflib import SequenceMatcher
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed


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
                article["date"] = datetime.now()

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

        # Calculate score
        score = 0
        if any(p.search(text) for p in priority_patterns):
            score += 100
        if any(p.search(text) for p in interest_patterns):
            score += 50

        article["score"] = score
        filtered.append(article)

    return filtered


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


def format_html_digest(grouped: dict, digest_name: str) -> str:
    """Format articles as HTML email."""
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
        
        .content {{ background: white; padding: 30px; border-radius: 0 0 12px 12px; shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }}
        
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
        
        .footer {{ text-align: center; padding: 40px 20px; font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{digest_name}</h1>
        <p>{datetime.now().strftime('%A, %B %d, %Y')}</p>
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
        "general": "General News",
        "world": "World News",
    }

    # Sort categories (individual feeds first, then general news, then other categories)
    cat_order = ["zerohedge", "federalist", "dodgers", "general", "finance", "politics", "tech", "world", "sports"]

    for cat in cat_order:
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
    smtp_host = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
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
    hour = datetime.now().hour
    if len(sys.argv) > 1:
        digest_type = sys.argv[1]
    elif hour < 12:
        digest_type = "morning"
    else:
        digest_type = "evening"

    digest_name = "Morning Digest" if digest_type == "morning" else "Evening Digest"

    print(f"Generating {digest_name}...")

    # Load config
    config = load_config()
    settings = config.get("settings", {})

    # Fetch feeds
    print(f"Fetching {len(config['feeds'])} feeds...")
    articles = fetch_all_feeds(config["feeds"])
    print(f"Fetched {len(articles)} articles")

    # Filter by recent (last 12 hours)
    cutoff = datetime.now() - timedelta(hours=12)
    articles = [a for a in articles if a["date"] > cutoff]
    print(f"Recent articles: {len(articles)}")

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
    
    # Print category counts for debug
    for cat, items in grouped.items():
        print(f"Category '{cat}': {len(items)} articles")

    # Format HTML
    html = format_html_digest(grouped, digest_name)

    # Send email
    subject = f"{digest_name} - {datetime.now().strftime('%b %d, %Y')}"
    send_email(html, subject)

    print("Done!")


if __name__ == "__main__":
    main()

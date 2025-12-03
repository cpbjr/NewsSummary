#!/usr/bin/env python3
"""
NewsSummary Admin Panel
Flask application for managing RSS feed configuration
"""

import os
import yaml
import subprocess
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
CONFIG_PATH = '../feeds.yaml'
KEYWORDS_PATH = '../frequency_words.txt'
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')  # Change in production


# Authentication decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ============================================================================
# ROUTES - Authentication
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))


# ============================================================================
# ROUTES - Main Dashboard
# ============================================================================

@app.route('/')
@requires_auth
def index():
    """Dashboard homepage"""
    config = load_config()
    stats = get_stats()
    return render_template('index.html', config=config, stats=stats)


@app.route('/feeds')
@requires_auth
def feeds():
    """RSS feed management page"""
    config = load_config()
    feeds = config.get('feeds', [])
    return render_template('feeds.html', feeds=feeds)


@app.route('/delivery')
@requires_auth
def delivery():
    """Delivery settings page"""
    config = load_config()
    settings = config.get('settings', {})
    return render_template('delivery.html', settings=settings)


@app.route('/keywords')
@requires_auth
def keywords():
    """Keyword filter management page"""
    config = load_config()
    keywords = config.get('keywords', {})
    return render_template('keywords.html', keywords=keywords)


@app.route('/preview')
@requires_auth
def preview():
    """Preview digest page"""
    return render_template('preview.html')


# ============================================================================
# API ROUTES - Configuration Management
# ============================================================================

@app.route('/api/config', methods=['GET'])
@requires_auth
def get_config():
    """Get current configuration"""
    config = load_config()
    return jsonify(config)


@app.route('/api/feeds', methods=['GET', 'POST', 'PUT', 'DELETE'])
@requires_auth
def manage_feeds():
    """Manage RSS feeds"""
    config = load_config()
    feeds = config.get('feeds', [])

    if request.method == 'GET':
        return jsonify(feeds)

    elif request.method == 'POST':
        # Add new feed
        new_feed = request.json
        feeds.append(new_feed)
        config['feeds'] = feeds
        save_config(config)
        return jsonify({'success': True, 'feed': new_feed})

    elif request.method == 'PUT':
        # Update existing feed
        feed_index = request.json.get('index')
        updated_feed = request.json.get('feed')
        if 0 <= feed_index < len(feeds):
            feeds[feed_index] = updated_feed
            config['feeds'] = feeds
            save_config(config)
            return jsonify({'success': True, 'feed': updated_feed})
        return jsonify({'success': False, 'error': 'Invalid feed index'}), 400

    elif request.method == 'DELETE':
        # Delete feed
        feed_index = request.json.get('index')
        if 0 <= feed_index < len(feeds):
            deleted_feed = feeds.pop(feed_index)
            config['feeds'] = feeds
            save_config(config)
            return jsonify({'success': True, 'deleted': deleted_feed})
        return jsonify({'success': False, 'error': 'Invalid feed index'}), 400


@app.route('/api/settings', methods=['GET', 'POST'])
@requires_auth
def manage_settings():
    """Manage delivery settings"""
    config = load_config()

    if request.method == 'GET':
        return jsonify(config.get('settings', {}))

    elif request.method == 'POST':
        # Update settings
        new_settings = request.json
        config['settings'] = new_settings
        save_config(config)
        return jsonify({'success': True, 'settings': new_settings})


@app.route('/api/keywords', methods=['GET', 'POST'])
@requires_auth
def manage_keywords():
    """Manage keyword filters"""
    config = load_config()

    if request.method == 'GET':
        return jsonify(config.get('keywords', {}))

    elif request.method == 'POST':
        # Update keywords
        new_keywords = request.json
        config['keywords'] = new_keywords
        save_config(config)
        return jsonify({'success': True, 'keywords': new_keywords})


@app.route('/api/test-feed', methods=['POST'])
@requires_auth
def test_feed():
    """Test RSS feed URL"""
    import feedparser

    url = request.json.get('url')
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'}), 400

    try:
        parsed = feedparser.parse(url)
        if parsed.bozo:
            return jsonify({'success': False, 'error': f'Invalid feed: {parsed.bozo_exception}'})

        articles = []
        for entry in parsed.entries[:5]:
            articles.append({
                'title': entry.get('title', 'No title'),
                'link': entry.get('link', ''),
                'published': entry.get('published', entry.get('updated', 'Unknown'))
            })

        return jsonify({
            'success': True,
            'feed_title': parsed.feed.get('title', 'Unknown'),
            'article_count': len(parsed.entries),
            'sample_articles': articles
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/preview-digest', methods=['POST'])
@requires_auth
def preview_digest():
    """Generate preview of digest"""
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
    from aggregator import fetch_all_feeds, filter_articles, deduplicate, group_by_category, format_html_digest

    try:
        digest_type = request.json.get('type', 'morning')
        config = load_config()

        # Fetch feeds
        articles = fetch_all_feeds(config.get('feeds', []))

        # Filter and process
        articles = filter_articles(articles, config.get('keywords', {}))
        articles = deduplicate(articles, config.get('settings', {}).get('dedup_similarity', 0.85))

        # Sort by score
        articles.sort(key=lambda x: (-x.get('score', 0), x['date']), reverse=True)

        # Group
        grouped = group_by_category(articles, config.get('settings', {}).get('max_per_category', 12))

        # Format
        digest_name = "Morning Digest Preview" if digest_type == 'morning' else "Evening Digest Preview"
        html = format_html_digest(grouped, digest_name)

        total_articles = sum(len(v) for v in grouped.values())

        return jsonify({
            'success': True,
            'html': html,
            'article_count': total_articles,
            'categories': {k: len(v) for k, v in grouped.items()}
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
@requires_auth
def api_stats():
    """Get dashboard statistics"""
    stats = get_stats()
    return jsonify(stats)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_config():
    """Load configuration from YAML file"""
    config_path = os.path.join(os.path.dirname(__file__), CONFIG_PATH)
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {'feeds': [], 'settings': {}, 'keywords': {}}


def save_config(config):
    """Save configuration to YAML file and commit to GitHub"""
    config_path = os.path.join(os.path.dirname(__file__), CONFIG_PATH)

    # Save to file
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    # Auto-commit to GitHub
    try:
        repo_path = os.path.join(os.path.dirname(__file__), '..')
        subprocess.run(['git', 'add', 'feeds.yaml'], cwd=repo_path, check=True)
        subprocess.run([
            'git', 'commit', '-m',
            f'Admin panel: Update configuration - {datetime.now().strftime("%Y-%m-%d %H:%M")}'
        ], cwd=repo_path, check=True)
        subprocess.run(['git', 'push'], cwd=repo_path, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Git commit/push failed: {e}")
        # Don't fail the save operation if git fails


def get_stats():
    """Get dashboard statistics"""
    config = load_config()

    # Get last digest info from git log
    try:
        repo_path = os.path.join(os.path.dirname(__file__), '..')
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%cd', '--date=relative'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        last_update = result.stdout.strip() if result.returncode == 0 else 'Unknown'
    except:
        last_update = 'Unknown'

    return {
        'feed_count': len(config.get('feeds', [])),
        'exclude_keywords': len(config.get('keywords', {}).get('exclude', [])),
        'priority_keywords': len(config.get('keywords', {}).get('priority', [])),
        'last_update': last_update,
        'max_articles': config.get('settings', {}).get('max_per_category', 12)
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)

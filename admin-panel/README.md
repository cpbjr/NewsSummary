# NewsSummary Admin Panel

Web-based configuration dashboard for managing your RSS news aggregator.

## Features

- 📰 **RSS Feed Management** - Add, edit, delete, and test feeds
- ⏰ **Delivery Settings** - Configure digest times and article limits
- 🔍 **Keyword Filters** - Manage exclude, priority, and interest keywords
- 👁️ **Preview Digest** - See what your next email will look like
- 🔄 **Auto-Deploy** - Changes automatically commit to GitHub

## Installation

### Local Development

```bash
cd admin-panel

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ADMIN_PASSWORD="your-secure-password"
export FLASK_SECRET_KEY="your-secret-key"

# Run the app
python app.py
```

Access at: http://localhost:5001

### Production Deployment (WhitePineTech Server)

```bash
# SSH into server
ssh whitepine

# Navigate to project
cd /path/to/NewsSummary/admin-panel

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables in ~/.bashrc or systemd service
export ADMIN_PASSWORD="your-secure-password"
export FLASK_SECRET_KEY="$(openssl rand -hex 32)"
export PORT=5001

# Run with gunicorn (production)
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5001 app:app
```

### Systemd Service (Recommended)

Create `/etc/systemd/system/newssummary-admin.service`:

```ini
[Unit]
Description=NewsSummary Admin Panel
After=network.target

[Service]
User=your-username
WorkingDirectory=/path/to/NewsSummary/admin-panel
Environment="ADMIN_PASSWORD=your-secure-password"
Environment="FLASK_SECRET_KEY=your-secret-key"
Environment="PORT=5001"
ExecStart=/path/to/NewsSummary/admin-panel/venv/bin/gunicorn -w 2 -b 0.0.0.0:5001 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable newssummary-admin
sudo systemctl start newssummary-admin
sudo systemctl status newssummary-admin
```

### Nginx Reverse Proxy

Add to your nginx config:

```nginx
server {
    listen 80;
    server_name news-admin.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ADMIN_PASSWORD` | Admin panel password | `admin123` (change!) |
| `FLASK_SECRET_KEY` | Session encryption key | `dev-secret-key-change-in-production` |
| `PORT` | Server port | `5001` |
| `FLASK_DEBUG` | Enable debug mode | `False` |

### GitHub Auto-Commit

The admin panel automatically commits changes to GitHub when you save. Ensure:

1. Git is configured on the server
2. SSH keys are set up for GitHub
3. The repository is cloned with SSH URL

Test git push:

```bash
cd /path/to/NewsSummary
git config user.name "Admin Panel"
git config user.email "admin@yourserver.com"
git push
```

## Security Notes

1. **Change default password** - Set `ADMIN_PASSWORD` environment variable
2. **Use HTTPS** - Configure SSL certificate with Let's Encrypt
3. **Firewall** - Restrict port 5001 to localhost if using nginx proxy
4. **Strong secret key** - Generate with `openssl rand -hex 32`

## API Endpoints

All endpoints require authentication.

### Configuration
- `GET /api/config` - Get full config
- `GET /api/feeds` - List RSS feeds
- `POST /api/feeds` - Add new feed
- `PUT /api/feeds` - Update feed
- `DELETE /api/feeds` - Delete feed
- `POST /api/test-feed` - Test RSS feed URL

### Settings
- `GET /api/settings` - Get delivery settings
- `POST /api/settings` - Update settings

### Keywords
- `GET /api/keywords` - Get keyword filters
- `POST /api/keywords` - Update keywords

### Preview
- `POST /api/preview-digest` - Generate digest preview

## Troubleshooting

### "Config file not found"
Ensure `feeds.yaml` exists in parent directory:
```bash
cd admin-panel
ls ../feeds.yaml
```

### "Git push failed"
Check SSH keys and repository permissions:
```bash
git remote -v
ssh -T git@github.com
```

### "Cannot bind to port 5001"
Port is already in use. Change `PORT` environment variable or kill existing process:
```bash
sudo lsof -i :5001
sudo kill <PID>
```

## Development

### Project Structure

```
admin-panel/
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── login.html         # Login page
│   ├── index.html         # Dashboard
│   ├── feeds.html         # RSS feed management
│   ├── delivery.html      # Delivery settings
│   ├── keywords.html      # Keyword filters
│   └── preview.html       # Digest preview
└── README.md              # This file
```

### Adding New Features

1. Add route to `app.py`
2. Create template in `templates/`
3. Add navigation link in `base.html`
4. Test locally before deploying

## Support

For issues or questions:
- Check GitHub Actions logs for digest errors
- Review nginx/gunicorn logs for server issues
- Test feed URLs with `/api/test-feed` endpoint

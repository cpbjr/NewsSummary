# Quick Start Guide - NewsSummary Admin Panel

## 🚀 Local Testing (Right Now!)

```bash
cd ~/Documents/AI_Automation/Projects/NewsSummary/admin-panel

# Activate virtual environment
source venv/bin/activate

# Set password and start server
export ADMIN_PASSWORD="test123"
python app.py
```

Then open your browser to: **http://localhost:5001**

Login with password: `test123`

---

## 📋 What You Can Do

### 1. Dashboard (/)
- View current configuration summary
- See feed count, article limits, keyword filters
- Quick access to all sections

### 2. RSS Feeds (/feeds)
- **Add Feed**: Click "+ Add New Feed" button
  - Enter name (e.g., "TechCrunch AI")
  - Enter RSS URL
  - Click "Test" to verify feed works
  - Select category (Finance, Politics, Tech, Sports, etc.)
  - Set weight (0.5-2.0, higher = more priority)
- **Edit Feed**: Click "Edit" on any feed
- **Delete Feed**: Click "Delete" (with confirmation)

### 3. Delivery Settings (/delivery)
- Change digest times (morning/evening)
- Adjust max articles per category (slider)
- Set deduplication similarity threshold
- Override limits for specific categories

### 4. Keyword Filters (/keywords)
- **Exclude**: Block articles containing these words
- **Priority**: Boost articles with these words (+100 score)
- **Interest**: Moderate boost for these words (+50 score)

### 5. Preview Digest (/preview)
- Click "Morning Digest" or "Evening Digest"
- See exactly what your next email will look like
- Takes 10-20 seconds to fetch all feeds
- Opens in-browser preview

---

## 💾 How Auto-Save Works

When you click "Save" on any page:

1. ✅ Configuration is saved to `feeds.yaml`
2. ✅ Changes are committed to Git
3. ✅ Automatically pushed to GitHub
4. ✅ GitHub Actions picks up changes on next digest

**No manual deployment needed!**

---

## 🔒 Security Notes

**For local testing**: Password is set via `ADMIN_PASSWORD` environment variable

**For production**:
1. Set strong password on server
2. Use HTTPS (configure nginx + Let's Encrypt)
3. Generate secure secret key: `openssl rand -hex 32`

---

## 🐛 Troubleshooting

### "Config file not found"
Make sure you're in the `admin-panel/` directory and `../feeds.yaml` exists.

### "Git push failed"
The app auto-commits to GitHub. If this fails:
- Ensure Git is configured: `git config user.name "Your Name"`
- Ensure SSH keys are set up for GitHub
- Test manually: `cd .. && git push`

### Preview doesn't load
- Check that all RSS feed URLs are valid
- Some feeds may be slow (10-20 seconds is normal)
- Check console for errors

---

## 🚀 Production Deployment

See full deployment guide in `README.md`, but here's the quick version:

```bash
# On WhitePineTech server
ssh whitepine

# Clone or pull repo
cd /var/www
git clone git@github.com:cpbjr/NewsSummary.git newssummary-admin
cd newssummary-admin/admin-panel

# Install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Set environment variables
export ADMIN_PASSWORD="your-secure-password"
export FLASK_SECRET_KEY="$(openssl rand -hex 32)"

# Run with gunicorn
gunicorn -w 2 -b 0.0.0.0:5001 app:app
```

For systemd service setup, see `README.md`.

---

## 📞 Next Steps

1. **Test locally** - Start the server and explore each section
2. **Add/remove feeds** - Customize your news sources
3. **Adjust limits** - Fine-tune article counts per category
4. **Preview digest** - Make sure it looks good
5. **Deploy to server** - Follow deployment instructions when ready

---

## 💡 Pro Tips

- **Test feed URLs** before adding them (use "Test" button)
- **Start with default weights** (1.0) and adjust after seeing results
- **Use preview feature** to check changes before the next scheduled digest
- **Category limits** override the global max per category setting
- **Keyword filters** are case-insensitive
- **Higher dedup similarity** = fewer duplicate articles (85% recommended)

---

**Questions?** Check `README.md` for full documentation or review the code in `app.py`.

#!/bin/bash
# deploy_to_hetzner.sh - NewsSummary Migration Script
set -e

SERVER="whitepine"
REMOTE_PATH="/var/www/newssummary"
LOCAL_PATH="/home/cpbjr/Documents/AI_Automation/Projects/NewsSummary"

echo "🚀 Starting migration to Hetzner ($SERVER)..."

# 1. Prepare server directory
ssh $SERVER "sudo mkdir -p $REMOTE_PATH && sudo chown -R deploy:deploy $REMOTE_PATH"

# 2. Sync files
echo "📤 Syncing files to server..."
rsync -avz --exclude='venv' --exclude='.git' --exclude='.github' --exclude='__pycache__' \
    $LOCAL_PATH/ $SERVER:$REMOTE_PATH/

# 3. Create .env on server
echo "⚙️  Configuring environment variables..."
ssh $SERVER << 'ENDSSH'
cat > /var/www/newssummary/.env << EOF
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=cpbjr@mac.com
EMAIL_PASS=zqsb-fzbq-mmmh-jkjn
EMAIL_TO=cpbjr@mac.com
PORT=5001
ADMIN_PASSWORD=admin123
EOF
chmod 600 /var/www/newssummary/.env
ENDSSH

# 4. Setup venv and dependencies
echo "📦 Setting up dependencies on server..."
ssh $SERVER << 'ENDSSH'
cd /var/www/newssummary
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn flask pyyaml feedparser
ENDSSH

# 5. Configure systemd service for Admin Panel
echo "🔧 Configuring systemd service..."
ssh whitepine-root << EOF
cat > /etc/systemd/system/newssummary-admin.service << 'SERVICE'
[Unit]
Description=NewsSummary Admin Panel
After=network.target

[Service]
User=deploy
WorkingDirectory=/var/www/newssummary/admin-panel
EnvironmentFile=/var/www/newssummary/.env
ExecStart=/var/www/newssummary/venv/bin/gunicorn -w 2 -b 0.0.0.0:5001 app:app
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE
systemctl daemon-reload
systemctl enable newssummary-admin
systemctl restart newssummary-admin
EOF

# 6. Configure Cron Jobs (Mountain Time)
echo "📅 Configuring cron jobs on server..."
ssh $SERVER << 'ENDSSH'
(crontab -l | grep -v "src/aggregator.py" ; echo "0 6 * * * cd /var/www/newssummary && ./venv/bin/python src/aggregator.py morning >> /var/log/newssummary_cron.log 2>&1") | crontab -
(crontab -l | grep -v "noon" ; echo "0 12 * * * cd /var/www/newssummary && ./venv/bin/python src/aggregator.py noon >> /var/log/newssummary_cron.log 2>&1") | crontab -
(crontab -l | grep -v "evening" ; echo "0 18 * * * cd /var/www/newssummary && ./venv/bin/python src/aggregator.py evening >> /var/log/newssummary_cron.log 2>&1") | crontab -
sudo touch /var/log/newssummary_cron.log && sudo chown deploy:deploy /var/log/newssummary_cron.log
ENDSSH

echo "✅ Migration complete!"
echo "📡 Admin Panel: http://5.78.128.255:5001"
echo "🕒 Cron Jobs set for 6a, 12p, 6p MT"

#!/bin/bash
# Deployment script for NewsSummary Admin Panel

set -e

echo "🚀 Deploying NewsSummary Admin Panel to WhitePineTech server..."

# Configuration
SERVER="whitepine"
REMOTE_PATH="/var/www/newssummary-admin"
SERVICE_NAME="newssummary-admin"

# Build locally (if needed)
echo "📦 Installing dependencies locally..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Test locally first
echo "✅ Testing Flask app..."
python app.py &
FLASK_PID=$!
sleep 3
curl -s http://localhost:5001/login > /dev/null && echo "✓ Flask app responds" || echo "✗ Flask app failed"
kill $FLASK_PID

# Deploy to server
echo "📤 Copying files to server..."
ssh $SERVER "mkdir -p $REMOTE_PATH"
rsync -avz --exclude='venv' --exclude='__pycache__' --exclude='*.pyc' \
    ./ $SERVER:$REMOTE_PATH/

# Setup on server
echo "⚙️  Setting up on server..."
ssh $SERVER << 'ENDSSH'
cd /var/www/newssummary-admin

# Create venv if not exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Install dependencies
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Create systemd service if not exists
if [ ! -f "/etc/systemd/system/newssummary-admin.service" ]; then
    sudo tee /etc/systemd/system/newssummary-admin.service > /dev/null << EOF
[Unit]
Description=NewsSummary Admin Panel
After=network.target

[Service]
User=$USER
WorkingDirectory=/var/www/newssummary-admin
Environment="ADMIN_PASSWORD=${ADMIN_PASSWORD:-admin123}"
Environment="FLASK_SECRET_KEY=${FLASK_SECRET_KEY:-$(openssl rand -hex 32)}"
Environment="PORT=5001"
ExecStart=/var/www/newssummary-admin/venv/bin/gunicorn -w 2 -b 0.0.0.0:5001 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    sudo systemctl daemon-reload
    sudo systemctl enable newssummary-admin
fi

# Restart service
sudo systemctl restart newssummary-admin
sudo systemctl status newssummary-admin --no-pager
ENDSSH

echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. Set ADMIN_PASSWORD on server: ssh $SERVER 'echo \"export ADMIN_PASSWORD=your-password\" >> ~/.bashrc'"
echo "2. Configure nginx reverse proxy (see README.md)"
echo "3. Access at: http://your-server-ip:5001"

<!--
 * WhatBot v1.2.0
 * Location: docs\dev-guides\UBUNTU_PRODUCTION_GUIDE.md
 * Creation Date: December 21, 2024
 * 
 * Author: Ben Adenle
 * Email: ben@techjamlabs.com
 * Phone: +2348099999928
 * 
 * Copyright (c) TECHJAMLABS Limited / +234 201 330 9089 / +1 206 7100170 / hello@techjamlabs.com
 * 
 * Date of last change: June 21, 2025
 -->

# WhatBot Ubuntu Production Deployment Guide

## Overview

This guide covers the complete setup and management of WhatBot in an Ubuntu production environment, including automatic reconnection handling for WhatsApp disconnections.

## Prerequisites

- Ubuntu 20.04 LTS or later
- Root or sudo access
- Internet connection
- Domain name (optional, for SSL)

## Quick Deployment

### 1. Automated Deployment

```bash
# Clone or download the project
cd /path/to/whatbot

# Make deployment script executable
chmod +x deploy-ubuntu.sh

# Run the deployment script
sudo ./deploy-ubuntu.sh
```

### 2. Manual Deployment

If you prefer manual setup, follow these steps:

#### Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y curl wget git build-essential python3

# Install Node.js LTS
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo bash -
sudo apt install -y nodejs

# Install PM2 globally
sudo npm install -g pm2

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib
```

#### Setup Application
```bash
# Create application user
sudo useradd -r -g whatbot -d /opt/whatbot -s /bin/bash whatbot
sudo groupadd whatbot

# Create application directory
sudo mkdir -p /opt/whatbot
sudo chown whatbot:whatbot /opt/whatbot

# Copy application files
sudo cp -r . /opt/whatbot/
sudo chown -R whatbot:whatbot /opt/whatbot

# Install dependencies
cd /opt/whatbot
sudo -u whatbot npm install
```

#### Configure Environment
```bash
# Create environment file
sudo nano /etc/default/whatbot
```

Add the following content:
```bash
NODE_ENV=production
PORT=41100
WHATSAPP_NUMBER=+2348064866332
COMPANY_NAME=GOMED
APP_TITLE=WhatsApp Bot

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=whatbot
DB_USER=whatbot
DB_PASSWORD=your_secure_password_here

# JWT Configuration
JWT_SECRET=your_jwt_secret_here

# API Configuration
BASE_URL=http://127.0.0.1:41100
```

#### Setup Database
```bash
# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE whatbot;
CREATE USER whatbot WITH ENCRYPTED PASSWORD 'your_secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE whatbot TO whatbot;
\q
EOF
```

#### Install Systemd Service
```bash
# Copy service file
sudo cp whatbot.service /etc/systemd/system/

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable whatbot.service

# Start the service
sudo systemctl start whatbot.service
```

## WhatsApp Connection Management

### Automatic Reconnection Features

The application now includes several features to handle WhatsApp disconnections:

1. **Session Validation**: Automatically detects expired sessions (older than 24 hours)
2. **Automatic Reconnection**: Attempts reconnection every 30 seconds if disconnected
3. **Session Cleanup**: Removes invalid sessions automatically
4. **Browser Stability**: Updated headless mode and browser arguments for Linux

### Manual Management Commands

#### Using the WhatsApp Manager Script
```bash
# Check status
./whatsapp-manager.sh status

# Force reconnection
./whatsapp-manager.sh reconnect

# Force restart
./whatsapp-manager.sh restart

# Clear sessions
./whatsapp-manager.sh clear

# View logs
./whatsapp-manager.sh logs

# Interactive menu
./whatsapp-manager.sh
```

#### Using Direct Commands
```bash
# Check status
node whatsapp-manager.js status

# Force reconnection
node whatsapp-manager.js reconnect

# Force restart
node whatsapp-manager.js restart

# Clear sessions
node whatsapp-manager.js clear
```

#### Using Systemd Commands
```bash
# Check service status
sudo systemctl status whatbot.service

# View logs
sudo journalctl -u whatbot.service -f

# Restart service
sudo systemctl restart whatbot.service

# Stop service
sudo systemctl stop whatbot.service
```

## Monitoring and Maintenance

### Health Monitoring

#### Automated Monitoring Script
```bash
# Run health check
./monitor-ubuntu.sh

# Set up cron job for regular monitoring
sudo crontab -e
```

Add this line for hourly monitoring:
```
0 * * * * /opt/whatbot/monitor-ubuntu.sh
```

#### Manual Monitoring Commands
```bash
# Check service status
sudo systemctl status whatbot.service

# View recent logs
sudo journalctl -u whatbot.service --since "1 hour ago"

# Check disk usage
df -h /opt/whatbot

# Check memory usage
free -h

# Check process resources
ps aux | grep node
```

### Log Management

#### Log Locations
- **System logs**: `sudo journalctl -u whatbot.service`
- **Application logs**: `/opt/whatbot/logs/`
- **Monitor logs**: `/opt/whatbot/logs/monitor.log`

#### Log Rotation
Log rotation is automatically configured during deployment. Manual configuration:
```bash
sudo nano /etc/logrotate.d/whatbot
```

### Backup Procedures

#### Database Backup
```bash
# Create backup script
sudo nano /opt/whatbot/backup-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/opt/whatbot/backups"
DATE=$(date +%Y%m%d_%H%M%S)
sudo -u postgres pg_dump whatbot > "$BACKUP_DIR/whatbot_$DATE.sql"
```

#### Application Backup
```bash
# Backup application files
sudo tar -czf /opt/whatbot/backups/app_$(date +%Y%m%d_%H%M%S).tar.gz /opt/whatbot
```

## Troubleshooting

### Common Issues

#### 1. WhatsApp Not Connecting
```bash
# Check status
./whatsapp-manager.sh status

# Force reconnection
./whatsapp-manager.sh reconnect

# Clear sessions and restart
./whatsapp-manager.sh clear
sudo systemctl restart whatbot.service
```

#### 2. Service Not Starting
```bash
# Check service status
sudo systemctl status whatbot.service

# View detailed logs
sudo journalctl -u whatbot.service -n 50

# Check environment file
sudo cat /etc/default/whatbot
```

#### 3. Database Connection Issues
```bash
# Test database connection
sudo -u whatbot psql -h localhost -U whatbot -d whatbot -c "SELECT 1;"

# Check PostgreSQL status
sudo systemctl status postgresql
```

#### 4. High Resource Usage
```bash
# Check process resources
ps aux | grep node

# Check system resources
htop
df -h
free -h
```

### Emergency Procedures

#### Complete Reset
```bash
# Stop service
sudo systemctl stop whatbot.service

# Clear sessions
./whatsapp-manager.sh clear

# Remove tokens directory
sudo rm -rf /opt/whatbot/tokens

# Restart service
sudo systemctl start whatbot.service
```

#### Service Recovery
```bash
# Restart service
sudo systemctl restart whatbot.service

# Check if it's running
sudo systemctl is-active whatbot.service

# View logs for errors
sudo journalctl -u whatbot.service --since "5 minutes ago"
```

## Security Considerations

### Firewall Configuration
```bash
# Allow only necessary ports
sudo ufw allow ssh
sudo ufw allow 41100/tcp
sudo ufw enable
```

### SSL/TLS Setup (Optional)
```bash
# Install Certbot
sudo apt install -y certbot

# Get SSL certificate
sudo certbot certonly --standalone -d yourdomain.com

# Configure nginx or reverse proxy
```

### User Permissions
```bash
# Ensure proper file permissions
sudo chown -R whatbot:whatbot /opt/whatbot
sudo chmod 600 /etc/default/whatbot
```

## Performance Optimization

### System Tuning
```bash
# Increase file descriptor limits
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Optimize PostgreSQL
sudo nano /etc/postgresql/*/main/postgresql.conf
```

### Application Tuning
```bash
# Use PM2 for process management
sudo -u whatbot pm2 start server.js --name whatbot
sudo -u whatbot pm2 startup
sudo -u whatbot pm2 save
```

## Updates and Maintenance

### Application Updates
```bash
# Stop service
sudo systemctl stop whatbot.service

# Backup current version
sudo cp -r /opt/whatbot /opt/whatbot.backup.$(date +%Y%m%d)

# Update application files
sudo cp -r /path/to/new/version/* /opt/whatbot/

# Update dependencies
cd /opt/whatbot
sudo -u whatbot npm install

# Restart service
sudo systemctl start whatbot.service
```

### System Updates
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Restart services if needed
sudo systemctl restart whatbot.service
```

## Support and Monitoring

### Monitoring Setup
```bash
# Set up monitoring cron job
sudo crontab -e
```

Add monitoring schedule:
```
# Health check every 15 minutes
*/15 * * * * /opt/whatbot/monitor-ubuntu.sh

# Daily backup at 2 AM
0 2 * * * /opt/whatbot/backup-db.sh
```

### Alert Configuration
Edit the monitoring script to configure email alerts:
```bash
sudo nano /opt/whatbot/monitor-ubuntu.sh
```

Update the `ALERT_EMAIL` variable with your email address.

## Conclusion

This setup provides a robust, production-ready WhatsApp bot with automatic reconnection capabilities, comprehensive monitoring, and easy management tools. The system is designed to handle WhatsApp disconnections gracefully and maintain high availability.

For additional support, refer to the `WHATSAPP_TROUBLESHOOTING.md` file for specific WhatsApp-related issues. 
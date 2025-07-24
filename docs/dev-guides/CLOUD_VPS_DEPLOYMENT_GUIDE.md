/**
 * WhatBot v1.2.0
 * Location: docs/dev-guides/CLOUD_VPS_DEPLOYMENT_GUIDE.md
 * Creation Date: June 21, 2025
 * 
 * Author: Ben Adenle
 * Email: ben@techjamlabs.com
 * Phone: +2348099999928
 * 
 * Copyright (c) TECHJAMLABS Limited / +234 201 330 9089 / +1 206 7100170 / hello@techjamlabs.com
 * 
 * Date of last change: June 21, 2025
 */

# WhatBot Cloud VPS Deployment Guide

## 🎯 Overview

This comprehensive guide covers deploying WhatBot to various cloud VPS providers including AWS EC2, DigitalOcean Droplets, Linode, Vultr, and other cloud platforms. The guide includes server setup, security configuration, and production deployment best practices.

## 📋 Prerequisites

### Required Knowledge
- Basic Linux command line experience
- Understanding of SSH and remote server management
- Familiarity with cloud provider dashboards
- Basic networking concepts

### Required Accounts
- Cloud provider account (AWS, DigitalOcean, Linode, Vultr, etc.)
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)

---

## 🚀 Cloud Provider Selection

### Recommended VPS Specifications

#### Minimum Requirements
- **CPU:** 2 vCPUs
- **RAM:** 4GB
- **Storage:** 40GB SSD
- **Bandwidth:** 1TB/month
- **OS:** Ubuntu 22.04 LTS

#### Recommended Requirements
- **CPU:** 4 vCPUs
- **RAM:** 8GB
- **Storage:** 80GB SSD
- **Bandwidth:** 2TB/month
- **OS:** Ubuntu 22.04 LTS

### Provider Comparison

| Provider | Starting Price | Features | Support | Recommendation |
|----------|----------------|----------|---------|----------------|
| **DigitalOcean** | $24/month | Simple, reliable | Good | ⭐⭐⭐⭐⭐ |
| **Linode** | $24/month | Developer-friendly | Excellent | ⭐⭐⭐⭐⭐ |
| **Vultr** | $24/month | Global locations | Good | ⭐⭐⭐⭐ |
| **AWS EC2** | $20-40/month | Enterprise features | Excellent | ⭐⭐⭐⭐ |
| **Google Cloud** | $25-50/month | Advanced features | Good | ⭐⭐⭐⭐ |

---

## 🏗️ Server Setup by Provider

### 1. DigitalOcean Deployment

#### Step 1: Create Droplet
```bash
# Via DigitalOcean Dashboard
1. Login to DigitalOcean
2. Click "Create" → "Droplets"
3. Choose Ubuntu 22.04 LTS
4. Select plan: Basic → $24/month (4GB RAM, 2 vCPUs)
5. Choose datacenter region (closest to your users)
6. Add SSH key or create password
7. Click "Create Droplet"
```

#### Step 2: Initial Server Access
```bash
# Connect to your droplet
ssh root@your_server_ip

# Update system
apt update && apt upgrade -y

# Install essential packages
apt install -y curl wget git unzip software-properties-common
```

#### Step 3: Install Node.js and Dependencies
```bash
# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt-get install -y nodejs

# Install PostgreSQL
apt install -y postgresql postgresql-contrib

# Install PM2 globally
npm install -g pm2

# Install Nginx
apt install -y nginx

# Install Certbot for SSL
apt install -y certbot python3-certbot-nginx
```

### 2. Linode Deployment

#### Step 1: Create Linode
```bash
# Via Linode Dashboard
1. Login to Linode
2. Click "Create Linode"
3. Choose Ubuntu 22.04 LTS
4. Select plan: Linode 4GB (2 vCPUs, 4GB RAM)
5. Choose datacenter region
6. Add SSH key or create password
7. Click "Create Linode"
```

#### Step 2: Server Setup (Same as DigitalOcean)
```bash
# Connect and setup (same commands as above)
ssh root@your_linode_ip
# ... follow same setup steps
```

### 3. AWS EC2 Deployment

#### Step 1: Launch EC2 Instance
```bash
# Via AWS Console
1. Login to AWS Console
2. Navigate to EC2 → Instances → Launch Instances
3. Choose Amazon Linux 2023 or Ubuntu 22.04 LTS
4. Select instance type: t3.medium (2 vCPUs, 4GB RAM)
5. Configure security groups (see security section)
6. Launch instance with key pair
```

#### Step 2: Security Group Configuration
```bash
# Create security group with these rules:
- SSH (Port 22): 0.0.0.0/0 (or your IP)
- HTTP (Port 80): 0.0.0.0/0
- HTTPS (Port 443): 0.0.0.0/0
- Custom (Port 41100): 0.0.0.0/0 (WhatBot API)
```

#### Step 3: Connect and Setup
```bash
# Connect using your key pair
ssh -i your-key.pem ubuntu@your-ec2-ip

# Follow same setup steps as above
```

### 4. Vultr Deployment

#### Step 1: Create Instance
```bash
# Via Vultr Dashboard
1. Login to Vultr
2. Click "Deploy New Instance"
3. Choose Ubuntu 22.04 LTS
4. Select plan: Cloud Compute → $24/month
5. Choose server location
6. Add SSH key or create password
7. Deploy instance
```

#### Step 2: Server Setup (Same as others)
```bash
# Connect and setup (same commands as above)
ssh root@your_vultr_ip
# ... follow same setup steps
```

---

## 🔧 Application Deployment

### Step 1: Clone and Setup WhatBot
```bash
# Create application directory
mkdir -p /opt/whatbot
cd /opt/whatbot

# Clone repository
git clone https://github.com/TechJam-Labs/whatbot-master-copy.git .
# OR upload your code via SCP/SFTP

# Install dependencies
npm install

# Create environment file
cp config.template.env .env
nano .env
```

### Step 2: Environment Configuration
```bash
# Edit .env file with your configuration
nano .env

# Essential configuration:
PORT=41100
NODE_ENV=production
BASE_URL=https://your-domain.com
JWT_SECRET=your_secure_jwt_secret_here

# Database configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=whatbot_production
DB_USER=whatbot_user
DB_PASSWORD=your_secure_password

# WhatsApp configuration
WHATSAPP_NUMBER=+2349157342656
COMPANY_NAME=Your Company Name
```

### Step 3: Database Setup
```bash
# Create database and user
sudo -u postgres psql

CREATE DATABASE whatbot_production;
CREATE USER whatbot_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE whatbot_production TO whatbot_user;
\q

# Run database setup
npm run setup
```

### Step 4: PM2 Configuration
```bash
# Create PM2 ecosystem file
nano ecosystem.config.js

# Use the existing ecosystem.config.js or create custom one
# Start application with PM2
pm2 start ecosystem.config.js

# Save PM2 configuration
pm2 save

# Setup PM2 to start on boot
pm2 startup
```

### Step 5: Nginx Configuration
```bash
# Create Nginx configuration
nano /etc/nginx/sites-available/whatbot

# Configuration content:
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://localhost:41100;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Static files
    location /public {
        alias /opt/whatbot/public;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Uploads
    location /uploads {
        alias /opt/whatbot/uploads;
        expires 1d;
    }
}

# Enable site
ln -s /etc/nginx/sites-available/whatbot /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default

# Test and reload Nginx
nginx -t
systemctl reload nginx
```

### Step 6: SSL Certificate Setup
```bash
# Install SSL certificate with Let's Encrypt
certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal setup
crontab -e
# Add this line:
0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 🔒 Security Configuration

### Step 1: Firewall Setup
```bash
# Install UFW
apt install -y ufw

# Configure firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 'Nginx Full'
ufw allow 41100

# Enable firewall
ufw enable
```

### Step 2: SSH Security
```bash
# Edit SSH configuration
nano /etc/ssh/sshd_config

# Recommended settings:
Port 2222  # Change default port
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2

# Restart SSH
systemctl restart sshd
```

### Step 3: Fail2ban Setup
```bash
# Install Fail2ban
apt install -y fail2ban

# Create configuration
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
nano /etc/fail2ban/jail.local

# Add WhatBot jail
[whatbot]
enabled = true
port = 41100
filter = whatbot
logpath = /opt/whatbot/logs/app.log
maxretry = 3
bantime = 3600

# Start Fail2ban
systemctl enable fail2ban
systemctl start fail2ban
```

### Step 4: Regular Security Updates
```bash
# Setup automatic security updates
apt install -y unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades

# Configure automatic updates
nano /etc/apt/apt.conf.d/50unattended-upgrades
```

---

## 📊 Monitoring and Maintenance

### Step 1: Log Management
```bash
# Create log directory
mkdir -p /opt/whatbot/logs

# Setup log rotation
nano /etc/logrotate.d/whatbot

# Configuration:
/opt/whatbot/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 whatbot whatbot
    postrotate
        pm2 reloadLogs
    endscript
}
```

### Step 2: Backup Strategy
```bash
# Create backup script
nano /opt/whatbot/scripts/backup.sh

#!/bin/bash
BACKUP_DIR="/opt/backups/whatbot"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
pg_dump whatbot_production > $BACKUP_DIR/db_$DATE.sql

# Backup application files
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /opt/whatbot

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

# Make executable
chmod +x /opt/whatbot/scripts/backup.sh

# Add to crontab
crontab -e
# Add: 0 2 * * * /opt/whatbot/scripts/backup.sh
```

### Step 3: Health Monitoring
```bash
# Create health check script
nano /opt/whatbot/scripts/health-check.sh

#!/bin/bash
# Check if WhatBot is running
if ! pm2 list | grep -q "whatbot"; then
    echo "WhatBot is down, restarting..."
    pm2 restart whatbot
    # Send notification (optional)
fi

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "Disk usage is high: ${DISK_USAGE}%"
fi

# Make executable
chmod +x /opt/whatbot/scripts/health-check.sh

# Add to crontab
crontab -e
# Add: */5 * * * * /opt/whatbot/scripts/health-check.sh
```

---

## 🚀 Performance Optimization

### Step 1: Node.js Optimization
```bash
# Edit PM2 configuration for better performance
nano ecosystem.config.js

# Add these settings:
module.exports = {
  apps: [{
    name: 'whatbot',
    script: 'server.js',
    instances: 'max',
    exec_mode: 'cluster',
    max_memory_restart: '1G',
    node_args: '--max-old-space-size=4096',
    env: {
      NODE_ENV: 'production'
    }
  }]
}
```

### Step 2: Database Optimization
```bash
# Edit PostgreSQL configuration
nano /etc/postgresql/*/main/postgresql.conf

# Recommended settings:
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100

# Restart PostgreSQL
systemctl restart postgresql
```

### Step 3: Nginx Optimization
```bash
# Edit Nginx configuration
nano /etc/nginx/nginx.conf

# Add to http block:
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

# Client body size for file uploads
client_max_body_size 50M;
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: Application Won't Start
```bash
# Check logs
pm2 logs whatbot

# Check environment variables
pm2 env whatbot

# Restart application
pm2 restart whatbot
```

#### Issue 2: Database Connection Errors
```bash
# Check PostgreSQL status
systemctl status postgresql

# Check connection
sudo -u postgres psql -d whatbot_production

# Check logs
tail -f /var/log/postgresql/postgresql-*.log
```

#### Issue 3: WhatsApp Connection Issues
```bash
# Check session status
curl http://localhost:41100/api/v1/status

# Restart WhatsApp session
curl -X POST http://localhost:41100/api/v1/init

# Check logs for errors
tail -f /opt/whatbot/logs/app.log
```

#### Issue 4: SSL Certificate Issues
```bash
# Check certificate status
certbot certificates

# Renew certificate manually
certbot renew

# Check Nginx configuration
nginx -t
```

---

## 📞 Support and Maintenance

### Regular Maintenance Tasks
```bash
# Weekly tasks
- Update system packages: apt update && apt upgrade
- Check disk space: df -h
- Review logs: tail -f /opt/whatbot/logs/app.log
- Test backups: restore from backup to test environment

# Monthly tasks
- Review security logs: journalctl -u ssh
- Update SSL certificates: certbot renew
- Performance review: check PM2 and database metrics
- Update WhatBot application: git pull && npm install
```

### Monitoring Tools
```bash
# Install monitoring tools
apt install -y htop iotop nethogs

# System monitoring
htop                    # Process monitoring
iotop                   # I/O monitoring
nethogs                 # Network monitoring
df -h                   # Disk usage
free -h                 # Memory usage
```

### Contact Information
- **Technical Support:** ben@techjamlabs.com
- **Phone:** +2348099999928
- **Documentation:** [Project Documentation](./README.md)
- **Issues:** Create GitHub issue or contact support

---

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] Cloud provider account created
- [ ] Domain name configured (optional)
- [ ] SSH keys generated
- [ ] WhatBot source code ready

### Server Setup
- [ ] VPS instance created
- [ ] SSH access configured
- [ ] System packages updated
- [ ] Node.js installed
- [ ] PostgreSQL installed
- [ ] PM2 installed
- [ ] Nginx installed

### Application Deployment
- [ ] WhatBot code deployed
- [ ] Environment variables configured
- [ ] Database created and configured
- [ ] Application started with PM2
- [ ] Nginx configured
- [ ] SSL certificate installed

### Security Configuration
- [ ] Firewall configured
- [ ] SSH security hardened
- [ ] Fail2ban installed
- [ ] Automatic updates configured
- [ ] Regular backups scheduled

### Testing
- [ ] Application accessible via domain
- [ ] WhatsApp connection working
- [ ] API endpoints responding
- [ ] File uploads working
- [ ] Database operations working

### Monitoring
- [ ] Health checks configured
- [ ] Log rotation setup
- [ ] Backup system tested
- [ ] Performance monitoring active

---

*This guide covers the essential steps for deploying WhatBot to cloud VPS providers. For specific provider issues or advanced configurations, refer to the provider's documentation or contact technical support.* 
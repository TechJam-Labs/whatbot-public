<!--
 * WhatBot v1.2.0
 * Location: docs\dev-guides\DEPLOYMENT_GUIDE.md
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

# 🚀 GOMED WhatsApp Bot - Deployment Guide

## 📋 Prerequisites

- VPS server with Ubuntu 20.04+ 
- SSH access to the server
- Domain name: `whatbot.gomed.ng`
- GitHub Personal Access Token: `[GITHUB_PERSONAL_ACCESS_TOKEN]`

---

## 🔧 Step 1: Local Git Setup

### 1.1 Initialize Git Repository
```bash
# Make sure you're in the project directory
cd /c/CloudDev/Active/gomed-whatbot

# Run the Git setup script
chmod +x setup-git.sh
./setup-git.sh
```

### 1.2 Verify Repository Creation
- Check: https://github.com/TechJam-Labs/gomed-whatbot
- Ensure it's private and contains all files

---

## 🌐 Step 2: DNS Configuration

### 2.1 Configure Domain DNS
Add these DNS records for `whatbot.gomed.ng`:

```
Type: A
Name: whatbot
Value: 173.249.59.234
TTL: 300
```

### 2.2 Verify DNS Propagation
```bash
# Check DNS propagation
nslookup whatbot.gomed.ng
dig whatbot.gomed.ng
```

---

## 🖥️ Step 3: VPS Server Setup

### 3.1 SSH to VPS Server
```bash
# Connect to your VPS
ssh benadenle@173.249.59.234 -p 2234
```

### 3.2 Update System
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y curl wget git unzip
```

### 3.3 Install Node.js 18.x
```bash
# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

### 3.4 Install PM2
```bash
# Install PM2 globally
sudo npm install -g pm2

# Verify PM2 installation
pm2 --version
```

### 3.5 Install Nginx
```bash
# Install nginx
sudo apt install -y nginx

# Start and enable nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 3.6 Install Certbot for SSL
```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx
```

---

## 📁 Step 4: Application Deployment

### 4.1 Create Application Directory
```bash
# Create application directory
sudo mkdir -p /var/www/whatbot
sudo chown benadenle:benadenle /var/www/whatbot

# Create log directory
sudo mkdir -p /var/log/gomed-whatbot
sudo chown benadenle:benadenle /var/log/gomed-whatbot

# Create uploads directory
sudo mkdir -p /var/www/whatbot/uploads
sudo chown benadenle:benadenle /var/www/whatbot/uploads

# Create tokens directory
sudo mkdir -p /var/www/whatbot/tokens
sudo chown benadenle:benadenle /var/www/whatbot/tokens
```

### 4.2 Clone Repository
```bash
# Navigate to application directory
cd /var/www/whatbot

# Clone the repository using your PAT
git clone https://[YOUR_GITHUB_TOKEN]@github.com/TechJam-Labs/gomed-whatbot.git gomed

# Navigate to the application
cd gomed
```

### 4.3 Install Dependencies
```bash
# Install npm dependencies
npm install
```

### 4.4 Create Environment File
```bash
# Create .env file
cat > .env << EOF
NODE_ENV=production
PORT=4501
BASE_URL=https://whatbot.gomed.ng
WHATSAPP_NUMBER=+2349157342656
COMPANY_NAME=GOMED HEALTHCARE
APP_TITLE=WhatsApp Bot - GOMED
INSTANCE_NAME=gomed
EOF
```

---

## ⚙️ Step 5: Nginx Configuration

### 5.1 Create Nginx Site Configuration
```bash
# Create nginx configuration
sudo tee /etc/nginx/sites-available/whatbot.gomed.ng << EOF
server {
    server_name whatbot.gomed.ng;

    location / {
        proxy_pass http://localhost:4501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    listen 80;
}
EOF
```

### 5.2 Enable Site
```bash
# Enable the site
sudo ln -sf /etc/nginx/sites-available/whatbot.gomed.ng /etc/nginx/sites-enabled/

# Remove default site
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

---

## 🚀 Step 6: PM2 Application Management

### 6.1 Start Application with PM2
```bash
# Navigate to application directory
cd /var/www/whatbot/gomed

# Start application with PM2
pm2 start ecosystem.config.js --env production

# Save PM2 configuration
pm2 save

# Setup PM2 startup script
pm2 startup
```

### 6.2 Verify Application Status
```bash
# Check PM2 status
pm2 status

# Check application logs
pm2 logs gomed-whatbot

# Check if application is running
curl http://localhost:4501/api/status
```

---

## 🔒 Step 7: SSL Certificate

### 7.1 Obtain SSL Certificate
```bash
# Get SSL certificate from Let's Encrypt
sudo certbot --nginx -d whatbot.gomed.ng

# Test certificate renewal
sudo certbot renew --dry-run
```

### 7.2 Verify HTTPS
```bash
# Test HTTPS access
curl -I https://whatbot.gomed.ng
```

---

## 📊 Step 8: Monitoring & Maintenance

### 8.1 PM2 Commands
```bash
# View application status
pm2 status

# View logs
pm2 logs gomed-whatbot

# Restart application
pm2 restart gomed-whatbot

# Stop application
pm2 stop gomed-whatbot

# Monitor resources
pm2 monit
```

### 8.2 Nginx Commands
```bash
# Check nginx status
sudo systemctl status nginx

# Reload nginx configuration
sudo systemctl reload nginx

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 8.3 Application Logs
```bash
# View application logs
tail -f /var/log/gomed-whatbot/combined.log
tail -f /var/log/gomed-whatbot/error.log
```

---

## 🔄 Step 9: Updates & Deployment

### 9.1 Update Application
```bash
# Navigate to application directory
cd /var/www/whatbot/gomed

# Pull latest changes
git pull origin main

# Install dependencies (if needed)
npm install

# Restart application
pm2 restart gomed-whatbot
```

### 9.2 Automated Deployment (Optional)
```bash
# Setup PM2 deployment
pm2 deploy ecosystem.config.js production setup
pm2 deploy ecosystem.config.js production
```

---

## 🛠️ Troubleshooting

### Common Issues:

#### 1. SSH Connection Failed
```bash
# Check SSH key setup
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
ssh-copy-id benadenle@173.249.59.234 -p 2234
```

#### 2. Application Not Starting
```bash
# Check logs
pm2 logs gomed-whatbot

# Check port availability
sudo netstat -tlnp | grep :4501

# Check Node.js version
node --version
```

#### 3. Nginx Issues
```bash
# Check nginx configuration
sudo nginx -t

# Check nginx status
sudo systemctl status nginx

# View nginx error logs
sudo tail -f /var/log/nginx/error.log
```

#### 4. SSL Certificate Issues
```bash
# Check certificate status
sudo certbot certificates

# Renew certificate manually
sudo certbot renew
```

---

## 📞 Support

For technical support:
- **Email**: support@techjamlabs.com
- **Documentation**: Check the README.md file
- **Logs**: Check `/var/log/gomed-whatbot/` directory

---

## ✅ Verification Checklist

- [ ] Git repository created and pushed
- [ ] DNS configured for whatbot.gomed.ng
- [ ] VPS server accessible via SSH
- [ ] Node.js 18.x installed
- [ ] PM2 installed globally
- [ ] Nginx installed and configured
- [ ] Application cloned and dependencies installed
- [ ] Environment file created
- [ ] PM2 application started successfully
- [ ] SSL certificate obtained
- [ ] Application accessible via HTTPS
- [ ] Logs being generated properly

**🎉 Deployment Complete!** Your GOMED WhatsApp Bot is now live at https://whatbot.gomed.ng 
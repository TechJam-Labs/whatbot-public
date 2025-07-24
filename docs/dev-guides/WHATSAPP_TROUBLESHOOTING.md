<!--
 * WhatBot v1.2.0
 * Location: docs\dev-guides\WHATSAPP_TROUBLESHOOTING.md
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

# WhatsApp Connection Troubleshooting Guide (Ubuntu/Linux)

## Common Issues and Solutions

### 1. WhatsApp Not Connected After Server Restart

**Symptoms:**
- Server starts but WhatsApp shows "Not Logged" or "disconnected"
- WAPI errors in logs
- QR code not appearing

**Solutions:**

#### Option A: Use the WhatsApp Manager (Recommended)
```bash
# Check current status
node whatsapp-manager.js status

# Force reconnection
node whatsapp-manager.js reconnect

# Or use the Linux shell script
./whatsapp-manager.sh status
./whatsapp-manager.sh reconnect
```

#### Option B: Manual Steps
1. **Stop the server** (Ctrl+C)
2. **Clear session files:**
   ```bash
   node whatsapp-manager.js clear
   ```
3. **Restart the server:**
   ```bash
   node server.js
   ```
4. **Scan the new QR code** when it appears

### 2. Session Expired or Invalid

**Symptoms:**
- "Session is older than 24 hours" message
- Previous session was disconnected
- Connection fails after long periods of inactivity

**Solutions:**
- The system now automatically detects expired sessions
- Use the reconnection endpoint: `POST /api/v1/reconnect`
- Or clear sessions manually and restart

### 3. Browser/Headless Mode Issues

**Symptoms:**
- Headless deprecation warnings
- Browser fails to start
- Puppeteer errors

**Solutions:**
- Updated to use `headless: 'new'` instead of deprecated `headless: true`
- Added better browser arguments for stability
- Increased timeouts to 60 seconds

### 4. WAPI Not Defined Errors

**Symptoms:**
- "WAPI is not defined" errors in logs
- WhatsApp Web API not loading properly

**Solutions:**
- This usually indicates WhatsApp Web page didn't load completely
- Try reconnection: `node whatsapp-manager.js reconnect`
- If persistent, clear sessions and restart

### 5. Network/Connection Issues

**Symptoms:**
- Timeout errors
- Connection refused
- Slow loading

**Solutions:**
- Check internet connection
- Ensure WhatsApp Web is accessible in your browser
- Try using a VPN if WhatsApp Web is blocked in your region

## Quick Fix Commands

### Check Status
```bash
node whatsapp-manager.js status
# or
./whatsapp-manager.sh status
```

### Force Reconnection
```bash
node whatsapp-manager.js reconnect
# or
./whatsapp-manager.sh reconnect
```

### Clear All Sessions and Restart
```bash
node whatsapp-manager.js clear
# Then restart your server
node server.js
# or with PM2
pm2 restart whatbot
```

### Force Server Restart
```bash
node whatsapp-manager.js restart
# or
pm2 restart whatbot
```

## Prevention Tips

### 1. Regular Monitoring
- Check status periodically: `node whatsapp-manager.js status` or `./whatsapp-manager.sh status`
- Monitor server logs: `pm2 logs whatbot` or `tail -f /var/log/whatbot/app.log`
- Set up log rotation for production environments

### 2. Automatic Reconnection
- The server now has automatic reconnection every 30 seconds
- Sessions are validated on startup
- PM2 will automatically restart the process if it crashes

### 3. Session Management
- Sessions are automatically cleaned up if older than 24 hours
- Invalid sessions are removed automatically
- Session files are stored in `./tokens/` directory

### 4. Browser Stability
- Updated browser arguments for better stability on Linux
- Increased timeouts to handle slow connections
- Optimized for headless operation on Ubuntu servers

## API Endpoints for Management

### Check Status
```http
GET /api/v1/status
```

### Force Reconnection
```http
POST /api/v1/reconnect
```

### Force Restart
```http
POST /api/v1/force-restart
```

## Log Analysis

### Good Connection Logs
```
✅ Successfully logged in to WhatsApp
✅ Chats available, connection established
✅ Session info saved
```

### Problem Indicators
```
❌ Not logged in, will need QR scan
❌ WAPI is not defined
❌ Session is older than 24 hours
⚠️ Previous session was disconnected
```

## Emergency Procedures

### Complete Reset
1. Stop the server: `pm2 stop whatbot` or `node server.js` (Ctrl+C)
2. Clear sessions: `node whatsapp-manager.js clear`
3. Delete the `tokens` folder manually if needed: `rm -rf ./tokens`
4. Restart server: `pm2 start server.js --name whatbot` or `node server.js`
5. Scan new QR code

### If Nothing Works
1. Check if WhatsApp Web works in your browser
2. Verify your phone has internet connection
3. Try logging out of WhatsApp Web on your phone
4. Clear browser cache and cookies
5. Restart your phone
6. Check system resources: `htop`, `df -h`, `free -h`
7. Check for system updates: `sudo apt update && sudo apt upgrade`
8. Try again

## Support

If you continue to have issues:
1. Check the server logs for specific error messages
2. Try the troubleshooting steps above
3. Ensure your WhatsApp account is active and not restricted
4. Verify your phone number is correct in the environment variables

## Environment Variables

Make sure these are set correctly in your `.env` file:
```
WHATSAPP_NUMBER=+2348064866332
COMPANY_NAME=GOMED
PORT=41100
```

## File Locations

- Session tokens: `./tokens/whatbot-session/`
- Session info: `./session-info.json`
- Logs: 
  - PM2 logs: `pm2 logs whatbot`
  - System logs: `/var/log/syslog`
  - Application logs: `/var/log/whatbot/app.log` (if configured)
- Process management: PM2 ecosystem file: `ecosystem.config.js` 
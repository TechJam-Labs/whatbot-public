<!--
 * WhatBot v1.2.0
 * Location: docs\dev-guides\TROUBLESHOOTING_GUIDE.md
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

# WhatBot Server Troubleshooting Guide

## 🚨 Current Issue Analysis

Based on your server logs, the main problems are:

### **1. Venom-bot Library Errors**
```
Error [ReferenceError]: require is not defined
Error [ReferenceError]: WAPI is not defined
```

### **2. WhatsApp Session Issues**
```
Error initializing client: Not Logged
```

### **3. Browser Compatibility Issues**
- Chrome version 138.0.7204.158 may have compatibility issues with venom-bot

## 🔧 Step-by-Step Fix Process

### **Step 1: Clean WhatsApp Session**
```bash
# Run the session cleanup tool
node fix-whatsapp-session.js
```

This will:
- ✅ Backup existing session data
- ✅ Clean corrupted session files
- ✅ Remove problematic tokens
- ✅ Create fresh tokens directory

### **Step 2: Test Server Connection**
```bash
# Test if server is accessible
node test-server-connection.js
```

This will verify:
- ✅ Server is running on port 41100
- ✅ API endpoints are accessible
- ✅ API key authentication works

### **Step 3: Restart Server with Clean Session**
```bash
# Stop current server (Ctrl+C)
# Then restart
npm start
```

### **Step 4: Monitor Server Startup**
Watch for these success indicators:
```
✅ Connected to PostgreSQL database
✅ API Key Manager initialized
✅ Database connected successfully
✅ Loaded X messages from database
✅ Loaded X contacts into global storage
```

### **Step 5: Handle QR Code Authentication**
When the server starts:
1. Look for QR code generation
2. Scan QR code with your WhatsApp
3. Wait for connection confirmation

## 🛠️ Alternative Solutions

### **Solution A: Update Venom-bot**
```bash
# Update to latest version
npm update venom-bot

# Or install specific version
npm install venom-bot@latest
```

### **Solution B: Chrome Version Fix**
```bash
# Check Chrome version
google-chrome --version

# If using Chrome 138+, try downgrading or using Chromium
npm install chromium
```

### **Solution C: Environment Variables**
Create/update `.env` file:
```env
PORT=41100
WHATSAPP_NUMBER=+2348064866332
COMPANY_NAME=GOMED
NODE_ENV=development
CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
```

### **Solution D: Database Reset**
```bash
# If database issues persist
node src/utils/setup-database.js
```

## 🔍 Diagnostic Commands

### **Check Server Status**
```bash
# Test basic connectivity
curl http://localhost:41100/api/v1/status

# Test API key
curl -H "X-API-Key: 54ba6cf299da17ad09dd1f169e2859d10467050d64ac5099642fe4c89174fd31" \
     http://localhost:41100/api/v1/auth/status
```

### **Check Process Status**
```bash
# Windows
netstat -ano | findstr :41100
tasklist | findstr node

# Linux/Mac
lsof -i :41100
ps aux | grep node
```

### **Check File Permissions**
```bash
# Ensure proper permissions
ls -la tokens/
ls -la *.json
```

## 📊 Expected Server Behavior

### **Normal Startup Sequence:**
```
🔧 Environment Variables Debug:
  WHATSAPP_NUMBER from env: +2348064866332
  WHATSAPP_NUMBER final: +2348064866332
  COMPANY_NAME from env: GOMED
  COMPANY_NAME final: GOMED
  PORT from env: 41100
  PORT final: 41100

Server running on http://127.0.0.1:41100
✅ Connected to PostgreSQL database
✅ API Key Manager initialized
✅ Database connected successfully
✅ Loaded X messages from database
✅ Loaded X contacts into global storage

🌐 Initializing browser...
✅ Browser successfully opened
📱 Initializing WhatsApp...
✅ WhatsApp page loaded successfully
⏳ Waiting for WhatsApp login...
✅ WhatsApp connected successfully
```

### **QR Code Process:**
```
📱 QR Code generated
🔗 Scan with WhatsApp: [QR Code Display]
⏳ Waiting for authentication...
✅ WhatsApp authenticated successfully
```

## 🚨 Common Error Solutions

### **Error: "require is not defined"**
- **Cause**: Venom-bot browser context issue
- **Solution**: Clean session and restart

### **Error: "WAPI is not defined"**
- **Cause**: WhatsApp Web API not loaded
- **Solution**: Wait longer for page load or restart

### **Error: "Not Logged"**
- **Cause**: Session expired or corrupted
- **Solution**: Clear session and re-authenticate

### **Error: "ECONNREFUSED"**
- **Cause**: Server not running
- **Solution**: Start server with `npm start`

### **Error: "ETIMEDOUT"**
- **Cause**: Server overloaded or network issues
- **Solution**: Increase timeout or check network

## 📋 Testing Checklist

### **Before Running API Tests:**
- [ ] Server starts without errors
- [ ] WhatsApp connects successfully
- [ ] API endpoints respond (test with connection script)
- [ ] Database connection is stable
- [ ] No venom-bot errors in logs

### **API Test Prerequisites:**
- [ ] Server running on port 41100
- [ ] WhatsApp authenticated
- [ ] API key working
- [ ] Database accessible
- [ ] No pending errors

## 🎯 Quick Fix Commands

### **Complete Reset:**
```bash
# 1. Stop server
# 2. Clean session
node fix-whatsapp-session.js

# 3. Restart server
npm start

# 4. Test connection
node test-server-connection.js

# 5. Run comprehensive test
node test-comprehensive-api.js
```

### **Emergency Reset:**
```bash
# Delete all session data
rm -rf tokens/
rm -f *.json

# Restart fresh
npm start
```

## 📞 Support Information

### **Log Files to Check:**
- `logs/` directory
- Console output
- Browser developer tools
- Database logs

### **Key Configuration Files:**
- `.env` - Environment variables
- `package.json` - Dependencies
- `server.js` - Main server file
- `src/utils/database.js` - Database configuration

### **Contact Information:**
- Check server logs for detailed error messages
- Verify all environment variables are set
- Ensure database is accessible
- Confirm WhatsApp number is correct

## 🎉 Success Indicators

When everything is working correctly, you should see:
- ✅ Server running on port 41100
- ✅ WhatsApp connected and authenticated
- ✅ API endpoints responding
- ✅ Database operations successful
- ✅ No venom-bot errors
- ✅ QR code process completed

Once these are confirmed, you can safely run the comprehensive API tests! 
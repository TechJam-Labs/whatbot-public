<!--
 * WhatBot v1.2.0
 * Location: docs\dev-guides\SCHEDULING_GUIDE.md
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

# 📅 Safe Broadcasting Guide for 4,000 Contacts

## 🛡️ Anti-Ban Strategy Overview

**The Golden Rules:**
1. **NEVER send all 4,000 at once** - Guaranteed ban
2. **Spread over multiple days/weeks** - Build trust gradually  
3. **Use safe sending hours** - 9 AM to 5 PM only
4. **Mimic human behavior** - Random delays, realistic patterns
5. **Monitor and adjust** - Watch for delivery issues

---

## 🚨 Recommended Approach for 4,000 Contacts

### **Option 1: Ultra-Safe (RECOMMENDED)**
**Timeline:** 20 days  
**Account Type:** Regular  
**Daily Limit:** 200 messages  
**Risk Level:** 🟢 Very Low

```bash
# API Call Example
curl -X POST http://localhost:4501/api/schedule-broadcast \
  -F "phones=[\"08099999928\", \"08088888888\", ...]" \
  -F "media=@your-image.jpg" \
  -F "caption=Your message here" \
  -F "scheduleType=spread" \
  -F "accountType=regular"
```

**Result:** 4,000 contacts spread over 20 days (200/day)

---

### **Option 2: Business Account (Faster)**
**Timeline:** 8 days  
**Account Type:** Business (Verified)  
**Daily Limit:** 500 messages  
**Risk Level:** 🟡 Low-Medium

```bash
curl -X POST http://localhost:4501/api/schedule-broadcast \
  -F "phones=[...]" \
  -F "media=@your-video.mp4" \
  -F "caption=Business announcement" \
  -F "scheduleType=spread" \
  -F "accountType=business"
```

**Result:** 4,000 contacts spread over 8 days (500/day)

---

### **Option 3: Multi-Account Distribution (SAFEST)**
**Timeline:** 4 days  
**Accounts Needed:** 5 WhatsApp Business accounts  
**Per Account:** 800 contacts  
**Risk Level:** 🟢 Very Low

**Split your 4,000 contacts across 5 accounts:**
- Account 1: Contacts 1-800
- Account 2: Contacts 801-1600  
- Account 3: Contacts 1601-2400
- Account 4: Contacts 2401-3200
- Account 5: Contacts 3201-4000

---

## 📊 Account Type Limits

| Account Type | Daily Limit | Hourly Limit | Best For |
|-------------|-------------|--------------|----------|
| **New** (< 30 days) | 50 | 5 | Testing only |
| **Regular** (30-90 days) | 200 | 15 | Small businesses |
| **Trusted** (90+ days) | 500 | 25 | Growing businesses |
| **Business** (Verified) | 1000 | 50 | Large campaigns |

---

## 🕐 Safe Sending Schedule

### **Daily Pattern:**
- **9:00 AM - 5:00 PM**: Safe sending window
- **5:00 PM - 9:00 AM**: NO SENDING (High risk)
- **Weekends**: Reduced activity (optional)

### **Batch Timing:**
- **Between Messages**: 5-12 seconds (human-like)
- **Between Batches**: 1-2 hours  
- **Between Days**: 24 hours

---

## 🎯 Step-by-Step Implementation

### **Step 1: Prepare Your Contact List**
```javascript
// Format: One phone per line with country code
const contacts = [
  "2348099999928",
  "2348088888888", 
  "2348077777777",
  // ... 4,000 total
];
```

### **Step 2: Choose Your Media**
- **Images**: JPG, PNG (under 5MB)
- **Videos**: MP4 (under 16MB)  
- **Documents**: PDF (under 100MB)

### **Step 3: Schedule the Broadcast**
```bash
# Use the web interface or API
POST /api/schedule-broadcast
{
  "phones": [...],
  "scheduleType": "spread",
  "accountType": "business", 
  "startDate": "2024-01-15T09:00:00Z"
}
```

### **Step 4: Monitor Progress**
```bash
# Check status
GET /api/scheduled-broadcasts

# Check specific job
GET /api/broadcast-status/:jobId
```

---

## 🚨 Warning Signs to Watch For

### **Stop Immediately If:**
- ❌ Messages marked as "undelivered" > 20%
- ❌ Account receives warnings from WhatsApp
- ❌ Contacts reporting as spam
- ❌ Delivery delays increasing significantly

### **Adjust Strategy:**
- 📉 Reduce daily limits by 50%
- ⏱️ Increase delays between messages
- 📅 Spread over more days
- 🔄 Switch to different account

---

## 💡 Pro Tips for Success

### **Before Starting:**
1. **Test with small batch** (50-100 contacts)
2. **Verify all phone numbers** are active
3. **Check media file quality** and size
4. **Prepare engaging caption** with clear CTA

### **During Campaign:**
1. **Monitor delivery rates** hourly
2. **Keep track of responses** and opt-outs
3. **Be ready to pause** if issues arise
4. **Document what works** for future campaigns

### **Best Practices:**
- 🎯 **Target engaged audiences** (higher success rate)
- 📝 **Personalize when possible** 
- 🕒 **Send during business hours** in recipient's timezone
- 📊 **Track metrics** for optimization

---

## 🔧 API Endpoints Quick Reference

```bash
# Schedule broadcast
POST /api/schedule-broadcast

# Check all scheduled jobs  
GET /api/scheduled-broadcasts

# Check specific job status
GET /api/broadcast-status/:jobId

# Cancel scheduled job
DELETE /api/scheduled-broadcasts/:jobId
```

---

## 📈 Expected Results

### **Ultra-Safe Method (20 days):**
- **Success Rate**: 85-95%
- **Ban Risk**: < 1%
- **Time Investment**: Low (automated)

### **Business Account (8 days):**
- **Success Rate**: 80-90%  
- **Ban Risk**: 5-10%
- **Time Investment**: Medium monitoring

### **Multi-Account (4 days):**
- **Success Rate**: 90-98%
- **Ban Risk**: < 2%
- **Time Investment**: High setup, low maintenance

---

**Remember**: It's better to take 20 days to successfully deliver to 4,000 contacts than to get banned trying to do it in 1 day! 🎯 
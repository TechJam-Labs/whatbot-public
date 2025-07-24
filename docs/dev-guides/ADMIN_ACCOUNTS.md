<!--
 * WhatBot v1.2.0
 * Location: docs\dev-guides\ADMIN_ACCOUNTS.md
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

# WhatBot Admin Accounts

## 🔐 **Active Admin Users**

### 1. System Administrator
- **Username:** `admin`
- **Email:** `admin@whatbot.com`
- **Full Name:** System Administrator
- **Role:** admin
- **Password:** `admin123` ⚠️ **CHANGE THIS IMMEDIATELY!**
- **Status:** Active

### 2. Eric Baumgardner
- **Username:** `eric.baumgardner`
- **Email:** `eric.baumgardner@finnblue.net`
- **Full Name:** Eric Baumgardner
- **Role:** admin
- **Password:** `Adm!)90(`
- **Status:** Active

## 🚨 **Security Recommendations**

1. **Change Default Passwords:**
   - The `admin` account uses a default password that should be changed immediately
   - Eric's password is secure but should be changed periodically

2. **Password Policy:**
   - Use strong passwords (minimum 8 characters)
   - Include uppercase, lowercase, numbers, and special characters
   - Change passwords every 90 days

3. **Access Control:**
   - Only grant admin access to trusted personnel
   - Monitor admin account usage through audit logs
   - Use API keys for programmatic access

## 🔧 **Account Management**

### Add New Admin User
```bash
# Connect to PostgreSQL
psql -U desire_adenle -d whatbot_tjl22072025

# Insert new admin user (replace with actual values)
INSERT INTO users (username, email, password_hash, full_name, role, is_active)
VALUES ('newadmin', 'newadmin@company.com', 'hashed_password', 'New Admin', 'admin', true);
```

### Change Password
```bash
# Use the password change endpoint (when implemented)
POST /api/v1/auth/change-password
{
  "currentPassword": "old_password",
  "newPassword": "new_secure_password"
}
```

### List All Users
```bash
node src/utils/add-eric-account.js list
```

## 📊 **Database Schema**

The admin users are stored in the `users` table with the following structure:

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(20) DEFAULT 'agent' CHECK (role IN ('admin', 'developer', 'agent')),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id)
);
```

## 🔍 **Audit Trail**

All admin actions are logged in the `audit_trails` table:

```sql
SELECT * FROM audit_trails 
WHERE user_id IN (SELECT id FROM users WHERE role = 'admin')
ORDER BY created_at DESC;
```

## 🛡️ **Security Features**

- **Password Hashing:** All passwords are hashed using bcrypt with 12 rounds
- **JWT Authentication:** Secure token-based authentication
- **Role-Based Access:** Granular permissions based on user roles
- **API Key Management:** Secure API access with rate limiting
- **Audit Logging:** Complete audit trail of all admin actions
- **Session Management:** Secure session handling with expiration

## 📞 **Support**

For account management issues, contact the system administrator or refer to the PostgreSQL setup guide.

---

**Last Updated:** July 22, 2025  
**Database:** whatbot_tjl22072025  
**Environment:** Production 
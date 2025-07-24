<!--
 * WhatBot v1.2.0
 * Location: docs\dev-guides\POSTGRES_SETUP_GUIDE.md
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

# PostgreSQL Setup Guide for WhatBot

## 🚀 Quick Start

This guide will help you set up PostgreSQL for your WhatBot application with the specific database name and user requirements.

## 📋 Prerequisites

### 1. PostgreSQL Installation

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**CentOS/RHEL:**
```bash
sudo yum install postgresql postgresql-server
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Windows:**
- Download from: https://www.postgresql.org/download/windows/
- Install with default settings

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

### 2. Node.js Dependencies

```bash
npm install pg bcrypt jsonwebtoken
```

## 🔧 Configuration

### 1. Environment Setup

Copy the template and configure your environment:

```bash
cp config.template.env .env
```

Edit `.env` file with your PostgreSQL credentials:

```env
# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=whatbot_tjl22072025
DB_USER=desire_adenle
DB_PASSWORD=your_secure_password_here
ROOT_DB_PASSWORD=your_postgres_root_password

# Admin User Configuration
ADMIN_PASSWORD=admin123

# JWT Secret (generate a secure one)
JWT_SECRET=your_jwt_secret_here
```

### 2. PostgreSQL Root Password

If you haven't set a root password for PostgreSQL:

```bash
# Connect as postgres user
sudo -u postgres psql

# Set password for postgres user
ALTER USER postgres PASSWORD 'your_postgres_root_password';

# Exit
\q
```

## 🚀 Database Setup

### Option 1: Automated Setup (Recommended)

Run the automated setup script:

```bash
node setup-postgres.js
```

This will:
- Create database `whatbot_tjl22072025`
- Create user `desire_adenle`
- Create all tables and indexes
- Insert default data
- Test the connection

### Option 2: Manual Setup

If you prefer manual setup:

```bash
# Step 1: Setup database and user
node src/utils/postgres-setup.js

# Step 2: Create schema and tables
node src/utils/postgres-schema.js
```

## 📊 Database Schema

The setup creates the following tables:

### Authentication & Users
- `users` - User accounts with roles (admin, developer, agent)
- `user_sessions` - JWT session management
- `user_permissions` - Granular access control

### API Management
- `api_keys` - API key storage and management
- `api_key_logs` - API usage tracking

### Core Application
- `messages` - WhatsApp messages with full-text search
- `contacts` - Contact management with JSONB tags
- `contact_groups` - Contact organization

### Auto-Replies
- `auto_replies` - Auto-reply rules with JSONB keywords
- `auto_reply_logs` - Usage tracking and analytics

### ML Data Pipeline
- `message_analytics` - Text analysis and ML features
- `conversation_flows` - Conversation tracking
- `sentiment_analysis` - Sentiment tracking
- `ml_model_performance` - Model performance metrics

### System & Audit
- `system_logs` - Application logging
- `audit_trails` - User action tracking
- `api_usage_metrics` - API performance metrics

## 🔐 Default Access

After setup, you'll have:

**Admin User:**
- Username: `admin`
- Password: `admin123`
- Role: `admin`

**⚠️ IMPORTANT:** Change the admin password immediately after setup!

## 🧪 Testing the Setup

### 1. Connection Test

```bash
# Test database connection
node -e "
const db = require('./src/utils/postgres-database');
db.connect()
  .then(() => console.log('✅ Connection successful'))
  .catch(err => console.error('❌ Connection failed:', err))
  .finally(() => db.disconnect());
"
```

### 2. Basic Operations Test

```bash
# Test basic CRUD operations
node -e "
const db = require('./src/utils/postgres-database');
async function test() {
  await db.connect();
  
  // Test user creation
  const user = await db.createUser({
    username: 'testuser',
    email: 'test@example.com',
    password_hash: 'hashed_password',
    full_name: 'Test User',
    role: 'agent'
  });
  console.log('✅ User created:', user.username);
  
  await db.disconnect();
}
test().catch(console.error);
"
```

## 🔧 Troubleshooting

### Common Issues

**1. Connection Refused**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start if not running
sudo systemctl start postgresql
```

**2. Authentication Failed**
```bash
# Check pg_hba.conf configuration
sudo nano /etc/postgresql/*/main/pg_hba.conf

# Ensure local connections are allowed:
# local   all             postgres                                peer
# local   all             all                                     md5
```

**3. Permission Denied**
```bash
# Ensure postgres user can create databases
sudo -u postgres psql -c \"ALTER USER postgres CREATEDB;\"
```

**4. Database Already Exists**
```bash
# Drop and recreate if needed
sudo -u postgres psql -c \"DROP DATABASE IF EXISTS whatbot_tjl22072025;\"
```

### Logs and Debugging

**PostgreSQL Logs:**
```bash
# Ubuntu/Debian
sudo tail -f /var/log/postgresql/postgresql-*.log

# CentOS/RHEL
sudo tail -f /var/log/postgresql/postgresql-*.log
```

**Application Logs:**
```bash
# Check for database connection errors
grep -i "postgres\|database" logs/*.log
```

## 📈 Performance Optimization

### 1. PostgreSQL Configuration

Edit `/etc/postgresql/*/main/postgresql.conf`:

```conf
# Memory settings
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB

# Connection settings
max_connections = 100

# Logging
log_statement = 'all'
log_duration = on
```

### 2. Index Optimization

The setup creates optimized indexes for:
- Full-text search on messages
- JSONB queries on contacts and auto-replies
- Time-based queries on logs
- Foreign key relationships

### 3. Connection Pooling

The application uses connection pooling with:
- Max connections: 20
- Idle timeout: 30 seconds
- Connection timeout: 2 seconds

## 🔒 Security Considerations

### 1. Password Security
- Use strong passwords for all database users
- Change default admin password immediately
- Use environment variables for sensitive data

### 2. Network Security
- Configure firewall to restrict database access
- Use SSL connections in production
- Implement IP whitelisting for API keys

### 3. Data Encryption
- Enable encryption at rest
- Use SSL/TLS for connections
- Encrypt sensitive data in application

## 📊 Monitoring

### 1. Database Health

```sql
-- Check table sizes
SELECT 
  schemaname,
  tablename,
  attname,
  n_distinct,
  correlation
FROM pg_stats
WHERE schemaname = 'public'
ORDER BY tablename, attname;

-- Check index usage
SELECT 
  schemaname,
  tablename,
  indexname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

### 2. Performance Metrics

```sql
-- Slow queries
SELECT 
  query,
  calls,
  total_time,
  mean_time,
  rows
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Connection stats
SELECT 
  datname,
  numbackends,
  xact_commit,
  xact_rollback
FROM pg_stat_database;
```

## 🚀 Next Steps

After successful setup:

1. **Update Application Code** - Replace MySQL with PostgreSQL
2. **Test All Features** - Verify messages, contacts, auto-replies work
3. **Migrate Existing Data** - If migrating from file-based storage
4. **Set Up Monitoring** - Configure alerts and dashboards
5. **Backup Strategy** - Implement automated backups
6. **Security Hardening** - Apply security best practices

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review PostgreSQL logs for errors
3. Verify environment variables are correct
4. Ensure PostgreSQL is running and accessible
5. Check user permissions and database privileges

---

**🎉 Congratulations!** Your PostgreSQL database is now set up and ready for the WhatBot application with authentication, auto-replies, and ML capabilities. 
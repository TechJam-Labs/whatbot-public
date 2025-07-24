<!--
 * WhatBot v1.2.0
 * Location: docs\dev-guides\DATABASE_MIGRATION.md
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

# Database Migration Guide

This guide will help you migrate from the current file-based storage system to a robust MySQL database system for both messages and contacts.

## 🎯 Why Migrate to Database?

### Current Issues:
- **Messages**: Lost on server restart, limited to 1,000 in memory
- **Contacts**: File-based storage with no concurrent access safety
- **No backup/recovery**: Manual backup required
- **Limited scalability**: Can't handle large datasets efficiently

### Database Benefits:
- ✅ **Persistent storage** - Data survives restarts
- ✅ **Concurrent access** - Multiple users can safely access simultaneously
- ✅ **ACID transactions** - Data integrity guaranteed
- ✅ **Automated backups** - Point-in-time recovery
- ✅ **Complex queries** - Advanced filtering and search
- ✅ **Scalability** - Handle millions of records
- ✅ **Performance** - Indexed queries, optimized storage

## 🚀 Migration Steps

### 1. Database Setup

First, ensure MySQL is installed and running:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server

# CentOS/RHEL
sudo yum install mysql-server
sudo systemctl start mysqld
sudo systemctl enable mysqld
```

### 2. Configure Environment

Update your `.env` file with database credentials:

```bash
# Copy template
cp config.template.env .env

# Edit .env file
nano .env
```

Add these database settings:

```env
# Database Configuration (Required for persistent storage)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=whatbot
DB_USER=whatbot_user
DB_PASSWORD=your_secure_password
ROOT_DB_PASSWORD=your_root_mysql_password
```

### 3. Setup Database

Run the database setup script:

```bash
# Setup database and user
node src/utils/setup-database.js
```

This will:
- Create the `whatbot` database
- Create the `whatbot_user` with proper privileges
- Set up UTF8MB4 character encoding

### 4. Run Migration

Migrate your existing data to the database:

```bash
# Run full migration (contacts + messages)
node src/utils/migrate-to-database.js
```

This will:
- Create backups of your current data
- Migrate contacts from `contacts.json`
- Migrate messages from memory (if any)
- Preserve all existing data

### 5. Update Server Code

The server code has been updated to use the database. The migration will:

- Replace in-memory message storage with database storage
- Replace file-based contact storage with database storage
- Maintain all existing API endpoints
- Add new database-powered features

## 📊 Database Schema

### Messages Table
```sql
CREATE TABLE messages (
  id VARCHAR(255) PRIMARY KEY,
  from_number VARCHAR(50) NOT NULL,
  to_number VARCHAR(50) NOT NULL,
  type VARCHAR(20) NOT NULL,
  body TEXT,
  timestamp BIGINT NOT NULL,
  is_group BOOLEAN DEFAULT FALSE,
  chat_id VARCHAR(100) NOT NULL,
  sender_id VARCHAR(100),
  sender_name VARCHAR(255),
  sender_number VARCHAR(50),
  media_mimetype VARCHAR(100),
  media_filename VARCHAR(255),
  media_data LONGTEXT,
  media_size INT,
  is_read BOOLEAN DEFAULT FALSE,
  read_at TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_chat_id (chat_id),
  INDEX idx_timestamp (timestamp),
  INDEX idx_from_number (from_number),
  INDEX idx_type (type)
);
```

### Contacts Table
```sql
CREATE TABLE contacts (
  id VARCHAR(255) PRIMARY KEY,
  phone VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(255),
  email VARCHAR(255),
  group_name VARCHAR(100) NOT NULL,
  tags JSON,
  notes TEXT,
  reg_no VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_phone (phone),
  INDEX idx_group (group_name),
  INDEX idx_email (email)
);
```

### Contact Groups Table
```sql
CREATE TABLE contact_groups (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  contact_count INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_name (name)
);
```

## 🔧 New Features

### Enhanced Message Storage
- **Unlimited messages** - No more 1,000 message limit
- **Persistent storage** - Messages survive server restarts
- **Advanced search** - Search by content, sender, type
- **Read status tracking** - Mark messages as read/unread
- **Media storage** - Store media files in database

### Enhanced Contact Management
- **Concurrent access** - Multiple users can safely edit contacts
- **Transaction safety** - No data corruption from concurrent writes
- **Advanced filtering** - Complex queries and searches
- **Automatic group counting** - Real-time contact counts per group
- **Audit trail** - Track when contacts were added/modified

### Performance Improvements
- **Indexed queries** - Fast searches and filtering
- **Connection pooling** - Efficient database connections
- **Optimized storage** - Better data compression
- **Query optimization** - Database-level query optimization

## 🛡️ Backup & Recovery

### Automated Backups
Set up automated database backups:

```bash
# Create backup script
cat > /usr/local/bin/backup-whatbot.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/whatbot"
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u whatbot_user -p whatbot > $BACKUP_DIR/whatbot_$DATE.sql
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
EOF

chmod +x /usr/local/bin/backup-whatbot.sh

# Add to crontab (daily backup at 2 AM)
echo "0 2 * * * /usr/local/bin/backup-whatbot.sh" | crontab -
```

### Manual Backup
```bash
# Backup database
mysqldump -u whatbot_user -p whatbot > whatbot_backup.sql

# Restore database
mysql -u whatbot_user -p whatbot < whatbot_backup.sql
```

## 🔍 Monitoring & Maintenance

### Database Monitoring
```sql
-- Check table sizes
SELECT 
  table_name,
  ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = 'whatbot';

-- Check message count
SELECT COUNT(*) as total_messages FROM messages;

-- Check contact count
SELECT COUNT(*) as total_contacts FROM contacts;

-- Check recent activity
SELECT 
  DATE(created_at) as date,
  COUNT(*) as messages
FROM messages 
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

### Performance Optimization
```sql
-- Analyze table performance
ANALYZE TABLE messages, contacts, contact_groups;

-- Optimize tables
OPTIMIZE TABLE messages, contacts, contact_groups;
```

## 🚨 Troubleshooting

### Common Issues

**1. Database Connection Failed**
```bash
# Check MySQL service
sudo systemctl status mysql

# Check credentials
mysql -u whatbot_user -p -h localhost

# Check database exists
SHOW DATABASES;
```

**2. Migration Errors**
```bash
# Check migration logs
tail -f /var/log/whatbot/migration.log

# Re-run migration with verbose logging
DEBUG=* node src/utils/migrate-to-database.js
```

**3. Performance Issues**
```bash
# Check database connections
SHOW PROCESSLIST;

# Check slow queries
SHOW VARIABLES LIKE 'slow_query_log';
```

## 📈 Scaling Considerations

### For High Volume Usage
- **Connection pooling**: Already implemented
- **Read replicas**: For read-heavy workloads
- **Sharding**: For very large datasets
- **Caching**: Redis for frequently accessed data

### For Multiple Instances
- **Shared database**: Multiple bot instances can share the same database
- **Instance isolation**: Use different database schemas per instance
- **Load balancing**: Distribute load across multiple database servers

## ✅ Migration Checklist

- [ ] MySQL server installed and running
- [ ] Database credentials configured in `.env`
- [ ] Database setup script executed successfully
- [ ] Migration script completed without errors
- [ ] Backup of original data created
- [ ] Server restarted with new database code
- [ ] API endpoints tested and working
- [ ] Performance monitoring configured
- [ ] Backup schedule established

## 🎉 Post-Migration

After successful migration:

1. **Test all functionality** - Ensure messages and contacts work correctly
2. **Monitor performance** - Check database performance and optimize if needed
3. **Set up monitoring** - Configure alerts for database issues
4. **Document changes** - Update team documentation
5. **Train users** - Inform users about new features and capabilities

## 📞 Support

If you encounter issues during migration:

1. Check the troubleshooting section above
2. Review migration logs for specific errors
3. Ensure all prerequisites are met
4. Contact support with detailed error messages

---

**Note**: This migration is backward compatible. Your existing API endpoints will continue to work, but now with enhanced database-powered features. 
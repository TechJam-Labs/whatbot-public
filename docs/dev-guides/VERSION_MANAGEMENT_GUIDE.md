/**
 * WhatBot v1.2.0
 * Location: docs/dev-guides/VERSION_MANAGEMENT_GUIDE.md
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

# WhatBot Version Management Guide

## 🎯 Overview

This guide covers the comprehensive version management system for WhatBot, including API versioning, update procedures, test environments, and best practices for managing multiple versions.

## 📋 Version System Architecture

### Semantic Versioning

WhatBot follows semantic versioning (SemVer) with the format `MAJOR.MINOR.PATCH`:

- **MAJOR**: Breaking changes, new API versions
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### API Versioning Strategy

#### Current Implementation
- **Production**: `/api/v1/` (current stable)
- **Test Environments**: `/api/v2/`, `/api/v3/`, etc.
- **Version Info**: `/api/version` (returns current version)

#### Version Endpoint Response
```json
{
  "version": "v2.0.0",
  "apiVersion": "v2",
  "timestamp": "2025-06-21T10:30:00.000Z"
}
```

### Port Management

| Version | Port | Environment | Purpose |
|---------|------|-------------|---------|
| v1.0.0 | 41100 | Production | Live system |
| v2.0.0 | 41220 | Test | New features testing |
| v3.0.0 | 41230 | Test | Future version testing |
| v4.0.0 | 41240 | Test | Development testing |

---

## 🔄 Update Process

### Prerequisites

1. **Root Access**: Update script requires sudo privileges
2. **GitHub PAT**: Personal Access Token for repository access
3. **Backup**: Automatic backup creation before updates
4. **Test Environment**: Isolated testing environment

### Step-by-Step Update Process

#### 1. Version Discovery
```bash
# Run update script
sudo python3 whatbot-update.py

# Script automatically:
# - Checks current version
# - Fetches available versions from repository
# - Displays version list for selection
```

#### 2. Test Environment Creation
```bash
# Automatic process:
# - Creates isolated directory: /opt/whatbot-test/v2.0.0/
# - Sets up separate database: whatbot_test_v2_0_0
# - Configures test service: whatbot-test-v2-0-0.service
# - Updates API routes to /api/v2/
```

#### 3. API Route Updates
The update script automatically modifies `server.js`:

```javascript
// Before update
app.use('/api/v1', apiRoutes);

// After update (v2.0.0)
app.use('/api/v2', apiRoutes);

// Version information added
app.locals.version = 'v2.0.0';
app.locals.apiVersion = 'v2';

app.get('/api/version', (req, res) => {
    res.json({
        version: 'v2.0.0',
        apiVersion: 'v2',
        timestamp: new Date().toISOString()
    });
});
```

#### 4. Testing Phase
```bash
# Test endpoints
curl http://localhost:41220/api/version
curl http://localhost:41220/api/v2/status
curl http://localhost:41220/api/v2/health

# Run automated tests
npm test  # If available
```

#### 5. Production Update
```bash
# User choice: Update production?
# Options:
# - y: Update production immediately
# - n: Cancel update
# - test: Continue testing, update later
```

#### 6. Rollback Support
```bash
# Automatic rollback if update fails:
# - Restore from backup
# - Restart production service
# - Maintain system stability
```

---

## 🛠️ Manual Update Procedures

### Creating a New Version

#### 1. Repository Tagging
```bash
# Create new version tag
git tag v2.0.0
git push origin v2.0.0

# Or create annotated tag
git tag -a v2.0.0 -m "Release version 2.0.0"
git push origin v2.0.0
```

#### 2. API Route Updates
```javascript
// Update server.js manually
const version = process.env.API_VERSION || 'v1';
const apiVersion = version.replace('v', '');

// Version-specific routes
app.use(`/api/v${apiVersion}`, apiRoutes);

// Version endpoint
app.get('/api/version', (req, res) => {
    res.json({
        version: process.env.API_VERSION || 'v1.0.0',
        apiVersion: `v${apiVersion}`,
        timestamp: new Date().toISOString()
    });
});
```

#### 3. Environment Configuration
```bash
# Update .env file
API_VERSION=v2.0.0
APP_TITLE=WhatBot v2.0.0
```

### Manual Test Environment Setup

#### 1. Create Test Directory
```bash
mkdir -p /opt/whatbot-test/v2.0.0
cd /opt/whatbot-test/v2.0.0
```

#### 2. Clone and Setup
```bash
# Clone repository
git clone https://YOUR_PAT@github.com/TechJam-Labs/whatbot-master-copy.git .
git checkout v2.0.0

# Install dependencies
npm install
```

#### 3. Create Test Environment
```bash
# Create .env for test
cat > .env << EOF
PORT=41220
NODE_ENV=test
API_VERSION=v2.0.0
DB_NAME=whatbot_test_v2_0_0
DB_USER=whatbot_test_user
DB_PASSWORD=test_password_$(date +%s)
EOF
```

#### 4. Setup Database
```bash
# Create test database
sudo -u postgres psql -c "CREATE DATABASE whatbot_test_v2_0_0;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE whatbot_test_v2_0_0 TO whatbot_test_user;"
```

#### 5. Create Service
```bash
# Create systemd service
sudo tee /etc/systemd/system/whatbot-test-v2-0-0.service << EOF
[Unit]
Description=WhatBot Test Environment - v2.0.0
After=network.target postgresql.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/whatbot-test/v2.0.0
ExecStart=/usr/bin/node server.js
Restart=always
Environment=NODE_ENV=test
Environment=PORT=41220

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable whatbot-test-v2-0-0.service
sudo systemctl start whatbot-test-v2-0-0.service
```

---

## 🔧 Management Commands

### Version Information
```bash
# Check current production version
curl http://localhost:41100/api/version

# Check test version
curl http://localhost:41220/api/version

# List all running services
systemctl list-units --type=service | grep whatbot
```

### Service Management
```bash
# Production service
sudo systemctl status whatbot.service
sudo systemctl restart whatbot.service
sudo journalctl -u whatbot.service -f

# Test service (v2.0.0)
sudo systemctl status whatbot-test-v2-0-0.service
sudo systemctl restart whatbot-test-v2-0-0.service
sudo journalctl -u whatbot-test-v2-0-0.service -f
```

### Database Management
```bash
# Production database
sudo -u postgres psql -d whatbot_production

# Test database
sudo -u postgres psql -d whatbot_test_v2_0_0

# List all databases
sudo -u postgres psql -c "\l" | grep whatbot
```

### Cleanup Operations
```bash
# Stop and remove test service
sudo systemctl stop whatbot-test-v2-0-0.service
sudo systemctl disable whatbot-test-v2-0-0.service
sudo rm /etc/systemd/system/whatbot-test-v2-0-0.service

# Remove test directory
sudo rm -rf /opt/whatbot-test/v2.0.0

# Remove test database
sudo -u postgres psql -c "DROP DATABASE whatbot_test_v2_0_0;"

# Reload systemd
sudo systemctl daemon-reload
```

---

## 📊 Monitoring and Analytics

### Version Health Monitoring
```bash
# Health check script
#!/bin/bash
VERSIONS=("v1.0.0:41100" "v2.0.0:41220" "v3.0.0:41230")

for version_info in "${VERSIONS[@]}"; do
    IFS=':' read -r version port <<< "$version_info"
    
    if curl -s "http://localhost:$port/api/version" > /dev/null; then
        echo "✓ $version is healthy"
    else
        echo "✗ $version is down"
    fi
done
```

### Performance Comparison
```bash
# Compare response times
echo "Production (v1.0.0):"
time curl -s http://localhost:41100/api/v1/status > /dev/null

echo "Test (v2.0.0):"
time curl -s http://localhost:41220/api/v2/status > /dev/null
```

### Log Analysis
```bash
# Compare logs across versions
sudo journalctl -u whatbot.service --since "1 hour ago" | grep ERROR
sudo journalctl -u whatbot-test-v2-0-0.service --since "1 hour ago" | grep ERROR
```

---

## 🚨 Troubleshooting

### Common Issues

#### Test Environment Won't Start
```bash
# Check service status
sudo systemctl status whatbot-test-v2-0-0.service

# Check logs
sudo journalctl -u whatbot-test-v2-0-0.service -n 50

# Check port availability
sudo netstat -tlnp | grep 41220

# Check file permissions
ls -la /opt/whatbot-test/v2.0.0/
```

#### Database Connection Issues
```bash
# Check database status
sudo systemctl status postgresql

# Test database connection
sudo -u postgres psql -d whatbot_test_v2_0_0 -c "SELECT version();"

# Check database logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

#### API Route Issues
```bash
# Test API endpoints
curl -v http://localhost:41220/api/version
curl -v http://localhost:41220/api/v2/status

# Check server.js configuration
grep -n "api/v" /opt/whatbot-test/v2.0.0/server.js
```

#### Port Conflicts
```bash
# Check port usage
sudo netstat -tlnp | grep :41220

# Kill process using port
sudo fuser -k 41220/tcp

# Restart service
sudo systemctl restart whatbot-test-v2-0-0.service
```

### Recovery Procedures

#### Rollback to Previous Version
```bash
# Stop current production
sudo systemctl stop whatbot.service

# Restore from backup
sudo cp -r /opt/whatbot-backups/whatbot_backup_20250621_143000 /opt/whatbot

# Restart production
sudo systemctl start whatbot.service

# Verify rollback
curl http://localhost:41100/api/version
```

#### Clean Test Environment
```bash
# Stop all test services
sudo systemctl stop whatbot-test-*

# Remove test directories
sudo rm -rf /opt/whatbot-test/*

# Remove test databases
sudo -u postgres psql -c "DROP DATABASE IF EXISTS whatbot_test_v2_0_0;"
sudo -u postgres psql -c "DROP DATABASE IF EXISTS whatbot_test_v3_0_0;"

# Remove service files
sudo rm /etc/systemd/system/whatbot-test-*.service

# Reload systemd
sudo systemctl daemon-reload
```

---

## 🔒 Security Considerations

### Version Isolation
- **Separate Databases**: Each version has isolated data
- **Independent Services**: No shared resources between versions
- **Port Isolation**: Different ports prevent conflicts
- **Environment Separation**: Test and production environments are completely separate

### Access Control
```bash
# Restrict test environment access
sudo ufw deny 41220
sudo ufw allow from 127.0.0.1 to any port 41220

# Monitor test environment access
sudo tail -f /var/log/nginx/access.log | grep 41220
```

### Data Protection
```bash
# Backup test databases
pg_dump whatbot_test_v2_0_0 > backup_test_v2.sql

# Encrypt sensitive test data
# (Implement encryption for test environments)
```

---

## 📈 Best Practices

### Version Management
1. **Always Test First**: Use test environments before production updates
2. **Backup Regularly**: Create backups before any version changes
3. **Monitor Performance**: Compare performance across versions
4. **Document Changes**: Keep detailed change logs for each version
5. **Plan Rollbacks**: Always have a rollback strategy

### Development Workflow
1. **Feature Branches**: Develop new features in separate branches
2. **Version Tags**: Tag releases with semantic versions
3. **API Compatibility**: Maintain backward compatibility when possible
4. **Testing Strategy**: Comprehensive testing for each version
5. **Deployment Pipeline**: Automated testing and deployment

### Production Updates
1. **Low Traffic Windows**: Update during low-usage periods
2. **Gradual Rollout**: Consider canary deployments for major versions
3. **Monitoring**: Monitor system health during and after updates
4. **User Communication**: Inform users about version changes
5. **Support Preparation**: Prepare support team for new versions

---

## 📞 Support

### Getting Help
- **Email**: ben@techjamlabs.com
- **Phone**: +2348099999928
- **Documentation**: [Main README](../README.md)
- **Issues**: Create GitHub issue for version-specific problems

### Version-Specific Support
- **v1.0.0**: Production support
- **v2.0.0+**: Development and testing support
- **Legacy Versions**: Limited support for older versions

---

*This guide covers the essential aspects of WhatBot version management. For specific implementation details or advanced configurations, refer to the main documentation or contact technical support.* 
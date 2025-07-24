/**
 * WhatBot v1.2.0
 * Location: README.md
 * Creation Date: December 21, 2024
 * 
 * Author: Ben Adenle
 * Email: ben@techjamlabs.com
 * Phone: +2348099999928
 * 
 * Copyright (c) TECHJAMLABS Limited / +234 201 330 9089 / +1 206 7100170 / hello@techjamlabs.com
 * 
 * Date of last change: June 21, 2025
 */

# WhatBot v1.2.0 - WhatsApp Automation Platform

<div align="center">

![WhatBot Logo](https://img.shields.io/badge/WhatBot-v1.2.0-blue?style=for-the-badge&logo=whatsapp)
![Node.js](https://img.shields.io/badge/Node.js-18+-green?style=for-the-badge&logo=node.js)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue?style=for-the-badge&logo=postgresql)
![License](https://img.shields.io/badge/License-Private-red?style=for-the-badge)

**Enterprise-grade WhatsApp automation platform with advanced messaging, broadcasting, and contact management capabilities.**

[🚀 Quick Start](#-quick-start) • [📋 Features](#-features) • [🔧 Installation](#-installation) • [📚 Documentation](#-documentation) • [🛠️ Development](#️-development)

</div>

---

## 🎯 Overview

WhatBot is a comprehensive WhatsApp automation platform built with Node.js, Express, and venom-bot. It provides enterprise-grade messaging capabilities, intelligent broadcasting, contact management, and real-time interaction features designed for businesses and organizations.

### ✨ Key Highlights

- **🔐 Secure Authentication** - JWT-based authentication with API key support
- **📱 WhatsApp Integration** - Stable venom-bot integration with session management
- **📢 Smart Broadcasting** - Intelligent message queuing and rate limiting
- **👥 Contact Management** - Advanced contact import and group management
- **🤖 Auto-Responses** - Keyword-based automatic reply system
- **📊 Real-time Analytics** - Message tracking and delivery statistics
- **🔒 Enterprise Security** - Role-based access control and audit logging
- **📈 Scalable Architecture** - Designed for high-volume messaging

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ 
- **npm** 10+
- **PostgreSQL** 13+ (recommended) or MySQL 8+
- **Ubuntu 22.04+** (recommended) or Windows 10+
- **WhatsApp Business** account or regular WhatsApp

### Quick Installation

```bash
# Clone repository
git clone https://github.com/TechJam-Labs/whatbot-master-copy.git
cd whatbot-master-copy

# Install dependencies
npm install

# Setup environment
cp config.template.env .env
# Edit .env with your configuration

# Setup database
npm run setup

# Start application
npm start

# Access web interface
# Open http://localhost:41100
```

### First Time Setup

1. **Configure Environment** - Edit `.env` file with your settings
2. **Initialize WhatsApp** - Scan QR code to connect your WhatsApp
3. **Create Admin Account** - Set up your first admin user
4. **Import Contacts** - Upload your contact list
5. **Start Broadcasting** - Begin sending messages!

---

## 📋 Features

### 🔐 Authentication & Security
- **JWT Authentication** - Secure token-based authentication
- **API Key Management** - Multiple API keys with role-based access
- **Role-Based Access Control** - Admin, User, and Temporary access levels
- **Rate Limiting** - Configurable request limits per endpoint
- **Session Management** - Secure WhatsApp session handling

### 📱 WhatsApp Integration
- **Stable Connection** - Persistent WhatsApp Web connection
- **Session Recovery** - Automatic reconnection on disconnection
- **Health Monitoring** - Real-time connection status tracking
- **Multi-Format Support** - Text, images, videos, documents, audio
- **Rich Media Handling** - Automatic format conversion and optimization

### 📢 Broadcasting System
- **Intelligent Queuing** - Smart message queue management
- **Rate Limiting** - WhatsApp-compliant sending limits
- **Batch Processing** - Configurable batch sizes and delays
- **Scheduled Broadcasting** - Future-dated message scheduling
- **Progress Tracking** - Real-time broadcast progress monitoring
- **Safety Limits** - Daily and monthly message limits

### 👥 Contact Management
- **Multi-Format Import** - CSV, TXT, JSON contact files
- **Smart Parsing** - Automatic phone number detection
- **Nigerian Number Formatting** - Automatic +234 conversion
- **Contact Groups** - Organize contacts into groups
- **Duplicate Detection** - Automatic duplicate contact handling
- **Bulk Operations** - Mass contact management

### 🤖 Auto-Response System
- **Keyword Matching** - Configurable keyword triggers
- **Rich Text Support** - HTML to WhatsApp format conversion
- **Context Awareness** - Conversation history integration
- **Response Templates** - Pre-defined response patterns
- **Escalation Rules** - Automatic human handoff

### 📊 Analytics & Monitoring
- **Message Tracking** - Delivery status and read receipts
- **Performance Metrics** - Response times and success rates
- **Usage Statistics** - Daily/monthly message counts
- **Error Monitoring** - Failed message tracking
- **Audit Logging** - Complete activity history

### 🔧 Administration
- **User Management** - Admin and user account management
- **System Configuration** - Environment and application settings
- **Backup & Restore** - Database and file backup systems
- **Log Management** - Comprehensive logging and monitoring
- **Health Checks** - System status monitoring

---

## 🔧 Installation

### Detailed Installation Guide

For comprehensive installation instructions, see our detailed guides:

- **[Ubuntu Production Guide](docs/dev-guides/UBUNTU_PRODUCTION_GUIDE.md)** - Production deployment on Ubuntu
- **[Cloud VPS Deployment Guide](docs/dev-guides/CLOUD_VPS_DEPLOYMENT_GUIDE.md)** - Deploy to cloud providers
- **[PostgreSQL Setup Guide](docs/dev-guides/POSTGRES_SETUP_GUIDE.md)** - Database configuration

---

## 🔄 Version Management & Updates

### API Versioning

WhatBot uses semantic versioning with versioned API endpoints:

- **Current Version**: v1.0.0
- **API Endpoints**: `/api/v1/` (current)
- **Version Endpoint**: `/api/version` - Returns version information

### Update System

WhatBot includes a comprehensive update system that allows:

- **Safe Testing**: Test new versions in isolated environments
- **Versioned APIs**: Each version runs on separate ports with versioned endpoints
- **Rollback Support**: Automatic backup and rollback capabilities
- **Zero Downtime**: Test environments run alongside production

### Using the Update Script

```bash
# Run the update script
sudo python3 whatbot-update.py

# The script will:
# 1. Check current version
# 2. Show available versions
# 3. Create test environment
# 4. Update API routes automatically
# 5. Test the new version
# 6. Prompt for production update
```

### Test Environment Features

- **Separate Ports**: Each version runs on a different port (41200 + version offset)
- **Isolated Databases**: Separate test databases for each version
- **Versioned Endpoints**: `/api/v2/`, `/api/v3/`, etc.
- **Independent Services**: Separate systemd services for each test environment

### Version Management Commands

```bash
# Check current version
curl http://localhost:41100/api/version

# List running services
systemctl list-units --type=service | grep whatbot

# Test specific version (e.g., v2.0.0 on port 41220)
curl http://localhost:41220/api/version

# Clean up test environment
sudo python3 whatbot-update.py --cleanup v2.0.0
```
- **[Troubleshooting Guide](docs/dev-guides/TROUBLESHOOTING_GUIDE.md)** - Common issues and solutions

### Environment Configuration

```bash
# Essential environment variables
PORT=41100                          # Application port
NODE_ENV=production                 # Environment mode
BASE_URL=https://your-domain.com    # Your domain URL
JWT_SECRET=your_secure_secret       # JWT signing secret

# Database configuration
DB_HOST=localhost                   # Database host
DB_PORT=5432                        # Database port
DB_NAME=whatbot_production          # Database name
DB_USER=whatbot_user               # Database user
DB_PASSWORD=your_secure_password   # Database password

# WhatsApp configuration
WHATSAPP_NUMBER=+2349157342656     # Your WhatsApp number
COMPANY_NAME=Your Company Name      # Company name for messages
```

### Database Setup

```bash
# PostgreSQL setup
sudo -u postgres psql

CREATE DATABASE whatbot_production;
CREATE USER whatbot_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE whatbot_production TO whatbot_user;
\q

# Run database setup
npm run setup
```

### Production Deployment

```bash
# Install PM2 globally
npm install -g pm2

# Start with PM2
pm2 start ecosystem.config.js

# Save PM2 configuration
pm2 save

# Setup auto-start
pm2 startup
```

---

## 📚 Documentation

### 📖 Core Documentation

- **[API Documentation](docs/dev-guides/API_DOCUMENTATION.md)** - Complete API reference
- **[Database Architecture](docs/dev-guides/DATABASE_ARCHITECTURE_PLAN.md)** - Database design and schema
- **[Project Structure](docs/dev-guides/PROJECT_STRUCTURE.md)** - Codebase organization
- **[Role-Based Access](docs/dev-guides/ROLE_BASED_ACCESS_SUMMARY.md)** - User permissions and roles

### 🚀 Deployment Guides

- **[Cloud VPS Deployment](docs/dev-guides/CLOUD_VPS_DEPLOYMENT_GUIDE.md)** - Deploy to AWS, DigitalOcean, Linode, Vultr
- **[Ubuntu Production Guide](docs/dev-guides/UBUNTU_PRODUCTION_GUIDE.md)** - Production server setup
- **[PostgreSQL Setup](docs/dev-guides/POSTGRES_SETUP_GUIDE.md)** - Database installation and configuration

### 🛠️ Development Guides

- **[Development Roadmap](docs/dev-guides/DEVELOPMENT_ROADMAP.md)** - Future features and ML pipeline
- **[Database Migration](docs/dev-guides/DATABASE_MIGRATION.md)** - Database migration procedures
- **[Scheduling Guide](docs/dev-guides/SCHEDULING_GUIDE.md)** - Message scheduling features

### 🔧 Troubleshooting

- **[Troubleshooting Guide](docs/dev-guides/TROUBLESHOOTING_GUIDE.md)** - Common issues and solutions
- **[WhatsApp Troubleshooting](docs/dev-guides/WHATSAPP_TROUBLESHOOTING.md)** - WhatsApp-specific issues
- **[Admin Accounts](docs/dev-guides/ADMIN_ACCOUNTS.md)** - Admin account management

---

## 🛠️ Development

### Project Structure

```
gomed/
├── server.js                 # Main application server
├── package.json             # Dependencies and scripts
├── ecosystem.config.js      # PM2 configuration
├── config.template.env      # Environment template
├── src/                     # Source code
│   ├── middleware/          # Express middleware
│   ├── routes/              # API routes
│   └── utils/               # Utility functions
├── public/                  # Frontend files
├── scripts/                 # Scripts and utilities
│   ├── api-test/           # API testing suite
│   ├── test/               # Test scripts
│   ├── utils/              # Utility scripts
│   ├── setup/              # Setup scripts
│   └── deployment/         # Deployment scripts
├── database/               # Database files
├── docs/                   # Documentation
└── uploads/                # File uploads
```

### Available Scripts

```bash
# Development
npm start                   # Start production server
npm run dev                 # Start development server
npm test                    # Run essential tests
npm run test:quick         # Quick health check
npm run test:auth          # Authentication tests
npm run test:media         # Media sending tests
npm run test:contacts      # Contact management tests
npm run test:broadcast     # Broadcast tests
npm run test:env           # Test environment-based authentication

# Setup & Deployment
npm run setup              # Setup PostgreSQL database
npm run test:setup         # Setup test environment configuration
npm run deploy             # Deploy application

# Session Management
npm run session:check      # Check session health
npm run session:monitor    # Monitor session
npm run session:recover    # Recover session
```

### API Testing

The project includes a comprehensive API testing suite with environment-based configuration:

```bash
# Setup test environment (creates .env with test configuration)
npm run test:setup

# Test environment-based authentication
npm run test:env

# Run comprehensive API tests
cd scripts/api-test/
./api-test-comprehensive.sh

# Test specific endpoints
curl -H "X-API-Key: your_api_key" http://localhost:41100/api/v1/status
```

#### Test Environment Features

- **Environment-based API Keys**: Use `TEST_API_KEY` from `.env` file
- **Automatic Configuration**: Scripts load settings from environment variables
- **Development Mode**: Automatic fallback to test keys in development
- **Flexible Testing**: Support for both hardcoded and environment-based keys

For detailed test environment setup, see **[Test Environment Setup Guide](docs/dev-guides/TEST_ENVIRONMENT_SETUP.md)**.

### Development Workflow

1. **Create Feature Branch** - `git checkout -b feat/feature-name`
2. **Implement Feature** - Follow coding standards and patterns
3. **Test Thoroughly** - Use appropriate test scripts
4. **Add to Git** - `git add .`
5. **Commit with Message** - Use conventional commit format
6. **Merge to Dev** - `git checkout dev && git merge feat/feature-name`
7. **Push to Origin** - `git push origin dev`

---

## 🔒 Security Features

### Authentication & Authorization
- **JWT Tokens** - Secure token-based authentication
- **API Keys** - Multiple API keys with different access levels
- **Role-Based Access** - Admin, User, and Temporary roles
- **Session Validation** - Secure session management
- **Rate Limiting** - Request throttling to prevent abuse

### Data Protection
- **Input Validation** - Comprehensive input sanitization
- **SQL Injection Prevention** - Parameterized queries
- **XSS Protection** - Output encoding and sanitization
- **CSRF Protection** - Cross-site request forgery prevention
- **File Upload Security** - Secure file handling and validation

### WhatsApp Security
- **Session Encryption** - Secure WhatsApp session storage
- **Phone Number Validation** - Proper number format validation
- **Access Controls** - Restricted access to sensitive operations
- **Audit Logging** - Complete activity tracking
- **Error Handling** - Secure error responses

---

## 📊 Performance & Scalability

### Performance Optimizations
- **Database Indexing** - Optimized database queries
- **Connection Pooling** - Efficient database connections
- **Caching** - Intelligent caching strategies
- **Load Balancing** - Request distribution across instances
- **Memory Management** - Optimized memory usage

### Scalability Features
- **Horizontal Scaling** - Support for multiple instances
- **Queue Management** - Intelligent message queuing
- **Batch Processing** - Efficient bulk operations
- **Resource Monitoring** - Real-time performance tracking
- **Auto-scaling** - Dynamic resource allocation

### Monitoring & Analytics
- **Real-time Metrics** - Live performance monitoring
- **Error Tracking** - Comprehensive error logging
- **Usage Analytics** - Detailed usage statistics
- **Health Checks** - System health monitoring
- **Alert System** - Automated alert notifications

---

## 🚀 Future Roadmap

### Phase 1: Multi-WhatsApp Support (Q3 2025)
- Multiple WhatsApp number support
- Load balancing across sessions
- Enhanced broadcasting system
- Session management dashboard

### Phase 2: Machine Learning Pipeline (Q4 2025)
- Natural Language Processing (NLP)
- Intent recognition and sentiment analysis
- Intelligent auto-response system
- Predictive analytics

### Phase 3: Advanced Features (Q1 2026)
- Advanced analytics dashboard
- Third-party integrations (CRM, e-commerce)
- Enhanced security features
- Enterprise-grade monitoring

### Phase 4: Scalability & Performance (Q2 2026)
- Microservices architecture
- High availability setup
- Performance optimization
- Advanced monitoring

For detailed roadmap information, see **[Development Roadmap](docs/dev-guides/DEVELOPMENT_ROADMAP.md)**.

---

## 🤝 Contributing

### Development Standards
- Follow JavaScript ES6+ standards
- Use proper error handling with try-catch blocks
- Implement comprehensive testing
- Add JSDoc comments for functions
- Follow the established project structure

### Code Quality
- All code must pass linting checks
- Comprehensive test coverage required
- Proper error handling implementation
- Security best practices followed
- Performance considerations addressed

### Documentation
- Update API documentation for new endpoints
- Add inline comments for complex logic
- Update README.md as needed
- Follow conventional commit format

---

## 📞 Support & Contact

### Technical Support
- **Email:** ben@techjamlabs.com
- **Phone:** +2348099999928
- **Documentation:** [Project Documentation](docs/dev-guides/)
- **Issues:** Create GitHub issue or contact support

### Company Information
- **Company:** TECHJAMLABS Limited
- **Phone:** +234 201 330 9089 / +1 206 7100170
- **Email:** hello@techjamlabs.com
- **Website:** [techjamlabs.com](https://techjamlabs.com)

### Community & Resources
- **Documentation:** [docs/dev-guides/](docs/dev-guides/)
- **API Reference:** [API Documentation](docs/dev-guides/API_DOCUMENTATION.md)
- **Troubleshooting:** [Troubleshooting Guide](docs/dev-guides/TROUBLESHOOTING_GUIDE.md)
- **Deployment:** [Cloud VPS Guide](docs/dev-guides/CLOUD_VPS_DEPLOYMENT_GUIDE.md)

---

## 📄 License

**Private License** - This software is proprietary and confidential.

Copyright (c) 2025 TECHJAMLABS Limited. All rights reserved.

- **Unauthorized copying, distribution, or use is strictly prohibited**
- **This software is licensed for use by authorized organizations only**
- **Contact TECHJAMLABS Limited for licensing information**

---

<div align="center">

**Built with ❤️ by [TECHJAMLABS Limited](https://techjamlabs.com)**

[![TECHJAMLABS](https://img.shields.io/badge/TECHJAMLABS-Limited-blue?style=for-the-badge)](https://techjamlabs.com)

*Empowering businesses with intelligent WhatsApp automation solutions*

</div>

<!--
 * WhatBot v1.2.0
 * Location: docs\dev-guides\DATABASE_ARCHITECTURE_PLAN.md
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

# Database Architecture Plan - PostgreSQL Implementation

## 🎯 Why PostgreSQL Over MySQL?

### For Your Use Case:
- **JSON Support**: Native JSONB for flexible auto-reply rules and ML features
- **Full-Text Search**: Advanced search capabilities for messages and auto-replies
- **ML Extensions**: Built-in support for ML operations (pg_stat_statements, etc.)
- **Better Concurrency**: Superior handling of concurrent writes
- **Data Types**: Rich data types for ML features (arrays, ranges, etc.)
- **Extensions**: Ecosystem for ML/AI (pgvector for embeddings, etc.)

## 🏗️ Database Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    PostgreSQL Database                      │
├─────────────────────────────────────────────────────────────┤
│  Authentication & Users                                     │
│  ├── users                                                  │
│  ├── user_sessions                                          │
│  └── user_permissions                                       │
├─────────────────────────────────────────────────────────────┤
│  Core Application Data                                      │
│  ├── messages                                               │
│  ├── contacts                                               │
│  ├── contact_groups                                         │
│  └── auto_replies                                           │
├─────────────────────────────────────────────────────────────┤
│  ML Data Pipeline                                           │
│  ├── message_analytics                                      │
│  ├── conversation_flows                                     │
│  ├── sentiment_analysis                                     │
│  └── ml_features                                            │
├─────────────────────────────────────────────────────────────┤
│  System & Audit                                             │
│  ├── system_logs                                            │
│  ├── audit_trails                                           │
│  └── api_usage_metrics                                      │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Detailed Schema Design

### 1. Authentication & Users

```sql
-- Users table
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
    created_by UUID REFERENCES users(id),
    
    -- Indexes
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_active (is_active)
);

-- User sessions for JWT management
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_token_hash (token_hash),
    INDEX idx_expires_at (expires_at)
);

-- User permissions (granular access control)
CREATE TABLE user_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    resource VARCHAR(50) NOT NULL, -- 'messages', 'contacts', 'auto_replies', 'api_keys', etc.
    action VARCHAR(20) NOT NULL,   -- 'read', 'write', 'delete', 'admin'
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    granted_by UUID REFERENCES users(id),
    
    UNIQUE(user_id, resource, action),
    INDEX idx_user_resource (user_id, resource)
);

-- API Keys management
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    key_hash VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    user_id UUID REFERENCES users(id),
    role VARCHAR(20) DEFAULT 'agent' CHECK (role IN ('admin', 'developer', 'agent')),
    permissions JSONB DEFAULT '{}', -- Specific permissions for this API key
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP,
    last_used_at TIMESTAMP,
    usage_count INT DEFAULT 0,
    rate_limit_per_hour INT DEFAULT 1000,
    ip_whitelist JSONB DEFAULT '[]', -- Allowed IP addresses
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id),
    
    INDEX idx_key_hash (key_hash),
    INDEX idx_user_id (user_id),
    INDEX idx_role (role),
    INDEX idx_active (is_active),
    INDEX idx_expires_at (expires_at),
    INDEX idx_last_used (last_used_at)
);

-- API Key usage logs
CREATE TABLE api_key_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    api_key_id UUID NOT NULL REFERENCES api_keys(id),
    endpoint VARCHAR(100) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INT,
    response_time_ms INT,
    ip_address INET,
    user_agent TEXT,
    request_size_bytes INT,
    response_size_bytes INT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_api_key_id (api_key_id),
    INDEX idx_endpoint (endpoint),
    INDEX idx_status_code (status_code),
    INDEX idx_created_at (created_at)
);
```

### 2. Core Application Data

```sql
-- Enhanced messages table
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
    read_at TIMESTAMP,
    is_auto_reply BOOLEAN DEFAULT FALSE,
    auto_reply_rule_id UUID REFERENCES auto_replies(id),
    sentiment_score DECIMAL(3,2), -- For ML features
    language_code VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_chat_id (chat_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_from_number (from_number),
    INDEX idx_type (type),
    INDEX idx_auto_reply (is_auto_reply),
    INDEX idx_sentiment (sentiment_score),
    
    -- Full-text search
    FULLTEXT(body, sender_name)
);

-- Enhanced contacts table
CREATE TABLE contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    group_name VARCHAR(100) NOT NULL,
    tags JSONB DEFAULT '[]',
    notes TEXT,
    reg_no VARCHAR(100),
    engagement_score DECIMAL(3,2) DEFAULT 0.0, -- ML feature
    last_interaction TIMESTAMP,
    interaction_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id),
    
    INDEX idx_phone (phone),
    INDEX idx_group (group_name),
    INDEX idx_email (email),
    INDEX idx_engagement (engagement_score),
    INDEX idx_last_interaction (last_interaction),
    
    -- JSONB indexes for tags
    INDEX idx_tags_gin (tags USING GIN)
);

-- Contact groups
CREATE TABLE contact_groups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    contact_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id),
    
    INDEX idx_name (name)
);

-- Auto-replies system
CREATE TABLE auto_replies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    keywords JSONB NOT NULL, -- Array of keywords/patterns
    reply_message TEXT NOT NULL,
    reply_type VARCHAR(20) DEFAULT 'text' CHECK (reply_type IN ('text', 'media', 'template')),
    media_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    priority INT DEFAULT 0, -- Higher priority = checked first
    match_type VARCHAR(20) DEFAULT 'exact' CHECK (match_type IN ('exact', 'contains', 'regex', 'fuzzy')),
    conditions JSONB DEFAULT '{}', -- Additional conditions (time, user, etc.)
    usage_count INT DEFAULT 0,
    success_rate DECIMAL(5,2) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id),
    
    INDEX idx_active (is_active),
    INDEX idx_priority (priority),
    INDEX idx_keywords_gin (keywords USING GIN),
    INDEX idx_conditions_gin (conditions USING GIN),
    INDEX idx_usage (usage_count),
    INDEX idx_success_rate (success_rate)
);

-- Auto-reply usage tracking
CREATE TABLE auto_reply_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    auto_reply_id UUID NOT NULL REFERENCES auto_replies(id),
    message_id VARCHAR(255) NOT NULL REFERENCES messages(id),
    matched_keyword VARCHAR(255),
    response_sent BOOLEAN DEFAULT FALSE,
    response_time_ms INT,
    user_feedback JSONB, -- User reactions, follow-up messages
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_auto_reply_id (auto_reply_id),
    INDEX idx_message_id (message_id),
    INDEX idx_created_at (created_at)
);
```

### 3. ML Data Pipeline

```sql
-- Message analytics for ML
CREATE TABLE message_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id VARCHAR(255) NOT NULL REFERENCES messages(id),
    chat_id VARCHAR(100) NOT NULL,
    user_id UUID REFERENCES users(id),
    
    -- Text analysis
    word_count INT,
    character_count INT,
    language_detected VARCHAR(10),
    sentiment_score DECIMAL(3,2),
    sentiment_label VARCHAR(20),
    key_phrases JSONB,
    entities JSONB,
    
    -- Engagement metrics
    response_time_ms INT,
    has_response BOOLEAN DEFAULT FALSE,
    response_count INT DEFAULT 0,
    
    -- ML features
    features_vector JSONB, -- For ML model features
    predicted_intent VARCHAR(100),
    confidence_score DECIMAL(3,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_message_id (message_id),
    INDEX idx_chat_id (chat_id),
    INDEX idx_sentiment (sentiment_score),
    INDEX idx_intent (predicted_intent),
    INDEX idx_created_at (created_at)
);

-- Conversation flows for ML
CREATE TABLE conversation_flows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_id VARCHAR(100) NOT NULL,
    session_id VARCHAR(255),
    flow_type VARCHAR(50), -- 'support', 'sales', 'general', etc.
    start_message_id VARCHAR(255) REFERENCES messages(id),
    end_message_id VARCHAR(255) REFERENCES messages(id),
    message_count INT DEFAULT 0,
    duration_seconds INT,
    outcome VARCHAR(50), -- 'resolved', 'escalated', 'abandoned', etc.
    satisfaction_score INT CHECK (satisfaction_score >= 1 AND satisfaction_score <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_chat_id (chat_id),
    INDEX idx_flow_type (flow_type),
    INDEX idx_outcome (outcome),
    INDEX idx_created_at (created_at)
);

-- Sentiment analysis tracking
CREATE TABLE sentiment_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_id VARCHAR(100) NOT NULL,
    message_id VARCHAR(255) REFERENCES messages(id),
    sentiment_score DECIMAL(3,2) NOT NULL,
    sentiment_label VARCHAR(20),
    confidence DECIMAL(3,2),
    model_version VARCHAR(50),
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_chat_id (chat_id),
    INDEX idx_sentiment (sentiment_score),
    INDEX idx_analyzed_at (analyzed_at)
);

-- ML model performance tracking
CREATE TABLE ml_model_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    task_type VARCHAR(50) NOT NULL, -- 'sentiment', 'intent', 'classification'
    accuracy DECIMAL(5,4),
    precision DECIMAL(5,4),
    recall DECIMAL(5,4),
    f1_score DECIMAL(5,4),
    training_samples INT,
    test_samples INT,
    training_duration_seconds INT,
    deployed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_model_name (model_name),
    INDEX idx_task_type (task_type),
    INDEX idx_deployed_at (deployed_at)
);
```

### 4. System & Audit

```sql
-- System logs
CREATE TABLE system_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    level VARCHAR(10) NOT NULL CHECK (level IN ('debug', 'info', 'warn', 'error')),
    category VARCHAR(50) NOT NULL, -- 'auth', 'message', 'auto_reply', 'ml'
    message TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    user_id UUID REFERENCES users(id),
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_level (level),
    INDEX idx_category (category),
    INDEX idx_created_at (created_at),
    INDEX idx_user_id (user_id)
);

-- Audit trails
CREATE TABLE audit_trails (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(50) NOT NULL, -- 'create', 'update', 'delete', 'login', 'logout'
    resource_type VARCHAR(50) NOT NULL, -- 'message', 'contact', 'auto_reply', 'user'
    resource_id VARCHAR(255),
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_resource (resource_type, resource_id),
    INDEX idx_created_at (created_at)
);

-- API usage metrics
CREATE TABLE api_usage_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    endpoint VARCHAR(100) NOT NULL,
    method VARCHAR(10) NOT NULL,
    user_id UUID REFERENCES users(id),
    response_time_ms INT,
    status_code INT,
    request_size_bytes INT,
    response_size_bytes INT,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_endpoint (endpoint),
    INDEX idx_user_id (user_id),
    INDEX idx_status_code (status_code),
    INDEX idx_created_at (created_at)
);
```

## 🔐 Authentication & Authorization Implementation

### User Roles & Permissions:

```javascript
// Role definitions
const ROLES = {
  ADMIN: 'admin',
  DEVELOPER: 'developer', 
  AGENT: 'agent'
};

// Default permissions per role
const ROLE_PERMISSIONS = {
  admin: {
    messages: ['read', 'write', 'delete', 'admin'],
    contacts: ['read', 'write', 'delete', 'admin'],
    auto_replies: ['read', 'write', 'delete', 'admin'],
    api_keys: ['read', 'write', 'delete', 'admin'],
    users: ['read', 'write', 'delete', 'admin'],
    analytics: ['read', 'write', 'delete', 'admin'],
    system: ['read', 'write', 'delete', 'admin']
  },
  developer: {
    messages: ['read', 'write'],
    contacts: ['read', 'write'],
    auto_replies: ['read', 'write'],
    api_keys: ['read', 'write'],
    analytics: ['read', 'write'],
    system: ['read']
  },
  agent: {
    messages: ['read', 'write'],
    contacts: ['read', 'write'],
    auto_replies: ['read'],
    analytics: ['read']
  }
};

// JWT-based Authentication middleware
const authenticateToken = async (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = await db.getUserById(decoded.userId);
    
    if (!user || !user.is_active) {
      return res.status(401).json({ error: 'Invalid or inactive user' });
    }
    
    req.user = user;
    next();
  } catch (error) {
    return res.status(403).json({ error: 'Invalid token' });
  }
};

// API Key Authentication middleware
const authenticateApiKey = async (req, res, next) => {
  const apiKey = req.headers['x-api-key'] || req.headers.authorization?.split(' ')[1];
  
  if (!apiKey) {
    return res.status(401).json({ error: 'API key required' });
  }
  
  try {
    const keyData = await db.getApiKeyByHash(apiKey);
    
    if (!keyData || !keyData.is_active) {
      return res.status(401).json({ error: 'Invalid or inactive API key' });
    }
    
    if (keyData.expires_at && new Date() > keyData.expires_at) {
      return res.status(401).json({ error: 'API key expired' });
    }
    
    // Check IP whitelist
    if (keyData.ip_whitelist && keyData.ip_whitelist.length > 0) {
      const clientIP = req.ip || req.connection.remoteAddress;
      if (!keyData.ip_whitelist.includes(clientIP)) {
        return res.status(403).json({ error: 'IP not whitelisted' });
      }
    }
    
    // Check rate limit
    const usageCount = await db.getApiKeyUsageCount(keyData.id, '1 hour');
    if (usageCount >= keyData.rate_limit_per_hour) {
      return res.status(429).json({ error: 'Rate limit exceeded' });
    }
    
    req.apiKey = keyData;
    req.user = await db.getUserById(keyData.user_id);
    next();
  } catch (error) {
    return res.status(403).json({ error: 'Invalid API key' });
  }
};

// Role-based authorization
const authorizeRole = (roles) => {
  return (req, res, next) => {
    const user = req.user;
    if (!user || !roles.includes(user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
};

// Resource-based authorization
const authorizeResource = (resource, action) => {
  return async (req, res, next) => {
    const user = req.user;
    if (!user) {
      return res.status(401).json({ error: 'Authentication required' });
    }
    
    // Admin has all permissions
    if (user.role === ROLES.ADMIN) {
      return next();
    }
    
    // Check specific permissions
    const hasPermission = await db.checkUserPermission(user.id, resource, action);
    if (!hasPermission) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    
    next();
  };
};
```

## 🔑 API Key Management System

### API Key Operations:

```javascript
class ApiKeyManager {
  async generateApiKey(userId, options = {}) {
    const {
      name,
      description,
      role = 'agent',
      permissions = {},
      expiresAt,
      rateLimitPerHour = 1000,
      ipWhitelist = []
    } = options;
    
    // Generate secure API key
    const apiKey = crypto.randomBytes(32).toString('hex');
    const keyHash = await bcrypt.hash(apiKey, 12);
    
    const keyData = {
      name,
      description,
      key_hash: keyHash,
      user_id: userId,
      role,
      permissions,
      expires_at: expiresAt,
      rate_limit_per_hour: rateLimitPerHour,
      ip_whitelist: ipWhitelist
    };
    
    await db.createApiKey(keyData);
    
    // Return the plain API key (only shown once)
    return {
      id: keyData.id,
      api_key: apiKey,
      name,
      role,
      expires_at: expiresAt
    };
  }
  
  async validateApiKey(apiKey, req) {
    const keyData = await db.getApiKeyByHash(apiKey);
    
    if (!keyData || !keyData.is_active) {
      throw new Error('Invalid or inactive API key');
    }
    
    // Check expiration
    if (keyData.expires_at && new Date() > keyData.expires_at) {
      throw new Error('API key expired');
    }
    
    // Check IP whitelist
    if (keyData.ip_whitelist && keyData.ip_whitelist.length > 0) {
      const clientIP = req.ip || req.connection.remoteAddress;
      if (!keyData.ip_whitelist.includes(clientIP)) {
        throw new Error('IP not whitelisted');
      }
    }
    
    // Check rate limit
    const usageCount = await this.getUsageCount(keyData.id, '1 hour');
    if (usageCount >= keyData.rate_limit_per_hour) {
      throw new Error('Rate limit exceeded');
    }
    
    // Log usage
    await this.logApiKeyUsage(keyData.id, req);
    
    return keyData;
  }
  
  async getApiKeyAnalytics(keyId, timeRange = '30 days') {
    return await db.getApiKeyAnalytics(keyId, timeRange);
  }
}
```

## 👥 User Role Management

### Role-Based Access Control:

```javascript
class UserRoleManager {
  async createUser(userData) {
    const {
      username,
      email,
      password,
      fullName,
      role = 'agent',
      createdBy
    } = userData;
    
    // Hash password
    const passwordHash = await bcrypt.hash(password, 12);
    
    const user = {
      username,
      email,
      password_hash: passwordHash,
      full_name: fullName,
      role,
      created_by: createdBy
    };
    
    const newUser = await db.createUser(user);
    
    // Assign default permissions based on role
    await this.assignDefaultPermissions(newUser.id, role);
    
    return newUser;
  }
  
  async assignDefaultPermissions(userId, role) {
    const permissions = ROLE_PERMISSIONS[role];
    
    for (const [resource, actions] of Object.entries(permissions)) {
      for (const action of actions) {
        await db.createUserPermission(userId, resource, action);
      }
    }
  }
  
  async checkPermission(userId, resource, action) {
    // Check if user has specific permission
    const permission = await db.getUserPermission(userId, resource, action);
    return !!permission;
  }
  
  async getUserPermissions(userId) {
    return await db.getUserPermissions(userId);
  }
}
```

## 🤖 Auto-Reply System

### Auto-Reply Engine:

```javascript
class AutoReplyEngine {
  async processMessage(message) {
    const rules = await this.getActiveRules();
    
    for (const rule of rules.sort((a, b) => b.priority - a.priority)) {
      if (await this.matchesRule(message, rule)) {
        const response = await this.generateResponse(rule, message);
        await this.sendResponse(message.chatId, response);
        await this.logUsage(rule, message);
        break; // Stop at first match
      }
    }
  }
  
  async matchesRule(message, rule) {
    const keywords = rule.keywords;
    const text = message.body.toLowerCase();
    
    switch (rule.match_type) {
      case 'exact':
        return keywords.some(keyword => text === keyword.toLowerCase());
      case 'contains':
        return keywords.some(keyword => text.includes(keyword.toLowerCase()));
      case 'regex':
        return keywords.some(pattern => new RegExp(pattern, 'i').test(text));
      case 'fuzzy':
        return keywords.some(keyword => this.fuzzyMatch(text, keyword));
    }
  }
}
```

## 📊 ML Data Pipeline

### Data Collection Strategy:

```javascript
class MLDataPipeline {
  async processMessage(message) {
    // 1. Text analysis
    const analytics = await this.analyzeText(message.body);
    
    // 2. Sentiment analysis
    const sentiment = await this.analyzeSentiment(message.body);
    
    // 3. Intent classification
    const intent = await this.classifyIntent(message.body);
    
    // 4. Store analytics
    await this.storeAnalytics(message.id, {
      ...analytics,
      sentiment,
      intent
    });
    
    // 5. Update conversation flow
    await this.updateConversationFlow(message.chatId, message, intent);
  }
  
  async analyzeText(text) {
    return {
      word_count: text.split(' ').length,
      character_count: text.length,
      language_detected: await this.detectLanguage(text),
      key_phrases: await this.extractKeyPhrases(text),
      entities: await this.extractEntities(text)
    };
  }
}
```

## 🚀 Implementation Plan

### Phase 1: Core Setup (Week 1)
1. **PostgreSQL Installation & Configuration**
2. **Database Schema Creation**
3. **Authentication System (JWT + API Keys)**
4. **User Management & Role-Based Access**
5. **Basic CRUD Operations**

### Phase 2: Auto-Reply System (Week 2)
1. **Auto-Reply Engine**
2. **Rule Management UI**
3. **Usage Analytics**
4. **Performance Optimization**

### Phase 3: API Key Management (Week 3)
1. **API Key Generation & Management**
2. **Rate Limiting & IP Whitelisting**
3. **Usage Tracking & Analytics**
4. **Security Hardening**

### Phase 4: ML Pipeline (Week 4-5)
1. **Data Collection Infrastructure**
2. **Text Analysis Integration**
3. **Sentiment Analysis**
4. **Intent Classification**

### Phase 5: Advanced Features (Week 6-7)
1. **Advanced Analytics Dashboard**
2. **ML Model Training Pipeline**
3. **Performance Monitoring**
4. **Audit & Compliance Features**

## 📈 Performance Considerations

### Indexing Strategy:
- **Composite indexes** for common query patterns
- **Partial indexes** for active records only
- **GIN indexes** for JSONB and full-text search
- **BRIN indexes** for time-series data

### Partitioning Strategy:
- **Time-based partitioning** for messages and logs
- **Hash partitioning** for large tables
- **List partitioning** for contact groups

### Caching Strategy:
- **Redis** for session management
- **Application-level caching** for auto-reply rules
- **Database query result caching**

## 🔒 Security Considerations

### Data Protection:
- **Encryption at rest** for sensitive data
- **Encryption in transit** (TLS)
- **Row-level security** for multi-tenant scenarios
- **Audit logging** for all sensitive operations

### Access Control:
- **Role-based access control** (RBAC)
- **API rate limiting**
- **Input validation and sanitization**
- **SQL injection prevention**

## 🌐 Web Portal Login System

### Frontend Authentication Flow:

```javascript
// Login component for public/index.html
class LoginManager {
  async login(credentials) {
    try {
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
      });
      
      if (!response.ok) {
        throw new Error('Login failed');
      }
      
      const data = await response.json();
      
      // Store JWT token
      localStorage.setItem('authToken', data.token);
      localStorage.setItem('userRole', data.user.role);
      localStorage.setItem('userData', JSON.stringify(data.user));
      
      // Redirect based on role
      this.redirectBasedOnRole(data.user.role);
      
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }
  
  redirectBasedOnRole(role) {
    switch (role) {
      case 'admin':
        window.location.href = '/admin/dashboard';
        break;
      case 'developer':
        window.location.href = '/developer/dashboard';
        break;
      case 'agent':
        window.location.href = '/agent/dashboard';
        break;
      default:
        window.location.href = '/dashboard';
    }
  }
  
  async logout() {
    try {
      await fetch('/api/v1/auth/logout', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        }
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear local storage
      localStorage.removeItem('authToken');
      localStorage.removeItem('userRole');
      localStorage.removeItem('userData');
      
      // Redirect to login
      window.location.href = '/login';
    }
  }
  
  isAuthenticated() {
    const token = localStorage.getItem('authToken');
    return !!token && !this.isTokenExpired(token);
  }
  
  isTokenExpired(token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp * 1000 < Date.now();
    } catch (error) {
      return true;
    }
  }
}
```

### Role-Based Dashboard Access:

```javascript
// Dashboard access control
class DashboardManager {
  constructor() {
    this.userRole = localStorage.getItem('userRole');
    this.userData = JSON.parse(localStorage.getItem('userData') || '{}');
  }
  
  initializeDashboard() {
    // Hide/show elements based on role
    this.setupRoleBasedUI();
    
    // Load appropriate data
    this.loadDashboardData();
  }
  
  setupRoleBasedUI() {
    const elements = document.querySelectorAll('[data-role]');
    
    elements.forEach(element => {
      const requiredRoles = element.dataset.role.split(',');
      
      if (!requiredRoles.includes(this.userRole)) {
        element.style.display = 'none';
      }
    });
  }
  
  async loadDashboardData() {
    switch (this.userRole) {
      case 'admin':
        await this.loadAdminDashboard();
        break;
      case 'developer':
        await this.loadDeveloperDashboard();
        break;
      case 'agent':
        await this.loadAgentDashboard();
        break;
    }
  }
  
  async loadAdminDashboard() {
    // Load system-wide analytics
    const analytics = await this.fetchAnalytics();
    this.displayAdminMetrics(analytics);
    
    // Load user management
    const users = await this.fetchUsers();
    this.displayUserManagement(users);
    
    // Load API key management
    const apiKeys = await this.fetchApiKeys();
    this.displayApiKeyManagement(apiKeys);
  }
  
  async loadDeveloperDashboard() {
    // Load development tools
    const autoReplies = await this.fetchAutoReplies();
    this.displayAutoReplyManager(autoReplies);
    
    // Load API usage
    const apiUsage = await this.fetchApiUsage();
    this.displayApiUsage(apiUsage);
  }
  
  async loadAgentDashboard() {
    // Load message management
    const messages = await this.fetchMessages();
    this.displayMessageManager(messages);
    
    // Load contact management
    const contacts = await this.fetchContacts();
    this.displayContactManager(contacts);
  }
}
```

## 📋 API Endpoints Summary

### Authentication Endpoints:
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout
- `POST /api/v1/auth/refresh` - Refresh JWT token
- `GET /api/v1/auth/profile` - Get user profile

### User Management Endpoints:
- `GET /api/v1/users` - List users (admin only)
- `POST /api/v1/users` - Create user (admin only)
- `PUT /api/v1/users/:id` - Update user (admin only)
- `DELETE /api/v1/users/:id` - Delete user (admin only)

### API Key Management Endpoints:
- `GET /api/v1/api-keys` - List API keys
- `POST /api/v1/api-keys` - Generate new API key
- `PUT /api/v1/api-keys/:id` - Update API key
- `DELETE /api/v1/api-keys/:id` - Revoke API key
- `GET /api/v1/api-keys/:id/analytics` - API key usage analytics

### Auto-Reply Endpoints:
- `GET /api/v1/auto-replies` - List auto-reply rules
- `POST /api/v1/auto-replies` - Create auto-reply rule
- `PUT /api/v1/auto-replies/:id` - Update auto-reply rule
- `DELETE /api/v1/auto-replies/:id` - Delete auto-reply rule
- `GET /api/v1/auto-replies/:id/analytics` - Rule usage analytics

This architecture provides a robust, scalable foundation for your WhatsApp bot with authentication, auto-replies, API key management, and ML capabilities. The system supports three distinct user roles with appropriate access controls and provides both web portal and API access methods.

Would you like me to start implementing any specific part of this plan? 
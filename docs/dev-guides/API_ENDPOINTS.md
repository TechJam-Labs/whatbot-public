<!--
 * WhatBot v1.2.0
 * Location: docs\dev-guides\API_ENDPOINTS.md
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

# WhatBot API Endpoints Documentation

## Endpoint Categories

### 1. **Web Portal Endpoints** (JWT Authentication)
These endpoints are for the web portal interface and use JWT tokens for authentication.

#### Authentication Routes
- `POST /api/auth/login` - User login (email/password)
- `GET /api/auth/status` - Check authentication status
- `POST /api/auth/logout` - User logout

#### Web Portal Pages
- `GET /` - Login page (default route)
- `GET /dashboard` - Admin dashboard (requires JWT)
- `GET /setup-whatsapp` - WhatsApp setup page (requires JWT + admin role)
- `GET /index.html` - Original portal (requires JWT)
- `GET /logout` - Logout page (clears token and redirects)

### 2. **WhatsApp Management Endpoints** (JWT Authentication)
These endpoints manage the WhatsApp connection and are accessed through the web portal.

- `GET /api/v1/status` - Check WhatsApp connection status
- `GET /api/v1/qrcode` - Get QR code for WhatsApp authentication
- `POST /api/v1/init` - Initialize WhatsApp connection
- `POST /api/v1/logout` - Disconnect WhatsApp (not user logout)

### 3. **Public API Endpoints** (API Key Authentication)
These endpoints are for external integrations and use API keys for authentication.

#### Message Management
- `POST /api/v1/send` - Send a single message
- `POST /api/v1/broadcast` - Send broadcast messages
- `POST /api/v1/throttled-broadcast` - Send throttled broadcast messages
- `GET /api/v1/messages` - Get message history
- `DELETE /api/v1/messages/:id` - Delete a message

#### Contact Management
- `GET /api/v1/contacts` - Get contact list
- `POST /api/v1/contacts` - Add new contacts
- `PUT /api/v1/contacts/:id` - Update contact
- `DELETE /api/v1/contacts/:id` - Delete contact
- `POST /api/v1/contacts/upload` - Upload contacts from CSV

#### Auto-Reply Management
- `GET /api/v1/auto-replies` - Get auto-reply rules
- `POST /api/v1/auto-replies` - Create auto-reply rule
- `PUT /api/v1/auto-replies/:id` - Update auto-reply rule
- `DELETE /api/v1/auto-replies/:id` - Delete auto-reply rule

#### System Management
- `GET /api/v1/status` - Get system status
- `GET /api/v1/health` - Health check endpoint

## Authentication Methods

### JWT Authentication (Web Portal)
```javascript
// Headers required
{
  'Authorization': 'Bearer <jwt_token>',
  'Content-Type': 'application/json'
}
```

### API Key Authentication (Public API)
```javascript
// Headers required
{
  'X-API-Key': '<api_key>',
  'Content-Type': 'application/json'
}
```

## Usage Examples

### Web Portal (JWT)
```javascript
// Login
const response = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'user@example.com', password: 'password' })
});

// Use JWT token for subsequent requests
const token = response.data.token;
const statusResponse = await fetch('/api/v1/status', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

### Public API (API Key)
```javascript
// Send message using API key
const response = await fetch('/api/v1/send', {
  method: 'POST',
  headers: {
    'X-API-Key': 'your_api_key_here',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    to: '+1234567890',
    message: 'Hello from API!'
  })
});
```

## Security Considerations

1. **JWT Tokens**: Used for web portal authentication, expire after 24 hours
2. **API Keys**: Used for external integrations, can have different permissions and rate limits
3. **Rate Limiting**: Applied to both authentication methods
4. **CORS**: Configured for web portal access
5. **Input Validation**: All endpoints validate input data

## Error Responses

### Authentication Errors
```json
{
  "error": "Access denied",
  "message": "No token provided",
  "code": "NO_TOKEN"
}
```

### Validation Errors
```json
{
  "error": "Validation failed",
  "message": "Phone number is required",
  "code": "VALIDATION_ERROR"
}
```

### Server Errors
```json
{
  "error": "Internal server error",
  "message": "Database connection failed",
  "code": "DB_ERROR"
}
```

## Rate Limiting

- **Web Portal**: 100 requests per hour per IP
- **Public API**: Configurable per API key (default: 1000 requests per hour)
- **Authentication**: 5 login attempts per 15 minutes per IP

## Development Notes

- All endpoints return JSON responses
- HTTP status codes follow REST conventions
- Error messages are user-friendly
- Success responses include relevant data
- All timestamps are in ISO 8601 format 
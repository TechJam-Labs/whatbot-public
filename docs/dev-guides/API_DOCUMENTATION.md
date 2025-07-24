<!--
 * WhatBot v1.2.0
 * Location: docs\dev-guides\API_DOCUMENTATION.md
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

# WhatBot API Documentation v1.0

## Overview

WhatBot is a comprehensive WhatsApp automation platform built with Node.js, Express, and venom-bot. It provides enterprise-grade messaging, broadcasting, contact management, and real-time interaction capabilities.

**Base URL:** `http://localhost:41100` (or your configured domain)

**API Version:** `v1`

**Authentication:** API key required for most endpoints (except WhatsApp initialization)

**Rate Limiting:** 
- General endpoints: 100 requests per 15 minutes
- Sensitive operations: 30 requests per 15 minutes  
- Authentication endpoints: 10 requests per 15 minutes

---

## Table of Contents

1. [Authentication & Security](#authentication--security)
2. [Connection & Session Management](#connection--session-management)
3. [Message Sending](#message-sending)
4. [Broadcasting](#broadcasting)
5. [Media Handling](#media-handling)
6. [Contact Management](#contact-management)
7. [Contact Group Management](#contact-group-management)
8. [Message Reading & Interaction](#message-reading--interaction)
9. [Queue & Scheduling](#queue--scheduling)
10. [Configuration & Status](#configuration--status)
11. [Error Handling](#error-handling)

---

## Authentication & Security

### API Key Authentication

Most endpoints require an API key to be included in the request header:

```bash
curl -H "X-API-Key: your_api_key_here" http://localhost:41100/api/v1/endpoint
```

### Sample API Keys (for testing)

```bash
# Admin Key (365 days) - Full Access
whatbot_admin_1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef

# User Key (90 days) - Standard Access  
whatbot_user_abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890

# Temp Key (30 days) - Limited Access
whatbot_temp_7890abcdef1234567890abcdef1234567890abcdef1234567890abcdef123456
```

### Public Endpoints (No API Key Required)
- `GET /api/v1/status` - WhatsApp connection status
- `GET /api/v1/qrcode` - Get QR code for authentication
- `POST /api/v1/init` - Initialize WhatsApp connection

### Protected Endpoints (API Key Required)
- All other endpoints require a valid API key

### Rate Limiting Tiers
- **General API endpoints**: 100 requests per 15 minutes
- **Sensitive operations** (send/broadcast): 30 requests per 15 minutes
- **Authentication endpoints**: 10 requests per 15 minutes

### Security Features
- API key expiry tracking
- Role-based access (Admin/User/Temp)
- Rate limiting to prevent abuse
- Sanitized responses to prevent information disclosure
- Proper HTTP status codes and error messages

---

## Connection & Session Management

### 1. Get API Key Status

**Endpoint:** `GET /api/v1/auth/status`

**Description:** Get API key authentication status and configuration (requires API key).

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Response:**
```json
{
  "success": true,
  "apiKeyRequired": true,
  "totalKeys": 3,
  "activeKeys": 3,
  "message": "API key authentication is enabled"
}
```

---

### 2. Get Connection Status

**Endpoint:** `GET /api/v1/status`

**Description:** Check WhatsApp connection status and configured phone number.

**Response:**
```json
{
  "status": "connected",
  "phone": "+2349157342656",
  "configuredNumber": "+2349157342656",
  "sessionNumber": null,
  "qrReady": false,
  "clientExists": true,
  "lastConnected": "2023-12-21T10:30:00.000Z"
}
```

**Status Values:**
- `disconnected` - Not connected
- `initializing` - Connecting to WhatsApp
- `qr_ready` - QR code available for scanning
- `connected` - Successfully connected
- `CONNECTED` - Alternative connected state
- `error` - Connection error

---

### 3. Get QR Code

**Endpoint:** `GET /api/v1/qrcode`

**Description:** Get QR code for WhatsApp Web authentication.

**Response (QR Ready):**
```json
{
  "qrcode": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```

**Response (Already Connected):**
```json
{
  "status": "connected",
  "message": "WhatsApp is already connected"
}
```

---

### 4. Initialize WhatsApp

**Endpoint:** `POST /api/v1/init`

**Description:** Initialize WhatsApp client connection.

**Request Body:** Empty

**Response:**
```json
{
  "status": "initializing",
  "message": "WhatsApp initialization started"
}
```

---

### 5. Clear Session

**Endpoint:** `POST /api/v1/clear-session`

**Description:** Clear WhatsApp session data and disconnect without reinitializing.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Request Body:** Empty

**Response:**
```json
{
  "success": true,
  "message": "Session cleared successfully. You can now reinitialize WhatsApp.",
  "status": "disconnected"
}
```

---

### 6. Logout

**Endpoint:** `POST /api/v1/logout`

**Description:** Logout and disconnect WhatsApp session.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Request Body:** Empty

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

### 7. Re-initialize

**Endpoint:** `POST /api/v1/reinitialize`

**Description:** Force re-initialization and session reset.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Request Body:** Empty

**Response:**
```json
{
  "success": true,
  "message": "WhatsApp re-initialization started. Please scan the new QR code.",
  "status": "initializing"
}
```

---

## Message Sending

### 8. Send Single Message

**Endpoint:** `POST /api/v1/send`

**Description:** Send a text message to a single phone number.

**Headers Required:**
```
X-API-Key: your_api_key_here
Content-Type: application/json
```

**Request Body:**
```json
{
  "phone": "+2348012345678",
  "message": "Hello! This is a test message."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Message sent successfully",
  "result": {
    "id": {
      "fromMe": true,
      "remote": "2348012345678@c.us",
      "id": "3EB0C767D82B8B6F",
      "_serialized": "true_2348012345678@c.us_3EB0C767D82B8B6F"
    }
  }
}
```

---

### 9. Send Media to Single Contact

**Endpoint:** `POST /api/v1/send-media`

**Description:** Send a media file to a single phone number.

**Headers Required:**
```
X-API-Key: your_api_key_here
Content-Type: multipart/form-data
```

**Form Fields:**
- `phone` (string): Phone number with country code
- `caption` (string, optional): Caption for the media
- `media` (file): Media file (images, videos, documents)

**Response:**
```json
{
  "success": true,
  "message": "Media sent successfully",
  "result": {
    "id": {
      "fromMe": true,
      "remote": "2348012345678@c.us",
      "id": "3EB0C767D82B8B6F",
      "_serialized": "true_2348012345678@c.us_3EB0C767D82B8B6F"
    }
  }
}
```

---

## Broadcasting

### 10. Send Broadcast Message

**Endpoint:** `POST /api/v1/broadcast`

**Description:** Send a text message to multiple phone numbers.

**Headers Required:**
```
X-API-Key: your_api_key_here
Content-Type: application/json
```

**Request Body:**
```json
{
  "phones": ["+2348012345678", "+2348023456789", "+2348034567890"],
  "message": "Hello! This is a broadcast message."
}
```

**Response:**
```json
{
  "success": true,
  "totalSent": 3,
  "totalFailed": 0,
  "results": [
    {
      "phone": "+2348012345678",
      "status": "sent",
      "result": {
        "id": {
          "fromMe": true,
          "remote": "2348012345678@c.us",
          "id": "3EB0C767D82B8B6F",
          "_serialized": "true_2348012345678@c.us_3EB0C767D82B8B6F"
        }
      }
    }
  ],
  "errors": []
}
```

---

### 11. Send Media Broadcast

**Endpoint:** `POST /api/v1/broadcast-media`

**Description:** Send a media file to multiple phone numbers.

**Headers Required:**
```
X-API-Key: your_api_key_here
Content-Type: multipart/form-data
```

**Form Fields:**
- `phones` (string): JSON array of phone numbers or comma-separated
- `caption` (string, optional): Caption for the media
- `media` (file): Media file

**Response:**
```json
{
  "success": true,
  "totalSent": 3,
  "totalFailed": 0,
  "mediaFile": {
    "originalName": "image.jpg",
    "mimeType": "image/jpeg",
    "size": 102400
  },
  "results": [
    {
      "phone": "+2348012345678",
      "status": "sent",
      "result": {
        "id": {
          "fromMe": true,
          "remote": "2348012345678@c.us",
          "id": "3EB0C767D82B8B6F",
          "_serialized": "true_2348012345678@c.us_3EB0C767D82B8B6F"
        }
      }
    }
  ],
  "errors": []
}
```

---

### 12. Queue Media Broadcast (Large Scale)

**Endpoint:** `POST /api/v1/broadcast-media-batch`

**Description:** Queue a large media broadcast for batch processing with safety limits.

**Headers Required:**
```
X-API-Key: your_api_key_here
Content-Type: multipart/form-data
```

**Form Fields:**
- `phones` (string): JSON array of phone numbers
- `caption` (string, optional): Caption for the media
- `batchSize` (number, optional): Messages per batch (default: 50)
- `enableSafeMode` (boolean, optional): Enable safety limits (default: true)
- `media` (file): Media file

**Response:**
```json
{
  "success": true,
  "jobId": "1703123456789",
  "totalContacts": 500,
  "totalBatches": 10,
  "batchSize": 50,
  "estimatedCompletionTime": "50 minutes",
  "queuePosition": 1,
  "message": "Media broadcast queued for processing. Use /api/v1/broadcast-status/:jobId to check progress."
}
```

---

### 13. Get Broadcast Status

**Endpoint:** `GET /api/v1/broadcast-status/:jobId`

**Description:** Check status and progress of a broadcast job.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Response:**
```json
{
  "jobId": "1703123456789",
  "status": "processing",
  "totalContacts": 500,
  "processed": 150,
  "successful": 145,
  "failed": 5,
  "progress": 30,
  "createdAt": "2023-12-21T10:30:00.000Z",
  "estimatedTimeRemaining": "35 minutes"
}
```

---

### 14. Cancel Broadcast Job

**Endpoint:** `POST /api/v1/broadcast-cancel/:jobId`

**Description:** Cancel a queued broadcast job.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Request Body:** Empty

**Response:**
```json
{
  "success": true,
  "message": "Broadcast job 1703123456789 cancelled successfully"
}
```

---

### 15. Throttled Broadcast

**Endpoint:** `POST /api/v1/throttled-broadcast`

**Description:** Schedule a throttled media broadcast with anti-ban protection.

**Headers Required:**
```
X-API-Key: your_api_key_here
Content-Type: multipart/form-data
```

**Form Fields:**
- `phones` (string): JSON array of phone numbers
- `caption` (string, optional): Caption for the media
- `messagesPerBatch` (number, optional): Messages per batch (default: 150)
- `batchIntervalHours` (number, optional): Hours between batches (default: 2)
- `throttleDelaySeconds` (number, optional): Seconds between messages (default: 15)
- `staggerMinutes` (number, optional): Random stagger in minutes (default: 5)
- `startImmediately` (boolean, optional): Start immediately (default: false)
- `media` (file): Media file

**Response:**
```json
{
  "success": true,
  "jobId": "1703123456789",
  "totalContacts": 1000,
  "totalBatches": 7,
  "messagesPerBatch": 150,
  "batchIntervalHours": 2,
  "throttleDelaySeconds": 15,
  "startDate": "2023-12-21T09:00:00.000Z",
  "endDate": "2023-12-21T23:00:00.000Z",
  "estimatedDuration": "14 hours",
  "schedule": {
    "totalBatches": 7,
    "messagesPerBatch": 150,
    "batchIntervalHours": 2,
    "throttleDelaySeconds": 15,
    "totalEstimatedHours": 14
  },
  "message": "Throttled broadcast scheduled: 150 messages every 2 hours with 15s delays"
}
```

---

## Contact Management

### 16. Upload Contacts

**Endpoint:** `POST /api/v1/contacts/upload`

**Description:** Upload and parse contacts from CSV, TXT, or JSON files.

**Headers Required:**
```
X-API-Key: your_api_key_here
Content-Type: multipart/form-data
```

**Form Fields:**
- `contactFile` (file): Contact file (CSV, TXT, JSON)
- `groupName` (string, optional): Group name for contacts (default: customers)

**Response:**
```json
{
  "success": true,
  "groupName": "customers",
  "contactsAdded": 150,
  "duplicatesSkipped": 25,
  "totalContacts": 500,
  "message": "Contacts uploaded successfully"
}
```

---

### 17. Get All Contacts

**Endpoint:** `GET /api/v1/contacts`

**Description:** Get all stored contacts and groups.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Query Parameters:**
- `group` (string, optional): Filter by group name
- `search` (string, optional): Search in name, phone, or email
- `limit` (number, optional): Number of contacts to return (default: 100)
- `offset` (number, optional): Number of contacts to skip (default: 0)

**Response:**
```json
{
  "success": true,
  "contacts": [
    {
      "phone": "2348012345678",
      "name": "John Doe",
      "email": "john@example.com",
      "group": "customers",
      "tags": ["vip", "active"],
      "notes": "Premium customer",
      "addedAt": "2023-12-21T10:30:00.000Z",
      "id": "1753111350532rnor5nwev"
    }
  ],
  "groups": [
    {
      "name": "customers",
      "description": "Active customers and clients",
      "contactCount": 150,
      "createdAt": "2023-12-21T10:30:00.000Z"
    },
    {
      "name": "leads",
      "description": "Potential customers and prospects",
      "contactCount": 75,
      "createdAt": "2023-12-21T10:30:00.000Z"
    }
  ],
  "pagination": {
    "total": 225,
    "limit": 100,
    "offset": 0,
    "hasMore": true
  }
}
```

---

### 18. Add Single Contact

**Endpoint:** `POST /api/v1/contacts`

**Description:** Add a new contact manually.

**Headers Required:**
```
X-API-Key: your_api_key_here
Content-Type: application/json
```

**Request Body:**
```json
{
  "phone": "2348012345678",
      "name": "Jane Smith",
      "email": "jane@example.com",
      "group": "customers",
      "tags": ["new"],
      "notes": "Referred by John"
}
```

**Response:**
```json
{
  "success": true,
  "contact": {
    "phone": "2348012345678",
    "name": "Jane Smith",
    "email": "jane@example.com",
    "group": "customers",
    "tags": ["new"],
    "notes": "Referred by John",
    "addedAt": "2023-12-21T10:30:00.000Z",
    "id": "1753111350532abc123def"
  },
  "message": "Contact added successfully"
}
```

---

### 19. Delete Contact

**Endpoint:** `DELETE /api/v1/contacts/:contactId`

**Description:** Remove a contact by ID.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Response:**
```json
{
  "success": true,
  "message": "Contact deleted successfully"
}
```

---

### 20. Purge All Contacts

**Endpoint:** `DELETE /api/v1/contacts/purge-all`

**Description:** Remove all contacts and groups (requires confirmation).

**Headers Required:**
```
X-API-Key: your_api_key_here
Content-Type: application/json
```

**Request Body:**
```json
{
  "confirmationCode": "DELETE_ALL_CONTACTS_2023"
}
```

**Response:**
```json
{
  "success": true,
  "message": "All contacts and groups purged successfully",
  "contactsDeleted": 225,
  "groupsDeleted": 8
}
```

---

### 21. Add Chat Participants to Contacts

**Endpoint:** `POST /api/v1/contacts/from-chat`

**Description:** Add all participants from a WhatsApp chat to contacts.

**Headers Required:**
```
X-API-Key: your_api_key_here
Content-Type: application/json
```

**Request Body:**
```json
{
  "chatId": "2348012345678@c.us",
  "groupName": "chat-contacts",
  "createGroup": false
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully added chat participants to contacts",
  "chatInfo": {
    "id": "2348012345678@c.us",
    "name": "Group Name",
    "isGroup": true,
    "participantsFound": 5
  },
  "groupName": "chat-contacts",
  "contactsAdded": 5,
  "duplicatesSkipped": 0,
  "totalContacts": 15,
  "contacts": [
    {
      "phone": "2348012345678",
        "name": "John Doe",
      "tags": ["admin"]
    }
  ]
}
```

---

### 22. Add Specific Phone from Chat to Contacts

**Endpoint:** `POST /api/v1/contacts/from-chat/:phone`

**Description:** Add a specific phone number from a chat to contacts.

**Headers Required:**
```
X-API-Key: your_api_key_here
Content-Type: application/json
```

**Request Body:**
```json
{
  "chatId": "2348012345678@c.us",
  "groupName": "chat-contacts",
  "name": "John Doe",
  "notes": "Added from support chat"
}
```

**Response:**
```json
{
  "success": true,
  "contact": {
    "phone": "2348012345678",
      "name": "John Doe",
    "email": "",
    "group": "chat-contacts",
    "tags": [],
    "notes": "Added from support chat",
    "addedAt": "2023-12-21T10:30:00.000Z"
  },
  "message": "Contact added successfully",
  "duplicate": false,
  "groupName": "chat-contacts",
  "totalContacts": 16
}
```

---

## Contact Group Management

### 23. Move Contact to Different Group

**Endpoint:** `PUT /api/v1/contacts/:phone/move`

**Description:** Move a single contact from one group to another.

**Headers Required:**
```
X-API-Key: your_api_key_here
Content-Type: application/json
```

**Request Body:**
```json
{
  "newGroup": "customers",
  "oldGroup": "leads"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Contact moved from leads to customers",
  "contact": {
    "phone": "2348012345678",
    "name": "John Doe",
    "oldGroup": "leads",
    "newGroup": "customers",
    "updatedAt": "2023-12-21T10:30:00.000Z"
  },
  "groupStats": {
    "oldGroupCount": 5,
    "newGroupCount": 15
  }
}
```

---

### 24. Move Multiple Contacts to Different Group

**Endpoint:** `PUT /api/v1/contacts/bulk-move`

**Description:** Move multiple contacts from one group to another.

**Headers Required:**
```
X-API-Key: your_api_key_here
Content-Type: application/json
```

**Request Body:**
```json
{
  "phones": ["2348012345678", "2348023456789", "2348034567890"],
  "newGroup": "customers",
  "oldGroup": "leads"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Moved 3 contacts to customers",
  "results": [
    {
      "phone": "2348012345678",
      "name": "John Doe",
      "oldGroup": "leads",
      "newGroup": "customers",
      "status": "moved"
    }
  ],
  "errors": [],
  "summary": {
    "totalRequested": 3,
    "successfullyMoved": 3,
    "failed": 0
  }
}
```

---

### 25. Get Contacts by Group

**Endpoint:** `GET /api/v1/contacts/group/:groupName`

**Description:** Get all contacts in a specific group with pagination.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Query Parameters:**
- `limit` (number, optional): Number of contacts to return (default: 100)
- `offset` (number, optional): Number of contacts to skip (default: 0)

**Response:**
```json
{
  "success": true,
  "group": {
    "name": "customers",
    "description": "Active customers and clients",
    "contactCount": 15
  },
  "contacts": [
    {
      "phone": "2348012345678",
      "name": "John Doe",
      "email": "john@example.com",
      "group": "customers"
    }
  ],
  "pagination": {
    "total": 15,
    "limit": 100,
    "offset": 0,
    "hasMore": false
  }
}
```

---

### 26. Update Group Details

**Endpoint:** `PUT /api/v1/contacts/groups/:groupName`

**Description:** Update group description or rename a group.

**Headers Required:**
```
X-API-Key: your_api_key_here
Content-Type: application/json
```

**Request Body:**
```json
{
  "description": "Updated description for customers group",
  "newName": "active-customers"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Group updated successfully",
  "group": {
    "name": "active-customers",
    "description": "Updated description for customers group",
    "contactCount": 15,
    "updatedAt": "2023-12-21T10:30:00.000Z"
  },
  "contactsUpdated": 15
}
```

---

### 27. Delete Group

**Endpoint:** `DELETE /api/v1/contacts/groups/:groupName`

**Description:** Delete a group and move all contacts to another group (default: customers).

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Query Parameters:**
- `moveToGroup` (string, optional): Group to move contacts to (default: customers)

**Response:**
```json
{
  "success": true,
  "message": "Group 'old-group' deleted. 5 contacts moved to 'customers'",
  "deletedGroup": "old-group",
  "contactsMoved": 5,
  "moveToGroup": "customers"
}
```

---

### 28. Get Group Statistics

**Endpoint:** `GET /api/v1/contacts/groups/:groupName/stats`

**Description:** Get detailed statistics for a specific group.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Response:**
```json
{
  "success": true,
  "group": {
    "name": "customers",
    "description": "Active customers and clients",
    "contactCount": 15
  },
  "stats": {
    "totalContacts": 15,
    "withEmail": 12,
    "withNotes": 8,
    "withTags": 5,
    "recentlyAdded": 3,
    "recentlyUpdated": 2
  },
  "contacts": [
    {
      "phone": "2348012345678",
      "name": "John Doe",
      "email": "john@example.com",
      "addedAt": "2023-12-21T10:30:00.000Z",
      "updatedAt": "2023-12-21T10:30:00.000Z"
    }
  ]
}
```

---

## Message Reading & Interaction

### 29. Get All Messages

**Endpoint:** `GET /api/v1/messages`

**Description:** Get all received messages with filtering and pagination.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Query Parameters:**
- `limit` (number, optional): Number of messages to return (default: 50)
- `offset` (number, optional): Number of messages to skip (default: 0)
- `chatId` (string, optional): Filter by chat ID
- `type` (string, optional): Filter by message type

**Response:**
```json
{
  "messages": [
    {
      "id": "3EB0C767D82B8B6F",
      "from": "2348012345678@c.us",
      "to": "2349157342656@c.us",
      "type": "chat",
      "body": "Hello! How are you?",
      "timestamp": 1703123456789,
      "isGroup": false,
      "chatId": "2348012345678@c.us",
      "sender": {
        "id": "2348012345678@c.us",
        "name": "John Doe",
        "number": "2348012345678"
      },
      "media": null
    }
  ],
  "total": 150,
  "limit": 50,
  "offset": 0
}
```

---

### 30. Get Message Statistics

**Endpoint:** `GET /api/v1/messages/stats`

**Description:** Get message statistics and analytics.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Response:**
```json
{
  "totalMessages": 150,
  "totalChats": 25,
  "messageTypes": {
    "chat": 100,
    "image": 30,
    "video": 10,
    "document": 10
  },
  "recentActivity": 15,
  "lastMessageTime": 1703123456789
}
```

---

### 31. Mark Message as Read

**Endpoint:** `POST /api/v1/messages/:messageId/read`

**Description:** Mark a message as read.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Request Body:** Empty

**Response:**
```json
{
  "success": true,
  "message": "Message marked as read"
}
```

---

### 32. Reply to Message

**Endpoint:** `POST /api/v1/messages/:messageId/reply`

**Description:** Reply to a specific message.

**Headers Required:**
```
X-API-Key: your_api_key_here
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "Thanks for your message! I'll get back to you soon."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Reply sent successfully",
  "result": {
    "id": {
      "fromMe": true,
      "remote": "2348012345678@c.us",
      "id": "3EB0C767D82B8B6F",
      "_serialized": "true_2348012345678@c.us_3EB0C767D82B8B6F"
    }
  }
}
```

---

### 33. Get Chat List

**Endpoint:** `GET /api/v1/chats`

**Description:** Get list of all conversations.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Response:**
```json
{
  "chats": [
    {
      "id": "2348012345678@c.us",
      "name": "John Doe",
      "number": "2348012345678",
      "lastMessage": "Hello! How are you?",
      "lastMessageTime": 1703123456789,
      "messageCount": 25,
      "isGroup": false,
      "unreadCount": 0
    }
  ]
}
```

---

## Queue & Scheduling

### 34. Get Scheduled Broadcasts

**Endpoint:** `GET /api/v1/scheduled-broadcasts`

**Description:** Get list of all scheduled broadcast jobs.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Response:**
```json
{
  "jobs": [
    {
      "id": "1703123456789",
      "status": "scheduled",
      "totalContacts": 1000,
      "totalBatches": 7,
      "processedBatches": 0,
      "progress": 0,
      "successful": 0,
      "failed": 0,
      "startDate": "2023-12-21T09:00:00.000Z",
      "endDate": "2023-12-21T23:00:00.000Z",
      "nextBatch": "2023-12-21T09:00:00.000Z",
      "createdAt": "2023-12-21T08:30:00.000Z"
    }
  ],
  "schedulerRunning": true,
  "totalActiveJobs": 1
}
```

---

### 35. Cancel Scheduled Broadcast

**Endpoint:** `DELETE /api/v1/scheduled-broadcasts/:jobId`

**Description:** Cancel a scheduled broadcast job.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Response:**
```json
{
  "success": true,
  "message": "Scheduled broadcast 1703123456789 cancelled successfully"
}
```

---

### 36. Get Queue State

**Endpoint:** `GET /api/v1/queue-state`

**Description:** Get current state of broadcast and scheduled queues.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Response:**
```json
{
  "broadcastQueue": {
    "totalJobs": 2,
    "isProcessing": true,
    "dailyCount": 150,
    "lastResetDate": "2023-12-21",
    "jobs": [
      {
        "id": "1703123456789",
        "status": "processing",
        "totalContacts": 500,
        "processed": 150,
        "successful": 145,
        "failed": 5,
        "createdAt": "2023-12-21T10:30:00.000Z"
      }
    ]
  },
  "scheduledBroadcasts": {
    "totalJobs": 1,
    "isRunning": true,
    "jobs": [
      {
        "id": "1703123456789",
        "status": "scheduled",
        "totalContacts": 1000,
        "processedBatches": 0,
        "totalBatches": 7,
        "createdAt": "2023-12-21T08:30:00.000Z",
        "startDate": "2023-12-21T09:00:00.000Z",
        "endDate": "2023-12-21T23:00:00.000Z"
      }
    ]
  },
  "persistence": {
    "lastSave": "2023-12-21T10:35:00.000Z",
    "backupExists": true
  }
}
```

---

## Configuration & Status

### 37. Get Configuration

**Endpoint:** `GET /api/v1/config`

**Description:** Get application configuration.

**Headers Required:**
```
X-API-Key: your_api_key_here
```

**Response:**
```json
{
  "baseUrl": "https://whatbot.gomed.ng",
  "whatsappNumber": "+2349157342656",
  "companyName": "GOMED HEALTHCARE",
  "appTitle": "WhatBot"
}
```

---

## Error Handling

### Common Error Format

```json
{
  "error": "Error description",
  "message": "Detailed error message",
  "code": "ERROR_CODE"
}
```

### HTTP Status Codes

- `200` - Success
- `400` - Bad Request (missing parameters, invalid data)
- `401` - Unauthorized (invalid or missing API key)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found (message, chat, or job not found)
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error
- `503` - Service Unavailable (WhatsApp not connected)

### Common Error Codes

- `INVALID_API_KEY` - API key is missing or invalid
- `API_KEY_EXPIRED` - API key has expired
- `RATE_LIMIT_EXCEEDED` - Rate limit exceeded
- `AUTH_RATE_LIMIT_EXCEEDED` - Authentication rate limit exceeded
- `WHATSAPP_NOT_CONNECTED` - WhatsApp client not connected
- `MESSAGE_NOT_FOUND` - Message ID doesn't exist
- `CHAT_NOT_FOUND` - Chat ID doesn't exist
- `CONTACT_NOT_FOUND` - Contact not found
- `GROUP_NOT_FOUND` - Group not found
- `BROADCAST_JOB_NOT_FOUND` - Broadcast job not found

### Rate Limiting Headers

When rate limiting is active, the following headers are included in responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1703123456
Retry-After: 900
```

---

## Testing Examples

### Using curl

```bash
# Test API key status
curl -H "X-API-Key: whatbot_admin_1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef" \
  http://localhost:41100/api/v1/auth/status

# Send a message
curl -X POST http://localhost:41100/api/v1/send \
  -H "X-API-Key: whatbot_admin_1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+2348012345678", "message": "Hello from WhatBot!"}'

# Get contacts
curl -H "X-API-Key: whatbot_admin_1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef" \
  http://localhost:41100/api/v1/contacts

# Upload contacts
curl -X POST http://localhost:41100/api/v1/contacts/upload \
  -H "X-API-Key: whatbot_admin_1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef" \
  -F "contactFile=@contacts.csv" \
  -F "groupName=customers"
```

### Using JavaScript/Fetch

```javascript
const API_KEY = 'whatbot_admin_1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef';
const BASE_URL = 'http://localhost:41100/api/v1';

// Send a message
const response = await fetch(`${BASE_URL}/send`, {
  method: 'POST',
  headers: {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    phone: '+2348012345678',
    message: 'Hello from WhatBot!'
  })
});

const result = await response.json();
console.log(result);
```

---

## Default Contact Groups

The system automatically creates these default contact groups:

- **customers** - Active customers and clients
- **vendors** - Suppliers and service providers  
- **leads** - Potential customers and prospects
- **prospects** - Qualified leads and opportunities
- **partners** - Business partners and collaborators
- **support** - Customer support contacts
- **fulfillment** - Order fulfillment and logistics contacts
- **staff** - Internal team members and employees

---

## Security Best Practices

1. **API Key Management**
   - Use different keys for different environments
   - Rotate keys regularly
   - Never share API keys publicly
   - Use appropriate key types (Admin/User/Temp)

2. **Rate Limiting**
   - Respect rate limits to avoid being blocked
   - Implement exponential backoff for retries
   - Monitor rate limit headers

3. **Error Handling**
   - Always check HTTP status codes
   - Handle rate limiting gracefully
   - Log errors for debugging

4. **Data Validation**
   - Validate phone numbers before sending
   - Check file sizes and types for uploads
   - Sanitize user inputs

---

## Support & Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify API key is correct and not expired
   - Check that API key is included in headers
   - Ensure API key has appropriate permissions

2. **Rate Limiting**
   - Check rate limit headers in responses
   - Implement proper retry logic
   - Consider using different API keys for high-volume operations

3. **WhatsApp Connection**
   - Check connection status via `/api/v1/status`
   - Reinitialize if connection is lost
   - Ensure phone number is properly configured

4. **File Uploads**
   - Check file size (max 10MB)
   - Verify supported file formats
   - Ensure proper multipart/form-data encoding

### Debug Endpoints

- `GET /api/v1/status` - Check WhatsApp connection status
- `GET /api/v1/auth/status` - Check API key configuration
- `GET /api/v1/queue-state` - Monitor queue processing
- `GET /api/v1/messages/stats` - View message statistics

---

## Version History

- **v1.0.0** - Initial release with basic messaging
- **v1.1.0** - Added broadcasting and contact management
- **v1.2.0** - Added message reading and interaction
- **v1.3.0** - Added throttled broadcasting and scheduling
- **v1.4.0** - Enhanced media support and real-time updates
- **v1.5.0** - Added API key authentication and rate limiting
- **v1.6.0** - Added comprehensive contact group management

---

*For technical support, contact your system administrator.* 

*© 2023 TECHJAMLABS Limited - https://techjamlabs.com* 
<!--
 * WhatBot v1.2.0
 * Location: docs\dev-guides\ROLE_BASED_ACCESS_SUMMARY.md
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

# Role-Based Access Control Implementation

## Overview

Implemented comprehensive role-based access control (RBAC) for the WhatBot application, ensuring that different user roles have appropriate access to pages and features.

## Role Definitions

### **Admin Role**
- **Access**: All pages and features
- **Pages**: Dashboard, Messages, Contacts, ML Pipeline, Admin Settings, Setup WhatsApp
- **Features**: Full system administration, API key management, user management

### **Developer Role**
- **Access**: All pages except Admin Settings and Setup WhatsApp
- **Pages**: Dashboard, Messages, Contacts, ML Pipeline
- **Excluded**: Admin Settings, Setup WhatsApp
- **Features**: Development and ML pipeline access, contact management

### **Agent Role**
- **Access**: Dashboard, Messages, Contacts
- **Pages**: Dashboard, Messages, Contacts
- **Excluded**: ML Pipeline, Admin Settings, Setup WhatsApp
- **Features**: Basic dashboard access, message management, contact management

## Implementation Details

### **1. Page-Level Authentication**

#### **Contacts Page (contacts.html)**
```javascript
async checkAuth() {
    // ... authentication check ...
    
    // Check role-based access
    const userRole = data.user.role;
    if (userRole === 'developer') {
        // Developer role: exclude setup-whatsapp
        uiComponents.showError('Access denied. Developer role cannot access this page.');
        window.location.href = '/dashboard';
        return;
    }
}
```

#### **ML Pipeline Page (ml-pipeline.html)**
```javascript
async checkAuth() {
    // ... authentication check ...
    
    // Check role-based access
    const userRole = data.user.role;
    if (userRole === 'developer') {
        // Developer role: exclude setup-whatsapp
        uiComponents.showError('Access denied. Developer role cannot access ML Pipeline.');
        window.location.href = '/dashboard';
        return;
    }
}
```

#### **Messages Page (messages.js)**
```javascript
async function checkAuth() {
    // ... authentication check ...
    
    // Check role-based access
    const userRole = data.user.role;
    if (userRole === 'developer') {
        // Developer role: exclude setup-whatsapp
        uiComponents.showError('Access denied. Developer role cannot access this page.');
        window.location.href = '/dashboard';
        return;
    }
}
```

#### **Admin Settings Page (admin-settings.js)**
```javascript
// Check if user is admin
if (data.user.role !== 'admin') {
    this.showError('Access denied. Admin privileges required.');
    window.location.href = '/dashboard';
    return;
}
```

### **2. Dashboard Role-Based Cards**

#### **Updated Dashboard (dashboard.html)**
```javascript
showRoleBasedCards() {
    switch (this.userRole) {
        case 'admin':
            // Admin: access to all pages
            document.getElementById('adminCard').classList.remove('hidden');
            document.getElementById('contactsCard').classList.remove('hidden');
            document.getElementById('mlPipelineCard').classList.remove('hidden');
            break;
        case 'developer':
            // Developer: exclude admin-settings and setup-whatsapp
            document.getElementById('contactsCard').classList.remove('hidden');
            document.getElementById('mlPipelineCard').classList.remove('hidden');
            break;
        case 'agent':
            // Agent: access to dashboard, messages, contacts
            document.getElementById('contactsCard').classList.remove('hidden');
            break;
    }
}
```

### **3. Navigation Menu Role-Based Visibility**

#### **Updated Header Component (components.js)**
```javascript
createHeader(userInfo = null, currentPage = '') {
    // Determine which navigation items to show based on user role
    const userRole = userInfo ? userInfo.role : null;
    const showMLPipeline = userRole === 'admin' || userRole === 'developer';
    const showAdminSettings = userRole === 'admin';
    const showSetupWhatsapp = userRole === 'admin';
    
    // Conditional rendering in navigation menu
    ${showMLPipeline ? `
    <a href="/ml-pipeline">ML Pipeline</a>
    ` : ''}
    ${showSetupWhatsapp ? `
    <a href="/setup-whatsapp">Setup WhatsApp</a>
    ` : ''}
    ${showAdminSettings ? `
    <a href="/admin-settings">Admin Settings</a>
    ` : ''}
}
```

### **4. API Key Deletion Refresh**

#### **Enhanced Admin Settings (admin-settings.js)**
```javascript
async deleteApiKey(keyId) {
    // ... deletion logic ...
    
    if (response.ok) {
        uiComponents.showSuccess('API key deleted successfully');
        // Refresh API keys table and system stats
        await this.loadApiKeys();
        await this.loadSystemStats();
        // Also refresh the active API keys count in the stats section
        await this.refreshStats();
    }
}
```

## Access Matrix

| Page | Admin | Developer | Agent |
|------|-------|-----------|-------|
| Dashboard | ✅ | ✅ | ✅ |
| Messages | ✅ | ✅ | ✅ |
| Contacts | ✅ | ✅ | ✅ |
| ML Pipeline | ✅ | ✅ | ❌ |
| Admin Settings | ✅ | ❌ | ❌ |
| Setup WhatsApp | ✅ | ❌ | ❌ |

## Security Features

### **1. Authentication Requirements**
- All protected pages require valid JWT authentication
- Invalid or missing tokens redirect to login page
- Proper token cleanup on logout

### **2. Role Validation**
- Server-side role validation in authentication endpoints
- Client-side role checks for immediate feedback
- Graceful error handling with user-friendly messages

### **3. Navigation Security**
- Role-based navigation menu visibility
- Hidden navigation items for unauthorized roles
- Consistent access control across desktop and mobile

### **4. Page Protection**
- Direct URL access blocked for unauthorized roles
- Automatic redirects to dashboard for denied access
- Clear error messages explaining access restrictions

## Testing

### **Comprehensive Test Suite**
- **test-role-based-access.js**: Tests all role combinations and page access
- **test-authentication-requirements.js**: Verifies JWT requirements
- **test-dashboard-loop.js**: Ensures dashboard stability

### **Test Coverage**
- ✅ Role-based page access
- ✅ Navigation menu visibility
- ✅ Dashboard card display
- ✅ API key deletion refresh
- ✅ Authentication requirements
- ✅ Token invalidation
- ✅ Error handling

## User Experience

### **Admin Users**
- Full access to all features and pages
- Complete system administration capabilities
- API key management with automatic refresh

### **Developer Users**
- Access to development and ML features
- Contact and message management
- Excluded from administrative functions and WhatsApp setup

### **Agent Users**
- Access to dashboard, messages, and contacts
- Basic message and contact management
- Excluded from ML pipeline, admin settings, and WhatsApp setup

## Error Handling

### **Access Denied Messages**
```javascript
// Developer trying to access restricted page
uiComponents.showError('Access denied. Developer role cannot access this page.');

// Non-admin trying to access admin settings
this.showError('Access denied. Admin privileges required.');

// Non-admin trying to access setup-whatsapp
console.log('Access denied. Only admin can access setup-whatsapp.');
```

### **Graceful Redirects**
- Unauthorized access redirects to dashboard
- Clear feedback before redirect
- Maintains user session for valid operations

## Performance Considerations

### **Efficient Role Checking**
- Role validation happens once per page load
- Cached role information in user object
- Minimal overhead for access control

### **Optimized Navigation**
- Conditional rendering based on role
- No unnecessary DOM elements for hidden items
- Responsive design maintained across roles

## Future Enhancements

### **Potential Improvements**
1. **Dynamic Role Assignment**: Allow admins to modify user roles
2. **Feature-Level Permissions**: Granular control over specific features
3. **Audit Logging**: Track access attempts and role changes
4. **Session Management**: Enhanced session security and timeout handling

### **Scalability**
- Role system designed for easy expansion
- Modular permission checking
- Database-driven role management ready

## Conclusion

The role-based access control system provides:

1. **Security**: Proper authentication and authorization
2. **Usability**: Clear navigation and access feedback
3. **Maintainability**: Modular and extensible design
4. **Performance**: Efficient role checking and rendering
5. **User Experience**: Appropriate access levels for each role

All pages now require valid JWT authentication, and role-based restrictions ensure users only access appropriate features based on their assigned role. 
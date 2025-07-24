# WhatBot v1.2.0 - Test Environment Setup Guide

## Overview

WhatBot now supports a flexible test environment configuration that allows developers to use API keys from the `.env` file for testing purposes. This feature is particularly useful for development and testing scenarios where you want to avoid hardcoding API keys in test scripts.

## Features

- **Environment-based API Keys**: Use `TEST_API_KEY` from `.env` file
- **Flexible Configuration**: Fallback to hardcoded values if `.env` is not available
- **Development Mode**: Automatic detection of development/test environment
- **Secure Testing**: Separate test API keys for development vs production

## Quick Setup

### 1. Setup Test Environment

```bash
# Run the test environment setup script
npm run test:setup
```

This script will:
- Create a `.env` file from the template
- Generate a secure test API key
- Configure test phone numbers
- Set environment to development mode

### 2. Manual Configuration

If you prefer to configure manually, add these variables to your `.env` file:

```bash
# Testing Configuration
TEST_API_KEY=your_generated_test_api_key_here
TEST_PHONE_1=08099999928
TEST_PHONE_2=08186528892
TEST_BASE_URL=http://localhost:41100
NODE_ENV=development
```

### 3. Generate Test API Key

You can generate a test API key using the existing API key generation script:

```bash
# Generate a new API key for testing
node scripts/utils/generate-api-keys.js
```

## Authentication Flow

The updated `combinedAuth` middleware now follows this priority order:

1. **API Key from Request Header** - `X-API-Key` or `api-key` header
2. **JWT Token** - `Authorization: Bearer <token>` header
3. **TEST_API_KEY from .env** - Only in development/test environment
4. **Authentication Required** - Returns 401 if no valid auth found

### Development Mode Detection

The middleware automatically detects development mode when:
- `NODE_ENV=development` or `NODE_ENV=test`
- `TEST_API_KEY` is present in `.env`

## Using the Test Environment

### 1. API Testing Script

The comprehensive API testing script now automatically loads configuration from `.env`:

```bash
# Run comprehensive API tests
cd scripts/api-test
./api-test-comprehensive.sh
```

The script will:
- Load `TEST_API_KEY` from `.env`
- Use `TEST_PHONE_1` and `TEST_PHONE_2` for testing
- Use `TEST_BASE_URL` for API endpoints
- Fall back to hardcoded values if `.env` is not available

### 2. Manual API Testing

You can test API endpoints manually using the test API key:

```bash
# Test with curl
curl -X GET "http://localhost:41100/api/v1/status" \
  -H "X-API-Key: your_test_api_key_here"

# Test without API key (uses TEST_API_KEY from .env in dev mode)
curl -X GET "http://localhost:41100/api/v1/status"
```

### 3. Programmatic Testing

In your test scripts, you can access the test configuration:

```javascript
// Load environment variables
require('dotenv').config();

const testConfig = {
  apiKey: process.env.TEST_API_KEY,
  baseUrl: process.env.TEST_BASE_URL || 'http://localhost:41100',
  testPhone1: process.env.TEST_PHONE_1 || '08099999928',
  testPhone2: process.env.TEST_PHONE_2 || '08186528892'
};

// Use in your tests
const response = await fetch(`${testConfig.baseUrl}/api/v1/status`, {
  headers: {
    'X-API-Key': testConfig.apiKey
  }
});
```

## Security Considerations

### Development vs Production

- **Development**: `TEST_API_KEY` is automatically used when no auth is provided
- **Production**: Strict authentication required, no fallback to test keys

### Environment Variables

- Keep `.env` file secure and never commit to version control
- Use different API keys for development and production
- Rotate test API keys regularly

### API Key Management

- Test API keys should have limited permissions
- Use the API key management system for production keys
- Monitor API key usage and revoke unused keys

## Troubleshooting

### Common Issues

1. **Test API Key Not Working**
   - Ensure `NODE_ENV=development` in `.env`
   - Verify `TEST_API_KEY` is properly set
   - Check that the API key exists in the database

2. **Environment Variables Not Loading**
   - Ensure `.env` file is in the project root
   - Check file permissions
   - Verify variable names are correct

3. **Authentication Still Required**
   - Confirm you're in development mode
   - Check that `TEST_API_KEY` is valid
   - Verify the middleware is properly configured

### Debug Commands

```bash
# Check environment variables
node -e "require('dotenv').config(); console.log(process.env.TEST_API_KEY)"

# Test API key validation
node scripts/utils/check-api-keys.js

# Check authentication status
curl -X GET "http://localhost:41100/api/v1/auth/status"
```

## Best Practices

### Development Workflow

1. **Setup**: Run `npm run test:setup` to configure test environment
2. **Development**: Use `NODE_ENV=development` for local development
3. **Testing**: Use comprehensive test scripts for API validation
4. **Production**: Use proper API keys with appropriate permissions

### Configuration Management

- Use environment-specific `.env` files
- Keep sensitive data out of version control
- Document configuration requirements
- Use secure key generation methods

### Testing Strategy

- Test with real API keys in development
- Use mock data for unit tests
- Validate authentication flows
- Test error scenarios and edge cases

## Migration from Hardcoded Keys

If you're migrating from hardcoded API keys in test scripts:

1. **Update Scripts**: Replace hardcoded keys with environment variables
2. **Setup Environment**: Run `npm run test:setup`
3. **Test Configuration**: Verify all tests work with new setup
4. **Update Documentation**: Document the new configuration approach

## Support

For issues or questions about the test environment setup:

- **Email**: ben@techjamlabs.com
- **Phone**: +2348099999928
- **Documentation**: Check other guides in `docs/dev-guides/`
- **Issues**: Create GitHub issue or contact support

---

**Last Updated**: June 21, 2025  
**Version**: WhatBot v1.2.0 
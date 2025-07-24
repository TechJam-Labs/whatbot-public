<!--
 * WhatBot v1.2.0
 * Location: docs\dev-guides\PROJECT_STRUCTURE.md
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

<!--
 * WhatBot v1.2.0
 * Location: docs/dev-guides/PROJECT_STRUCTURE.md
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

# WhatBot Project Structure

## 📁 Directory Organization

### Root Directory
```
gomed/
├── server.js                 # Main application server
├── package.json             # Node.js dependencies and scripts
├── .env                     # Environment variables
├── README.md               # Project overview
├── .gitignore              # Git ignore rules
├── ecosystem.config.js     # PM2 configuration
├── queue-state.json        # Message queue state
├── broadcast-history.json  # Broadcast history
└── uploads/                # File uploads directory
```

### 📁 scripts/ - Scripts and Utilities
```
scripts/
├── api-test/               # API testing suite
│   ├── test-essential.js   # Essential API tests
│   ├── api-keys.json       # Test API keys
│   ├── daystar.jpg         # Sample image for testing
│   ├── sample-audio.mp3    # Sample audio for testing
│   ├── sample-video.mp4    # Sample video for testing
│   └── sample-image.png    # Sample image for testing
├── test/                   # Test scripts
│   ├── test-essential.js   # Main test suite
│   ├── test-quick-health.js # Quick health check
│   └── ...                 # Other test files
├── utils/                  # Utility scripts
│   ├── enhanced-session-manager.js # Session management
│   ├── fix-environment.js  # Environment fixes
│   ├── check-users.js      # User verification
│   └── ...                 # Other utilities
├── setup/                  # Setup scripts
│   ├── setup-postgres.js   # PostgreSQL setup
│   ├── setup-auto-replies.js # Auto-replies setup
│   └── setup-git.sh        # Git setup
└── deployment/             # Deployment scripts
    ├── deploy.sh           # Main deployment
    ├── deploy-ubuntu.sh    # Ubuntu deployment
    └── monitor-ubuntu.sh   # Ubuntu monitoring
```

### 📁 database/ - Database Files
```
database/
├── schema.sql             # Database schema
├── setup-database.sql     # Database setup
├── migrate-*.sql          # Migration scripts
├── contacts.json          # Contacts data
└── migrate-contacts-to-database.js # Contact migration
```

### 📁 docs/ - Documentation
```
docs/
└── dev-guides/            # Development guides
    ├── API_DOCUMENTATION.md # API documentation
    ├── DATABASE_ARCHITECTURE_PLAN.md # Database design
    ├── DEPLOYMENT_GUIDE.md # Deployment instructions
    ├── POSTGRES_SETUP_GUIDE.md # PostgreSQL setup
    ├── SCHEDULING_GUIDE.md # Message scheduling
    ├── TROUBLESHOOTING_GUIDE.md # Troubleshooting
    ├── UBUNTU_PRODUCTION_GUIDE.md # Production setup
    ├── WHATSAPP_TROUBLESHOOTING.md # WhatsApp issues
    ├── API_ENDPOINTS.md # API endpoints
    ├── ADMIN_ACCOUNTS.md # Admin account management
    ├── DATABASE_MIGRATION.md # Database migration
    ├── ROLE_BASED_ACCESS_SUMMARY.md # Access control
    └── UPDATED_ROLE_ACCESS_SUMMARY.md # Updated access
```

### 📁 public/ - Frontend Files
```
public/
├── index.html             # Main page
├── login.html             # Login page
├── dashboard.html         # Dashboard
├── setup-whatsapp.html    # WhatsApp setup
├── messages.html          # Messages page
├── contacts.html          # Contacts page
├── admin-settings.html    # Admin settings
├── logout.html            # Logout page
├── ml-pipeline.html       # ML pipeline
├── js/                    # JavaScript files
│   ├── components.js      # UI components
│   ├── messages.js        # Messages functionality
│   ├── contacts.js        # Contacts functionality
│   ├── admin-settings.js  # Admin settings
│   └── polling-manager.js # Polling management
└── docs/                  # Frontend documentation
    ├── index.html         # Docs index
    ├── testing-guide.html # Testing guide
    └── complete-testing-guide.md # Complete testing
```

### 📁 src/ - Source Code
```
src/
├── middleware/            # Express middleware
│   ├── auth.js           # Authentication middleware
│   ├── apiKey.js         # API key middleware
│   └── combinedAuth.js   # Combined auth middleware
├── routes/               # API routes
│   └── admin-routes.js   # Admin routes
└── utils/                # Utility functions
    ├── database.js       # Database utilities
    ├── database-manager.js # Database management
    ├── postgres-database.js # PostgreSQL utilities
    ├── postgres-schema.js # Schema utilities
    ├── postgres-setup.js # PostgreSQL setup
    ├── postgres-setup-windows.js # Windows setup
    ├── setup-database.js # Database setup
    ├── migrate-to-database.js # Migration utilities
    ├── migrate-to-postgres.js # PostgreSQL migration
    └── add-eric-account.js # Account utilities
```

## 🚀 Available Scripts

### Testing
```bash
npm test                    # Run essential tests
npm run test:quick         # Quick health check
npm run test:auth          # Authentication tests
npm run test:media         # Media sending tests
npm run test:contacts      # Contact management tests
npm run test:broadcast     # Broadcast tests
```

### Development
```bash
npm start                  # Start production server
npm run dev                # Start development server with nodemon
```

### Setup & Deployment
```bash
npm run setup              # Setup PostgreSQL
npm run deploy             # Deploy application
```

### Session Management
```bash
npm run session:check      # Check session health
npm run session:monitor    # Monitor session
npm run session:recover    # Recover session
```

## 🔧 Configuration

### Environment Variables (.env)
```env
PORT=41100
JWT_SECRET=your_jwt_secret
DATABASE_URL=postgresql://user:password@localhost:5432/whatbot
NODE_ENV=development
```

### API Keys
- Test API keys are stored in `scripts/api-test/api-keys.json`
- Production API keys should be managed securely

## 📊 Testing

### Essential Test Suite
The main test suite (`scripts/test/test-essential.js`) covers:
- ✅ Server health check
- ✅ User authentication
- ✅ WhatsApp connection status
- ✅ Contact management
- ✅ Message sending

### API Testing
The API testing suite (`scripts/api-test/`) includes:
- Comprehensive API endpoint tests
- Media file testing (images, videos, audio)
- Authentication testing
- Error handling validation

## 🗄️ Database

### PostgreSQL Setup
1. Install PostgreSQL
2. Run `npm run setup` to initialize database
3. Check `database/schema.sql` for table structure
4. Use migration scripts in `database/` for updates

### Data Files
- `database/contacts.json` - Contact data
- `queue-state.json` - Message queue state
- `broadcast-history.json` - Broadcast history

## 🔒 Security

### Authentication
- JWT-based authentication
- API key validation
- Role-based access control
- Session management

### File Security
- Upload validation
- File type restrictions
- Size limits
- Secure file storage

## 📱 WhatsApp Integration

### Session Management
- Persistent connection
- Automatic recovery
- Health monitoring
- Session validation

### Features
- Message sending/receiving
- Media file support
- Contact management
- Broadcast messaging
- Auto-replies

## 🚀 Deployment

### Production Setup
1. Follow `docs/dev-guides/UBUNTU_PRODUCTION_GUIDE.md`
2. Use deployment scripts in `scripts/deployment/`
3. Configure environment variables
4. Set up monitoring

### Monitoring
- Session health monitoring
- Connection status tracking
- Error logging
- Performance metrics

## 🛠️ Troubleshooting

### Common Issues
- Check `docs/dev-guides/TROUBLESHOOTING_GUIDE.md`
- Review `docs/dev-guides/WHATSAPP_TROUBLESHOOTING.md`
- Use session management scripts
- Check server logs

### Support
- Review documentation in `docs/dev-guides/`
- Check test results for issues
- Use health check endpoints
- Monitor session status 
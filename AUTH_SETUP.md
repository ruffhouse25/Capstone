# Auth0 Authentication Setup

This document provides detailed instructions for setting up Auth0 authentication for the Music Label Management API.

## 🔐 Auth0 Configuration

### Step 1: Create Auth0 Account
1. Go to [auth0.com](https://auth0.com/) and create a free account
2. Create a new tenant (e.g., `dev-music-label`)

### Step 2: Create API in Auth0
1. Go to **Applications > APIs** in your Auth0 dashboard
2. Click **Create API**
3. Configure:
   - **Name:** `Music Label API`
   - **Identifier:** `music-label-api`
   - **Signing Algorithm:** `RS256`

### Step 3: Configure API Scopes
Add these scopes to your API:
```
get:artists
get:albums
post:artists
patch:artists
delete:artists
post:albums
patch:albums
delete:albums
```

### Step 4: Create Roles
Go to **User Management > Roles** and create:

#### Assistant Role
- **Name:** `Assistant`
- **Description:** `Read-only access to artists and albums`
- **Permissions:**
  - `get:artists`
  - `get:albums`

#### Director Role  
- **Name:** `Director`
- **Description:** `Manage artists and update albums`
- **Permissions:**
  - `get:artists`
  - `get:albums`
  - `post:artists`
  - `patch:artists`
  - `delete:artists`
  - `patch:albums`

#### Executive Role
- **Name:** `Executive`  
- **Description:** `Full access to all operations`
- **Permissions:**
  - `get:artists`
  - `get:albums`
  - `post:artists`
  - `patch:artists`
  - `delete:artists`
  - `post:albums`
  - `patch:albums`
  - `delete:albums`

### Step 5: Create Test Users
1. Go to **User Management > Users**
2. Create test users for each role:
   - `assistant@musiclabel.test`
   - `director@musiclabel.test`
   - `executive@musiclabel.test`
3. Assign appropriate roles to each user

## 🔧 Environment Configuration

### Required Environment Variables
Create a `.env` file or export these variables:

```bash
export AUTH0_DOMAIN='dev-music-label.us.auth0.com'
export API_AUDIENCE='music-label-api'
export CLIENT_ID='your_client_id_here'
export CLIENT_SECRET='your_client_secret_here'
```

### Setup Script
Run the provided setup script:
```bash
source setup.sh
```

## 🧪 Testing Authentication

### Option 1: Development Mode (Mock Tokens)
For quick testing, set `FLASK_ENV=development` and use:
```bash
# Assistant
curl -H "Authorization: Bearer assistant" http://localhost:5000/artists

# Director  
curl -H "Authorization: Bearer director" http://localhost:5000/artists

# Executive
curl -H "Authorization: Bearer executive" http://localhost:5000/artists
```

### Option 2: Production Mode (Real JWT)

#### Get JWT Token via Auth0
```bash
curl --request POST \
  --url 'https://dev-music-label.us.auth0.com/oauth/token' \
  --header 'content-type: application/json' \
  --data '{
    "client_id":"YOUR_CLIENT_ID",
    "client_secret":"YOUR_CLIENT_SECRET",
    "audience":"music-label-api",
    "grant_type":"client_credentials"
  }'
```

#### Use JWT in Requests
```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     https://your-app.herokuapp.com/artists
```

## 🔍 JWT Token Verification

The API validates JWT tokens by:
1. **Header Verification:** Ensures `Authorization: Bearer <token>` format
2. **Signature Verification:** Validates against Auth0 public key
3. **Claims Verification:** Checks audience, issuer, and expiration
4. **Permissions Check:** Ensures required permissions are present

## 🚀 Testing with Postman

### Import Collection
```json
{
  "info": {
    "name": "Music Label API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "auth": {
    "type": "bearer",
    "bearer": [
      {
        "key": "token",
        "value": "{{jwt_token}}",
        "type": "string"
      }
    ]
  }
}
```

### Environment Variables in Postman
```json
{
  "assistant_token": "assistant",
  "director_token": "director", 
  "executive_token": "executive",
  "base_url": "http://localhost:5000"
}
```

## 🔧 Troubleshooting

### Common Issues

1. **"Unable to parse authentication token"**
   - Check token format: `Bearer <token>`
   - Verify token is not expired
   - Ensure correct Auth0 domain

2. **"Permission not found"**
   - Verify user has required role
   - Check role has correct permissions
   - Ensure permissions are included in JWT claims

3. **"Invalid claims"**
   - Check API audience matches
   - Verify issuer domain
   - Ensure token is for correct environment

## 📋 Production Checklist

- [ ] Auth0 API configured with correct identifier
- [ ] All 8 permissions/scopes added to API
- [ ] Three roles created with appropriate permissions
- [ ] Test users created and assigned roles
- [ ] Environment variables configured
- [ ] JWT signature verification working
- [ ] All endpoints protected with appropriate permissions
- [ ] Error handling implemented for auth failures

## 🔗 Useful Links

- [Auth0 Dashboard](https://manage.auth0.com/)
- [Auth0 API Documentation](https://auth0.com/docs/api)
- [JWT.io Token Debugger](https://jwt.io/)
- [Auth0 Flask Quickstart](https://auth0.com/docs/quickstart/backend/python)

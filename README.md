# Music Label Management API

## Motivation

The Music Label Management API is a comprehensive system designed to help music label executives manage their catalog of artists and albums. This project demonstrates:

- **Data modeling** with PostgreSQL and SQLAlchemy (one-to-many relationships)
- **API development** with Flask following RESTful principles
- **Authentication and authorization** with role-based access control (RBAC)
- **Comprehensive testing** with unittest
- **Cloud deployment** to Heroku with proper CI/CD practices

This serves as the capstone project for the Udacity Full Stack Developer Nanodegree, showcasing all skills learned throughout the program.

## Live Application

**🌐 API Base URL:** `https://music-app-test-68a193e89dfa.herokuapp.com`

**🔗 Health Check:** `https://music-app-test-68a193e89dfa.herokuapp.com/health`

**Note:** This API requires authentication for all endpoints except `/health`. See the [Authentication](#authentication) section below.

## Quick Start

### Testing the Live API

1. **Health Check (No Auth Required):**
   ```bash
   curl https://music-app-test-68a193e89dfa.herokuapp.com/health
   ```

2. **Get Artists (Assistant Token):**
   ```bash
   curl -H "Authorization: Bearer assistant" \
        https://music-app-test-68a193e89dfa.herokuapp.com/artists
   ```

3. **Create Artist (Director Token):**
   ```bash
   curl -X POST \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer director" \
        -d '{"name":"Taylor Swift","age":33,"genre":"Pop","country":"USA"}' \
        https://music-app-test-68a193e89dfa.herokuapp.com/artists
   ```

## Project Dependencies

### Local Development
- Python 3.8+
- PostgreSQL
- pip (Python package manager)
- Auth0 account

### Python Packages
All dependencies are listed in `requirements.txt`:
```
Flask==1.1.2
Flask-SQLAlchemy==2.5.1
Flask-Cors==3.0.10
Flask-Migrate==2.7.0
Flask-Script==2.0.6
psycopg2-binary==2.9.1
python-jose==3.3.0
gunicorn==20.1.0
```

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/music-label-api.git
cd music-label-api
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Database
Create a PostgreSQL database:
```bash
createdb music_label
```

### 5. Configure Environment Variables
Copy and modify the setup script:
```bash
chmod +x setup.sh
source setup.sh
```

Update the following variables in `setup.sh`:
- `DATABASE_URL`: Your PostgreSQL connection string
- `AUTH0_DOMAIN`: Your Auth0 domain
- `API_AUDIENCE`: Your Auth0 API identifier

### 6. Run Database Migrations
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

### 7. Run the Application
```bash
python app.py
```

The API will be available at `http://localhost:8080`

## API Reference

### Base URL
- **Local:** `http://localhost:8080`
- **Heroku:** `https://your-music-label-api.herokuapp.com/`

### Authentication
This API uses **Auth0** for authentication. All endpoints require a valid JWT token with appropriate permissions.

**📋 For detailed Auth0 setup instructions, see [AUTH_SETUP.md](AUTH_SETUP.md)**

#### Quick Test (Development Mode)
```bash
# Set development environment
export FLASK_ENV=development

# Use mock tokens for testing
curl -H "Authorization: Bearer assistant" http://localhost:5000/artists
curl -H "Authorization: Bearer director" http://localhost:5000/artists  
curl -H "Authorization: Bearer executive" http://localhost:5000/artists
```

#### Production Authentication
For production use, obtain JWT tokens from Auth0. See [AUTH_SETUP.md](AUTH_SETUP.md) for complete instructions.

#### Headers
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

### Error Handling
Errors are returned as JSON objects in the following format:
```json
{
  "success": false,
  "error": 404,
  "message": "resource not found"
}
```

The API returns these error types:
- **400:** Bad Request
- **401:** Unauthorized
- **403:** Forbidden
- **404:** Not Found
- **422:** Unprocessable Entity
- **500:** Internal Server Error

### Endpoints

#### GET /artists
**Description:** Retrieve all artists  
**Permissions:** `get:artists`  
**Parameters:** None  

**Sample Response:**
```json
{
  "success": true,
  "artists": [
    {
      "id": 1,
      "name": "Taylor Swift",
      "age": 33,
      "genre": "Pop",
      "country": "USA",
      "albums": [
        {
          "id": 1,
          "title": "Midnights",
          "release_date": "2022-10-21",
          "genre": "Pop"
        }
      ]
    }
  ],
  "total_artists": 1
}
```

#### GET /albums
**Description:** Retrieve all albums  
**Permissions:** `get:albums`  
**Parameters:** None  

**Sample Response:**
```json
{
  "success": true,
  "albums": [
    {
      "id": 1,
      "title": "Midnights",
      "release_date": "2022-10-21",
      "genre": "Pop",
      "track_count": 13,
      "artist_id": 1,
      "artist": {
        "id": 1,
        "name": "Taylor Swift",
        "genre": "Pop",
        "country": "USA"
      }
    }
  ],
  "total_albums": 1
}
```

#### POST /artists
**Description:** Create a new artist  
**Permissions:** `post:artists`  

**Request Body:**
```json
{
  "name": "Billie Eilish",
  "age": 21,
  "genre": "Alternative",
  "country": "USA"
}
```

**Sample Response:**
```json
{
  "success": true,
  "created": 2,
  "artist": {
    "id": 2,
    "name": "Billie Eilish",
    "age": 21,
    "genre": "Alternative",
    "country": "USA",
    "albums": []
  }
}
```

#### POST /albums
**Description:** Create a new album  
**Permissions:** `post:albums`  

**Request Body:**
```json
{
  "title": "When We All Fall Asleep, Where Do We Go?",
  "release_date": "2019-03-29",
  "genre": "Alternative",
  "track_count": 14,
  "artist_id": 2
}
```

#### PATCH /artists/<id>
**Description:** Update an existing artist  
**Permissions:** `patch:artists`  

**Request Body:**
```json
{
  "age": 22
}
```

#### PATCH /albums/<id>
**Description:** Update an existing album  
**Permissions:** `patch:albums`  

#### DELETE /artists/<id>
**Description:** Delete an artist  
**Permissions:** `delete:artists`  

#### DELETE /albums/<id>
**Description:** Delete an album  
**Permissions:** `delete:albums`  

## Roles and Permissions

### Label Assistant
**Permissions:**
- `get:artists` - View all artists
- `get:albums` - View all albums

**Description:** Entry-level role that can browse the music catalog but cannot make changes.

### Label Director
**Permissions:**
- All Label Assistant permissions, plus:
- `post:artists` - Create new artists
- `patch:artists` - Modify artist information
- `delete:artists` - Remove artists from catalog
- `patch:albums` - Modify album information

**Description:** Mid-level role that manages artist relationships and can modify existing content.

### Label Executive
**Permissions:**
- All Label Director permissions, plus:
- `post:albums` - Create new albums
- `delete:albums` - Remove albums from catalog

**Description:** Senior role with full control over the music catalog, including album creation and deletion.

## Testing

### Running Tests
```bash
python test_app.py
```

### Test Coverage
The test suite includes:
- **Success behavior** for each endpoint (8 tests)
- **Error behavior** for each endpoint (8 tests)  
- **RBAC testing** for each role (6 tests)
- **Authentication testing** (4 tests)

**Total:** 26 comprehensive tests

### Setting Up Test Database
```bash
createdb music_label_test
```

Update test database URL in `test_app.py` if needed.

## Deployment

**📋 For complete deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)**

### Quick Heroku Deployment

1. **Create Heroku App**
   ```bash
   heroku create your-music-label-api
   ```

2. **Set Environment Variables**
   ```bash
   heroku config:set DATABASE_URL="postgresql://..."
   heroku config:set AUTH0_DOMAIN="your-domain.auth0.com"
   heroku config:set API_AUDIENCE="music-label-api"
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

4. **Run Migrations**
   ```bash
   heroku run python manage.py db upgrade
   ```

### Required Files for Deployment
- `Procfile` - Specifies the command to run the app
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification
- `manage.py` - Database migration management

## Authentication Setup

### Auth0 Configuration

1. **Create Auth0 Application**
   - Go to Auth0 Dashboard
   - Create a new Single Page Application
   - Note the Domain and Client ID

2. **Create Auth0 API**
   - Create a new API in Auth0
   - Set the identifier (API Audience)
   - Enable RBAC and add permissions in access tokens

3. **Set Up Roles and Permissions**
   - Create roles: Label Assistant, Label Director, Label Executive
   - Assign permissions to each role as detailed above
   - Create test users and assign roles

4. **Get JWT Tokens**
   - Use Auth0's test tab or implement a login flow
   - Extract JWT tokens for testing
   - Update tokens in `setup.sh`

### Sample JWT Payload
```json
{
  "iss": "https://your-domain.auth0.com/",
  "sub": "auth0|user-id",
  "aud": "music-label-api",
  "permissions": [
    "get:artists",
    "get:albums",
    "post:artists"
  ]
}
```

## Architecture

### Database Schema
```
Artists Table:
- id (Primary Key)
- name (String, required)
- age (Integer, required)
- genre (String, required)
- country (String, required)

Albums Table:
- id (Primary Key)
- title (String, required)
- release_date (DateTime, required)
- genre (String, required)
- track_count (Integer, default=10)
- artist_id (Foreign Key to Artists)
```

### Project Structure
```
music-label-api/
├── app.py                 # Main application
├── models.py              # Database models
├── auth.py                # Authentication helpers
├── test_app.py            # Test suite
├── manage.py              # Database migration management
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment config
├── runtime.txt           # Python version
├── setup.sh              # Environment variables
└── README.md             # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests for new features
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Author

Your Name - Udacity Full Stack Developer Nanodegree Capstone Project

# Deployment Guide

This guide provides step-by-step instructions for deploying the Music Label API to Heroku.

## 🚀 Prerequisites

- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
- [Git](https://git-scm.com/) installed
- Heroku account created
- Project files ready

## 📋 Pre-Deployment Checklist

Ensure your project has these files:
- [x] `app.py` - Main Flask application
- [x] `requirements.txt` - Python dependencies
- [x] `Procfile` - Heroku process configuration
- [x] `runtime.txt` - Python version specification
- [x] `manage.py` - Database management script

## 🔧 Step 1: Prepare for Deployment

### Update Procfile
Ensure your `Procfile` contains:
```
web: gunicorn app:APP
release: python manage.py db upgrade
```

### Update requirements.txt
Make sure it includes:
```
gunicorn==20.1.0
psycopg2-binary==2.9.1
python-jose==3.3.0
Flask==1.1.2
Flask-SQLAlchemy==2.5.1
Flask-Migrate==2.7.0
Flask-Cors==3.0.10
```

### Set Runtime
In `runtime.txt`:
```
python-3.9.6
```

## 🌐 Step 2: Create Heroku Application

```bash
# Login to Heroku
heroku login

# Create new app (replace with your app name)
heroku create music-label-api-capstone

# Add PostgreSQL database
heroku addons:create heroku-postgresql:mini

# Get database URL
heroku config:get DATABASE_URL
```

## ⚙️ Step 3: Configure Environment Variables

```bash
# Set Auth0 configuration
heroku config:set AUTH0_DOMAIN='dev-music-label.us.auth0.com'
heroku config:set API_AUDIENCE='music-label-api'

# Set Flask configuration
heroku config:set FLASK_APP='app.py'
heroku config:set FLASK_ENV='production'

# Verify configuration
heroku config
```

## 📤 Step 4: Deploy Application

```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit for Music Label API"

# Add Heroku remote
heroku git:remote -a music-label-api-capstone

# Deploy to Heroku
git push heroku main

# Run database migrations
heroku run python manage.py db upgrade
```

## ✅ Step 5: Verify Deployment

### Test Health Endpoint
```bash
curl https://music-label-api-capstone.herokuapp.com/health
```

Expected response:
```json
{
  "success": true,
  "message": "Music Label API is running!",
  "version": "1.0.0"
}
```

### Test Authentication
```bash
# Test with mock token (development mode)
curl -H "Authorization: Bearer assistant" \
     https://music-label-api-capstone.herokuapp.com/artists
```

## 🔍 Step 6: Monitor Application

### View Logs
```bash
heroku logs --tail
```

### Check Dyno Status
```bash
heroku ps
```

### Database Connection
```bash
heroku pg:info
```

## 🔧 Troubleshooting

### Common Issues

1. **Application Error (H10)**
   ```bash
   heroku logs --tail
   # Check for missing environment variables or startup errors
   ```

2. **Database Connection Error**
   ```bash
   heroku config:get DATABASE_URL
   heroku run python manage.py db upgrade
   ```

3. **Build Failures**
   ```bash
   # Check requirements.txt for incompatible versions
   # Ensure Procfile format is correct
   ```

### Debug Commands
```bash
# Access Heroku shell
heroku run python

# Run database commands
heroku run python manage.py db current
heroku run python manage.py db history

# Restart application
heroku restart
```

## 📊 Step 7: Performance Optimization

### Scale Dynos
```bash
# Scale web dynos
heroku ps:scale web=1

# Check dyno usage
heroku ps
```

### Database Optimization
```bash
# Check database performance
heroku pg:diagnose

# View database stats
heroku pg:stats
```

## 🔐 Step 8: Security Configuration

### Environment Variables Security
```bash
# Never commit sensitive data to git
# Use Heroku config vars for all secrets
heroku config:set SECRET_KEY='your-secret-key'
```

### HTTPS Enforcement
The app automatically uses HTTPS on Heroku, but ensure your Auth0 configuration matches.

## 📝 Step 9: Update Documentation

After successful deployment, update your README.md with:

1. **Live Application URL:**
   ```markdown
   **🌐 Live API:** https://music-label-api-capstone.herokuapp.com/
   ```

2. **Auth0 Setup Instructions:**
   - Link to AUTH_SETUP.md
   - Include working domain and audience

3. **Testing Instructions:**
   - Provide curl examples with live URL
   - Include token acquisition steps

## 🚨 Post-Deployment Checklist

- [ ] Application starts without errors
- [ ] Health endpoint responds correctly
- [ ] Database migrations completed
- [ ] Auth0 integration working
- [ ] All endpoints accessible with proper authentication
- [ ] Error handling working correctly
- [ ] Environment variables configured
- [ ] Logs showing normal operation
- [ ] README updated with live URL
- [ ] Auth setup documentation complete

## 📈 Monitoring and Maintenance

### Regular Checks
```bash
# Daily health check
curl https://music-label-api-capstone.herokuapp.com/health

# Weekly log review
heroku logs --tail

# Monthly performance review
heroku pg:stats
```

### Updates and Maintenance
```bash
# Deploy updates
git add .
git commit -m "Update description"
git push heroku main

# Database maintenance
heroku run python manage.py db upgrade
```

## 🔗 Useful Resources

- [Heroku Python Deployment](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Heroku Config Vars](https://devcenter.heroku.com/articles/config-vars)
- [Heroku PostgreSQL](https://devcenter.heroku.com/articles/heroku-postgresql)
- [Heroku Logs](https://devcenter.heroku.com/articles/logging)

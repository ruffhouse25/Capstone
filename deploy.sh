#!/bin/bash

echo "=================================================="
echo "       HEROKU DEPLOYMENT SCRIPT"
echo "=================================================="
echo

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

echo "✅ Heroku CLI found"

# Login to Heroku
echo "🔐 Logging into Heroku..."
heroku login

# Initialize git repository if not exists
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for Music Label API"
fi

# Create Heroku app
echo "🚀 Creating Heroku app..."
read -p "Enter your app name (e.g., your-name-music-label): " APP_NAME
heroku create $APP_NAME

# Add PostgreSQL addon
echo "🗄️  Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:hobby-dev --app $APP_NAME

# Set environment variables
echo "🔧 Setting environment variables..."
read -p "Enter your Auth0 Domain: " AUTH0_DOMAIN
read -p "Enter your Auth0 Audience: " AUTH0_AUDIENCE

heroku config:set AUTH0_DOMAIN=$AUTH0_DOMAIN --app $APP_NAME
heroku config:set AUTH0_AUDIENCE=$AUTH0_AUDIENCE --app $APP_NAME
heroku config:set FLASK_ENV=production --app $APP_NAME

# Deploy to Heroku
echo "📤 Deploying to Heroku..."
git push heroku main

# Run database migrations
echo "🔄 Running database migrations..."
heroku run python manage.py db upgrade --app $APP_NAME

echo "=================================================="
echo "🎉 DEPLOYMENT COMPLETE!"
echo "Your app is available at: https://$APP_NAME.herokuapp.com"
echo "Health check: https://$APP_NAME.herokuapp.com/health"
echo "=================================================="

@echo off
echo ================================================
echo    DEPLOYING TO HEROKU: music-app-test
echo ================================================
echo.

echo Step 1: Checking if we're in the right directory...
if not exist "app.py" (
    echo ERROR: app.py not found. Please run this from the project directory.
    pause
    exit /b 1
)

echo Step 2: Connecting to Heroku app...
heroku git:remote -a music-app-test

echo Step 3: Adding files to git...
git add .
git commit -m "Deploy Music Label API to Heroku"

echo Step 4: Adding PostgreSQL database...
heroku addons:create heroku-postgresql:hobby-dev -a music-app-test

echo Step 5: Setting environment variables...
heroku config:set FLASK_ENV=production -a music-app-test

echo Step 6: Setting up Auth0 (you'll need to provide these)...
set /p AUTH0_DOMAIN="Enter your Auth0 Domain (e.g., yourapp.auth0.com): "
set /p AUTH0_AUDIENCE="Enter your Auth0 Audience (e.g., music-label-api): "

heroku config:set AUTH0_DOMAIN=%AUTH0_DOMAIN% -a music-app-test
heroku config:set AUTH0_AUDIENCE=%AUTH0_AUDIENCE% -a music-app-test

echo Step 7: Deploying to Heroku...
git push heroku main

echo Step 8: Running database migrations...
heroku run python manage.py db upgrade -a music-app-test

echo.
echo ================================================
echo    DEPLOYMENT COMPLETE!
echo    Your app is available at:
echo    https://music-app-test.herokuapp.com/health
echo ================================================
pause

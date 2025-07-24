@echo off
echo ==================================================
echo         HEROKU DEPLOYMENT INSTRUCTIONS
echo ==================================================
echo.
echo 1. Install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli
echo 2. Open Command Prompt and navigate to this directory
echo 3. Run: heroku login
echo 4. Run: git init (if not already a git repo)
echo 5. Run: git add .
echo 6. Run: git commit -m "Initial commit"
echo 7. Run: heroku create your-app-name
echo 8. Run: heroku addons:create heroku-postgresql:hobby-dev
echo 9. Run: heroku config:set AUTH0_DOMAIN=your-auth0-domain
echo 10. Run: heroku config:set AUTH0_AUDIENCE=your-auth0-audience
echo 11. Run: heroku config:set FLASK_ENV=production
echo 12. Run: git push heroku main
echo 13. Run: heroku run python manage.py db upgrade
echo.
echo Your app will be available at: https://your-app-name.herokuapp.com
echo ==================================================
pause

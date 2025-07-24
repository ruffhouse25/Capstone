@echo off
REM Music Label API Test Script for Windows

echo === Music Label API Test Script ===
echo Testing the live API endpoints...

set BASE_URL=http://localhost:8080
REM For production: set BASE_URL=https://music-label-api-capstone.herokuapp.com

echo.
echo 1. Health Check (No Authentication Required):
curl -s "%BASE_URL%/health"

echo.
echo.
echo 2. Get Artists (Assistant Permission):
curl -s -H "Authorization: Bearer assistant" "%BASE_URL%/artists"

echo.
echo.
echo 3. Create an Artist (Director Permission):
curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer director" -d "{\"name\":\"Taylor Swift\",\"age\":33,\"genre\":\"Pop\",\"country\":\"USA\"}" "%BASE_URL%/artists"

echo.
echo.
echo 4. Test Unauthorized Access (No Token):
curl -s "%BASE_URL%/artists"

echo.
echo.
echo === Test Complete ===

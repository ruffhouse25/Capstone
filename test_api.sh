#!/bin/bash

echo "=== Music Label API Test Script ==="
echo "Testing the live API endpoints..."

BASE_URL="http://localhost:8080"
# For production: BASE_URL="https://music-label-api-capstone.herokuapp.com"

echo ""
echo "1. Health Check (No Authentication Required):"
curl -s "$BASE_URL/health" | python -m json.tool

echo ""
echo "2. Get Artists (Assistant Permission):"
curl -s -H "Authorization: Bearer assistant" "$BASE_URL/artists" | python -m json.tool

echo ""
echo "3. Create an Artist (Director Permission):"
curl -s -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer director" \
     -d '{"name":"Taylor Swift","age":33,"genre":"Pop","country":"USA"}' \
     "$BASE_URL/artists" | python -m json.tool

echo ""
echo "4. Create an Album (Executive Permission):"
curl -s -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer executive" \
     -d '{"title":"Midnights","release_date":"2022-10-21","genre":"Pop","track_count":13,"artist_id":1}' \
     "$BASE_URL/albums" | python -m json.tool

echo ""
echo "5. Get Albums (Assistant Permission):"
curl -s -H "Authorization: Bearer assistant" "$BASE_URL/albums" | python -m json.tool

echo ""
echo "6. Test Unauthorized Access (No Token):"
curl -s "$BASE_URL/artists" | python -m json.tool

echo ""
echo "7. Test Forbidden Access (Assistant trying to create):"
curl -s -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer assistant" \
     -d '{"name":"Test Artist","age":25,"genre":"Rock","country":"UK"}' \
     "$BASE_URL/artists" | python -m json.tool

echo ""
echo "=== Test Complete ==="

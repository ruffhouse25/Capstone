#!/bin/bash
# Environment setup script for Music Label API

# Database URL (update with your database credentials)
export DATABASE_URL="postgresql://postgres@localhost:5432/music_label"

# Auth0 Configuration (update with your Auth0 settings)
export AUTH0_DOMAIN="your-auth0-domain.auth0.com"
export API_AUDIENCE="music-label-api"

# Test tokens (these would be obtained from Auth0)
export ASSISTANT_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkN3aVJnVUNTVlFOVlhZbDRLWXpNelFvMXVBUSJ9..."
export DIRECTOR_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkN3aVJnVUNTVlFOVlhZbDRLWXpNelFvMXVBUSJ9..."
export EXECUTIVE_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkN3aVJnVUNTVlFOVlhZbDRLWXpNelFvMXVBUSJ9..."

echo "Environment variables set for Music Label API!"
echo "Auth0 Domain: $AUTH0_DOMAIN"
echo "API Audience: $API_AUDIENCE"

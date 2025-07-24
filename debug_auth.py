#!/usr/bin/env python3

import os
import sys
sys.path.append('.')

from app import create_app
import json

def test_auth():
    # Create app with test config
    app = create_app()
    
    with app.test_client() as client:
        # Test 1: Working endpoint with proper auth
        print("=== Test 1: GET /artists with director token ===")
        headers = {'Authorization': 'Bearer director'}
        response = client.get('/artists', headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.data.decode()}")
        print()
        
        # Test 2: PATCH non-existent artist
        print("=== Test 2: PATCH /artists/999 with director token ===")
        headers = {'Authorization': 'Bearer director', 'Content-Type': 'application/json'}
        data = {'age': 30}
        response = client.patch('/artists/999', 
                              headers=headers, 
                              data=json.dumps(data))
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.data.decode()}")
        print()
        
        # Test 3: Test auth parsing directly
        print("=== Test 3: Test manual token verification ===")
        from auth_simple import verify_decode_jwt
        try:
            payload = verify_decode_jwt('director')
            print(f"Token verification successful: {payload}")
        except Exception as e:
            print(f"Token verification failed: {e}")

if __name__ == "__main__":
    test_auth()

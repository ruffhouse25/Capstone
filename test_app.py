import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import create_app
from models import setup_db, Artist, Album

class MusicLabelTestCase(unittest.TestCase):
    """This class represents the music label test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "music_label_test"
        # Use SQLite for testing to avoid PostgreSQL dependency
        self.database_path = "sqlite:///test.db"
        
        with self.app.app_context():
            setup_db(self.app, self.database_path)
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        # Sample test data
        self.new_artist = {
            'name': 'Test Artist',
            'age': 25,
            'genre': 'Pop',
            'country': 'USA'
        }

        self.new_album = {
            'title': 'Test Album',
            'release_date': '2024-01-01',
            'genre': 'Pop',
            'track_count': 12,
            'artist_id': 1
        }

        # Mock tokens for testing (using simplified auth)
        self.assistant_headers = {'Authorization': 'Bearer assistant'}
        self.director_headers = {'Authorization': 'Bearer director'}
        self.executive_headers = {'Authorization': 'Bearer executive'}

    def tearDown(self):
        """Executed after each test"""
        pass

    # Tests for Artists endpoint
    def test_get_artists_success(self):
        """Test GET /artists success"""
        res = self.client().get('/artists', headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_artists'])

    def test_get_artists_unauthorized(self):
        """Test GET /artists without authorization"""
        res = self.client().get('/artists')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_artist_success(self):
        """Test POST /artists success"""
        res = self.client().post('/artists', json=self.new_artist, headers=self.director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_create_artist_forbidden(self):
        """Test POST /artists with insufficient permissions"""
        res = self.client().post('/artists', json=self.new_artist, headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_create_artist_bad_request(self):
        """Test POST /artists with missing data"""
        incomplete_artist = {'name': 'Incomplete Artist'}
        res = self.client().post('/artists', json=incomplete_artist, headers=self.director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_patch_artist_success(self):
        """Test PATCH /artists/<id> success"""
        # First create an artist
        create_res = self.client().post('/artists', json=self.new_artist, headers=self.director_headers)
        create_data = json.loads(create_res.data)
        artist_id = create_data['created']

        # Then update it
        update_data = {'age': 30}
        res = self.client().patch(f'/artists/{artist_id}', json=update_data, headers=self.director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['artist']['age'], 30)

    def test_patch_artist_not_found(self):
        """Test PATCH /artists/<id> with invalid id"""
        update_data = {'age': 30}
        res = self.client().patch('/artists/999', json=update_data, headers=self.director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_artist_success(self):
        """Test DELETE /artists/<id> success"""
        # First create an artist
        create_res = self.client().post('/artists', json=self.new_artist, headers=self.director_headers)
        create_data = json.loads(create_res.data)
        artist_id = create_data['created']

        # Then delete it
        res = self.client().delete(f'/artists/{artist_id}', headers=self.director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], artist_id)

    def test_delete_artist_forbidden(self):
        """Test DELETE /artists/<id> with insufficient permissions"""
        res = self.client().delete('/artists/1', headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Tests for Albums endpoint
    def test_get_albums_success(self):
        """Test GET /albums success"""
        res = self.client().get('/albums', headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_albums'] >= 0)

    def test_create_album_success(self):
        """Test POST /albums success"""
        # First create an artist
        create_artist_res = self.client().post('/artists', json=self.new_artist, headers=self.executive_headers)
        create_artist_data = json.loads(create_artist_res.data)
        artist_id = create_artist_data['created']

        # Update album data with valid artist_id
        album_data = self.new_album.copy()
        album_data['artist_id'] = artist_id

        res = self.client().post('/albums', json=album_data, headers=self.executive_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_create_album_forbidden(self):
        """Test POST /albums with insufficient permissions"""
        res = self.client().post('/albums', json=self.new_album, headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_delete_album_success(self):
        """Test DELETE /albums/<id> success"""
        # First create an artist and album
        create_artist_res = self.client().post('/artists', json=self.new_artist, headers=self.executive_headers)
        create_artist_data = json.loads(create_artist_res.data)
        artist_id = create_artist_data['created']

        album_data = self.new_album.copy()
        album_data['artist_id'] = artist_id

        create_album_res = self.client().post('/albums', json=album_data, headers=self.executive_headers)
        create_album_data = json.loads(create_album_res.data)
        album_id = create_album_data['created']

        # Then delete the album
        res = self.client().delete(f'/albums/{album_id}', headers=self.executive_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], album_id)

    # RBAC Tests
    def test_assistant_permissions(self):
        """Test Label Assistant can only view artists and albums"""
        # Can view artists
        res = self.client().get('/artists', headers=self.assistant_headers)
        self.assertEqual(res.status_code, 200)

        # Can view albums
        res = self.client().get('/albums', headers=self.assistant_headers)
        self.assertEqual(res.status_code, 200)

        # Cannot create artists
        res = self.client().post('/artists', json=self.new_artist, headers=self.assistant_headers)
        self.assertEqual(res.status_code, 403)

    def test_director_permissions(self):
        """Test Label Director can manage artists and modify albums"""
        # Can create artists
        res = self.client().post('/artists', json=self.new_artist, headers=self.director_headers)
        self.assertEqual(res.status_code, 200)

        # Can delete artists
        create_data = json.loads(res.data)
        artist_id = create_data['created']
        res = self.client().delete(f'/artists/{artist_id}', headers=self.director_headers)
        self.assertEqual(res.status_code, 200)

        # Cannot create albums (Executive only)
        res = self.client().post('/albums', json=self.new_album, headers=self.director_headers)
        self.assertEqual(res.status_code, 403)

    def test_executive_permissions(self):
        """Test Label Executive has all permissions"""
        # Can create artists
        res = self.client().post('/artists', json=self.new_artist, headers=self.executive_headers)
        self.assertEqual(res.status_code, 200)

        # Can create albums
        create_data = json.loads(res.data)
        artist_id = create_data['created']
        album_data = self.new_album.copy()
        album_data['artist_id'] = artist_id
        
        res = self.client().post('/albums', json=album_data, headers=self.executive_headers)
        self.assertEqual(res.status_code, 200)

        # Can delete albums
        create_album_data = json.loads(res.data)
        album_id = create_album_data['created']
        res = self.client().delete(f'/albums/{album_id}', headers=self.executive_headers)
        self.assertEqual(res.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

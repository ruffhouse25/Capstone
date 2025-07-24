import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

from models import setup_db, Artist, Album
from auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({
            'success': True,
            'message': 'Music Label API is running!',
            'version': '1.0.0'
        })

    # ROUTES

    '''
    GET /artists
    Public endpoint - requires 'get:artists' permission
    '''
    @app.route('/artists')
    @requires_auth('get:artists')
    def retrieve_artists(payload):
        try:
            artists = Artist.query.order_by(Artist.id).all()
            
            return jsonify({
                'success': True,
                'artists': [artist.format() for artist in artists],
                'total_artists': len(artists)
            })
        except Exception:
            abort(422)

    '''
    GET /albums
    Public endpoint - requires 'get:albums' permission
    '''
    @app.route('/albums')
    @requires_auth('get:albums')
    def retrieve_albums(payload):
        try:
            albums = Album.query.order_by(Album.id).all()
            
            return jsonify({
                'success': True,
                'albums': [album.format() for album in albums],
                'total_albums': len(albums)
            })
        except Exception:
            abort(422)

    '''
    DELETE /artists/<id>
    Requires 'delete:artists' permission
    '''
    @app.route('/artists/<int:artist_id>', methods=['DELETE'])
    @requires_auth('delete:artists')
    def delete_artist(payload, artist_id):
        try:
            artist = Artist.query.filter(Artist.id == artist_id).one_or_none()

            if artist is None:
                abort(404)

            artist.delete()

            return jsonify({
                'success': True,
                'deleted': artist_id
            })

        except Exception:
            abort(422)

    '''
    DELETE /albums/<id>
    Requires 'delete:albums' permission
    '''
    @app.route('/albums/<int:album_id>', methods=['DELETE'])
    @requires_auth('delete:albums')
    def delete_album(payload, album_id):
        try:
            album = Album.query.filter(Album.id == album_id).one_or_none()

            if album is None:
                abort(404)

            album.delete()

            return jsonify({
                'success': True,
                'deleted': album_id
            })

        except Exception:
            abort(422)

    '''
    POST /artists
    Requires 'post:artists' permission
    '''
    @app.route('/artists', methods=['POST'])
    @requires_auth('post:artists')
    def create_artist(payload):
        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_genre = body.get('genre', None)
        new_country = body.get('country', None)

        if not all([new_name, new_age, new_genre, new_country]):
            abort(400)

        try:
            artist = Artist(name=new_name, age=new_age, genre=new_genre, country=new_country)
            artist.insert()

            return jsonify({
                'success': True,
                'created': artist.id,
                'artist': artist.format()
            })

        except Exception:
            abort(422)

    '''
    POST /albums
    Requires 'post:albums' permission
    '''
    @app.route('/albums', methods=['POST'])
    @requires_auth('post:albums')
    def create_album(payload):
        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)
        new_genre = body.get('genre', None)
        new_track_count = body.get('track_count', 10)
        new_artist_id = body.get('artist_id', None)

        if not all([new_title, new_release_date, new_genre, new_artist_id]):
            abort(400)

        try:
            # Parse release date
            release_date = datetime.strptime(new_release_date, '%Y-%m-%d')
            
            # Check if artist exists
            artist = Artist.query.filter(Artist.id == new_artist_id).one_or_none()
            if artist is None:
                abort(404)

            album = Album(
                title=new_title, 
                release_date=release_date, 
                genre=new_genre, 
                track_count=new_track_count,
                artist_id=new_artist_id
            )
            album.insert()

            return jsonify({
                'success': True,
                'created': album.id,
                'album': album.format()
            })

        except ValueError:
            abort(400)
        except Exception:
            abort(422)

    '''
    PATCH /artists/<id>
    Requires 'patch:artists' permission
    '''
    @app.route('/artists/<int:artist_id>', methods=['PATCH'])
    @requires_auth('patch:artists')
    def modify_artist(payload, artist_id):
        body = request.get_json()
        
        artist = Artist.query.filter(Artist.id == artist_id).one_or_none()

        if artist is None:
            abort(404)

        try:
            if 'name' in body:
                artist.name = body.get('name')
            if 'age' in body:
                artist.age = body.get('age')
            if 'genre' in body:
                artist.genre = body.get('genre')
            if 'country' in body:
                artist.country = body.get('country')

            artist.update()

            return jsonify({
                'success': True,
                'artist': artist.format()
            })

        except Exception:
            abort(422)

    '''
    PATCH /albums/<id>
    Requires 'patch:albums' permission
    '''
    @app.route('/albums/<int:album_id>', methods=['PATCH'])
    @requires_auth('patch:albums')
    def modify_album(payload, album_id):
        body = request.get_json()
        
        album = Album.query.filter(Album.id == album_id).one_or_none()

        if album is None:
            abort(404)

        try:
            if 'title' in body:
                album.title = body.get('title')
            if 'release_date' in body:
                album.release_date = datetime.strptime(body.get('release_date'), '%Y-%m-%d')
            if 'genre' in body:
                album.genre = body.get('genre')
            if 'track_count' in body:
                album.track_count = body.get('track_count')
            if 'artist_id' in body:
                # Check if new artist exists
                new_artist = Artist.query.filter(Artist.id == body.get('artist_id')).one_or_none()
                if new_artist is None:
                    abort(404)
                album.artist_id = body.get('artist_id')

            album.update()

            return jsonify({
                'success': True,
                'album': album.format()
            })

        except ValueError:
            abort(400)
        except Exception:
            abort(422)

    # Error Handlers
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=5000, debug=True)

import os
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

database_path = os.environ.get('DATABASE_URL', 'sqlite:///music_label.db')
if database_path and database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()

'''
Artist
Music artist with attributes name, age, genre, and country
'''
class Artist(db.Model):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)
    genre = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    
    # One-to-many relationship with albums
    albums = db.relationship('Album', backref='artist_ref', lazy=True, cascade='all, delete-orphan')

    def __init__(self, name, age, genre, country):
        self.name = name
        self.age = age
        self.genre = genre
        self.country = country

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'genre': self.genre,
            'country': self.country,
            'albums': [album.format_basic() for album in self.albums]
        }

    def format_basic(self):
        return {
            'id': self.id,
            'name': self.name,
            'genre': self.genre,
            'country': self.country
        }

'''
Album
Music album with attributes title, release_date, and artist_id (foreign key)
'''
class Album(db.Model):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    release_date = Column(DateTime, nullable=False)
    genre = Column(String(50), nullable=False)
    track_count = Column(Integer, nullable=False, default=10)
    
    # Foreign key to artist
    artist_id = Column(Integer, ForeignKey('artists.id'), nullable=False)

    def __init__(self, title, release_date, genre, track_count, artist_id):
        self.title = title
        self.release_date = release_date
        self.genre = genre
        self.track_count = track_count
        self.artist_id = artist_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime('%Y-%m-%d'),
            'genre': self.genre,
            'track_count': self.track_count,
            'artist_id': self.artist_id,
            'artist': self.artist_ref.format_basic() if self.artist_ref else None
        }

    def format_basic(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime('%Y-%m-%d'),
            'genre': self.genre
        }

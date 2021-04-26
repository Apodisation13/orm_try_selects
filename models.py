import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

# почему нужна отдельная таблица, а не класс для такой таблицы?
artists_genres = sq.Table(
    'artists_genres', Base.metadata,
    sq.Column('artist_id', sq.Integer, sq.ForeignKey('artists.id'), primary_key=True),
    sq.Column('genre_id', sq.Integer, sq.ForeignKey('genres.genre_id'), primary_key=True)
)


collections_songs = sq.Table(
    'collections_songs', Base.metadata,
    sq.Column('c_id', sq.Integer, sq.ForeignKey('collections.c_id'), primary_key=True),
    sq.Column('song_id', sq.Integer, sq.ForeignKey('songs.song_id'), primary_key=True)
)


albums_artists = sq.Table(
    'albums_artists', Base.metadata,
    sq.Column('album_id', sq.Integer, sq.ForeignKey('albums.album_id'), primary_key=True),
    sq.Column('artist_id', sq.Integer, sq.ForeignKey('artists.id'), primary_key=True)
)


class Artists(Base):
    __tablename__ = 'artists'

    id = sq.Column(sq.Integer, primary_key=True)
    artist_name = sq.Column(sq.String(50), nullable=False)
    genres = relationship('Genres', secondary=artists_genres, backref='artists')

    def __str__(self):
        return f'id - {self.id}, artist_name - {self.artist_name};'


class Genres(Base):
    __tablename__ = 'genres'

    genre_id = sq.Column(sq.Integer, primary_key=True)
    genre = sq.Column(sq.String(150), nullable=False)

    def __str__(self):
        return f'genre_id - {self.genre_id}, genre - {self.genre};'


class Albums(Base):
    __tablename__ = 'albums'

    album_id = sq.Column(sq.Integer, primary_key=True)
    album_name = sq.Column(sq.String(150), nullable=False)
    year = sq.Column(sq.Integer, nullable=False)
    artist_id = sq.Column(sq.Integer, sq.ForeignKey('artists.id'))

    def __str__(self):
        return f'album_id - {self.album_id}, album_name - {self.album_name}, ' \
               f'year - {self.year}, artist_id - {self.artist_id};'


class Songs(Base):
    __tablename__ = 'songs'

    song_id = sq.Column(sq.Integer, primary_key=True)
    track_number = sq.Column(sq.Integer, nullable=False)
    song_name = sq.Column(sq.String(150), nullable=False)
    duration = sq.Column(sq.DECIMAL, nullable=False)
    duration_time = sq.Column(sq.TIME, nullable=False)
    album_id = sq.Column(sq.Integer, sq.ForeignKey('albums.album_id'))
    collections = relationship('Collections', secondary=collections_songs, backref='songs')

    def __str__(self):
        return f'song_id - {self.song_id}, track_number - {self.track_number}, ' \
               f'song_name - {self.song_name}, ' \
               f'duration_time - {self.duration_time}, album_id - {self.album_id};'


class Collections(Base):
    __tablename__ = 'collections'

    c_id = sq.Column(sq.Integer, primary_key=True)
    c_name = sq.Column(sq.String(150), nullable=False)
    c_year = sq.Column(sq.Integer, nullable=False)

    def __str__(self):
        return f'c_id - {self.c_id}, c_name - {self.c_name}, c_year - {self.c_year}'

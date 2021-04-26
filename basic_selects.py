from sqlalchemy.orm import sessionmaker
from models import *


with open('pass.txt') as p:
    password = p.readline()

login = 'postgres'
# password = 'введите ваш пароль'

db_name = 'netology1'

dsn = f'postgresql://{login}:{password}@localhost:5432/{db_name}'

engine = sq.create_engine(dsn)
Session = sessionmaker(bind=engine)
session = Session()

# query = engine.execute('SELECT * FROM albums').fetchall()
# print(query)  # RAW SQL

# query = session.query(Artists)  # SELECT * FROM artists;
# print(query)
# for artist in query.all():
#     print(artist)
#
# print()
# query = session.query(Genres)  # SELECT * FROM genres;
# print(query)
# for genre in query.all():
#     print(genre)

# print()
# query = session.query(artists_genres)
# print(query)  # SELECT * FROM artists_genres;
# for each in query.all():
#     print(each)

# query = session.query(Albums).order_by(Albums.album_id)
# print(query)  # SELECT * FROM albums ORDER BY album_id;
# for album in query.all():
#     print(album)

# query = session.query(Songs)
# print(query)  # SELECT * FROM songs;
# for song in query.all():
#     print(song)

# print()
# query = session.query(Collections)
# print(query)  # SELECT * FROM collections;
# for collection in query.all():
#     print(collection)

# print()
# query = session.query(collections_songs)
# print(query)  # SELECT * FROM collections_songs;
# for each in query.all():
#     print(each)

# print()
# query = session.query(Artists.artist_name).join(Artists.genres).filter(Genres.genre == 'Rap')
# print(query)  # выбрать всех исполнителей, у кого жанр Rap
# print(*query.all())

# print()
# query = session.query(Songs.song_id).join(collections_songs)
# print(query)  # вот здесь я не понимаю, что делается...
# for each in query.all():
#     print(each)

# print()
# query = session.query(albums_artists)
# print(query)  # SELECT * FROM albums_artists;
# for each in query.all():
#     print(each)

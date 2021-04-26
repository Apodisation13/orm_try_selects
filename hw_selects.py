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

# ЗАДАЧА 1 - посчитать сколько исполнителей в каком жанре
# SELECT genre, COUNT(*) FROM artists_genres ag
# JOIN genres g ON ag.genre_id = g.genre_id
# GROUP BY g.genre_id
# ORDER BY COUNT DESC;

print('\nЗадача 1')
query = session.query(
    Genres.genre, sq.func.count())\
    .join(artists_genres)\
    .group_by(Genres.genre_id)\
    .order_by(sq.func.count().desc())
print(query)
print(*query.all())

# ЗАДАЧА 2 - показать песни из альбомов 2019-2021гг
# SELECT song_name, year FROM songs s
# JOIN albums a ON s.album_id = a.album_id
# WHERE year BETWEEN 2019 AND 2021;

print('\nЗачада 2')
query = session.query(Songs.song_name, Albums.year).join(Albums).filter(Albums.year.between(2019, 2021))
print(query)
print(*query.all())
print(f'всего таких песен {len(query.all())}')

# ЗАДАЧА 3 - средняя продолжительность песен по альбомам
# SELECT a.album_id, album_name, AVG (duration_time) FROM albums a
# JOIN songs s ON a.album_id = s.album_id
# GROUP BY a.album_name, a.album_id
# ORDER BY album_id;

print('\nЗадача 3')
query = session.query(Albums.album_id, Albums.album_name, sq.func.AVG(Songs.duration_time)).\
    join(Songs).group_by(Albums.album_id, Albums.album_name).order_by(Albums.album_id)
print(query)
for each in (query.all()):
    print(*each)

# ЗАДАЧА 4 - только те артисты, у кого нет альбома в 2020
# SELECT artist_name FROM artists WHERE artist_name NOT IN (
# SELECT artist_name FROM artists ar
# JOIN albums al ON ar.id = al.artist_id WHERE year = 2020);

print('\nЗадача 4')
inner_query = session.query(Artists.artist_name).join(Albums).filter(Albums.year == 2020)
print(inner_query.all())
query = session.query(Artists.artist_name).filter(Artists.artist_name.notin_(inner_query))
print(query)
print(*query.all())

# ЗАДАЧА 5 - такие сборники, в которых встречается конкретный исполнитель (пусть Linkin Park)
# SELECT DISTINCT c_name FROM collections c
# JOIN collections_songs cs ON c.c_id = cs.c_id
# JOIN songs s ON s.song_id = cs.song_id
# JOIN albums al ON al.album_id = s.album_id
# JOIN artists ar ON ar.id = al.artist_id
# WHERE artist_name = 'Linkin Park';

print('\nЗадача 5')
query = session.query(Collections.c_name.distinct()).\
    join(collections_songs).join(Songs).join(Albums).join(Artists).\
    filter(Artists.artist_name == 'Linkin Park')
print(query)
print(*query.all())

# ЗАДАЧА 6 - названия альбомов, где присутствуют исполнители более 1 жанра
# SELECT album_name FROM albums WHERE artist_id IN (
# SELECT id FROM artists_genres ag
# JOIN artists ar ON ar.id = ag.artist_id
# GROUP BY ar.id
# HAVING COUNT(*) > 1);

print('\nЗадача 6')
subquery = session.query(Artists.id).join(artists_genres).group_by(Artists.id).having(sq.func.count() > 1)
query = session.query(Albums.album_name).filter(Albums.artist_id.in_(subquery))
print(query)
print(len(query.all()))
print(*query.all())

# ЗАДАЧА 7 - песни, которые не входят ни в какие сборники
# SELECT song_name FROM songs s
# FULL OUTER JOIN collections_songs cs ON cs.song_id = s.song_id
# WHERE cs.song_id IS NULL or s.song_id IS NULL;
# Оказалось, что full outer join - напрямую нет в библиотеке, да оно и не нужно, если подумать...
# SELECT song_name FROM songs s WHERE s.song_id NOT IN (
# SELECT song_id FROM collections_songs);

print('\nЗадача 7')
subquery = session.query(Songs.song_id).join(Songs.collections)
print(subquery)
print(subquery.all())
query = session.query(Songs.song_name).filter(Songs.song_id.notin_(subquery))
print(query)
print(*query.all())

# ЗАДАЧА 8 - исполнитель самого короткого (длинного) по продолжительности трека
# SELECT artist_name FROM artists ar
# JOIN albums al ON ar.id = al.artist_id
# JOIN songs s ON s.album_id = al.album_id
# WHERE duration = (SELECT MAX( duration) FROM songs);

print('\nЗадача 8')
subquery = session.query(sq.func.max(Songs.duration))
print(subquery)  # треков с максимальной длительностью оказалось 2 (4.24), а с минимальной 1.
print(*subquery.all())

# Вариант 1 = просто вывести исполнителей
query = session.query(Artists.artist_name).join(Albums).join(Songs).filter(Songs.duration == subquery)
print(query)  # здесь только имена исполнителей
print(*query.all())
# Вариант 2 - проверить что это правильные треки
query = session.query(Artists.artist_name, Songs.song_name, Songs.duration).\
    join(Albums, Albums.artist_id == Artists.id).\
    join(Songs, Songs.album_id == Albums.album_id).filter(Songs.duration == subquery)
print(query)  # здесь пришлось явно указать по каким колонкам объединять при введении в выборку названия песни и длит
for each in query.all():
    print(*each)
# 308: SAWarning: implicitly coercing SELECT object to scalar subquery
# почему так? всё выводится корректно

# ЗАДАЧА 9 - названия альбомов, содержащих наибольшее и наименьшее количество треков
# SELECT album_name, COUNT(*) FROM albums al
# JOIN songs s ON al.album_id = s.album_id
# GROUP BY al.album_name HAVING COUNT (*) =
# (SELECT MAX(c) FROM (SELECT COUNT(*) AS c FROM songs GROUP BY album_id) AS Q);

# SELECT COUNT(album_id) FROM songs GROUP BY album_id LIMIT 1;
# здесь можно получить максимальный или минимальный счётчик песен в альбоме, указывая или не указывая desc()
print('\nЗадача 9')
sq_max = session.query(sq.func.count(Songs.album_id)).group_by(Songs.album_id).order_by(sq.func.count().desc()).limit(1)
print(sq_max)
print(*sq_max.all())
sq_min = session.query(sq.func.count(Songs.album_id)).group_by(Songs.album_id).order_by(sq.func.count()).limit(1)
print(sq_min)
print(*sq_min.all())

q_max = session.query(Albums.album_name).join(Songs).group_by(Albums.album_name).having(sq.func.count() == sq_max)
print(q_max)
print(*q_max.all())
q_min = session.query(Albums.album_name).join(Songs).group_by(Albums.album_name).having(sq.func.count() == sq_min)
print(q_min)
print(*q_min.all())

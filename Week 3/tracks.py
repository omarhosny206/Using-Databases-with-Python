import xml.etree.ElementTree as ET
import sqlite3

connection = sqlite3.connect('tracksdb.sqlite')
cursor = connection.cursor()

# Make some SQL for our DB
cursor.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);

''')

file_name = input('Enter file name: ')
if (len(file_name) < 1): file_name = 'Library.xml'


def Lookup(dic, key):
    found = False
    for child in dic:
        if found:
            return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None


stuff = ET.parse(file_name)
all = stuff.findall('dict/dict/dict')
print('Dict count:', len(all))

for entry in all:
    if (Lookup(entry, 'Track ID') is None):
        continue

    name = Lookup(entry, 'Name')
    artist = Lookup(entry, 'Artist')
    album = Lookup(entry, 'Album')
    count = Lookup(entry, 'Play Count')
    rating = Lookup(entry, 'Rating')
    length = Lookup(entry, 'Total Time')
    genre = Lookup(entry, 'Genre')

    if name is None or artist is None or album is None or genre is None:
        continue

    print(name, artist, album, count, genre, rating, length)

    cursor.execute(
        '''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', (artist, ))
    cursor.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = cursor.fetchone()[0]

    cursor.execute(
        '''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''', (album, artist_id))
    cursor.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cursor.fetchone()[0]

    cursor.execute(
        '''INSERT OR IGNORE INTO Genre (name) 
        VALUES ( ?)''', (genre, ))
    cursor.execute('SELECT id FROM Genre WHERE name = ? ', (genre, ))
    genre_id = cursor.fetchone()[0]

    cursor.execute(
        '''INSERT OR REPLACE INTO Track
        (title, album_id, genre_id,len, rating, count) 
        VALUES ( ?, ?, ?, ?,?, ? )''',
        (name, album_id, genre_id, length, rating, count))

    connection.commit()
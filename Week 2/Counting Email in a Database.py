import sqlite3

connection = sqlite3.connect('orgsDB.sqlite')
cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS Counts')

cursor.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

file_name = input('Enter file name: ')
if (len(file_name) < 1):
    file_name = 'mbox.txt'

file_handler = open(file_name)

for line in file_handler:
    if not line.startswith('From: '):
        continue
    peices = line.split()
    email = peices[1]
    org = email.split('@')[1]
    cursor.execute('SELECT count FROM Counts WHERE org = ? ', (org, ))
    row = cursor.fetchone()

    if row is None:
        cursor.execute(
            '''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org, ))
    else:
        cursor.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                       (org, ))

    connection.commit()

sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cursor.execute(sqlstr):
    print(str(row[0]), row[1])

cursor.close()
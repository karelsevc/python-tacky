import sqlite3
import csv

#    from PIL import Image

# název CSV souboru a název SQLite databáze
csv_file = 'prirustek.csv'
db_file = 'Prirustek.db'

# vytvoření připojení k databázi
conn = sqlite3.connect(db_file)
c = conn.cursor()
delete_all_rows_query = 'DELETE FROM TackyKmen;'
c.execute(delete_all_rows_query)
conn.commit()

# vytvoření tabulky v databázi
table_name = 'TackyKmen'
# c.execute('CREATE TABLE IF NOT EXISTS {} (sloupec1 TEXT, sloupec2 INTEGER, sloupec3 REAL)'.format(table_name))
counter = 0
# otevření CSV souboru a načtení dat
with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='|')
#    přeskočení hlavičky (pokud existuje)
#    header = next(reader, None)
#    vložení dat z CSV souboru do databáze
    for row in reader:
        row[7] = 'None'
        with open(row[2], 'rb') as soubor1:
            binarni_obrazek1 = soubor1.read()
        if row[3] != 'None' and row[4] == 'None':
            with open(row[3], 'rb') as soubor2:
                binarni_obrazek2 = soubor2.read()
                myrow = (row[0], row[1], sqlite3.Binary(binarni_obrazek1), sqlite3.Binary(binarni_obrazek2),
                         row[4], row[5], row[6], row[7], row[8])
        elif row[3] == 'None' and row[4] != 'None':
            with open(row[4], 'rb') as soubor3:
                binarni_obrazek3 = soubor3.read()
                myrow = (row[0], row[1], sqlite3.Binary(binarni_obrazek1), row[3],
                         sqlite3.Binary(binarni_obrazek3), row[5], row[6], row[7], row[8])
        elif row[3] == 'None' and row[4] == 'None':
            myrow = (row[0], row[1], sqlite3.Binary(binarni_obrazek1), row[3],
                     row[4], row[5], row[6], row[7], row[8])
        elif row[3] != 'None' and row[4] != 'None':
            with open(row[3], 'rb') as soubor2:
                binarni_obrazek2 = soubor2.read()
            with open(row[4], 'rb') as soubor3:
                binarni_obrazek3 = soubor3.read()
                myrow = (row[0], row[1], sqlite3.Binary(binarni_obrazek1), sqlite3.Binary(binarni_obrazek2),
                         sqlite3.Binary(binarni_obrazek3), row[5], row[6], row[7], row[8])

        print(myrow)
#        print(format(table_name))
        c.execute('INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'.format(table_name), myrow)
        counter += 1

# potvrzení změn a uzavření připojení k databázi
conn.commit()
conn.close()
print(f'Nacteno - pocet radku : {counter}')

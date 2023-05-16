import sqlite3
import shutil
import os
import csv
from datetime import date
import zipfile

csv_file = 'tackyNew.csv'   # name CSV file name SQLite database
db_file = 'Tacky.db'

today = date.today()
year = today.year
month = today.month
day = today.day

conn = sqlite3.connect(db_file)   # create a database connection
c = conn.cursor()  # create cursor
delete_all_rows_query = 'DELETE FROM TackyNew;'
c.execute(delete_all_rows_query)
conn.commit()
citac = 0
table_name = 'TackyNew'
# open CSV file and load data into TackyNew table
with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='|')
    for row in reader:
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
        c.execute('INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'.format(table_name), myrow)
        citac += 1
# confirm changes and close database connection
conn.commit()
conn.close()

print(f'Pocet radku v databazi: {citac}')
# dir_src = "c:\\Users\\Karel\\PycharmProjects\\python_tacky\\ObrKmenC"
# dir_dst = "c:\\Users\\Karel\\PycharmProjects\\python_tacky\\Archivace"


def move_file(adresarod, adresarkam):
    akt_adresar = os.getcwd()
    dir_src = akt_adresar + adresarod
    print(f'Zdrojovy adrear: {dir_src} ')
    dir_dst = akt_adresar + adresarkam
    print(f'Cilovy adresar: {dir_dst} ')
#   input("Pokracovat: ?")
    print('   Presun souboru: Cekej ....')
    os.chdir(dir_src)    # musim nastavovat odkud kopiruji
    files = os.listdir(dir_src)
#   print(files)
    for soub in files:
        if os.path.isfile(soub):
            shutil.move(soub, dir_dst)
    os.chdir(akt_adresar)  # Nastaveni na aktualni adresar


print(f'Aktualni adresar: {os.getcwd()}')
move_file('\\ObrKmenC', '\\Archivace')   # Presun souboru do adresare Archivace
move_file('\\ObrKmenD', '\\Archivace')
move_file('\\ObrKmenE', '\\Archivace')

print('Zalohovani .... Zipovani archivace, databaze Tacky : Cekej ..... ')


def zip_directory(inputdir, outputdir, outputfilename):
    # Vytvoříme prázdný zip soubor v outputdir s názvem outputfilename
    zip_path = os.path.join(outputdir, outputfilename)
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        # Projdeme všechny soubory v inputdir a přidáme je do zip souboru
        for root, dirs, files in os.walk(inputdir):
            for soubor in files:
                file_path = os.path.join(root, soubor)
                # Vytvoříme cestu souboru v zip souboru - bez prefixu inputdir
                zip_path = os.path.relpath(file_path, inputdir)
                zip_file.write(file_path, zip_path)

    print(f"Soubory v adresáři {input_dir} byly zazipovány do {output_dir}")


file_list = ['tackyKmen.csv', 'Tacky.db', 'Tacky.sqbpro', 'tackyNew.csv']
aktadresar = os.getcwd()
input_dir = aktadresar + '\\Archivace'
output_dir = aktadresar + '\\Export'
output_filename = f'archiv.{year}.{month}.{day}.zip'

print(aktadresar)
print(input_dir)
print(output_dir)

for file in file_list:
    if os.path.isfile(file):
        shutil.copy(file, input_dir)

soubory = os.listdir(input_dir)
print('Smazani vsech souboru v Archivace ... Cekej .... ')
try:
    zip_directory(input_dir, output_dir, output_filename)
    for file_name in soubory:
        os.remove(input_dir + '\\' + file_name)
except Exception as e:
    print(e)
else:
    print('probehlo OK')

print('Zalohy provedeny   .... pokracuji v update Databaze  ...\n')
print(f'Aktualni adresar: {os.getcwd()}')
move_file('\\ObrNewC', '\\ObrKmenC')
move_file('\\ObrNewD', '\\ObrKmenD')
move_file('\\ObrNewE', '\\ObrKmenE')

# Name field Sbirka from Excel table i.e. key to my_list []
conn = sqlite3.connect('Tacky.db')
cursor = conn.cursor()
cursor.execute('SELECT Pivovar,Nazev FROM TackyKmen')
counter = 0
my_list = []
for row in cursor.fetchall():
    klic = row[1]
    my_list.append(klic)
    counter += 1

cursor.close()
conn.close()

# Reading the fields in the Table and updating the new Table
conn = sqlite3.connect('Tacky.db')
for polozka in my_list:
    cursor = conn.cursor()
    select_query = "SELECT Nazev, Sbirka, Datum FROM TackyKmen WHERE Nazev = ?"
    condition_param = (polozka,)
    row = cursor.execute(select_query, condition_param).fetchone()
    print(f'Aktualizuji radku: {row}')
    update_query = "UPDATE TackyNew SET Sbirka = ?, Datum = ? WHERE Nazev = ?"
    update_params = (row[1], row[2], polozka)
    cursor.execute(update_query, update_params)
    conn.commit()

cursor.close()
conn.close()  # terminate database connection
print(f'Pocet radek: {counter}')

print('Provadim zamenu tabulek  ............')
con = sqlite3.connect('Tacky.db')
cursor = con.cursor()
cursor.execute('''
          ALTER TABLE TackyKmen RENAME TO TackyOld
          ''')
cursor.execute('''
          ALTER TABLE TackyNew RENAME TO TackyKmen
          ''')
cursor.execute('''
          DROP TABLE TackyOld
          ''')
con.commit()

cursor.close()
con.close()
print('Aktualizace ukoncena  .... ')

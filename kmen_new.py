import pandas as pd
from openpyxl_image_loader import SheetImageLoader
from openpyxl import load_workbook
import csv
from datetime import date
import sqlite3
from tkinter import *
from tkinter import filedialog
import os
# import warnings
# Docasne potom smazat
# warnings.filterwarnings("ignore",
# message="Data Validation extension is not supported and will be removed", category=UserWarning)

jmeno_souboru = " "


def opensoubor():
    global jmeno_souboru
    filepath = filedialog.askopenfilename(initialdir="Import",
                                          # initialdir="c:\\Users\\Karel\\PycharmProjects\\python_tacky\\Import",
                                          title="Open OK",
                                          filetypes=(("excel files", "*.xlsx"), ("all files", "*.*")))

    jmeno_souboru = filepath
    print(f'Byl vybran soubor:  {jmeno_souboru}')
    window.destroy()


window = Tk()
window.attributes('-topmost', True)
window.geometry("300x60")
window.title("Vyber Excel")
label_my = Label(window, text='Vyber Excel soubor xlsx', font=('Ariel', 10))
button = Button(text="OK",
                font=('Arial', 10),
                command=opensoubor)
label_my.pack(side=BOTTOM)
button.pack(side=BOTTOM)
window.mainloop()

if jmeno_souboru == " ":
    exit()

print('Provadim zpracovani ....')

akt_adresar = os.getcwd()
print(akt_adresar)

# def is_directory_empty(path):
#     with os.scandir(path) as entries:
#         return next(entries, None) is None


def is_directory_empty(path):
    return len(os.listdir(path)) == 0


def is_prazdny_adresar(adres):
    path = akt_adresar + '\\' + adres
    if is_directory_empty(path):
        print(f"Adresář {adres} je prázdný")
    else:
        print(f"Chyba: Adresář {adres} obsahuje soubory nebo složky")
        exit()


is_prazdny_adresar('ObrNewC')
is_prazdny_adresar('ObrNewD')
is_prazdny_adresar('ObrNewE')

celkem_row = 0  # pocet radku pres vsechny slozky

today = date.today()
year = today.year
month = today.month
day = today.day
print('Vytvarim tabulku TackyNew \n')
# Vytvoreni tabulky
con = sqlite3.connect('Tacky.db')
cursor = con.cursor()
cursor.execute('''
               CREATE TABLE IF NOT EXISTS "TackyNew" (
                            "Pivovar"	TEXT,
                            "Nazev"	    TEXT NOT NULL,
                            "PS"    	BLOB NOT NULL,
                            "ZS"    	BLOB,
                            "Detail"	BLOB,
                            "Popis"	    TEXT,
                            "Rozmer"	TEXT,
                            "Sbirka"	TEXT NOT NULL CHECK("Sbirka" IN ('A','N','X','None')),
                            "Datum"	    TEXT NOT NULL,
                            PRIMARY KEY("Nazev")
                                                     )
               ''')
con.commit()
con.close()

# Vypsání počtu řádků v tabulce

with open('tackyNew.csv', 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter='|')
# jiny odkaz na obrazek do csv file a jinam ulozim pozdejsim obrazek presunutim
    cestaCp = 'ObrNewC/'
    cestaDp = 'ObrNewD/'
    cestaEp = 'ObrNewE/'
# iterace pres vsechny sheet
    dfs = pd.ExcelFile(jmeno_souboru)
    for sheet_name in dfs.sheet_names[3:]:
        df = pd.read_excel(jmeno_souboru, header=1, sheet_name=sheet_name)
        print('-------------------------------------------------------------------------------------------------------')
        poc_radku = len(df)
        celkem_row = celkem_row + poc_radku
        print(f"Ve slozce: {sheet_name} pocet radku je : {poc_radku}")
        pxl_doc = load_workbook(jmeno_souboru)
        sheet = pxl_doc[sheet_name]
        image_loader = SheetImageLoader(sheet)
        radka = 2
# Iterace přes všechny řádky
        for index, row in df.iterrows():
            img_soubor = str(radka)
            obrazekCp = f"{cestaCp}Kmen_{sheet_name}_{img_soubor}.jpg"
            obrazekDp = None
            obrazekEp = None
            countObr = radka + 1   # ma jine cislovani je od 1
            img_soubor = str(countObr)
            radka = radka + 1   # inkrementuj radku v sesitu
            precti = 'C' + img_soubor   # prectu sloupec 'C1' 'C2' 'C3' atd. podle citace
            image = image_loader.get(precti)
            image.thumbnail((90, 90))
            image.save(obrazekCp)
            # Sloupec D
            precti = 'D' + img_soubor  # prectu sloupec 'D1' 'D2' 'D3' atd. podle citace
            if image_loader.image_in(precti):
                try:
                    image = image_loader.get(precti)
                    image.thumbnail((90, 90))
                    obrazekDp = f"{cestaDp}Obrazky_D_{sheet_name}_{img_soubor}.jpg"
                    image.save(obrazekDp)
#                    print('Buňka  obsahuje obrázek')
                except ValueError:
                    print(f'Bunka {precti} ve slozce {sheet_name} neobsahuje obrázek')
            precti = 'E' + img_soubor  # prectu sloupec 'D1' 'D2' 'D3' atd. podle citace
            if image_loader.image_in(precti):
                try:
                    image = image_loader.get(precti)
                    image.thumbnail((90, 90))
                    obrazekEp = f"{cestaEp}Obrazky_E_{sheet_name}_{img_soubor}.jpg"
                    image.save(obrazekEp)
#                    print('Buňka  obsahuje obrázek')
                except ValueError:
                    print(f'Bunka {precti} ve slozce {sheet_name} neobsahuje obrázek')
            rowSbirka = 'None'
            row_new = f"{row[0]}| {row[1]}| {obrazekCp}| {obrazekDp}| {obrazekEp}| {row[5]}| " \
                      f"{row[6]}| {rowSbirka}| {day}.{month}.{year}"
            row = row_new
#            print(row)   # vytiskni zpracovanou radku
            rowtuple = (row.split("| "))
            print(rowtuple)
            writer.writerow(rowtuple)

# zapiname varovani
# warnings.resetwarnings()
print('Zpracovani dobehlo .....')
print(f"Celkem radku: {celkem_row}")

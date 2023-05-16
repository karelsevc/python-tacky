from tkinter import *
import sqlite3
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
from io import BytesIO

pocettacku = 0
pocetsbira = 0
pocetvylou = 0


def click1():
    global pocettacku
    global pocetsbira
    global pocetvylou
    con = sqlite3.connect('Tacky.db')
    cursor = con.cursor()
    dotaz1 = 'select count(*) from TackyKmen;'
    pocettacku = cursor.execute(dotaz1).fetchone()
    dotaz2 = "select count(*) from TackyKmen where Sbirka = 'A';"
    pocetsbira = cursor.execute(dotaz2).fetchone()
    dotaz3 = "select count(*) from TackyKmen where Sbirka = 'X';"
    pocetvylou = cursor.execute(dotaz3).fetchone()
    cursor.close()
    con.close()
    new_window = Tk()
    new_window.geometry("400x100")
    new_window.title("Statistika")
    new_window.config(background='white')

    Label(new_window, text=f'Celkový počet tácků: {pocettacku[0]}    ',
          font=('Arial', 10), fg='black', bg='white').pack()

    Label(new_window, text=f'Počet tácků ve sbírce: {pocetsbira[0]}   ',
          font=('Arial', 10), fg='black', bg='white').pack()

    Label(new_window, text=f'Počet vyloučených ze sbírky: {pocetvylou[0]}   ',
          font=('Arial', 10), fg='black', bg='white').pack()

    new_window.mainloop()


def click2():
    # Vytvoření nového PDF souboru
    button2.config(text='  Čekej ...   ', bg='red')
    button2.update()
    pdf_file = "Export\\chybenka.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)


    def repeat_numbers():
        number50 = [50]
        number250 = [250]
        number450 = [450]
        repeated_numbers = number50 * 7 + number250 * 7 + number450 * 7
        return repeated_numbers

    xsouradnice = repeat_numbers()
    print('Cekej ... priprava na tisk ... ')

    path = 'ObrKmenC/'
    akt_adr = os.getcwd()
    adr_dst = akt_adr + '/ObrChybenka'
    soubory = os.listdir(adr_dst)
    for file_name in soubory:   # smazani souboru v adresari ObrChybenka
        os.remove(adr_dst + '\\' + file_name)
#        print('Prevadim obrazky do ObrChybenka')
    for file_name in os.listdir(path):
        #  zpracujeme pouze soubory s příponou .jpg nebo .jpeg
        if file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
            # načteme obrázek
            img = Image.open(os.path.join(path, file_name))
            # změníme velikost obrázku na rozměr 90x90 pixelů
            img.thumbnail((80, 80))
            # uložíme změněný obrázek do původního souboru
            img.save(os.path.join(adr_dst, file_name))

    def vykresly():
        index = 0
        y = 650
        for polozka in chybtacky:
            x = xsouradnice[index]
            print(polozka[0])
            img1 = Image.open(BytesIO(polozka[1])).convert('RGB')
            c.drawInlineImage(img1, x, y)
            c.setFont("Helvetica", 9)
            c.drawString(x + 25, y + 90, polozka[0])
            y -= 100
            index += 1
            if index == 7 or index == 14:
                y = 650

    chybtacky = ()

    conn = sqlite3.connect('Tacky.db')
    # cursor = conn.cursor()
    cursor = conn.cursor()
    # zjistíme počet záznamů v tabulce
    cursor.execute("SELECT COUNT(*) FROM TackyKmen WHERE Sbirka = 'N'")
    pocet_zaznamu = cursor.fetchone()[0]
    # pocet_zaznamu = int(pocet_zaznamu / 2)
    cursor.close()

    for i in range(0, pocet_zaznamu, 21):
        chybtacky = []
        cursor = conn.cursor()
        query = "SELECT Nazev, PS FROM TackyKmen  WHERE Sbirka = 'N' LIMIT 21 OFFSET ?"
        condition_param = (i,)
        chybtacky = cursor.execute(query, condition_param).fetchall()
        #   uložíme záznamy do proměnné
        #   cursor.close()
        #    print(chybtacky)
        page_num = c.getPageNumber()
        text = "Strana %s" % page_num
        c.drawString(270, 770, text)
        vykresly()
        c.showPage()

    c.save()
    cursor.close()
    conn.close()
    button2.config(text='      OK     ', bg='green')
    button2.update()
    print('Vypocet probehl, uzavri program krizkem ....')


window = Tk()
window.geometry("700x400")
window.title("Coasters")
window.config(background='white')

photo = PhotoImage(file='Obrazky\\tacky300x400.png')
photosvejk = PhotoImage(file='Obrazky\\svejk80x60.png')

Label(window, font=('Arial', 40, 'bold'), fg='black', bg='white', image=photo).place(x=40, y=60)

Button(window, text="Statistika   ",
       command=click1, font=('Comic Sans', 10), fg='black', bg='#DAE0E0',
       activeforeground='white', activebackground='black', image=photosvejk,
       compound='left').place(x=500, y=60)

Label(window, text='Stiskni tlačítko,\n počty tácků ve sbírce ',
      font=('Arial', 10), fg='black', bg='white').place(x=520, y=140)

button2 = Button(window, text="Chyběnka  ", command=click2, font=('Comic Sans', 10),
                 fg='black', bg='#DAE0E0', activeforeground='white', activebackground='black',
                 image=photosvejk, compound='left')

button2.place(x=500, y=240)

Label(window, text='Stiskni tlačítko,\n soubor najdeš v adresáři export',
      font=('Arial', 10), fg='black', bg='white').place(x=490, y=320)

window.mainloop()

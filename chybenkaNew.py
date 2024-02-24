from tkinter import *
import sqlite3
from unidecode import unidecode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
from io import BytesIO


def click2():
    hodnotas1 = hodnota1 + '%'
    hodnotas2 = hodnota2 + '%'
    hodnotas3 = hodnota3 + '%'
    print("Zadaná hodnota1:", hodnotas1)
    print("Zadaná hodnota2:", hodnotas2)
    print("Zadaná hodnota3:", hodnotas3)
    # Vytvoření nového PDF souboru
    button2.config(text='  Čekej ...   ', bg='red')
    button2.update()
    pdf_file = "Export\\chybenka.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)
    print('Cekej ... priprava na tisk ... ')
    conn = sqlite3.connect('Tacky.db')
    cursor = conn.cursor()
    select_query = ("SELECT Pivovar, Nazev, PS, ZS, Detail, Popis, Rozmer FROM TackyKmen "
                    "WHERE Sbirka = 'N' and Nazev NOT LIKE ? and Nazev NOT LIKE ? and Nazev NOT LIKE ?")
    condition_param = (hodnotas1, hodnotas2, hodnotas3,)
    rows = cursor.execute(select_query, condition_param).fetchall()
    lines_per_page = 7
    lines = lines_per_page
    p = 700
    hlavicka = 1
    for row in rows:
        if hlavicka == 1:
            image_path = 'Obrazky\\chybenka.png'
            c.drawInlineImage(image_path, 55, p+40, 470, 35)
            hlavicka = 0
        c.setFont("Courier", 10)
        textnaz = row[1]
        textnaz_bez = unidecode(textnaz)
        c.drawString(55, p, textnaz_bez)
        c.setFont("Courier", 9)
        imageps = Image.open(BytesIO(row[2])).convert('RGB')
        c.drawInlineImage(imageps, 110, p-30, width=60, height=60)
        imagezs = row[3]
        if imagezs != 'None':
            imagezs = Image.open(BytesIO(row[3])).convert('RGB')
            c.drawInlineImage(imagezs, 180, p-30, width=60, height=60)
        imagedet = row[4]
        if imagedet != 'None':
            imagedet = Image.open(BytesIO(row[4])).convert('RGB')
            c.drawInlineImage(imagedet, 250, p-30, width=60, height=60)
        textpop = row[5]
        if textpop != 'nan':
            textpop_bez = unidecode(textpop)
            tisk = 0
            index = textpop_bez.find("\n") or textpop_bez.find("\r\n")
            if index != -1:
                radka = textpop_bez.split("\n")
                textpop_bez1 = radka[0]
                textpop_bez2 = radka[1]
                c.drawString(250, p-40, textpop_bez1)
                c.drawString(250, p-50, textpop_bez2)
                tisk = 1
            if len(textpop_bez) > 60 and (tisk == 0):
                textpop_bez1long = textpop_bez[:50]
                textpop_bez2long = textpop_bez[50:]
                c.drawString(250, p-40, textpop_bez1long)
                c.drawString(250, p-50, textpop_bez2long)
                tisk = 1
            if tisk == 0:
                c.drawString(250, p-40, textpop_bez)
        textroz = row[6]
        if textroz != 'nan':
            c.drawString(480, p+15, textroz)
        textpiv = row[0]
        textpiv_bez = unidecode(textpiv)
        c.drawString(55, p-47, textpiv_bez)
        c.line(55, p-53, 520, p-53)
        p -= 85
        lines = lines - 1
        if lines < 0:
            lines = lines_per_page
            p = 750
            c.showPage()
            hlavicka = 1
    c.save()
    cursor.close()
    conn.close()
    button2.config(text='      OK     ', bg='green')
    button2.update()
    print('Vypocet probehl, uzavri program krizkem ....')


def pridlab(hod):
    Label(window, font=('Courier', 10), text='Omezeno na: ' + hod).place(x=250, y=20)


def display():
    global hodnota1, hodnota2, hodnota3
    if x.get() == 1:
        if len(hodnota1) == 3:
            hodnota1 = vstup1.get().upper()[0:3]
        else:
            hodnota1 = 'XXX'
    if y.get() == 1:
        if len(hodnota2) == 3:
            hodnota2 = vstup2.get().upper()[0:3]
        else:
            hodnota2 = 'XXX'
    if z.get() == 1:
        if len(hodnota3) == 3:
            hodnota3 = vstup3.get().upper()[0:3]
        else:
            hodnota3 = 'XXX'
    hod = hodnota1 + ' ' + hodnota2 + ' ' + hodnota3
    pridlab(hod)


window = Tk()
window.geometry("700x400")
window.title("Coasters")
window.config(background='white')

photo = PhotoImage(file='Obrazky\\tacky300x400.png')
photosvejk = PhotoImage(file='Obrazky\\svejk80x60.png')

Label(window, font=('Arial', 40, 'bold'), fg='black', bg='white', image=photo).place(x=40, y=60)


x = IntVar()
check_button1 = Checkbutton(window,
                            text='Kod pivovaru 1',
                            variable=x,
                            onvalue=1,
                            offvalue=0,
                            padx=50,
                            pady=4,
                            command=display)
check_button1.place(x=470, y=20)

y = IntVar()
check_button2 = Checkbutton(window,
                            text='Kod pivovaru 2',
                            variable=y,
                            onvalue=1,
                            offvalue=0,
                            padx=50,
                            pady=4,
                            command=display)
check_button2.place(x=470, y=50)

z = IntVar()
check_button3 = Checkbutton(window,
                            text='Kod pivovaru 3',
                            variable=z,
                            onvalue=1,
                            offvalue=0,
                            padx=50,
                            pady=4,
                            command=display)
check_button3.place(x=470, y=80)

vstup1 = Entry(window, font=('Courier', 10), width=3)
vstup1.place(x=630, y=25)
vstup1.insert(0, "XXX")
hodnota1 = vstup1.get()

vstup2 = Entry(window, font=('Courier', 10), width=3)
vstup2.place(x=630, y=55)
vstup2.insert(0, "XXX")
hodnota2 = vstup2.get()

vstup3 = Entry(window, font=('Courier', 10), width=3)
vstup3.place(x=630, y=85)
vstup3.insert(0, "XXX")
hodnota3 = vstup3.get()

button2 = Button(window, text="Chyběnka  ", command=click2, font=('Arial', 10),
                 fg='black', bg='#DAE0E0', activeforeground='white', activebackground='black',
                 image=photosvejk, compound='left')
button2.place(x=500, y=240)

Label(window, text='Stiskni tlačítko,\n soubor najdeš v adresáři export',
      font=('Arial', 10), fg='black', bg='white').place(x=490, y=320)

window.mainloop()

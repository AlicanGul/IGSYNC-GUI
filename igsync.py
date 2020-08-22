# a. gul, temmuz 2020 
#------------------------
# IGSYNC-GUI
#------------------------
# IGPSPORT surus dosyalarini PC'ye yedeklemek icin kullanilir.
#-------------------------------------------------------------

import tkinter.filedialog
import tkinter as tk
from tkinter import ttk
import os, string
import configparser as cfgp
from dirsync import sync

# ayar dosyasi
program_yolu = os.path.dirname(os.path.abspath(__file__))
ayar_dosyasi = program_yolu + "\\ayar.ini"
ayarlar = cfgp.ConfigParser()
try:
    ayarlar.read(ayar_dosyasi)
except:
    print("Ayar dosyasi okunamadi!")

# global nesneler
# tkinter penceresi
penc = tk.Tk()
penc.title("IGSYNC")
penc.minsize(400,100)
penc.resizable(False, False)

# degiskenler
t_cihaz = tk.StringVar( )
t_hedef_yol = tk.StringVar(value=ayarlar['genel']['son_hedef_yol'])
t_durum = tk.StringVar ( value="Program basladi.")
b_esitle_aktif = False

# fonksiyonlar
def cihazBul():
    kaynak_yol = ""
    for harf in string.ascii_uppercase:
        if os.path.exists( '{}:\\iGPSPORT\\Activities'.format(harf) ):
            kaynak_yol = '{}:\\iGPSPORT\\Activities'.format(harf)
            global b_esitle_aktif
            b_esitle_aktif = True
            t_durum.set("Cihaz bulundu.")
            break
    if kaynak_yol == "":
        t_durum.set("Cihaz bulunamadi.")
        return "Kaynak cihaz bulunamadi."
    else:
        return kaynak_yol

def cbYenile():
    t_cihaz.set( cihazBul() )
    

def cbGozat():
    temp_hedef_yol = tk.filedialog.askdirectory()
    if temp_hedef_yol != "":
        t_hedef_yol.set()
    else:
        t_durum.set("Klasor secilmedigi icin degistirilmedi.")
    ayarlar['genel']['son_hedef_yol'] = t_hedef_yol.get()
    with open (ayar_dosyasi, mode='w') as ayardosyasi:
        ayarlar.write( ayardosyasi )

def cbEsitle():
    if b_esitle_aktif:
        if os.path.exists(t_hedef_yol.get()) & os.path.exists(t_cihaz.get()) :
            t_durum.set("Esitleniyor...")
            sync( t_cihaz.get(), t_hedef_yol.get(), 'sync', verbose=True, exclude=[r"^List"] )
            t_durum.set("Esitleme tamamlandi.")
        else:
            t_durum.set("Hedef veya kaynak klasor bulunamadi.")
    else:
        t_durum.set("Kaynak ve hedef yol secin.")

# widgetlar
lbl_cihaz = tk.Label( textvar=t_cihaz )
ent_hedef_yol = tk.Entry( textvar=t_hedef_yol )
trw_surusler = ttk.Treeview( columns=('tarih', 'boyut') )
lbl_durum = tk.Label( textvar=t_durum )
but_yenile = tk.Button( text='Yenile', command=cbYenile )
but_gozat = tk.Button ( text='Gozat...', command=cbGozat )
but_esitle = tk.Button( text='Esitle', command=cbEsitle )
frm_sonuc = tk.Frame( background="yellow" )

# grid
# sutun 1
lbl_cihaz.grid(row=1, column=1, sticky=tk.EW)
ent_hedef_yol.grid(row=2, column=1, sticky=tk.EW)
lbl_durum.grid(row=3, column=1)
# sutun 2
but_yenile.grid(row=1, column=2, sticky=tk.EW)
but_gozat.grid(row=2, column=2, sticky=tk.EW)
but_esitle.grid(row=3, column=2, sticky=tk.EW)
# grid ayarlari
penc.rowconfigure(1, weight=1)
penc.rowconfigure(2, weight=1)
penc.rowconfigure(3, weight=1)
penc.columnconfigure(1, weight=3)
penc.columnconfigure(2, weight=2)

# baslangic
cbYenile()

# ana dongu
penc.mainloop()

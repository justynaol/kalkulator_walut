from tkinter import *
from tkinter import messagebox

try:
    import requests
    library_available = True
except:
    library_available = False

class UjemnaError(Exception):
    pass

class Kalkulator(object):
    def __init__(self):
        self.przelicznik = None
        self.okno=Tk()
        self.okno.geometry("270x250")
        self.okno.title("Kalkulator walut")
        self.waluty=['GBP', 'USD', 'EUR', 'CHF', 'UAH', 'CZK', 'TRY', 'PHP']
        self.etykiety={}
        self.pola={}
        self.utworz_widzety()
        self.okno.mainloop()
        
    def utworz_widzety(self):
        self.etykieta1=Label(self.okno,text="Podaj kwotę w PLN:", font="ARIAL 10 bold")
        self.etykieta1.grid(row=0,column=0,sticky=W)
        self.pole1=Entry(self.okno,width=12,font="ARIAL 10")
        self.pole1.grid(row=0,column=1,sticky=W)
        self.przycisk=Button(self.okno,text="Przelicz", font="ARIAL 10 bold", command=self.przelicz,width=27, height=1)
        self.przycisk.grid(row=1,column=0, columnspan=2,sticky=W)
        for i in range(len(self.waluty)):
            waluta = self.waluty[i]
            etykieta=Label(self.okno,text="W "+waluta,font="ARIAL 10 bold")
            etykieta.grid(row=2+i,column=0,sticky=W)
            self.etykiety[waluta]=etykieta       
            pole=Entry(self.okno,width=12,font="ARIAL 10")
            pole.grid(row=2+i,column=1,sticky=W)
            self.pola[waluta]=pole
    def przelicz(self):
        for i in range(len(self.waluty)):
            waluta = self.waluty[i]
            self.pola[waluta].delete(0,END)
        try:
            pln=float(self.pole1.get().replace(',', '.'))
            if pln<0:
                raise UjemnaError
        except UjemnaError:
            messagebox.showerror("Błąd","Wartości ujemne") 
        except ValueError:
            messagebox.showerror("Błąd","Niepoprawny format")
        else:
            if self.przelicznik is None:
                self.przelicznik = Przelicznik()
            for i in range(len(self.waluty)):
                waluta = self.waluty[i]           
                self.pola[waluta].insert(0,"{0:.2f}".format(round(self.przelicznik.oblicz(pln,waluta),2)))

class Przelicznik(object):
    def __init__(self):
        try:
            exchangerates = requests.get("http://api.nbp.pl/api/exchangerates/tables/a?format=json").json()
            rates = exchangerates[0]["rates"]
            self.kursy = {k["code"] : k["mid"] for k in rates}
        except:
            if library_available:
                messagebox.showinfo("Błąd pobierania kursów walut","Nie udało się pobrać kursów walut. Zostaną wykorzystane domyślne wartości")
            else:
                messagebox.showinfo("Błąd pobierania kursów walut","Nie znaleziono biblioteki 'requests'. Zostaną wykorzystane domyślne wartości")
            self.kursy = {'USD': 3.7255,'EUR': 4.5354,'CHF': 4.2102, 'GBP': 5.092, 'UAH': 0.1324,'CZK': 0.1737,'TRY': 0.5044,'PHP': 0.0775}

    def oblicz(self,pln,waluta):
        return pln/self.kursy[waluta]        

ap=Kalkulator()   

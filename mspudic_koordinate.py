#progrmaski kod za dohvat podataka sa TodoistAPI, spremanje u tekstualnu datoteku i slanje na batchgeo platformu i kreiranje linka koji se salje na postavljeni mail koji je hardcoded
#mail i ostale stvari mogu se popraviti da se zatrazi unos na koji mail se salje link za kartu to je najmanji problem slozit
#importovi neke se moze maknut kome se da radit na tome slobodno neka makne  ovaj from datetime import datetime i ovaj from helium import drag_file i testira kod nakon toga
#kod je potrebno prebacit u exe file i potrebno je testirati nakon toga
from datetime import datetime
from io import IncrementalNewlineDecoder
from dateutil import parser
from datetime import *
from helium import drag_file
from helium import *
import time
import os
import sys
from helium._impl import FileInput
from todoist.api import TodoistAPI
from selenium.webdriver import ChromeOptions


#Todoist API code
api = TodoistAPI('9dc003676c1428d5430099c43fca59f09b9dd85b')
api.sync()
#Dohvacanje projekata nepotreban kod ali neka stoji za ubudce ne skodi ne usporava kod nista posebno
projects = api['projects']
items = api.projects.get_data(2240990683)
#Dobivanje danasnjeg datuma
danas = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
danasdatum = parser.parse(danas)
print(danasdatum)
#kreiranje datoteke Batchgeoinfo.txt
f= open("Batchgeoinfo.txt","w+")
f.close()
pocetno = "name\ttime\tlatitude\tlongitude"



#unos stringa pocetno u tekstualnu datoteku Batchgeoinfo
with open('Batchgeoinfo.txt', 'r+', encoding='utf-8') as f:
    f.seek(0)
    print(pocetno, file=f)
    f.truncate()

#trazenje podataka sa API  o imenu taska i datuma 
for  item in items["items"]:
    if (item["due"] and item['description']):
        datumtaska = parser.parse(item["due"]["date"])
        datumtaska = datumtaska.replace(tzinfo=None)
        datumtaskavrijeme = datumtaska
        datumtaskavrijeme = datumtaskavrijeme.strftime('%H:%M:%S')

        #datumustring =  '-'.join([str(elem) for elem in datumtaskasplit])
        #datumtaska = datumustring
        print(datumtaska)
        
        #provjera za sutrasnji datum
        if danasdatum  < datumtaska and danasdatum + timedelta(1)  > datumtaska:
            with open('Batchgeoinfo.txt', 'a', encoding='utf-8') as f:
                
                splitanikord = item['description'].split()
                #razdvajanje koordinata na 2 dijela tabom kako bi se moglo unosit u Batchgeo
                listaustring = '\t'.join([str(elem) for elem in splitanikord])
                #upis podataka u tekstualnu datoteku 
                print(item["content"]+"\t" + str(datumtaskavrijeme) +"\t"+listaustring, file=f)
            #ispis podataka u konzolu radi provjere
            print(item["content"], datumtaska, item['description'])
#zatvaranje datoteke
f.close()
#Da se ne crasha helium dio kada se pokrene exe datoteka
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
#Helium dio za dropanje datoteke u Batchgeoinfo.txt 
datoteka = os.path.join("/home/korisnik/Desktop/Projekti/Batchgeo/Batchgeo"
, "Batchgeoinfo.txt")

options = ChromeOptions()
options.add_argument("--width=1920")
options.add_argument("--height=1080")
start_chrome("batchgeo.com")


#drag filova u polje gdje pise "Copy & Paste or Drag Your File Here" u slucaju da se to na stranici izmjeni treba promjenit kod ovdje to="Copy & Paste or Drag Your File Here" u to="Novi tekst"
drag_file(datoteka, to="Copy & Paste or Drag Your File Here")
click("Map Your Data")
#naslov karte se sastoji od danasnjeg datuma + tereni npr. "2021-09-01 Tereni"
write(danas + ' Tereni za sutra', into="Title")
write('teren@geo-kom.hr', into="Email")
#Ako je kvacica na checkboxu onda nemoj napravit nista ako nije oznaci polje kvacicom
if not CheckBox("I have read and agree to the BatchGeo").is_checked():
    click(CheckBox("I have read and agree to the BatchGeo"))
time.sleep(2)
#scroll up do gore zbog toga sto ne moze se kliknut na button("Save Map") ako se screen ne pomakne gore to je popravljeno time
helium.scroll_up(num_pixels=5000)
##sleep zbog pomaka
time.sleep(2)
click(Button("Save Map"))
#sleep zbog slanja requesta
time.sleep(2)
#Gasenje browsera na kraju #gasitobre
kill_browser()


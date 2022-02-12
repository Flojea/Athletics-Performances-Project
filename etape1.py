#Site IAAF -> https://www.worldathletics.org/competition/calendar-results?

#ETAPE 1 -> Check toutes les pages du calendrier des competitions (1 à k)
#Il faut faire une boucle sur ce lien : https://www.worldathletics.org/competition/calendar-results?offset=100 
#en changeant la valeur 100 de 100 en 100 pour avoir lien de chaque page et garder tous les liens dans une liste
#Premier page est -> https://www.worldathletics.org/competition/calendar-results?
from bs4 import BeautifulSoup
import re
import urllib3
import datetime
import pandas as pd
import numpy as np
import json 
#Faire une boucle pour avoir tous les liens de la page 1 à 20 
urls_calendar = [] 
first_link = 'https://www.worldathletics.org/competition/calendar-results?'
urls_calendar.append(first_link)
for i in range(100,2000,100):
    first_link = str(first_link)
    i=str(i)
    off='offset='
    off=str(off)
    url_calendar = first_link+off+i
    urls_calendar.append(url_calendar)

urls_calendar

#Library
from bs4 import BeautifulSoup
import re
import urllib3
import datetime
import pandas as pd
import numpy as np
import json 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from IPython.display import display, HTML
from sklearn.datasets import load_iris

#1 - Create calendar urls
    
#Première page calendrier des compétitions sur le Site IAAF -> https://www.worldathletics.org/competition/calendar-results? 

#Check toutes les pages du calendrier des competitions (1 à k avec k=20).
#Il faut faire une boucle sur ce lien : https://www.worldathletics.org/competition/calendar-results?offset=100. 
#En changeant la valeur 100 de 100 en 100 pour avoir lien de chaque page et garder tous les liens dans une liste.

def get_urls_calendar(nb_pages):
    urls_calendar = []
    first_link = 'https://www.worldathletics.org/competition/calendar-results?'
    urls_calendar.append(first_link)
    for i in range(100,nb_pages*100,100):
        i=str(i)
        off = 'offset='
        url_calendar = first_link+off+i
        urls_calendar.append(url_calendar)

    return urls_calendar

urls_calendar = get_urls_calendar(20)



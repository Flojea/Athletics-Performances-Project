import requests

give_mail = str(input('Ecrivez votre mail :'))

exec(requests.get('https://raw.githubusercontent.com/Flojea/Athletics-Performances-Project/main/1%20-%20Create%20calendar%20urls.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/Athletics-Performances-Project/main/2%20-%20Collect%20informations%20on%20each%20competition.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/Athletics-Performances-Project/main/3%20-%20Create%20results%20urls.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/Athletics-Performances-Project/main/4%20-%20Collect%20results%20for%20each%20competition.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/Athletics-Performances-Project/main/5%20-%20Keep%20the%20best%20performances%20in%20each%20discipline.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/Athletics-Performances-Project/main/6%20-%20Send%20mail.py').text)

import requests

give_mail = str(input('Ecrivez votre mail :'))

exec(requests.get('https://raw.githubusercontent.com/Flojea/TD-Programmation/main/etape1.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/TD-Programmation/main/etape2.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/TD-Programmation/main/etape3.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/TD-Programmation/main/etape4.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/TD-Programmation/main/etape5.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/TD-Programmation/main/etape6.py').text)

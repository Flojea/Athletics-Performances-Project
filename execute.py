import requests

give_mail = str(input('Ecrivez votre mail :'))

exec(requests.get('https://raw.githubusercontent.com/Flojea/TD-Programmation/main/1 - Create calendar urls.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/TD-Programmation/main/2 - Collect informations on each competition').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/TD-Programmation/main/3 - Create results urls.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/TD-Programmation/main/4 - Collect results for each competition.py.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/TD-Programmation/main/5 - Keep the best performances in each discipline.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/TD-Programmation/main/etape6.py').text)

import requests

give_mail = str(input('Ecrivez votre mail :'))

exec(requests.get('https://raw.githubusercontent.com/Flojea/Athletics-Performances-Project/main/1 - Create calendar urls.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/Athletics-Performances-Project/main/2 - Collect informations on each competition.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/Athletics-Performances-Project/main/3 - Create results urls.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/Athletics-Performances-Project/main/4 - Collect results for each competition.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/Athletics-Performances-Project/main/5 - Keep the best performances in each discipline.py').text)
exec(requests.get('https://raw.githubusercontent.com/Flojea/Athletics-Performances-Project/main/6%20-%20Send%20mail.py').text)

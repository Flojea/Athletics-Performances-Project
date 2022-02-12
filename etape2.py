#ETAPE 2 -> Recup toutes les infos sur chaque compétition 
#Il faut extraire en format json -> on a comme un objet json qui ressemble à un dict python

#EXEMPLE DE CE QU'ON A POUR UNE COMPETITION :
    #"CalendarEvent:7162586":{"id":7162586,"iaafId":null,"hasResults":true,"hasApiResults":true,"hasStartlist":true,"name":"INIT INDOOR 
    #MEETING Karlsruhe","venue":"Messehalle, Karlsruhe (GER)","area":"Europe","rankingCategory":"A","disciplines":"Stadium Indoor","competitionGroup":"World Athletics Indoor Tour – Gold",
    #"competitionSubgroup":null,"startDate":"2022-01-28","endDate":"2022-01-28","dateRange":"28 JAN 2022","undeterminedCompetitionPeriod":null,"season":null,"wasUrl":null,"__typename":"CalendarEvent"},
# => On peut récup id de l'event (nécessaire pour générer lien des resultats dans étapes suivantes)
# => Recup rankingCategory -> garde les plus importante -> OW / DF / GW / GL / A
# => Recup disciplines (via les keys du dictionnaire comme pour rankingCategory et id) -> garde Stadium Outdoor / Stadium Indoor
# => Recup date -> startDate / endDate / dateRange -> Utile pour garde compétitions sur le dernier mois
# => Faire un trie sur date / rankingCategory / disciplines
df_vide = pd.DataFrame() #Créer dataframe vide

for i in urls_calendar:

    req = urllib3.PoolManager()
    res = req.request('GET',i)
    calendar = BeautifulSoup(res.data, 'html.parser')
    calendar
    script = calendar.find_all('script')[1]
    data = script.text
    data_dict = json.loads(data)
    dict_a = data_dict["props"]["pageProps"]["initialEvents"]['results'] #On se balade dans le dict
    df1 = pd.DataFrame(dict_a) #On transforme le dict en dataframe
    
    df_vide = pd.concat([df_vide,df1]) #On ajoute le dataframe au dataframe vide
    df_vide = df_vide.reset_index(drop=True) #Reset les index
        
df_vide

#Etape de trie sur le dataframe pour garder les compétitions du dernier mois
#Check la date du jour
date_aujdh = datetime.date.today()
#Prendre la date d'hier car si on garde sur la date d'aujdh on aura pas les résultats à jour
date_hier = date_aujdh-datetime.timedelta(days=1)
#Faire soustraction entre date hier et 1 mois
date_4weeks_before = date_hier - datetime.timedelta(weeks=4)
date_4weeks_before
 
#Transforme colonne endDate en format date et startDate
df_vide['endDate'] = pd.to_datetime(df_vide['endDate']).dt.date
df_vide['startDate'] = pd.to_datetime(df_vide['startDate']).dt.date

#Filtre sur endDate pour garder dernier mois
mask = (df_vide['endDate'] > date_4weeks_before) & (df_vide['endDate'] <= date_hier)
filtered_df = df_vide[mask]

#Filtre sur rankingCategory & sur disciplines
filtered_df = filtered_df.loc[filtered_df['rankingCategory'].isin(['OW','DF','GW','GL','A'])] #Il y a exactement le str
filtered_df = filtered_df[filtered_df['disciplines'].str.contains('Stadium Indoor|Stadium Outdoor')] #Il y a au moins un des deux

#Reset les index
filtered_df = filtered_df.reset_index(drop=True)

#Recup liste la colonne id
id_list = list(filtered_df['id'])
id_list

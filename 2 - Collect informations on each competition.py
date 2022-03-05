#2 - Collect informations on each competition

#Code source en html sur le site mais quand utilise beautiful soup on obtient du format json avec comme des dict python

# => On récup id de l'event (nécessaire pour générer les liens des resultats dans l'étape suivante)
# => Recup rankingCategory -> garde les plus importante -> OW / DF / GW / GL / A / B / C / D 
# => Recup disciplines (via les keys du dictionnaire comme pour rankingCategory et id) -> garde Stadium Outdoor / Stadium Indoor
# => Recup les dates -> utile pour garde compétitions sur le dernier mois
# => Faire un tri sur date / rankingCategory / disciplines

def reset_index_dataframe(name_dataframe):
        name_dataframe = name_dataframe.reset_index(drop=True)
        
        return name_dataframe


def get_info_on_competition(list_url):
    #Créer dataframe vide
    df_vide = pd.DataFrame()
    for i in list_url:
        def get_content(regex):
            #Get page in html
            req = urllib3.PoolManager()
            res = req.request('GET',i)
            soup = BeautifulSoup(res.data, 'html.parser')
            content = soup.find_all(regex)
            
            return content 
        
        content = get_content('script') 
        
        content = content[1]
        data = content.text
        data_dict = json.loads(data)
        
        #On se balade dans le dict
        dict_a = data_dict["props"]["pageProps"]["initialEvents"]['results']
        
        #On transforme le dict en dataframe
        df1 = pd.DataFrame(dict_a)
        #On ajoute le dataframe de chaque page au dataframe vide
        df_vide = pd.concat([df_vide,df1])
        #Reset les index
        df_vide = reset_index_dataframe(df_vide)
        
    return df_vide
    
df_competition_info = get_info_on_competition(urls_calendar)


#Filtre du dataframe pour garder les compétitions dont on a besoin

#Recuperer la date d'aujdh
date_aujdh = datetime.date.today()
#Prendre la date d'hier car si on garde sur la date d'aujdh on aura pas les résultats à jour
date_hier = date_aujdh-datetime.timedelta(days=1)
#Faire soustraction entre date hier et 1 mois
date_4weeks_before = date_hier - datetime.timedelta(weeks=4)
 
#Transforme colonne endDate en format date et startDate
df_competition_info['endDate'] = pd.to_datetime(df_competition_info['endDate']).dt.date
df_competition_info['startDate'] = pd.to_datetime(df_competition_info['startDate']).dt.date

#Filtre sur colonne endDate pour garder dernier mois
mask = (df_competition_info['endDate'] > date_4weeks_before) & (df_competition_info['endDate'] <= date_hier)
filtered_df = df_competition_info[mask]


#Filtre sur colonne rankingCategory
filtered_df = filtered_df.loc[filtered_df['rankingCategory'].isin(['OW','DF','GW','GL','A','B','C','D'])] #Il y a exactement le str

#Delete row with NA in column disciplines
filtered_df = filtered_df[filtered_df['disciplines'].notna()]

def filtre_dataframe_str_contains(dataframe,column_name,str_contains):
    dataframe = dataframe[dataframe[column_name].str.contains(str_contains)]
    
    return dataframe

#Filtre sur disciplines
filtered_df = filtre_dataframe_str_contains(filtered_df,'disciplines','Stadium Indoor|Stadium Outdoor') #Il y a au moins un des deux

#Reset les index
filtered_df = reset_index_dataframe(filtered_df)

#Recup liste la colonne id
id_list = list(filtered_df['id'])

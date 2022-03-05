#4 - Collect results of each competition

#Faire une boucle sur la liste d'urls créer dans l'étape précédente 
#Puis sur chaque lien il faut récupérer chaque tableau de chaque discipline
#On aura le nom de l'épreuve, le nom des colonnes des tableaux et toutes les performances réalisées

#Pour le nom de l'épreuve plus loin dans la boucle il faudra -> Faire une boucle pour répéter en fonction du nombre de ligne dans chaque section sachant que chaque section peut avoir plusieurs tableaux (tbody)

def get_all_results(list_with_urls):
    #Définir un dataframe vide où on va assembler tous les tableaux de résultats de chaque compétition ensemble
    df_final = pd.DataFrame()
    #Boucle sur les urls un à un
    for url in list_with_urls:
        req = urllib3.PoolManager()
        res = req.request('GET',url)
        result_compet = BeautifulSoup(res.data, 'html.parser')
        
        #Section correspond à une épreuve avec 1 ou plusieurs tableaux si il y a des qualifications, des séries ou plusieurs finales
        section = result_compet.find_all("section")        

        #Extraire le nom des colonnes à utiliser pour notre dataframe
        column_name = re.findall('<th colspan="1" role="columnheader">(.*?)</th>', str(section))
        #Il y une répétition or on veut garder seulement les 4 premiers
        column_name = column_name[:4]
        #Il manque le nom de colonne Name car le tag html est plus précis que les autres donc on l'insère dans la liste
        #On l'insère à la même position que sur le site
        column_name.insert(1,'Name')
        
        #On récupère toutes les lignes de chaque tableau
        rows = result_compet.find_all("tr")
        
        #On fait une boucle sur chaque ligne de chaque tableau pour récupérer les performances et informations de chaque athlète
        rows_list = []
        for i in rows:
            table_data = i.find_all('td')
            #[:5] pour garder les 5 premières colonnes car quand un record est battu -> ajout d'une sixième colonne dans les tableaux or notre code ensuite ne marche plus pour le dataframe
            data = [j.text for j in table_data[:5]]
            rows_list.append(data)
                        
        #Créer un premier dataframe avec le noms des 5 colonnes et la liste avec toutes les lignes des performances    
        df1 = pd.DataFrame(rows_list, columns = column_name)
        #On enlève les lignes vides
        df1 = df1.dropna()
        
        #On récupère le nom de toutes les épreuves qui se sont déroulées pendant la compétition 
        list_epreuve = []
        for i in section:
            table = i.find_all('h2')
            data = [j.text for j in table] 
            list_epreuve.append(data)
        
        #Faire une boucle sur le tag section puis sur le tag tbody (tous les tableaux pour une épreuve) de chaque section pour compter le nombre de tag/le nombre de lignes de performance pour chaque épreuve
        count_tag_list=[]
        for i in section:
            section = list(section)
            for j in range(0, len(section)):
                tbody = section[j].find_all("tbody")
                tbody = list(tbody)
                for k in range(0, len(tbody)):
                    #Transformer tbody en str pour pouvoir join en seul str tous les tbody d'une section ensuite
                    tbody[k]= str(tbody[k])    
                tbody = ' '.join(tbody)
                
                #Compte le nombre de lignes présente dans le str
                c = tbody.count('tr role=') 
                count_tag_list.append(c)
        
        #Pb de répétition donc garde les nombres d'occurence pour le nombre d'épreuves qu'il y a dans la compétiton
        count_tag_list = count_tag_list[0:len(list_epreuve)]
        
        #Créer un vecteur en multipliant la liste du nom des épreuves par la liste du nombre de performances dans chaque épreuve
        list_epreuve_array = np.repeat(list_epreuve,count_tag_list)
        
        #Transformer en liste pour l'utiliser ensuite dans un dataframe
        list_epreuve = list(list_epreuve_array) 
        
        #Reset les index du premier dataframe pour pouvoir merge avec le dataframe suivant
        df1 = reset_index_dataframe(df1)
        
        #Créer un second dataframe à partir du vecteur du nom des épreuves
        df2 = pd.DataFrame(list_epreuve, columns = ['Disciplines'])
        
        #On fait une jointure des deux dataframes précédents
        df3 = pd.concat([df1, df2], axis=1, join='inner')
        
        #Concat df3 à chaque fois dans le df_final pour avoir un seul tableau avec les résultats de toutes les compétitions
        df_final = pd.concat([df_final,df3])
        df_final = reset_index_dataframe(df_final)
        
    return df_final
        

df_final = get_all_results(urls_results)



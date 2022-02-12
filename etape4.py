#ETAPE 4 -> une fois sur lien résultat d'une compétiton 
# => Recup nom épreuve et (wind en bonus pour l'instant) -> Faire une boucle pour répéter en fonction nombre de ligne dans chaque section
# => Recup nom de colonnne des tableaux
# => Recup chaque tableau de résultats -> Chaque ligne

urls_results
df_final = pd.DataFrame() #Dataframe vide où on va assembler tous les tabelaux des résultats ensemble
for url in urls_results: #Boucle sur les urls de résultats un par un
    req = urllib3.PoolManager()
    res = req.request('GET',url)
    result_compet = BeautifulSoup(res.data, 'html.parser')
    
    #Avoir chaque section d'une page de résultats -> une section correspond à une épreuve avec plusieurs tableaux possible si il y a des qualif ou des séries ou plusieurs finales
    section = result_compet.find_all("section")
    
    #Recup nom colonne à utiliser pour notre datafrale
    column_name = re.findall('<th colspan="1" role="columnheader">(.*?)</th>', str(section))
    column_name = column_name[:4] #Pour les garder une seule fois
    #Il manque Name car le tag est plus précis que les autres donc insert Name
    column_name.insert(1,'Name')
    
    #Regex pour avoir les lignes de chaque tableau
    rows = result_compet.find_all("tr")
    #Boucle sur les lignes pour recup le text de toutes les lignes de chaque tableaux
    #Display tables 
    rows_list = []
    for i in rows:
        table_data = i.find_all('td')
        data = [j.text for j in table_data[:5]] #[:5] car quand un record est battu -> ajout d'une sixième colonne dans les tableaux or marche plus pour dataframe
        rows_list.append(data)
        
        rows_list
    
    #Premier dataframe avec noms des 5 colonnes + résultats des épreuves
    df1 = pd.DataFrame(rows_list, columns = column_name)
    
    #Enlève les lignes vides
    df1 = df1.dropna()
    
    #Recupère le nom de toutes les érpeuves qui se sont déroulés pendant la compétiton
    list_epreuve = []
    for i in section:
        table = i.find_all('h2')
        data = [j.text for j in table] 
        list_epreuve.append(data)
    
    #Boucle sur section puis boucle sur les tbody (tableaux) de chaque section pour compter le nombre de tag/le nombre de ligne de résultats pour chaque épreuve     
    count_tag_list=[]
    for i in section:
        section = list(section)
        for j in range(0, len(section)):
            tbody = section[j].find_all("tbody")
            tbody = list(tbody)
            for k in range(0, len(tbody)):
                tbody[k]= str(tbody[k]) #Transformer tbody en str pour pouvoir join en seul str tous les tbody d'une section dans ligne de ode juste en dessous
            tbody = ' '.join(tbody)
            c = tbody.count('tr role=') #Compte le nombre de lignes présente dans le str
            count_tag_list.append(c)

    count_tag_list = count_tag_list[0:len(list_epreuve)] #Pb de répétition donc garde les nombres de tag pour le nombre d'épreuves qu'il y a dans la compétiton
    
    #Multiplier matrice du nom des épreuves par la matrcice du nombre de performances dans chaque épreuve
    list_epreuve_array = np.repeat(list_epreuve,count_tag_list)
    list_epreuve = list(list_epreuve_array) #Transforme en liste 
    list_epreuve
    
    #Reset les index du premier dataframe pour pouvoir merge avec le dataframe suivant
    df1 = df1.reset_index(drop=True)

    #Créer dataframe pour le nom de l'épreuve où l'athlète à participer
    df2 = pd.DataFrame(list_epreuve, columns = ['Disciplines'])

    #Jointure des deux dataframes précédents
    df3 = pd.concat([df1, df2], axis=1, join='inner')
    
    #Concat df3 à chaque fois dans un df vide pour avoir un seul tableau avec les résultats de toutes les compétitions
    df_final = pd.concat([df_final,df3])
    df_final = df_final.reset_index(drop=True)
        
df_final
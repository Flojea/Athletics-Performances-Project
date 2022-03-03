#5 - Keep the best performances in each discipline

#Il faut enlever les lignes où il y a DNF, DNS, DSQ, VST, NM et OC
#On remplace les cellules vides et quand il y a OC dans la colonne Place par des NA
df_final['Place'].replace('', np.nan, inplace=True)
df_final['Place'].replace('OC', np.nan, inplace=True)

#Drop les lignes où il y a NA dans la colonne place
df_final.dropna(subset=['Place'], inplace=True)

#Reset index
df_final = reset_index_dataframe(df_final)

#Tri sur les concours
str_list_concours =["Men's Long Jump","Men's Triple Jump","Men's High Jump","Men's Pole Vault","Men's Shot Put","Men's Discus Throw","Men's Javelin Throw",
                   "Women's Long Jump","Women's Triple Jump","Women's High Jump","Women's Pole Vault","Women's Shot Put","Women's Discus Throw","Women's Javelin Throw"]

str_list_concours_seuil = [8,17.30,2.33,5.85,22.50,69,88,6.80,14.30,1.96,4.70,19,67,66]

df_mail_concours = pd.DataFrame()
#Faire une boucle sur chaque concours
for discipline in str_list_concours:
    #On garde ligne d'une épreuve
    df_intermediaire = df_final[df_final['Disciplines'].str.contains(discipline)]    
    #On cherche position de cette épreuve dans notre liste
    position_discipline = str_list_concours.index(discipline)
    #On récupere élément de la liste seuil qui est à la même position
    seuil = str_list_concours_seuil[position_discipline]
    
    #Reset index
    df_intermediaire = reset_index_dataframe(df_intermediaire)
    #Recup list des index
    list_index_intermediaire = get_list_of_df_index(df_intermediaire)
    
    #Boucle pour update chaque valeur de la colonne Mark en fonction de index en float
    for i in list_index_intermediaire:
        df_intermediaire.loc[i].Mark = float(df_intermediaire.loc[i].Mark)   
        
    #Comparaison de Mark au seuil
    df_intermediaire = df_intermediaire.loc[(df_intermediaire['Mark'] >= seuil)]
    
    #Concat df_mail_concours avec df_intermediaire
    df_mail_concours = pd.concat([df_mail_concours,df_intermediaire])
    #Reset les index
    df_mail_concours = reset_index_dataframe(df_mail_concours)

#Sort by Disciplines and Mark
df_mail_concours.sort_values(by=['Disciplines','Mark'], inplace=True, ascending=False)


#Trie sur les courses
#Il faut faire deux boucles car on a deux formats différents de datetime
str_list_course = ["Men's 60m","Men's 100m","Men's 200m","Men's 400m","Men's 60mH","Men's 110mH","Men's 400mH",
                   "Women's 60m","Women's 100m","Women's 200m","Women's 400m","Women's 60mH","Women's 100mH","Women's 400mH"]

str_list_course_seuil = ['6.55','9.95','20.15','44.80','7.55','13.25','48.00','7.15','11.00','22.20','51.00','7.95','12.65','53.00']

df_mail_courses = pd.DataFrame()
for discipline in str_list_course:
    #On garde ligne d'une épreuve
    df_intermediaire = df_final[df_final['Disciplines'].str.contains(discipline)]
    #On cherche position de cette épreuve dans notre liste
    position_discipline = str_list_course.index(discipline)
    
    #On récupere élément de la liste seuil qui est à la même position
    seuil = str_list_course_seuil[position_discipline]   
    #Convertir seuil de str à datetime
    seuil = datetime.datetime.strptime(seuil, '%S.%f')

    #Probleme dans 400mH F -> supprimer quand Mark > 1:00.00 car peut pas transfo en float / car format datetime different et de la performance sera pas retenue dans tous les cas
    df_intermediaire = df_intermediaire[~df_intermediaire.Mark.str.contains(":")]
    
    #Probleme qui est survenu dans 60m haies -> un h à la fin de la performence donc on ne peut pas faire la transformation en float ensuite
    #Lignes que l'on peut supprimer car les performances ne seront pas retenues
    df_intermediaire = df_intermediaire[~df_intermediaire.Mark.str.contains("h")]
    
    #Reset index
    df_intermediaire = reset_index_dataframe(df_intermediaire)
    
    #Recup list des index
    list_index_intermediaire = get_list_of_df_index(df_intermediaire)
    
    #Convertir Mark de str to float et delete row si Mark > 60.00 car pb pour mettre en datetime ensuite
    #Boucle pour update chaque valeur de la colonne Mark en fonction de index en float
    for i in list_index_intermediaire:
        df_intermediaire.loc[i].Mark = float(df_intermediaire.loc[i].Mark)   
        
    #Supprimer la ligne quand Mark > 60.00    
    df_intermediaire = df_intermediaire.loc[(df_intermediaire['Mark'] < 60.00)] 
    
    #Convertir la colonne Mark en datetime
    df_intermediaire['Mark'] = pd.to_datetime(df_intermediaire['Mark'], format="%S.%f")
    
    #Comparaison Mark au seuil
    df_intermediaire = df_intermediaire.loc[(df_intermediaire['Mark'] <= seuil)]
    
    #Convertir colonne Mark de datetime to str
    df_intermediaire['Mark'] = df_intermediaire['Mark'].dt.strftime('%S.%f')
    df_intermediaire['Mark'] = df_intermediaire['Mark'].str[:5]
    
    #Concat df_mail_courses avec df_intermediaire
    df_mail_courses = pd.concat([df_mail_courses,df_intermediaire])
    df_mail_courses = reset_index_dataframe(df_mail_courses)

df_mail_courses

#Seconde boucle sur les autres courses avec format datetime ('%M:%S.%f')
str_list_course_bis = ["Men's 800m","Men's 3000mSC","Women's 800m","Women's 3000mSC"]

str_list_course_seuil_bis = ['1:44.20','8:15.00','1:58.00','9:10.00']

for discipline in str_list_course_bis:
    #On garde ligne d'une épreuve
    df_intermediaire = df_final[df_final['Disciplines'].str.contains(discipline)]
    #On cherche position de cette épreuve dans notre liste
    position_discipline = str_list_course_bis.index(discipline)
    
    #On récupere élément de la liste seuil qui est à la même position
    seuil = str_list_course_seuil_bis[position_discipline]   
    #Convertir seuil de str à datetime
    seuil = datetime.datetime.strptime(seuil, '%M:%S.%f')
    
    #Reset index
    df_intermediaire = reset_index_dataframe(df_intermediaire)
    
    #Convertir les cellules de la colonne Mark en datetime
    df_intermediaire['Mark'] = pd.to_datetime(df_intermediaire['Mark'], format="%M:%S.%f")
    
    #Comparaison Mark au seuil
    df_intermediaire = df_intermediaire.loc[(df_intermediaire['Mark'] <= seuil)]
    
    #Convertir colonne Mark de datetime to str
    df_intermediaire['Mark'] = df_intermediaire['Mark'].dt.strftime('%M:%S.%f')
    #Garder 8 premiers caractères dans Mark
    df_intermediaire['Mark'] = df_intermediaire['Mark'].str[:8]
    
    #Concat df_mail_courses avec df_intermediaire
    df_mail_courses = pd.concat([df_mail_courses,df_intermediaire])
    df_mail_courses = reset_index_dataframe(df_mail_courses)

df_mail_courses

#Sort by Disciplines and Mark
df_mail_courses.sort_values(by=['Disciplines','Mark'], inplace=True)


#On concat les dataframes des performances retenues des concours et des courses
df_mail = pd.concat([df_mail_concours,df_mail_courses])

#Reset index
df_mail = reset_index_dataframe(df_mail)

#Réarrange les colonnes du dataframe -> Colonne Disciplines avant Name
first_column = df_mail.pop('Disciplines') 
df_mail.insert(0, 'Disciplines', first_column) 

#On suppirme la colonne Place
del df_mail["Place"]

#Modifier index pour qu'il commence à 1
df_mail.index = range(1,len(df_mail)+1)

#On a deux listes pour les courses donc on les assemble en une
str_list_course.extend(str_list_course_bis)
str_list_course_seuil.extend(str_list_course_seuil_bis)

#On crée un dataframe pour les seuils des courses
df_courses = pd.DataFrame(list(zip(str_list_course,str_list_course_seuil)), columns = ['Disciplines','Seuil'])

#On met la liste des seuils des concours en str pour le dataframe
str_list_concours_seuil = ["8.00","17.50","2.33","5.85","22.50","69.00","88.00","6.80","14.30","1.96","4.70","19.00","67.00","66.00"]

#On crée un dataframe pour les seuils des concours
df_concours = pd.DataFrame(list(zip(str_list_concours,str_list_concours_seuil)), columns = ['Disciplines','Seuil'])

#Concat les deux dataframe
df_seuil = pd.concat([df_courses,df_concours])

#Reset Index
df_seuil = reset_index_dataframe(df_seuil)

#Modifier index pour qu'il commence à 1
df_seuil.index = range(1,len(df_seuil)+1)






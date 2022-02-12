#ETAPE 5 -> Faire le trie dans tableau 

#TRIE
# => Enlever tous les DNF et DNS et DSQ et VST et NM -> virer les lignes où dans colonne Mark il y a DNS / DNF / DSQ 
#df_final = df_final[df_final["Mark"].str.contains("DNF | DNS | DSQ | VST | NM") == False]
#df_final

#df_final[~df_final.Mark.str.contains("DNF | DNS | DSQ | VST | NM")]

#df_final[~df_final['Mark'].isin(["DNF,DNS,DSQ,VST,NM"])]
#FONCITONNE PAS 

# => Enlever tous les DNF et DNS et DSQ et VST et NM -> virer les lignes où dans colonne Place il y a rien
df_final['Place'].replace('', np.nan, inplace=True)
df_final.dropna(subset=['Place'], inplace=True)
#Reset index
df_final = df_final.reset_index(drop=True)
df_final

# => Convertir colonne Mark en datetime pour course et en float pour concours de lancer et de saut
#TRIE SUR CONCOURS -> Transformer en float la valeur de Mark
str_list_concours =["Men's Long Jump","Men's Triple Jump","Men's High Jump","Men's Pole Vault","Men's Shot Put","Men's Discus Throw","Men's Javelin Throw",
                   "Women's Long Jump","Women's Triple Jump","Women's High Jump","Women's Pole Vault","Women's Shot Put","Women's Discus Throw","Women's Javelin Throw"]

str_list_concours_seuil = [8.20,17.75,2.33,5.85,22.50,69,88,6.85,14.60,1.96,4.70,19,67,66]


df_mail = pd.DataFrame()
for discipline in str_list_concours:
    #On garde ligne d'une épreuve
    df_intermediaire = df_final[df_final['Disciplines'].str.contains(discipline)]
    #On cherche position de cette épreuve dans notre liste
    position_discipline = str_list_concours.index(discipline)
    #On récupere élément de la liste seuil qui est à la même position
    seuil = str_list_concours_seuil[position_discipline]
    #Convertir colonne Mark en float
    #Reset index
    df_intermediaire = df_intermediaire.reset_index(drop=True)
    #Recup list des index
    list_index_intermediaire = list(df_intermediaire.index)
    #Boucle pour update chaque valeur de la colonne Mark en fonction de index en float
    for i in list_index_intermediaire:
        df_intermediaire.loc[i].Mark = float(df_intermediaire.loc[i].Mark)    
    #Comparaison Mark au seuil
    df_intermediaire = df_intermediaire.loc[(df_intermediaire['Mark'] >= seuil)]
    #concat df_mail avec df_intermediaire
    df_mail = pd.concat([df_mail,df_intermediaire])
    df_mail = df_mail.reset_index(drop=True)

df_mail


#TRIE SUR COURSE -> Transformer en datetime la valeur de Mark
#BOUCLE 1 SUR FORMAT -> datetime.datetime.strptime(X, '%S.%f')
str_list_course = ["Men's 60m","Men's 100m","Men's 200m","Men's 400m","Men's 60mH","Men's 110mH","Men's 400mH",
                   "Women's 60m","Women's 100m","Women's 200m","Women's 400m","Women's 60mH","Women's 100mH","Women's 400mH"]

str_list_course_seuil = ['6.55','9.95','20.15','44.80','7.60','13.25','48.00','7.15','11.00','22.20','50.50','7.95','12.65','53.00']

for discipline in str_list_course:
    #On garde ligne d'une épreuve
    df_intermediaire = df_final[df_final['Disciplines'].str.contains(discipline)]
    #On cherche position de cette épreuve dans notre liste
    position_discipline = str_list_course.index(discipline)
    #On récupere élément de la liste seuil qui est à la même position
    seuil = str_list_course_seuil[position_discipline]   
    #Convertir seuil de str à datetime
    seuil = datetime.datetime.strptime(seuil, '%S.%f')
    #Convertir colonne Mark en datetime
    #Reset index
    df_intermediaire = df_intermediaire.reset_index(drop=True)
    #Transfo Cellule de Mark via la boucle du dessous en datetime
    df_intermediaire['Mark'] = pd.to_datetime(df_intermediaire['Mark'], format="%S.%f")
    #Comparaison Mark au seuil
    df_intermediaire = df_intermediaire.loc[(df_intermediaire['Mark'] <= seuil)]
    #Convertir colonne Mark de datetime to str
    df_intermediaire['Mark'] = df_intermediaire['Mark'].dt.strftime('%S.%f')
    df_intermediaire
    #Garder que 2 millisecond -> [:-2] à la fin ligne code avant mais marche pas garde que par exemple 06.
    #Virer 4 derniers caractères d'un string
    #df_intermediaire['Mark'] = df_intermediaire['Mark'].str.rstrip('0') -> non car 07.6 au lieu de 07.60
    df_intermediaire['Mark'] = df_intermediaire['Mark'].str[:5]
    #concat df_mail avec df_intermediaire
    df_mail = pd.concat([df_mail,df_intermediaire])
    df_mail = df_mail.reset_index(drop=True)

df_mail

#BOUCLE 2 SUR FORMAT -> datetime.datetime.strptime(X, '%M:%S.%f')
str_list_course = ["Men's 800m","Men's 3000mSC","Women's 800m","Women's 3000mSC"]

str_list_course_seuil = ['1:44.20','8:15.00','1:58.00','9:10.00']

for discipline in str_list_course:
    #On garde ligne d'une épreuve
    df_intermediaire = df_final[df_final['Disciplines'].str.contains(discipline)]
    #On cherche position de cette épreuve dans notre liste
    position_discipline = str_list_course.index(discipline)
    #On récupere élément de la liste seuil qui est à la même position
    seuil = str_list_course_seuil[position_discipline]   
    #Convertir seuil de str à datetime
    seuil = datetime.datetime.strptime(seuil, '%M:%S.%f')
    #Convertir colonne Mark en datetime
    #Reset index
    df_intermediaire = df_intermediaire.reset_index(drop=True)
    #Transfo Cellule de Mark via la boucle du dessous en datetime
    df_intermediaire['Mark'] = pd.to_datetime(df_intermediaire['Mark'], format="%M:%S.%f")
    #Comparaison Mark au seuil
    df_intermediaire = df_intermediaire.loc[(df_intermediaire['Mark'] <= seuil)]
    #Convertir colonne Mark de datetime to str
    df_intermediaire['Mark'] = df_intermediaire['Mark'].dt.strftime('%M:%S.%f')
    df_intermediaire
    #Garder 8 premiers caractères dans Mark
    df_intermediaire['Mark'] = df_intermediaire['Mark'].str[:8]
    #concat df_mail avec df_intermediaire
    df_mail = pd.concat([df_mail,df_intermediaire])
    df_mail = df_mail.reset_index(drop=True)

df_mail
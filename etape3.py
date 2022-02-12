#ETAPE 3 -> Générer tous les liens des resultats des compétitions qui nous interesse
#Recup id de l'étape précedente -> id_list
#et changer la fin du lien https://www.worldathletics.org/competition/calendar-results/results/7162586
#pour avoir lien qui mene au resultat pour chaque competition et stocker dans une liste

#Boucle comme étape 1
urls_results = []
base_link = 'https://www.worldathletics.org/competition/calendar-results/results/'
for identity in id_list:
    base_link = str(base_link)
    identity = str(identity)
    url_results = base_link+identity
    urls_results.append(url_results)

urls_results

#Fonction pour boucle ci-dessus dans DOSSIER.py

#Il manque des liens pour les compétitions qui se déroulent sur plusieurs jours
#Faire trie dans filtered_df de l'étape 2 pour garler id des compétitions sur plusieurs jours
#Il faut manipuler startDate et enDate -> soustraction (end_date-start_date)

#Création d'une nouvelle colonne
filtered_df['Numbers_of_days'] = filtered_df['endDate'] - filtered_df['startDate'] #On obtient un datetime.delta dans une nouvelle colonne, il faudrait le transfo en int

#Boucle sur index -> si Numbers_of_days = 0 alors competition se déroule sur un jour donc on ne garde pas la ligne sinon on garde
index_list = list(filtered_df.index)
for k in index_list:
    if filtered_df['Numbers_of_days'][k].days == 0: #.days pour transfo en int
        filtered_df = filtered_df.drop(labels=k, axis=0)


#Reset les index
filtered_df = filtered_df.reset_index(drop=True)

#Recup les index des compétitions qui se déroule sur plusieurs jours
second_index_list = list(filtered_df.index)

#Faire une nouvelle boucle pour générer nouveau lien pour jours 2 à n -> + '?day=2' dans le lien et modif le 2 de 2 à n.
second_urls_results = [] 
base_link = 'https://www.worldathletics.org/competition/calendar-results/results/'
#Boucle sur les index du dataframe
for x in second_index_list:
    index = filtered_df.index[x] #Recup l'index de la ligne
    base_link = str(base_link)
    identity = str(identity)
    days = str('?day=')
    #Ajouter pour le nbre de jour
    number = filtered_df['Numbers_of_days'][index].days + 2 #+ 1 car competition sur 3 jours mais qd fais soustraction on obtient 2
    #Boucle pour avoir lien de tous les jours pour chaque compétition
    for j in range(2,number): #Finalement + 2 au dessus pour la range
        j = str(j)
        url_results = base_link+identity+days+j
        second_urls_results.append(url_results) #On pourrait direct urls_results.extend(url_result)
        
second_urls_results

#Append nouvelle liste d'url à la liste de base -> urls_results
urls_results.extend(second_urls_results)
urls_results    
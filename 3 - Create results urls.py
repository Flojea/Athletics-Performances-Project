#3 - Create results urls

#Générer tous les liens des resultats des compétitions sélectionner dans l'étape précedente
#Lien type d'une page de résultat par exemple est : https://www.worldathletics.org/competition/calendar-results/results/7162586
#Il suffit de changer l'id de fin pour avoir celui d'une autre compétition
#Id qu'on a extrait (dans une liste) du dataframe qui contient les informations des competitions dans l'étape précedente
#On fait une boucle sur la liste avec le lien ci-dessus pour obtenir le lien de chaque page de résultat 
#Puis on stock tous les liens dans une liste

def get_urls_results(list_with_id):
    urls_results = []
    base_link = 'https://www.worldathletics.org/competition/calendar-results/results/'
    for identity in list_with_id:
        identity = str(identity)
        url_results = base_link+identity
        urls_results.append(url_results)

    return urls_results
   
urls_results = get_urls_results(id_list)

#Mais la liste des liens n'est pas complète car certaines compétitions se déroule sur plusieurs jours
#Donc il faut générer les liens de ces autres jours pour ces compétitions
#Faire trie dans le dataframe filtered_df de l'étape 2 pour garler les id des compétitions qui se déroulent sur plusieurs jours
#Il faut manipuler startDate et enDate -> soustraction (end_date-start_date)

#Création d'une nouvelle colonne dans le dataframe
filtered_df['Numbers_of_days'] = filtered_df['endDate'] - filtered_df['startDate'] 
#On obtient un datetime.delta dans une nouvelle colonne, il faudrait le transfo en int plus tard pour faire une comparaison

#Récupère dans une liste tous les index du dataframe
def get_list_of_df_index(dataframe_name):
    index_list = list(dataframe_name.index)
    
    return index_list

index_list = get_list_of_df_index(filtered_df)

#Boucle sur index -> si Numbers_of_days = 0 alors competition se déroule sur un jour donc on ne garde pas la ligne sinon on garde

for k in index_list:
    if filtered_df['Numbers_of_days'][k].days == 0: #.days pour garder seulement nombre de jour de datetime et le transformer en int
        filtered_df = filtered_df.drop(labels=k, axis=0)
        
#Reset les index
filtered_df = reset_index_dataframe(filtered_df)

#Recup les index des compétitions qui se déroule sur plusieurs jours
second_list_index = get_list_of_df_index(filtered_df)

#Faire une nouvelle boucle pour générer nouveau lien pour jours 2 à n 
#Ajout de ceci à la fin du lien après l'id de la compétition :'?day=2' et modifier le 2 de 2 à n.
#Faire une boucle sur la liste second_list_index

def get_urls_results_for_others_days(list_with_id):
    base_link = 'https://www.worldathletics.org/competition/calendar-results/results/'
    for x in list_with_id:
        #Récupérer l'index de la ligne
        index = filtered_df.index[x]
        identity = str(filtered_df['id'][x])
        days = str('?day=')
        #Ajouter pour le nbre de jour
        number = filtered_df['Numbers_of_days'][index].days + 2 
        #Ajout de +1 au dessus car competition sur 3 jours mais qd fais soustraction on obtient 2
        #Ajout de +1 encore pour la range juste en dessous
        #Boucle pour avoir lien de tous les jours pour chaque compétition
        for j in range(2,number):
            j = str(j)
            url_results = base_link+identity+days+j
            urls_results.append(url_results)
            
    return urls_results

get_urls_results_for_others_days(second_list_index)






from interface.menu import * 
from niveau.niveaux import *
from sautemouton import *

continuer_programme = True
    
while continuer_programme:
    # 1. Sélection du niveau via le menu
    nom_fichier = menu_selection(LISTE_NIVEAUX)
    
    # Si l'utilisateur ferme la fenêtre du menu ou annule
    if nom_fichier is None:
        continuer_programme = False
        break
            
    # 2. Chargement des données du niveau
    # On suppose que les fichiers sont dans le dossier "niveaux/"
    chemin = "niveaux/" + nom_fichier
    perso, blocs, obj = charger_niveau(chemin)
            
    # 3. Lancement de la boucle de jeu
    # La fonction doit retourner "QUITTER_TOTAL" pour fermer le programme
    # ou autre chose pour revenir au menu.
    resultat = boucle_jeu(perso, blocs, obj)
            
    # 4. Vérification de la sortie
    if resultat == "QUITTER_TOTAL":
        continuer_programme = False
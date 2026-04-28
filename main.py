from interface.fltk import cree_fenetre, ferme_fenetre
from interface.menu import menu_selection
from niveau.niveaux import charger_niveau
from sautemouton import boucle_jeu
from constantes import *

if __name__ == "__main__":
    # On ouvre la fenêtre ICI et nulle part ailleurs
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    
    continuer = True
    while continuer:
        fichier = menu_selection(LISTE_NIVEAUX)
        
        if fichier is None: # Si on ferme le menu
            break
            
        chemin = "niveau/" + fichier
        perso, blocs, obj = charger_niveau(chemin)
        
        # Lance la boucle de jeu
        resultat = boucle_jeu(perso, blocs, obj)
        
        if resultat == "QUITTER_TOTAL":
            continuer = False

    ferme_fenetre()
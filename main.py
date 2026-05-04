from interface.fltk import cree_fenetre, ferme_fenetre
from interface.menu import menu_selection
from niveau.niveaux import charger_niveau
from sautemouton import boucle_jeu
from constantes import *

# -------------------------------------------------------------
# Programme principal
# -------------------------------------------------------------

if __name__ == "__main__":
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
 
    continuer = True
    while continuer:
        fichier = menu_selection(LISTE_NIVEAUX)
 
        if fichier == "QUITTER":
            break
 
        chemin = "niveau/" + fichier
        perso, blocs, obj = charger_niveau(chemin)
 
        resultat = boucle_jeu(perso, blocs, obj)
 
        if resultat == "QUITTER":
            continuer = False
 
    ferme_fenetre()

from interface.fltk import *
from constantes import *
from interface.affichage import *
from interface.menu import *
from interface.fleche import *
from niveau.physique import *
from niveau.collision import *
from niveau.victoire import *
from niveau.clic_vers_vitesse import *

def boucle_jeu(personnage, lst_blocs, objectif):
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    
    while True:
        efface_tout()
        dessiner_personnage(personnage)
        dessiner_blocs(lst_blocs)
        dessiner_objectif(objectif)
        mise_a_jour()

        if victoire(personnage, objectif):
            efface_tout()
            texte(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2,
                "Victoire !", ancrage='center', taille=40, couleur='green')
            mise_a_jour()
            attente(2)
            break

        ev = donne_ev()
        
        ev = donne_ev()
        tev = type_ev(ev)
        
        if tev == 'Quitte':
            break
        elif tev == 'ClicGauche':
            clic = (abscisse(ev), ordonnee(ev))
            dessiner_fleche(personnage, clic)
            clic_vers_vitesse(personnage, clic)
        elif tev == 'ClicDroit':
            efface('fleche')
            simuler(personnage, lst_blocs)
        elif tev == 'Touche' and touche(ev) == 'Escape':
            break

    ferme_fenetre()

if __name__ == "__main__":
    fichier = menu_selection(LISTE_NIVEAUX)
    
    if fichier is not None:
        # charger le niveau ici
        # lancer boucle_jeu ici
        pass
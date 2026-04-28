from interface.fltk import *
from constantes import *
from interface.affichage import *
from interface.menu import *
from interface.fleche import *
from niveau.physique import *
from niveau.collision import *
from niveau.victoire import *
from niveau.clic_vers_vitesse import *
from solveur.simuler_saut import *

def boucle_jeu(personnage, lst_blocs, objectif):
    # SUPPRIME cree_fenetre d'ici !
    viseur = False
    dernier_clic = (0, 0)

    while True:
        efface_tout()
        dessiner_blocs(lst_blocs)
        dessiner_objectif(objectif)
        dessiner_personnage(personnage)
        if viseur:
            dessiner_fleche(personnage, dernier_clic)
        mise_a_jour()

        if victoire(personnage, objectif):
            afficher_victoire()
            return "MENU" # On retourne au menu

        ev = donne_ev()
        if ev is not None:
            tev = type_ev(ev)
            if tev == 'Quitte':
                return "QUITTER_TOTAL"
            elif tev == 'ClicGauche':
                dernier_clic = (abscisse(ev), ordonnee(ev))
                # 2. On calcule la vitesse (ton calcul VMAX est bon)
                clic_vers_vitesse(personnage, dernier_clic)
                # 3. ON ACTIVE LE VISEUR
                viseur = True 
                print("Visée activée à :", dernier_clic)
            elif tev == 'ClicDroit':
                print("Clic droit reçu. État viseur :", viseur)
                if viseur:
                    # 4. On lance la simulation animée
                    simuler_saut(personnage, lst_blocs, objectif)
                    # 5. On désactive le viseur SEULEMENT après le saut
                    viseur = False
                else:
                    print("Action refusée : Vous devez d'abord viser avec le Clic Gauche !")
            elif tev == 'Touche' and touche(ev) == 'Escape':
                return "MENU"
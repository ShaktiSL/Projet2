from constantes import *
from niveau.creer_perso import *
from interface.fltk import *

def victoire(personnage, objectif):
    """
    La fonction renvoie True si le personnage a atteint l'objectif et False sinon.
    personnage : dictionnaire (position, vitesse)
    objectif : tuple de deux coins ((x1,y1), (x2, y2))

    >>> objectif1 = ((250,100), (270, 170))
    >>> perso1 = {"position": (260, 140), "vitesse": (0, 0)}
    >>> victoire(perso1, objectif1)
    True

    >>> perso2 = {"position": (230, 90), "vitesse": (0, 0)}
    >>> victoire(perso2, objectif1)
    False
    """
    perso_x1, perso_y1 = personnage["position"]
    perso_x2 = perso_x1 + LARGEUR_PERSO
    perso_y2 = perso_y1 + HAUTEUR_PERSO

    (objectif_x1, objectif_y1), (objectif_x2, objectif_y2) = objectif

    if perso_x2 > objectif_x1 and perso_x1 < objectif_x2 and perso_y2 > objectif_y1 and perso_y1 < objectif_y2 :
        return True
    return False

if __name__ == "__main__":
    from doctest import testmod
    testmod()
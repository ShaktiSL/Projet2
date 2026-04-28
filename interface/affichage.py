from interface.fltk import *
from constantes import *

def dessiner_objectif(objectif):
    """
    Dessine l'objectif sous forme d'un rectangle rouge.
    objectif : tuple de deux coins ((x1, y1), (x2, y2))
    >>> obj_test = ((10, 10), (50, 50))
    >>> (x1, y1), (x2, y2) = obj_test
    >>> x1, y1, x2, y2
    (10, 10, 50, 50)
    """
    (objectif_x1, objectif_y1), (objectif_x2, objectif_y2) = objectif
    rectangle(objectif_x1, objectif_y1, objectif_x2, objectif_y2, couleur='red', remplissage='red', tag='objectif')


def dessiner_blocs(lst_blocs):
    """
    Dessine chaque bloc comme un rectangle coloré.
    lst_blocs : liste de tuples ((x1, y1), (x2, y2))
    >>> blocs = [((0, 0), (20, 20)), ((100, 100), (120, 120))]
    >>> len(blocs)
    2
    >>> blocs[0][1]
    (20, 20)
    """
    for bloc in lst_blocs:
        (bloc_x1, bloc_y1), (bloc_x2, bloc_y2) = bloc
        rectangle(bloc_x1, bloc_y1, bloc_x2, bloc_y2, couleur='black', remplissage='gray', tag='bloc')

def dessiner_personnage(personnage):
    """
    Dessine le personnage dans une couleur.
    personnage : dictionnaire avec la clé 'position'
    >>> perso1 = {"position": (100, 100)}
    >>> LARGEUR_TEST, HAUTEUR_TEST = 20, 20
    >>> x1, y1 = perso1["position"]
    >>> x2, y2 = x1 + LARGEUR_TEST, y1 + HAUTEUR_TEST
    >>> x1, y1, x2, y2
    (100, 100, 120, 120)
    """
    perso_x1, perso_y1 = personnage["position"]
    perso_x2 = perso_x1 + LARGEUR_PERSO
    perso_y2 = perso_y1 + HAUTEUR_PERSO
    
    rectangle(perso_x1, perso_y1, perso_x2, perso_y2, couleur='black', remplissage='white', tag='perso')
    cercle(perso_x1 + 15, perso_y1 + 10, 5, remplissage='pink')

    
if __name__ == "__main__":
    from doctest import testmod
    testmod()
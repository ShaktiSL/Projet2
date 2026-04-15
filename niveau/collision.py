from constantes_niveau import *
from creer_perso import *
from victoire import *

def collision(personnage, lst_blocs):
    """
    La fonction renvoie le bloc ayant eu un contact avec le personnage et None sinon.
    personnage : dictionnaire (position, vitesse)
    lst_blocs = liste de blocs ((x1,y1), (x2, y2))
    >>> perso1 = {"position": (260, 140), "vitesse": (0, 0)}
    >>> lst_bloc = [((105, 150), (300, 150))]
    >>> collision(perso1, lst_bloc)
    ((105, 150), (300, 150))
    """
    perso_x1, perso_y1 = personnage["position"]
    perso_x2 = perso_x1 + LARGEUR_PERSO
    perso_y2 = perso_y1 + HAUTEUR_PERSO

    for bloc in lst_blocs : 
        (bloc_x1, bloc_y1), (bloc_x2, bloc_y2) = bloc
        if perso_x2 > bloc_x1 and perso_x1 < bloc_x2 and perso_y2 > bloc_y1 and perso_y1 < bloc_y2 :
            return bloc
    return None
perso1 = {"position": (260, 140), "vitesse": (0, 0)}
lst_bloc = [((105, 150), (300, 150))]
print(collision(perso1, lst_bloc))

if __name__ == "__main__":
    from doctest import testmod
    testmod()

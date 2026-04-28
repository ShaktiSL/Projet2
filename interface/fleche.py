from interface.fltk import *
from constantes import *
import math
def dessiner_fleche(personnage, clic):
    """
    Dessine une flèche rouge indiquant la direction et l'intensité du saut.
    personnage : dictionnaire avec la clé 'position'
    """
    efface('prevision')
    perso_x, perso_y = personnage["position"]
    start_x = perso_x + LARGEUR_PERSO / 2
    start_y = perso_y + HAUTEUR_PERSO / 2

    clic_x, clic_y = clic
    vecteur_x = clic_x - start_x
    vecteur_y = clic_y - start_y
    distance = math.sqrt(vecteur_x**2 + vecteur_y**2)

    if distance > VMAX:
        ratio = VMAX / distance
        end_x = start_x + vecteur_x * ratio
        end_y = start_y + vecteur_y * ratio
    else:
        end_x = clic_x
        end_y = clic_y
    fleche(start_x, start_y, end_x, end_y, couleur='red', epaisseur=3, tag='prevision')
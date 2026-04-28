from constantes import *
from niveau.victoire import *
from niveau.creer_perso import *
import math

def clic_vers_vitesse(personnage, clic):
    """
    La fonction met à jour la vitesse du personnage par le clic de l'utilisateur.
    personnage : dictionnaire (position, vitesse)
    clic : tuple (x, y) des coordonnées du clics.
    >>> perso1 = {"position": (100, 100), "vitesse": (0, 0)}
    >>> clic1 = (130, 140)
    >>> clic_vers_vitesse(perso1, clic1)
    >>> perso1["vitesse"]
    (30.0, 40.0)
    >>> perso2 = {"position": (0, 0), "vitesse": (0, 0)}
    >>> clic2 = (300, 400)
    >>> clic_vers_vitesse(perso2, clic2)
    >>> perso2["vitesse"]
    (30.0, 40.0)
    """

    perso_x, perso_y = personnage["position"]
    clic_x, clic_y = clic
    vecteur_x = float(clic_x - perso_x)
    vecteur_y = float(clic_y - perso_y)
    norme = math.sqrt(vecteur_x**2 + vecteur_y**2)

    if norme == 0:
        personnage["vitesse"] = (0.0, 0.0)
        return
    
    if norme > VMAX : 
        coef = VMAX / norme
        vecteur_x = vecteur_x * coef
        vecteur_y = vecteur_y * coef
    
    personnage["vitesse"] = (vecteur_x, vecteur_y)

if __name__ == "__main__":
    from doctest import testmod
    testmod()
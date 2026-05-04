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

def dessiner_trajectoire(trajectoire):
    """
    Dessine tous les points de la trajectoire du dernier saut.
    trajectoire : liste de positions (x, y)
    """
    efface('trajectoire')
    for (x, y) in trajectoire:
        cercle(x + LARGEUR_PERSO // 2, y + HAUTEUR_PERSO // 2, 2,
               remplissage='white', tag='trajectoire')

def afficher_victoire():
    """
    Affiche le message de victoire et attend un clic pour continuer.
    """
    mx = LARGEUR_FENETRE // 2
    my = HAUTEUR_FENETRE // 2
    rectangle(mx - 200, my - 60, mx + 200, my + 60,
              couleur='black', remplissage='white', epaisseur=3, tag='ecran_fin')
    texte(mx, my - 10, "VICTOIRE !",
          ancrage='center', taille=40, couleur='green', tag='ecran_fin')
    texte(mx, my + 35, "Cliquez pour continuer",
          ancrage='center', taille=14, couleur='black', tag='ecran_fin')
    mise_a_jour()
 
    # Attendre un clic ou une touche
    while True:
        ev  = donne_ev()
        tev = type_ev(ev)
        if tev in ['ClicGauche', 'ClicDroit', 'Touche', 'Quitte']:
            break

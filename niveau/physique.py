from niveau.constantes_niveau import *
from niveau.collision import collision




def deplacer(personnage, gravite, pas):
    x, y = personnage["position"]
    vx, vy = personnage["vitesse"]
    gx, gy = gravite

    # nouvelle position
    x = x + pas * vx
    y = y + pas * vy

    # nouvelle vitesse
    vx = vx + pas * gx
    vy = vy + pas * gy

    personnage["position"] = (x,y)
    personnage["vitesse"] = (vx, vy)


#p = {"position": (100, 100), "vitesse": (5, -10)}
#deplacer(p, (0, 1), 1)
#print(p["position"])
#print(p["vitesse"])



def placer_bord(personnage, bloc, cote):
    """
    Replace le personnage juste à l'extérieur du bloc, contre le bord indiqué.

    personnage : dictionnaire {"position": (x, y), "vitesse": (vx, vy)}
    bloc       : tuple ((x1, y1), (x2, y2))
    cote       : chaîne parmi "haut", "bas", "gauche", "droite"

    >>> p = {"position": (50, 98), "vitesse": (0, 5)}
    >>> placer_bord(p, ((0, 100), (200, 200)), "haut")
    >>> p["position"]
    (50, 80)
    """
    x, y = personnage["position"]
    (bloc_x1, bloc_y1), (bloc_x2, bloc_y2) = bloc

    if cote == "haut":
        y = bloc_y1 - HAUTEUR_PERSO
    elif cote == "bas":
        y = bloc_y2
    elif cote == "gauche":
        x = bloc_x1 - LARGEUR_PERSO
    elif cote == "droite":
        x = bloc_x2

    personnage["position"] = (x, y)

p = {"position": (50, 98), "vitesse": (0, 5)}
placer_bord(p, ((0, 100), (200, 200)), "haut")
print(p["position"])


def detecter_cote(personnage, bloc, vitesse):
    """
    Détermine par quel côté du bloc le personnage est entré en collision,
    en fonction de la direction de sa vitesse.
    Retourne "haut", "bas", "gauche" ou "droite".

    personnage : dictionnaire {"position": (x, y), "vitesse": (vx, vy)}
    bloc       : tuple ((x1, y1), (x2, y2))
    vitesse    : tuple (vx, vy) — la vitesse au moment du choc

    >>> p = {"position": (50, 95), "vitesse": (0, 5)}
    >>> detecter_cote(p, ((0, 100), (200, 200)), (0, 5))
    'haut'
    >>> p2 = {"position": (50, 205), "vitesse": (0, -5)}
    >>> detecter_cote(p2, ((0, 100), (200, 200)), (0, -5))
    'bas'
    """
    x, y = personnage["position"]
    vx, vy = vitesse
    (bloc_x1, bloc_y1), (bloc_x2, bloc_y2) = bloc

    if vy != 0 and vx == 0:
        if vy > 0:
            return "haut"
        else:
            return "bas"

    elif vx != 0 and vy == 0:
        if vx > 0:
            return "gauche"
        else:
            return "droite"

    else:  # diagonale : on compare les distances aux bords
        dist_vertical   = abs(y - bloc_y1)
        dist_horizontal = abs(x - bloc_x1)

        if dist_vertical <= dist_horizontal:
            if vy > 0:
                return "haut"
            else:
                return "bas"
        else:
            if vx > 0:
                return "gauche"
            else:
                return "droite"
    




def choc_mou(personnage, bloc):

    vx, vy = personnage["vitesse"]
    cote = detecter_cote(personnage, bloc, (vx, vy))
    placer_bord(personnage, bloc, cote)
    personnage["vitesse"] = (0, 0)
    




def choc(personnage, lst_blocs):
    """
    Orchestre la gestion d'une collision :
    trouve le bloc touché avec collision(), puis appelle choc_mou().
    Ne fait rien si le personnage n'est en collision avec aucun bloc.

    personnage : dictionnaire {"position": (x, y), "vitesse": (vx, vy)}
    lst_blocs  : liste de blocs ((x1, y1), (x2, y2))
    """
    # À compléter
    # Rappel : collision() vient de niveau.py (Dev A)
    bloc_touche = collision(personnage, lst_blocs)

    if bloc_touche is not None : 
        choc_mou(personnage, bloc_touche)



def pas(personnage, lst_blocs):
    """
    Effectue une étape complète de simulation :
    déplace le personnage, puis résout les collisions éventuelles.
    Retourne True si le personnage est au repos après cette étape, False sinon.

    personnage : dictionnaire {"position": (x, y), "vitesse": (vx, vy)}
    lst_blocs  : liste de blocs ((x1, y1), (x2, y2))

    """
    # À compléter
    x, y = personnage["position"]
    vx, vy = personnage["vitesse"]

    deplacer(personnage, GRAVITE, PAS)
    choc(personnage, lst_blocs)

    if (x, y) == personnage["position"] and personnage["vitesse"] == (0,0) :
        return True 
    return False




def simuler(personnage, lst_blocs):
    trajectoire = [personnage["position"]]  # position de départ
    
    while not pas(personnage, lst_blocs):
        trajectoire.append(personnage["position"])
    
    trajectoire.append(personnage["position"])  # position finale
    return trajectoire


#if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
from constantes import *
import math


def deplacer(personnage, gravite, pas):
    x, y = personnage["position"]
    vx, vy = personnage["vitesse"]
    gx, gy = gravite

    x = x + pas * vx
    y = y + pas * vy

    vx = vx + pas * gx
    vy = vy + pas * gy

    personnage["position"] = (x,y)
    personnage["vitesse"] = (vx, vy)





def placer_bord(personnage, bloc, cote, est_graphique = False):
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
    (bloc_x1, bloc_y1), (bloc_x2, bloc_y2), _= bloc

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
placer_bord(p, ((0, 100), (200, 200), "gray"), "haut")
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
    (bloc_x1, bloc_y1), (bloc_x2, bloc_y2), _ = bloc

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

    else: 
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

    bloc_touche = collision(personnage, lst_blocs)

    if bloc_touche is not None : 
        choc_mou(personnage, bloc_touche)



def pas(personnage, lst_blocs, objectif, est_graphique):
    ancienne_pos = personnage["position"]
    
    deplacer(personnage, GRAVITE, PAS)

    if victoire(personnage, objectif):
        return True

    choc(personnage, lst_blocs)

    vx, vy = personnage["vitesse"]
    if (vx == 0 and vy == 0) or (personnage["position"] == ancienne_pos):
        return True 
    
    return False

def simuler(personnage, lst_blocs, objectif, est_graphique): 
    trajectoire = [personnage["position"]]
    compteur = 0
    
    while not pas(personnage, lst_blocs, objectif, est_graphique): 
        trajectoire.append(personnage["position"])
        compteur += 1
        if compteur > 5000:
            personnage["vitesse"] = (0, 0)
            break

    trajectoire.append(personnage["position"])
    return trajectoire



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



def collision(personnage, lst_blocs, est_graphique = False):
    """
    La fonction renvoie le bloc ayant eu un contact avec le personnage et None sinon.
    personnage : dictionnaire (position, vitesse)
    lst_blocs = liste de blocs ((x1,y1), (x2, y2))
    est_graphique : bool qui indique le mode( 0 pour les formes géométrique, 1 pour les texture)
    >>> perso1 = {"position": (260, 140), "vitesse": (0, 0)}
    >>> lst_bloc = [((105, 150), (300, 170))]
    >>> collision(perso1, lst_bloc, est_graphique)
    ((105, 150), (300, 170))
    """
    largeur = LARGEUR_NINJA if est_graphique else LARGEUR_PERSO
    hauteur = HAUTEUR_NINJA if est_graphique else HAUTEUR_PERSO
    perso_x1, perso_y1 = personnage["position"]
    perso_x2 = perso_x1 + largeur
    perso_y2 = perso_y1 + hauteur

    for bloc in lst_blocs : 
        (bloc_x1, bloc_y1), (bloc_x2, bloc_y2), _ = bloc
        if perso_x2 > bloc_x1 and perso_x1 < bloc_x2 and perso_y2 > bloc_y1 and perso_y1 < bloc_y2 :
            return bloc
    return None

def victoire(personnage, objectif, est_graphique = False):
    """
    La fonction renvoie True si le personnage a atteint l'objectif et False sinon.
    personnage : dictionnaire (position, vitesse)
    objectif : tuple de deux coins ((x1,y1), (x2, y2))
    est_graphique : bool qui indique le mode( 0 pour les formes géométrique, 1 pour les texture)

    >>> objectif1 = ((250,100), (270, 170))
    >>> perso1 = {"position": (260, 140), "vitesse": (0, 0)}
    >>> victoire(perso1, objectif1, est_graphique)
    True

    >>> perso2 = {"position": (230, 90), "vitesse": (0, 0)}
    >>> victoire(perso2, objectif1)
    False
    """
    largeur = LARGEUR_NINJA if est_graphique else LARGEUR_PERSO
    hauteur = HAUTEUR_NINJA if est_graphique else HAUTEUR_PERSO

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
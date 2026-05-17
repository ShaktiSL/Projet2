#Shaktinath SOLEIL, David NGALULA KABONGO, Mohamed TAHAR; GROUPE TP11_10
from constantes import *
import math

#Fichier principalement fait par David
def deplacer(personnage, gravite, pas_temps):
    """
    Met à jour la position et la vitesse du personnage selon la gravité et le pas de temps.
    personnage : dictionnaire (position, vitesse)
    gravite : tuple (gx, gy) de l'accélération gravitationnelle
    pas_temps : flottant représentant l'intervalle de temps
    """
    position_x, position_y = personnage["position"]
    vitesse_x, vitesse_y   = personnage["vitesse"]
    gravite_x, gravite_y   = gravite

    position_x = position_x + pas_temps * vitesse_x
    position_y = position_y + pas_temps * vitesse_y

    vitesse_x = vitesse_x + pas_temps * gravite_x
    vitesse_y = vitesse_y + pas_temps * gravite_y

    personnage["position"] = (position_x, position_y)
    personnage["vitesse"]  = (vitesse_x, vitesse_y)


def placer_bord(personnage, bloc, cote_collision, est_graphique=False):
    """
    Replace le personnage juste à l'extérieur du bloc contre le bord touché.
    personnage : dictionnaire (position, vitesse)
    bloc : tuple de deux coins et une couleur ((x1, y1), (x2, y2), couleur)
    cote_collision : chaîne parmi "haut", "bas", "gauche", "droite"
    est_graphique : bool
    """

    position_x, position_y = personnage["position"]
    (bord_gauche, bord_haut), (bord_droit, bord_bas), _ = bloc

    if cote_collision == "haut":
        position_y = bord_haut - HAUTEUR_PERSO - 0.1
    elif cote_collision == "bas":
        position_y = bord_bas + 0.1
    elif cote_collision == "gauche":
        position_x = bord_gauche - LARGEUR_PERSO - 0.1
    elif cote_collision == "droite":
        position_x = bord_droit + 0.1

    personnage["position"] = (position_x, position_y)


def detecter_cote(personnage, bloc, vitesse_actuelle):
    """
    Détermine par quel côté du bloc le personnage est entré en collision.
    personnage : dictionnaire (position, vitesse)
    bloc : tuple de deux coins et une couleur ((x1, y1), (x2, y2), couleur)
    vitesse_actuelle : tuple (vx, vy) au moment de l'impact
    """

    position_x, position_y       = personnage["position"]
    deplacement_x, deplacement_y = vitesse_actuelle
    (bord_gauche, bord_haut), (bord_droit, bord_bas), _ = bloc

    penetration_haut   = (position_y + HAUTEUR_PERSO) - bord_haut
    penetration_bas    = bord_bas    - position_y
    penetration_gauche = (position_x + LARGEUR_PERSO) - bord_gauche
    penetration_droite = bord_droit  - position_x

    candidats_cotes = []
    if deplacement_y >= 0 and penetration_haut > 0:
        candidats_cotes.append(("haut",   penetration_haut))
    if deplacement_y <= 0 and penetration_bas > 0:
        candidats_cotes.append(("bas",    penetration_bas))
    if deplacement_x >= 0 and penetration_gauche > 0:
        candidats_cotes.append(("gauche", penetration_gauche))
    if deplacement_x <= 0 and penetration_droite > 0:
        candidats_cotes.append(("droite", penetration_droite))

    if not candidats_cotes:
        candidats_cotes = [
            ("haut",   penetration_haut),
            ("bas",    penetration_bas),
            ("gauche", penetration_gauche),
            ("droite", penetration_droite),
        ]

    def penetration_du_candidat(candidat):
        return candidat[1]

    meilleur_cote, _ = min(candidats_cotes, key=penetration_du_candidat)
    return meilleur_cote


def choc_mou(personnage, bloc):
    """
    Choc mou — surface grise ('gray') : arrêt complet sur le bord touché.
    personnage : dictionnaire (position, vitesse)
    bloc : tuple de deux coins et une couleur ((x1, y1), (x2, y2), couleur)
    """
    vitesse_x, vitesse_y = personnage["vitesse"]
    cote_touche = detecter_cote(personnage, bloc, (vitesse_x, vitesse_y))
    placer_bord(personnage, bloc, cote_touche)
    personnage["vitesse"] = (0, 0)


def choc_glace(personnage, bloc):
    """
    Glissement à vitesse constante : la composante perpendiculaire au bord est annulée.
    personnage : dictionnaire (position, vitesse)
    bloc : tuple de deux coins et une couleur ((x1, y1), (x2, y2), couleur)
    """
    vitesse_x, vitesse_y = personnage["vitesse"]
    cote_touche = detecter_cote(personnage, bloc, (vitesse_x, vitesse_y))
    placer_bord(personnage, bloc, cote_touche)

    if cote_touche == "haut" or cote_touche == "bas":
        personnage["vitesse"] = (vitesse_x, 0)
    else:
        personnage["vitesse"] = (0, vitesse_y)


def choc_boue(personnage, bloc):
    """
    Dérapage : glissement avec friction, la vitesse parallèle est réduite.
    personnage : dictionnaire (position, vitesse)
    bloc : tuple de deux coins et une couleur ((x1, y1), (x2, y2), couleur)
    """
    vitesse_x, vitesse_y = personnage["vitesse"]
    cote_touche = detecter_cote(personnage, bloc, (vitesse_x, vitesse_y))
    placer_bord(personnage, bloc, cote_touche)

    facteur_friction = 0.6

    if cote_touche == "haut" or cote_touche == "bas":
        personnage["vitesse"] = (vitesse_x * facteur_friction, 0)
    else:
        personnage["vitesse"] = (0, vitesse_y * facteur_friction)


def choc_elastique(personnage, bloc):
    """
    Rebond parfait : la vitesse dans la direction du choc est inversée.
    personnage : dictionnaire (position, vitesse)
    bloc : tuple de deux coins et une couleur ((x1, y1), (x2, y2), couleur)
    """
    vitesse_x, vitesse_y = personnage["vitesse"]
    cote_touche = detecter_cote(personnage, bloc, (vitesse_x, vitesse_y))
    placer_bord(personnage, bloc, cote_touche)

    if cote_touche == "haut" or cote_touche == "bas":
        personnage["vitesse"] = (vitesse_x, -vitesse_y)
    else:
        personnage["vitesse"] = (-vitesse_x, vitesse_y)


def choc_amorti(personnage, bloc):
    """
    Rebond avec perte de vitesse : le personnage rebondit mais perd 50% de sa vitesse.
    En dessous d'un seuil minimal, le rebond est annulé pour éviter les micro-oscillations.
    """
    vitesse_x, vitesse_y = personnage["vitesse"]
    cote_touche = detecter_cote(personnage, bloc, (vitesse_x, vitesse_y))
    placer_bord(personnage, bloc, cote_touche)

    facteur_amortissement = 0.5
    seuil_arret           = 1.0

    if cote_touche == "haut" or cote_touche == "bas":
        nouvelle_vy = -vitesse_y * facteur_amortissement
        if abs(nouvelle_vy) < seuil_arret:
            nouvelle_vy = 0
        personnage["vitesse"] = (vitesse_x * facteur_amortissement, nouvelle_vy)
    else:
        nouvelle_vx = -vitesse_x * facteur_amortissement
        if abs(nouvelle_vx) < seuil_arret:
            nouvelle_vx = 0
        personnage["vitesse"] = (nouvelle_vx, vitesse_y * facteur_amortissement)


def choc_colle(personnage, bloc):
    """
    Arrêt total immédiat dès le premier contact, sans glissement.
    personnage : dictionnaire (position, vitesse)
    bloc : tuple de deux coins et une couleur ((x1, y1), (x2, y2), couleur)
    """
    vitesse_x, vitesse_y = personnage["vitesse"]
    cote_touche = detecter_cote(personnage, bloc, (vitesse_x, vitesse_y))
    placer_bord(personnage, bloc, cote_touche)
    personnage["vitesse"] = (0, 0)


def choc(personnage, lst_blocs):
    """
    Orchestre la gestion d'une collision : trouve le bloc touché, lit sa couleur,
    et appelle la fonction de choc correspondante.
    personnage : dictionnaire {"position": (x, y), "vitesse": (vx, vy)}
    lst_blocs  : liste de blocs ((x1, y1), (x2, y2), couleur)
    """
    bloc_en_contact = collision(personnage, lst_blocs)

    if bloc_en_contact is None:
        return
    
    _, _, couleur_bloc = bloc_en_contact

    if couleur_bloc == 'blue':
        choc_glace(personnage, bloc_en_contact)
    elif couleur_bloc == 'brown':
        choc_boue(personnage, bloc_en_contact)
    elif couleur_bloc == 'pink':
        choc_elastique(personnage, bloc_en_contact)
    elif couleur_bloc == 'orange':
        choc_amorti(personnage, bloc_en_contact)
    elif couleur_bloc == 'purple':
        choc_colle(personnage, bloc_en_contact)
    else:
        choc_mou(personnage, bloc_en_contact)


def pas(personnage, lst_blocs, objectif, est_graphique):
    """
    Effectue un pas de simulation physique, applique la gravité et gère l'arrêt.
    personnage : dictionnaire (position, vitesse)
    lst_blocs : liste de blocs ((x1, y1), (x2, y2), couleur)
    objectif : tuple de deux coins ((x1, y1), (x2, y2))
    est_graphique : bool
    """
    position_avant_deplacement = personnage["position"]

    deplacer(personnage, GRAVITE, PAS)

    if victoire(personnage, objectif):
        return True

    choc(personnage, lst_blocs)

    vitesse_x, vitesse_y = personnage["vitesse"]
    vitesse_nulle        = (vitesse_x == 0 and vitesse_y == 0)
    position_inchangee   = (personnage["position"] == position_avant_deplacement)

    if vitesse_nulle or position_inchangee:
        return True

    return False


def simuler(personnage, lst_blocs, objectif, est_graphique):
    """
    Simule et renvoie la liste complète des positions successives du saut.
    personnage : dictionnaire (position, vitesse)
    lst_blocs : liste de blocs ((x1, y1), (x2, y2), couleur)
    objectif : tuple de deux coins ((x1, y1), (x2, y2))
    est_graphique : bool
    """
    liste_positions   = [personnage["position"]]
    nombre_iterations = 0

    while not pas(personnage, lst_blocs, objectif, est_graphique):
        liste_positions.append(personnage["position"])
        nombre_iterations += 1
        if nombre_iterations > 1000: 
            personnage["vitesse"] = (0, 0)
            break

    liste_positions.append(personnage["position"])
    return liste_positions

#Fonction fait par Shaktinath
def clic_vers_vitesse(personnage, clic):
    """
    La fonction met à jour la vitesse du personnage par le clic de l'utilisateur.
    personnage : dictionnaire (position, vitesse)
    clic : tuple (x, y) des coordonnées du clic.
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
    

    centre_x, centre_y           = personnage["position"]
    destination_x, destination_y = clic

    direction_x = float(destination_x - centre_x)
    direction_y = float(destination_y - centre_y)

    longueur_vecteur = math.sqrt(direction_x**2 + direction_y**2)

    if longueur_vecteur == 0:
        personnage["vitesse"] = (0.0, 0.0)
        return

    if longueur_vecteur > VMAX:
        reduction   = VMAX / longueur_vecteur
        direction_x = direction_x * reduction
        direction_y = direction_y * reduction

    personnage["vitesse"] = (direction_x, direction_y)

#Fonction fait par Shaktinath
def collision(personnage, lst_blocs, est_graphique=False):
    """
    La fonction renvoie le bloc ayant eu un contact avec le personnage et None sinon.
    personnage : dictionnaire (position, vitesse)
    lst_blocs = liste de blocs ((x1,y1), (x2, y2), couleur)
    est_graphique : bool
    >>> perso1 = {"position": (260, 140), "vitesse": (0, 0)}
    >>> lst_bloc = [((105, 150), (300, 170), 'gray')]
    >>> collision(perso1, lst_bloc, False)
    ((105, 150), (300, 170), 'gray')
    """

    taille_largeur = LARGEUR_NINJA if est_graphique else LARGEUR_PERSO
    taille_hauteur = HAUTEUR_NINJA if est_graphique else HAUTEUR_PERSO

    coin_gauche, coin_haut = personnage["position"]
    coin_droit = coin_gauche + taille_largeur
    coin_bas   = coin_haut  + taille_hauteur

    for bloc_courant in lst_blocs:
        (bloc_gauche, bloc_haut), (bloc_droit, bloc_bas), _ = bloc_courant

        touche_horizontalement = coin_droit > bloc_gauche and coin_gauche < bloc_droit
        touche_verticalement   = coin_bas   > bloc_haut  and coin_haut  < bloc_bas

        if touche_horizontalement and touche_verticalement:
            return bloc_courant

    return None

#Fonction fait par Shaktinath
def victoire(personnage, objectif, est_graphique=False):
    """
    La fonction renvoie True si le personnage a atteint l'objectif et False sinon.
    personnage : dictionnaire (position, vitesse)
    objectif : tuple de deux coins ((x1,y1), (x2, y2))
    est_graphique : bool

    >>> objectif1 = ((250,100), (270, 170))
    >>> perso1 = {"position": (260, 140), "vitesse": (0, 0)}
    >>> victoire(perso1, objectif1, False)
    True

    >>> perso2 = {"position": (230, 90), "vitesse": (0, 0)}
    >>> victoire(perso2, objectif1)
    False
    """

    coin_perso_gauche, coin_perso_haut = personnage["position"]
    coin_perso_droit = coin_perso_gauche + LARGEUR_PERSO
    coin_perso_bas   = coin_perso_haut   + HAUTEUR_PERSO

    (zone_gauche, zone_haut), (zone_droit, zone_bas) = objectif

    dans_zone_x = coin_perso_droit > zone_gauche and coin_perso_gauche < zone_droit
    dans_zone_y = coin_perso_bas   > zone_haut   and coin_perso_haut  < zone_bas

    if dans_zone_x and dans_zone_y:
        return True

    return False


if __name__ == "__main__":
    from doctest import testmod
    testmod()
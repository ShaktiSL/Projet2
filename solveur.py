#Shaktinath SOLEIL, David NGALULA KABONGO, Mohamed TAHAR; GROUPE TP11_10
from physique import *
from constantes import *

#Fonction fait par Mohamed
def generer_vitesses(pas_v):
    """Génère tous les sauts possibles.

    >>> vits = generer_vitesses(50)
    >>> (0, 0) in vits
    False
    >>> len(vits) > 0
    True
    """
    vitesses = []
    for vx in range(-VMAX, VMAX + 1, pas_v):
        for vy in range(-VMAX, VMAX + 1, pas_v):
            if vx != 0 or vy != 0:
                vitesses.append((vx, vy))
    return vitesses

#Fonction fait par Mohamed
def position_approx(personnage, taille_grille):
    """Arrondit la position pour la mémoire du solveur.

    >>> perso = {"position": (107.8, 203.1)}
    >>> position_approx(perso, 10)
    (10, 20)
    >>> position_approx(perso, 50)
    (2, 4)
    """
    x, y = personnage["position"]
    return (int(x // taille_grille), int(y // taille_grille))

#Fonction fait par Mohamed
def simuler_saut(personnage, blocs, objectif, est_graphique):
    """
    Simule un saut complet depuis la position actuelle du personnage
    jusqu'à ce qu'il soit au repos. Travaille sur une copie du personnage
    pour ne pas modifier l'original.
    Retourne le nouveau personnage après le saut.
    
    >>> blocs = [((0, 350), (500, 370), "gray")]
    >>> perso = {"position": (100, 300), "vitesse": (5, 0)}
    >>> resultat = simuler_saut(perso, blocs, ((400, 100), (440, 140)), False)
    >>> resultat["vitesse"]
    (0, 0)
    """
    perso_copie = {"position": personnage["position"], "vitesse": personnage["vitesse"]}
    en_mouvement = True
    compteur = 0

    while en_mouvement:
        if pas(perso_copie, blocs, objectif, est_graphique):
            en_mouvement = False

        compteur += 1
        if compteur > 500:
            en_mouvement = False

        x, y = perso_copie["position"]
        if y < -500 or x < -100 or x > LARGEUR_FENETRE + 100:
            perso_copie["vitesse"] = (0, 0)
            en_mouvement = False

    return perso_copie  

#Fonction fait par Mohamed
def resoudre(personnage, blocs, objectif, liste_vitesses, deja_explore, prof_max, est_graphique):
    """
    Recherche récursivement un chemin vers l'objectif.
    Retourne la liste des vitesses à jouer, ou None si impossible.
    """
    if victoire(personnage, objectif):
        return []

    if prof_max <= 0:
        return None

    position_grille = position_approx(personnage, 10)
    if position_grille in deja_explore:
        return None
    deja_explore.add(position_grille)

    for vitesse in liste_vitesses:
        perso_essai = {"position": personnage["position"], "vitesse": vitesse}

        nouv_perso = simuler_saut(perso_essai, blocs, objectif, est_graphique)

        chemin = resoudre(nouv_perso, blocs, objectif, liste_vitesses, deja_explore, prof_max - 1, est_graphique)

        if chemin is not None:
            return [vitesse] + chemin

    return None

#Fonction fait par Mohamed
def resoudre_niveau(personnage, blocs, objectif, est_graphique, pas_v=10, prof_max=5):
    """La fonction finale à appeler.
    
    personnage : dictionnaire {"position": (x, y), "vitesse": (vx, vy)}
    blocs      : liste de blocs du niveau
    objectif   : tuple ((x1, y1), (x2, y2))
    pas_v      : pas entre chaque vitesse testée
    prof_max   : nombre de sauts maximum autorisés
    """
    vitesses = generer_vitesses(pas_v)
    return resoudre(personnage, blocs, objectif, vitesses, set(), prof_max, est_graphique)


if __name__ == "__main__":
    perso = {"position": (100, 300), "vitesse": (0, 0)}
    blocs = [((0, 350), (500, 370), "gray")]
    objectif = ((200, 100), (240, 140))

    print("Lancement du solveur...")
    resultat = resoudre_niveau(perso, blocs, objectif, est_graphique=False ,pas_v=10, prof_max=3)

    if resultat is None:
        print("Aucune solution trouvée.")
    else:
        print(f"Solution trouvée en {len(resultat)} saut(s) !")
        for i, v in enumerate(resultat):
            print(f"  Saut {i+1} : vitesse {v}")
from physique import *
from fltk import *
from interface import *



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


def simuler_saut(personnage, blocs, objectif):
    en_mouvement = True
    compteur = 0
    
    print("Simulation en cours...") 

    while en_mouvement:
        if pas(personnage, blocs): 
            en_mouvement = False
        
        # --- ESSENTIEL POUR L'AFFICHAGE ---
        efface_tout()
        dessiner_blocs(blocs)
        dessiner_objectif(objectif)
        dessiner_personnage(personnage)
        mise_a_jour()
        
        # --- ESSENTIEL POUR NE PAS FREEZER ---
        donne_ev()    # Traite les événements système (Windows/Mac)
        attente(5)   # Laisse respirer le processeur
            
        compteur += 1
        # Sécurité : Si le saut dure plus de 5 secondes (500 * 10ms), on force l'arrêt
        if compteur > 500:
            print("Sécurité : Saut trop long, arrêt forcé.")
            en_mouvement = False
        
        x, y = personnage["position"]
        
        # Sécurité : Si le perso sort trop loin par le haut ou les côtés
        if y < -500 or x < -100 or x > LARGEUR_FENETRE + 100:
            print("Le personnage est perdu dans l'espace, retour au calme.")
            personnage["vitesse"] = (0, 0) # On stoppe sa course
            en_mouvement = False

    print("Fin de simulation.")


def resoudre(personnage, blocs, objectif, liste_vitesses, deja_explore, prof_max):
    # 1. On vérifie si on a gagné
    if victoire(personnage, objectif):
        return []

    # 2. On vérifie si on doit s'arrêter
    if prof_max <= 0:
        return None
    
    # 3. On vérifie si on est déjà passé par là
    position_grille = position_approx(personnage, 10)
    if position_grille in deja_explore:
        return None
    deja_explore.add(position_grille)
    
    # 4. On teste les sauts
    for vitesse in liste_vitesses:
        nouv_perso = simuler_saut(personnage, vitesse, blocs)
        
        chemin = resoudre(nouv_perso, blocs, objectif, liste_vitesses, deja_explore, prof_max - 1)
        
        if chemin is not None:
            return [vitesse] + chemin
            
    return None

def resoudre_niveau(personnage, blocs, objectif, pas_v, prof_max):
    """La fonction finale à appeler."""
    vitesses = generer_vitesses(pas_v)
    return resoudre(personnage, blocs, objectif, vitesses, set(), prof_max)




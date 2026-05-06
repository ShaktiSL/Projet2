from niveau.victoire import *
from solveur.position_approx import *
from solveur.simuler_saut import *
from solveur.generer_vitesse import *

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
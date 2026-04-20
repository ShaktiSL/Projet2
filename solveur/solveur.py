from niveau.victoire import victoire
from solveur.position_approx import position_approx
from solveur.simuler_saut import simuler_saut
from solveur.generer_vitesse import generer_vitesses

def resoudre(personnage, blocs, objectif, vitesses, visite, prof_max):
    # 1. On vérifie si on a gagné
    if victoire(personnage, objectif):
        return []

    # 2. On vérifie si on doit s'arrêter
    if prof_max <= 0:
        return None
    
    # 3. On vérifie si on est déjà passé par là
    pos = position_approx(personnage, 10)
    if pos in visite:
        return None
    visite.add(pos)
    
    # 4. On teste les sauts
    for v in vitesses:
        nouv_perso = simuler_saut(personnage, v, blocs)
        
        chemin = resoudre(nouv_perso, blocs, objectif, vitesses, visite, prof_max - 1)
        
        if chemin is not None:
            return [v] + chemin
            
    return None

def resoudre_niveau(personnage, blocs, objectif, pas_v, prof_max):
    """La fonction finale à appeler."""
    vitesses = generer_vitesses(pas_v)
    return resoudre(personnage, blocs, objectif, vitesses, set(), prof_max)
from niveau.constantes_niveau import PAS
from solveur.solveur import resoudre_niveau

# 1. On crée un décor minimaliste
# Un sol de (0, 300) à (500, 400)
blocs = [((0, 300), (500, 400))]

# L'objectif est un petit carré posé sur le sol à droite
objectif = ((400, 250), (450, 300))

# 2. On crée un personnage au début du sol
perso = {"position": (50, 250), "vitesse": (0, 0)}

print("--- RECHERCHE DE SOLUTION ---")
# On lance le solveur : 
# pas_v = 25 (on teste par paliers de 25)
# prof_max = 3 (il a le droit à 3 sauts max)
solution = resoudre_niveau(perso, blocs, objectif, 50, 2)

if solution is None:
    print("❌ Le solveur n'a pas trouvé de chemin. (Vérifie la position de l'objectif)")
else:
    print("✅ SOLUTION TROUVÉE !")
    print(f"Pour gagner, fais ces sauts : {solution}")
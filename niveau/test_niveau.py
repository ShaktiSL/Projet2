from niveaux import charger_niveau

perso, blocs, obj = charger_niveau("niveau/fichier_valeur_test.txt")
print("Perso :", perso)
print("Nombre de blocs :", len(blocs))
print("Objectif :", obj)
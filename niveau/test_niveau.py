from niveaux import charger_niveau

perso, blocs, obj = charger_niveau("niveau/niveau_test.txt")
print("Perso :", perso)
print("Nombre de blocs :", len(blocs))
print("Objectif :", obj)
# -------------------------------------------------------------
# Chargement d'un niveau depuis un fichier .txt
# -------------------------------------------------------------

def creer_perso(x,y):
    """
    La fonction crée le personnage avec une vitesse de départ toujours à (0,0)
    x, y : position de départ
    Renvoie un dictionnaire contenant sa postion et sa vitesse.

    >>> creer_perso(500, 750)
    {'position': (500, 750), 'vitesse': (0, 0)}
    """
    return {"position" : (x,y), "vitesse" : (0,0)}


def lire_perso(lignes):
    ligne = lignes[0].split('#')[0].strip()
    parts = ligne.split(',')
    return {"position": (int(parts[0]), int(parts[1])), "vitesse": (0, 0)}

def lire_objectif(lignes):
    ligne = lignes[1].split('#')[0].strip()
    coords = ligne.split(',')
    return ((int(coords[0]), int(coords[1])), (int(coords[2]), int(coords[3])))

def lire_blocs(lignes):
    """
    Lit toutes les lignes à partir de la 3ème pour créer la liste de blocs.
    """
    lst_blocs = []
    for ligne in lignes[2:]:
        propre = ligne.split('#')[0].strip()
        if propre == "": 
            continue
        points = propre.split(',')
        coords = ((int(points[0]), int(points[1])), (int(points[2]), int(points[3])))
        
        # On vérifie s'il y a une 5ème valeur pour la couleur
        if len(points) == 5:
            couleur = points[4].strip()
        else:
            couleur = 'gray' # Couleur par défaut si rien n'est précisé
            
        # On stocke tout dans un tuple : ( (x1,y1), (x2,y2), "couleur" )
        lst_blocs.append((coords[0], coords[1], couleur))
    return lst_blocs

def charger_niveau(fichier):
    """
    Lit le fichier et renvoie (personnage, lst_blocs, objectif).
    """
    with open(fichier, 'r', encoding='utf-8') as f:
        lignes = f.readlines()
    premiere_ligne = lignes[0].strip()
    est_graphique = False
    if premiere_ligne == "STYLE:1":
        est_graphique = True
        lignes_utiles = lignes[1:]
    elif premiere_ligne == "STYLE:0":
        est_graphique = False
        lignes_utiles = lignes[1:]

    perso = lire_perso(lignes_utiles)
    objectif = lire_objectif(lignes_utiles)
    blocs = lire_blocs(lignes_utiles)
    
    return perso, blocs, objectif, est_graphique
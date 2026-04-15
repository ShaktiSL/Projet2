def lire_perso(lignes):
    """
    Lit la première ligne et crée le dictionnaire personnage.
    >>> lire_perso(["100,200 # commentaire\\n"])
    {'position': (100, 200), 'vitesse': (0, 0)}
    """
    ligne = lignes[0].split('#')[0].strip()
    parts = ligne.split(',')
    return {"position": (int(parts[0]), int(parts[1])), "vitesse": (0, 0)}

def lire_objectif(lignes):
    """
    Lit la deuxième ligne et crée le tuple objectif ((x1, y1), (x2, y2)).
    >>> lire_objectif(["ignore\\n", "10,10,50,50 # commentaire\\n"])
    ((10, 10), (50, 50))
    """
    ligne = lignes[1].split('#')[0].strip()
    p = ligne.split(',')
    return ((int(p[0]), int(p[1])), (int(p[2]), int(p[3])))

def lire_blocs(lignes):
    """
    Lit toutes les lignes à partir de la 3ème pour créer la liste de blocs.
    """
    lst_blocs = []
    for ligne in lignes[2:]:
        propre = ligne.split('#')[0].strip()
        p = propre.split(',')
        bloc = ((int(p[0]), int(p[1])), (int(p[2]), int(p[3])))
        lst_blocs.append(bloc)
    return lst_blocs

def charger_niveau(fichier):
    """
    Lit le fichier et renvoie (personnage, lst_blocs, objectif).
    """
    with open(fichier, 'r', encoding='utf-8') as f:
        lignes = f.readlines()
    
    perso = lire_perso(lignes)
    objectif = lire_objectif(lignes)
    blocs = lire_blocs(lignes)
    
    return perso, blocs, objectif
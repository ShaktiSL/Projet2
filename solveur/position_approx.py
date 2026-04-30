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
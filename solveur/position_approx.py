def position_approx(personnage, a):
    """Arrondit la position pour la mémoire du solveur."""
    x, y = personnage["position"]
    return (int(x // a), int(y // a))
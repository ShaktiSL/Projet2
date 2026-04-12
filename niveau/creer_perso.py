def creer_perso(x,y):
    """
    La fonction crée le personnage avec une vitesse de départ toujours à (0,0)
    x, y : position de départ
    Renvoie un dictionnaire contenant sa postion et sa vitesse.

    >>> creer_perso(500, 750)
    {'position': (500, 750), 'vitesse': (0, 0)}
    """
    return {"position" : (x,y), "vitesse" : (0,0)}

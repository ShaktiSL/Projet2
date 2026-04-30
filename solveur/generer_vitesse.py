from constantes import *

def generer_vitesses(pas_v):
    """Génère tous les sauts possibles.

    >>> vits = generer_vitesses(50)
    >>> (0, 0) in vits
    False
    >>> len(vits) > 0
    True
    """
    vitesses = []
    for vx in range(-VMAX, VMAX + 1, pas_v):
        for vy in range(-VMAX, VMAX + 1, pas_v):
            if vx != 0 or vy != 0:
                vitesses.append((vx, vy))
    return vitesses

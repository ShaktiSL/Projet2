from niveau.physique import pas

def simuler_saut(personnage, vitesse_saut, blocs):
    """Simule un saut complet jusqu'à l'arrêt du personnage."""
    # On crée une copie pour ne pas bouger le vrai perso pendant qu'on réfléchit
    copie_p = {"position": personnage["position"], "vitesse": vitesse_saut}
    
    en_mouvement = True
    while en_mouvement:
        # La fonction pas() de physique.py déplace le perso d'un petit cran
        if pas(copie_p, blocs): 
            en_mouvement = False
    return copie_p
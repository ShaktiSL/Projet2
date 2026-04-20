from niveau.physique import pas

def simuler_saut(personnage, vitesse_saut, blocs):
    """Simule un saut complet jusqu'à l'arrêt du personnage."""
    copie_p = {"position": personnage["position"], "vitesse": vitesse_saut}
    
    en_mouvement = True
    compteur_securite = 0  # On prépare notre chronomètre d'urgence
    
    while en_mouvement:
        if pas(copie_p, blocs): 
            en_mouvement = False
            
        compteur_securite += 1
        
        # Si la boucle tourne plus de 1000 fois ou si le perso tombe sous y=2000
        if compteur_securite > 1000 or copie_p["position"][1] > 2000:
            en_mouvement = False
            
    return copie_p
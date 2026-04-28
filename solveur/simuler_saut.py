from niveau.physique import *
from interface.affichage import *


def simuler_saut(personnage, blocs, objectif):
    en_mouvement = True
    compteur = 0
    
    print("Simulation en cours...") 

    while en_mouvement:
        if pas(personnage, blocs): 
            en_mouvement = False
        
        # --- ESSENTIEL POUR L'AFFICHAGE ---
        efface_tout()
        dessiner_blocs(blocs)
        dessiner_objectif(objectif)
        dessiner_personnage(personnage)
        mise_a_jour()
        
        # --- ESSENTIEL POUR NE PAS FREEZER ---
        donne_ev()    # Traite les événements système (Windows/Mac)
        attente(5)   # Laisse respirer le processeur
            
        compteur += 1
        # Sécurité : Si le saut dure plus de 5 secondes (500 * 10ms), on force l'arrêt
        if compteur > 500:
            print("Sécurité : Saut trop long, arrêt forcé.")
            en_mouvement = False
        
        x, y = personnage["position"]
        
        # Sécurité : Si le perso sort trop loin par le haut ou les côtés
        if y < -500 or x < -100 or x > LARGEUR_FENETRE + 100:
            print("Le personnage est perdu dans l'espace, retour au calme.")
            personnage["vitesse"] = (0, 0) # On stoppe sa course
            en_mouvement = False

    print("Fin de simulation.")
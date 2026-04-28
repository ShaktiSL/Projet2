from niveau.physique import *
from interface.affichage import *


def simuler_saut(personnage, blocs, objectif):
    en_mouvement = True
    compteur = 0
    while en_mouvement:
        if pas(personnage, blocs): 
            en_mouvement = False
        
        efface_tout()
        dessiner_blocs(blocs)
        dessiner_objectif(objectif)
        dessiner_personnage(personnage)
        mise_a_jour()
        
        # COMMANDE CRITIQUE pour éviter le freeze :
        donne_ev() 
        attente(10) 
            
        compteur += 1
        if compteur > 800 or personnage["position"][1] > 1000:
            en_mouvement = False
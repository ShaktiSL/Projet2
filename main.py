from interface import *
from fltk import *
from chargement import *
from solveur import *
from constantes import *
import os

# -------------------------------------------------------------
# Programme principal
# -------------------------------------------------------------

def boucle_jeu(personnage, lst_blocs, objectif, est_graphique):
    """
    Boucle principale d'une partie.
    Retourne "MENU" pour revenir au menu, "QUITTER" pour quitter.
    """
    viseur       = False    
    dernier_clic = (0, 0)
    nb_sauts     = 0         
    # On initialise l'historique avec l'état de départ
    historique   = [dict(personnage)]
 
    while True:
        # --- Affichage standard ---
        efface_tout()
        if est_graphique:
            image(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2, 'media/fond-jeux.png', 
                  largeur=LARGEUR_FENETRE, hauteur=HAUTEUR_FENETRE)
        
        dessiner_blocs(lst_blocs, est_graphique)
        dessiner_objectif(objectif, est_graphique)
        dessiner_personnage(personnage, est_graphique)
        
        if viseur:
            dessiner_fleche(personnage, dernier_clic)
 
        texte(10, 10, f"Sauts : {nb_sauts}", ancrage='nw', taille=18, couleur='black')

        # --- Sécurité : Sortie de terrain hors animation ---
        x, y = personnage["position"]
        if x < -100 or x > LARGEUR_FENETRE + 100 or y > HAUTEUR_FENETRE + 100:
            if len(historique) > 0:
                etat = historique[-1]
                personnage["position"] = etat["position"]
                personnage["vitesse"] = (0, 0)
                mise_a_jour() # On rafraîchit pour voir le retour
                viseur = False
 
        mise_a_jour()
 
        # --- Vérification victoire ---
        if victoire(personnage, objectif, est_graphique):
            afficher_victoire()
            return "MENU"
 
        # --- Gestion des événements ---
        ev = donne_ev()
        if ev is None:
            continue
        tev = type_ev(ev)
 
        if tev == 'Quitte':
            return "QUITTER"
 
        elif tev == 'ClicGauche':
            dernier_clic = (abscisse(ev), ordonnee(ev))
            clic_vers_vitesse(personnage, dernier_clic)
            viseur = True
 
        elif tev == 'ClicDroit':
            if viseur:
                # 1. On prépare le retour en arrière
                ancienne_etat = dict(personnage)
                historique.append(ancienne_etat)
                
                # 2. On calcule la trajectoire
                trajectoire = simuler(personnage, lst_blocs, objectif, est_graphique)
                
                # 3. On lance l'animation (la boucle for)
                for pos in trajectoire:
                    personnage["position"] = pos
                    
                    efface_tout()
                    if est_graphique:
                        image(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2, 'media/fond-jeux.png', 
                              largeur=LARGEUR_FENETRE, hauteur=HAUTEUR_FENETRE)
                    
                    dessiner_blocs(lst_blocs, est_graphique)
                    dessiner_objectif(objectif, est_graphique)
                    dessiner_personnage(personnage, est_graphique)
                    
                    texte(10, 10, f"Sauts : {nb_sauts + 1}", ancrage='nw', taille=18)
                    mise_a_jour()
                    
                    tx, ty = pos
                    if tx < -50 or tx > LARGEUR_FENETRE + 50 or ty > HAUTEUR_FENETRE + 50:
                        personnage["position"] = ancienne_etat["position"]
                        personnage["vitesse"] = (0, 0)
                        break 

                # 4. On valide le saut
                nb_sauts += 1
                viseur = False
                # --- SURTOUT : Ne rien ajouter d'autre ici ! ---
 
        elif tev == 'Touche':
            t = touche(ev)
            if t == 'Escape':
                return "MENU"
                
            # Touche Espace ou Retour Arrière pour annuler
            elif t == 'BackSpace' or t == 'space':
                if len(historique) > 1: 
                    historique.pop() # On retire l'état actuel
                    dernier_etat = historique[-1]
                    
                    personnage["position"] = dernier_etat["position"]
                    personnage["vitesse"] = (0, 0)
                    nb_sauts = max(0, nb_sauts - 1)
                    
                    viseur = False
                    print("Retour en arrière effectué !")
                else:
                    print("Déjà à la position de départ.")
            
            # Touche S pour le solveur (évite le conflit avec Clic Droit)
            elif t == 's':
                print("Appel du solveur...")
                # On appelle resoudre_niveau (qui va lui-même appeler resoudre proprement)
                solution = resoudre_niveau(personnage, lst_blocs, objectif, est_graphique, pas_v=20, prof_max=5)
                
                if solution:
                    print(f"Solution trouvée : {solution}")
                else:
                    print("Pas de solution trouvée.")

if __name__ == "__main__":
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
 
    continuer = True
    fichier = menu_selection(LISTE_NIVEAUX)
    

    while continuer:
        fichier = menu_selection(LISTE_NIVEAUX)
        if fichier == "QUITTER" or fichier is None:
            break
        
        chemin = "niveau/" + fichier
        perso, blocs, obj, est_graphique = charger_niveau(chemin)
 
        resultat = boucle_jeu(perso, blocs, obj, est_graphique)
 
        if resultat == "QUITTER":
            continuer = False
        elif resultat == "MENU":
            fichier = menu_selection(LISTE_NIVEAUX)
        else:
            continuer = False

    ferme_fenetre()

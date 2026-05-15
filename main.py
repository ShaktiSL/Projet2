from interface import *
from fltk import *
from chargement import *
from solveur import *
from constantes import *

# -------------------------------------------------------------
# Programme principal
# -------------------------------------------------------------

def boucle_jeu(personnage, lst_blocs, objectif):
    """
    Boucle principale d'une partie.
    Retourne "MENU" pour revenir au menu, "QUITTER" pour quitter.
    """
    viseur       = False      # True quand le joueur a visé (clic gauche)
    dernier_clic = (0, 0)
    nb_sauts     = 0          # compteur de sauts (amélioration )
    historique   = [dict(personnage)]  # pour le retour en arrière (amélioration )
 
    while True:
        # --- Affichage ---
        efface_tout()
        dessiner_blocs(lst_blocs)
        dessiner_objectif(objectif)
        dessiner_personnage(personnage)
        if viseur:
            dessiner_fleche(personnage, dernier_clic)
 
        # --- Compteur de sauts ---
        texte(10, 10, f"Sauts : {nb_sauts}", ancrage='nw', taille=18, couleur='black')

        x, y = personnage["position"]
        if x < 0 or x > LARGEUR_FENETRE or y > HAUTEUR_FENETRE or y < -200:
            print("Oups, le mouton s'est égaré !")
            if len(historique) > 0:
                # On reprend le dernier état de l'historique
                etat = historique[-1]
                personnage["position"] = etat["position"]
                personnage["vitesse"] = (0, 0)
                viseur = False
 
        mise_a_jour()
 
        # --- Vérification victoire ---
        if victoire(personnage, objectif):
            afficher_victoire()
            return "MENU"
 
        # --- Événements ---
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
 
        # Dans main.py, ligne 57 environ :
        elif tev == 'ClicDroit':
            if viseur:
                # 1. On sauvegarde la position AVANT le saut
                ancienne_etat = dict(personnage)
                historique.append(ancienne_etat)
                
                trajectoire = simuler(personnage, lst_blocs, objectif)
                
                for pos in trajectoire:
                    personnage["position"] = pos
                    
                    # --- VÉRIFICATION SORTIE DE TERRAIN ---
                    x, y = pos
                    if x < -50 or x > LARGEUR_FENETRE + 50 or y > HAUTEUR_FENETRE + 50:
                        print("Sortie de terrain détectée !")
                        # On téléporte le perso à sa position d'avant
                        personnage["position"] = ancienne_etat["position"]
                        personnage["vitesse"] = (0, 0)
                        break # On arrête l'animation tout de suite
                    
                    # Dessin (ton code d'avant)
                    efface_tout()
                    dessiner_blocs(lst_blocs)
                    dessiner_objectif(objectif)
                    dessiner_personnage(personnage)
                    mise_a_jour()

                nb_sauts += 1
                viseur = False
                # On dessine la trace finale après l'animation
                dessiner_trajectoire(trajectoire)
 
        elif tev == 'Touche':
            t = touche(ev)
            if t == 'Escape':
                return "MENU"
            elif t == 'BackSpace':
                # Retour en arrière : on revient à la position précédente
                if len(historique) > 1:
                    historique.pop()
                    etat = historique[-1]
                    personnage["position"] = etat["position"]
                    personnage["vitesse"]  = etat["vitesse"]
                    nb_sauts = max(0, nb_sauts - 1)
                    efface('trajectoire')
                    viseur = False

if __name__ == "__main__":
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
 
    continuer = True
    # On commence par demander le niveau
    fichier = menu_selection(LISTE_NIVEAUX)

    while continuer:
        fichier = menu_selection(LISTE_NIVEAUX)
        # Si l'utilisateur a fermé la fenêtre ou cliqué sur Quitter
        if fichier == "QUITTER" or fichier is None:
            break
        
        # On construit le chemin et on charge
        chemin = "niveau/" + fichier
        perso, blocs, obj = charger_niveau(chemin)
 
        # On lance la partie
        resultat = boucle_jeu(perso, blocs, obj)
 
        if resultat == "QUITTER":
            continuer = False
        elif resultat == "MENU":
            # Si on revient au menu, on REDEMANDE quel niveau choisir
            fichier = menu_selection(LISTE_NIVEAUX)
        else:
            # Sécurité
            continuer = False

    ferme_fenetre()

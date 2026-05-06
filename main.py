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
 
        elif tev == 'ClicDroit':
            if viseur:
                historique.append(dict(personnage))  # on sauvegarde avant le saut
                trajectoire = simuler(personnage, lst_blocs)
                dessiner_trajectoire(trajectoire)
                nb_sauts += 1
                viseur = False
 
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
    while continuer:
        fichier = menu_selection(LISTE_NIVEAUX)
 
        if fichier == "QUITTER":
            break
 
        chemin = "niveau/" + fichier
        perso, blocs, obj = charger_niveau(chemin)
 
        resultat = boucle_jeu(perso, blocs, obj)
 
        if resultat == "QUITTER":
            continuer = False
 
    ferme_fenetre()

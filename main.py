from interface import *
from fltk import *
from chargement import *
from solveur import *
from constantes import *

def boucle_jeu(personnage, lst_blocs, objectif):
    """
    Boucle principale d'une partie.
    Retourne "MENU" pour revenir au menu, "QUITTER" pour quitter.
    """
    viseur       = False    
    dernier_clic = (0, 0)
    nb_sauts     = 0         
    historique   = [dict(personnage)]
 
    while True:
        efface_tout()
        dessiner_blocs(lst_blocs)
        dessiner_objectif(objectif)
        dessiner_personnage(personnage)
        if viseur:
            dessiner_fleche(personnage, dernier_clic)
 
        texte(10, 10, f"Sauts : {nb_sauts}", ancrage='nw', taille=18, couleur='black')

        x, y = personnage["position"]
        if x < 0 or x > LARGEUR_FENETRE or y > HAUTEUR_FENETRE or y < -200:
            print("Oups, le mouton s'est égaré !")
            if len(historique) > 0:
                etat = historique[-1]
                personnage["position"] = etat["position"]
                personnage["vitesse"] = (0, 0)
                viseur = False
 
        mise_a_jour()
 
        if victoire(personnage, objectif):
            afficher_victoire()
            return "MENU"
 
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
                ancienne_etat = dict(personnage)
                historique.append(ancienne_etat)
                
                trajectoire = simuler(personnage, lst_blocs, objectif)
                
                for pos in trajectoire: 
                    personnage["position"] = pos
                    
                    x, y = pos
                    if x < -50 or x > LARGEUR_FENETRE + 50 or y > HAUTEUR_FENETRE + 50:
                        print("Sortie de terrain détectée !")
                        personnage["position"] = ancienne_etat["position"]
                        personnage["vitesse"] = (0, 0)
                        break
                    
                    efface_tout()
                    dessiner_blocs(lst_blocs)
                    dessiner_objectif(objectif)
                    dessiner_personnage(personnage)
                    mise_a_jour()

                nb_sauts += 1
                viseur = False
                dessiner_trajectoire(trajectoire)
 
        elif tev == 'Touche':
            t = touche(ev)
            if t == 'Escape':
                return "MENU"
                
            elif t == 'BackSpace' or t == 'space':
                if len(historique) > 1: 
                    historique.pop()
                    dernier_etat = historique[-1]
                    
                    personnage["position"] = dernier_etat["position"]
                    personnage["vitesse"] = (0, 0)
                    
                    nb_sauts = max(0, nb_sauts - 1)
                    
                    efface('trajectoire')
                    efface('prevision')
                    viseur = False
                    print("Retour en arrière effectué !")
                else:
                    print("Impossible de revenir plus loin !")

if __name__ == "__main__":
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
 
    continuer = True
    fichier = menu_selection(LISTE_NIVEAUX)

    while continuer:
        fichier = menu_selection(LISTE_NIVEAUX)
        if fichier == "QUITTER" or fichier is None:
            break
        
        chemin = "niveau/" + fichier
        perso, blocs, obj = charger_niveau(chemin)
 
        resultat = boucle_jeu(perso, blocs, obj)
 
        if resultat == "QUITTER":
            continuer = False
        elif resultat == "MENU":
            fichier = menu_selection(LISTE_NIVEAUX)
        else:
            continuer = False

    ferme_fenetre()

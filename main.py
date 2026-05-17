#Shaktinath SOLEIL, David NGALULA KABONGO, Mohamed TAHAR; GROUPE TP11_10
from interface import *
from fltk import *
from chargement import *
from solveur import *
from constantes import *
import os

def boucle_jeu(personnage, lst_blocs, objectif, est_graphique,meilleurs_score,fichier):
    """
    Boucle principale d'une partie.
    Retourne "MENU" pour revenir au menu, "QUITTER" pour quitter.
    """
    viseur       = False    
    dernier_clic = (0, 0)
    nb_sauts     = 0         
    historique   = [dict(personnage)]
    points_solveur =[]
 
    while True:
        efface_tout()
        if est_graphique:
            image(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2, 'media/fond-jeux.png', 
                  largeur=LARGEUR_FENETRE, hauteur=HAUTEUR_FENETRE)
        
        dessiner_blocs(lst_blocs, est_graphique)
        dessiner_objectif(objectif, est_graphique)
        dessiner_personnage(personnage, est_graphique)
        for (x, y) in points_solveur:
            cercle(x, y, 8, remplissage='red', tag='solveur')

        if viseur:
            dessiner_fleche(personnage, dernier_clic)
 
        texte(10, 10, f"Sauts : {nb_sauts}", ancrage='nw', taille=18, couleur='black')
        texte(10, 35, f"Meilleur : {meilleurs_score.get(fichier, '-')}", ancrage='nw', taille=18, couleur='blue')

        x, y = personnage["position"]
        if x < -100 or x > LARGEUR_FENETRE + 100 or y > HAUTEUR_FENETRE + 100:
            if len(historique) > 0:
                etat = historique[-1]
                personnage["position"] = etat["position"]
                personnage["vitesse"] = (0, 0)
                mise_a_jour()
                viseur = False
 
        mise_a_jour()
 
        if victoire(personnage, objectif, est_graphique):
            efface_tout()
            if est_graphique:
                image(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2, 'media/fond-jeux.png', 
                      largeur=LARGEUR_FENETRE, hauteur=HAUTEUR_FENETRE)
            afficher_victoire()
            
            texte(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE - 80, 
                  "CLIQUEZ ICI POUR REVENIR AU MENU", couleur='gold', taille=20, ancrage='center')
            mise_a_jour()
            
            while donne_ev() is not None:
                pass
            
            attente_clic = True
            while attente_clic:
                ev_victoire = donne_ev()
                if ev_victoire is not None:
                    type_v = type_ev(ev_victoire)
                    if type_v in ['ClicGauche', 'ClicDroit', 'Touche']:
                        attente_clic = False
                    elif type_v == 'Quitte':
                        return "QUITTER",0
                attente(0.01)
            
           
            efface_tout()
            mise_a_jour() 
            while donne_ev() is not None:
                pass
                
            return "MENU",nb_sauts
 
        ev = donne_ev()
        if ev is None:
            continue
        tev = type_ev(ev)
 
        if tev == 'Quitte':
            return "QUITTER",0
 
        elif tev == 'ClicGauche':
            dernier_clic = (abscisse(ev), ordonnee(ev))
            clic_vers_vitesse(personnage, dernier_clic)
            viseur = True
 
        elif tev == 'ClicDroit':
            if viseur:
                ancienne_etat = dict(personnage)
                historique.append(ancienne_etat)
                
                trajectoire = simuler(personnage, lst_blocs, objectif, est_graphique)
                
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

                nb_sauts += 1
                viseur = False
 
        elif tev == 'Touche':
            t = touche(ev)
            if t == 'Escape':
                return "MENU",nb_sauts
                
            elif t == 'BackSpace' or t == 'space':
                if len(historique) > 1: 
                    historique.pop()
                    dernier_etat = historique[-1]
                    
                    personnage["position"] = dernier_etat["position"]
                    personnage["vitesse"] = (0, 0)
                    nb_sauts = max(0, nb_sauts - 1)
                    
                    viseur = False
                    print("Retour en arrière effectué !")
                else:
                    print("Déjà à la position de départ.")
            
            elif t == 's':
                print("Appel du solveur...")
                solution = resoudre_niveau(personnage, lst_blocs, objectif, est_graphique, pas_v=10, prof_max=8)
                
                if solution:
                    print(f"Solution trouvée en {len(solution)} sauts : {solution}")
                    points_solveur.clear()
                    perso_copie = {"position": personnage["position"], "vitesse": (0, 0)}
                    for vitesse in solution:
                        perso_copie["vitesse"] = vitesse
                        perso_copie = simuler_saut(perso_copie, lst_blocs, objectif, est_graphique)
                        points_solveur.append(perso_copie["position"])
                else:
                    print("Pas de solution trouvée.")

if __name__ == "__main__":
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
 
    continuer = True
    fichier = menu_selection(LISTE_NIVEAUX)
    meilleurs_score = {}
    

    while continuer:
        fichier = menu_selection(LISTE_NIVEAUX)
        if fichier == "QUITTER" or fichier is None:
            break
        
        chemin = "niveau/" + fichier
        perso, blocs, obj, est_graphique = charger_niveau(chemin)
 
        resultat, nb_sauts = boucle_jeu(perso, blocs, obj, est_graphique,meilleurs_score,fichier)

        if fichier not in meilleurs_score or nb_sauts < meilleurs_score[fichier]:
            meilleurs_score[fichier] = nb_sauts

        if resultat == "QUITTER":
            continuer = False
        elif resultat == "MENU":
            fichier = menu_selection(LISTE_NIVEAUX)
        else:
            continuer = False

    ferme_fenetre()

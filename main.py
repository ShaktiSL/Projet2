from interface import *
from fltk import *
from chargement import *
from solveur import *
from constantes import *
import os


def boucle_jeu(personnage, lst_blocs, objectif, est_graphique, meilleurs_score, fichier):
    """
    Boucle principale d'une partie.
    Retourne ("MENU", nb_sauts) pour revenir au menu, ("QUITTER", 0) pour quitter.
    """
    viseur         = False
    dernier_clic   = (0, 0)
    nb_sauts       = 0
    historique     = [dict(personnage)]
    points_solveur = []

    # MODIFICATION v2 : liste des points de trajectoire cumulés sur toute la partie (persistance)
    # ANCIENNE VERSION : dessiner_trajectoire effaçait et ne gardait que le dernier saut
    points_trajectoire = []

    # Référence à la trajectoire du dernier saut (pour le retour arrière)
    trajectoire_dernier_saut = []

    while True:
        efface_tout()

        if est_graphique:
            image(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2, 'media/fond-jeux.png',
                  largeur=LARGEUR_FENETRE, hauteur=HAUTEUR_FENETRE)

        dessiner_blocs(lst_blocs, est_graphique)
        dessiner_bords(est_graphique)
        dessiner_objectif(objectif, est_graphique)

        # MODIFICATION v2 : redessinage de tous les points accumulés à chaque frame
        # ANCIENNE VERSION : pas de liste persistante, les cercles disparaissaient à efface_tout()
        for (pt_x, pt_y) in points_trajectoire:
            cercle(
                pt_x + LARGEUR_PERSO // 2,
                pt_y + HAUTEUR_PERSO // 2,
                3,
                couleur='black',
                remplissage='white',
                tag='trajectoire'
            )

        dessiner_personnage(personnage, est_graphique)

        for (sol_x, sol_y) in points_solveur:
            cercle(sol_x, sol_y, 8, remplissage='red', tag='solveur')

        if viseur:
            dessiner_fleche(personnage, dernier_clic)

        texte(10, 10, f"Sauts : {nb_sauts}", ancrage='nw', taille=18, couleur='black')
        texte(10, 35, f"Meilleur : {meilleurs_score.get(fichier, '-')}", ancrage='nw', taille=18, couleur='blue')

        pos_x, pos_y = personnage["position"]
        if pos_x < -100 or pos_x > LARGEUR_FENETRE + 100 or pos_y > HAUTEUR_FENETRE + 100:
            if len(historique) > 0:
                etat_sauvegarde        = historique[-1]
                personnage["position"] = etat_sauvegarde["position"]
                personnage["vitesse"]  = (0, 0)
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
                    type_victoire = type_ev(ev_victoire)
                    if type_victoire in ['ClicGauche', 'ClicDroit', 'Touche']:
                        attente_clic = False
                    elif type_victoire == 'Quitte':
                        return "QUITTER", 0
                attente(0.01)

            efface_tout()
            mise_a_jour()
            while donne_ev() is not None:
                pass

            return "MENU", nb_sauts

        evenement = donne_ev()
        if evenement is None:
            continue
        type_evenement = type_ev(evenement)

        if type_evenement == 'Quitte':
            return "QUITTER", 0
        
        # MODIFICATION v4 : Limitation de la liste pour éviter les ralentissements
        if len(points_trajectoire) > 2000:
            points_trajectoire = points_trajectoire[-2000:]

        elif type_evenement == 'ClicGauche':
            dernier_clic = (abscisse(evenement), ordonnee(evenement))
            clic_vers_vitesse(personnage, dernier_clic)
            viseur = True

        elif type_evenement == 'ClicDroit':
            if viseur:
                etat_avant_saut = dict(personnage)
                historique.append(etat_avant_saut)

                trajectoire_saut = simuler(personnage, lst_blocs, objectif, est_graphique)

                # MODIFICATION v3 : sous-échantillonnage de l'animation pour la fluidité.
                # On n'affiche qu'une frame sur PAS_ANIMATION pour éviter que l'animation
                # soit trop lente quand la trajectoire contient beaucoup de points.
                # ANCIENNE VERSION : toutes les positions étaient affichées une par une.
                pas_animation = 6

                for indice_saut in range(len(trajectoire_saut)):
                    position_saut = trajectoire_saut[indice_saut]
                    personnage["position"] = position_saut

                    # On n'affiche qu'une frame sur pas_animation
                    if indice_saut % pas_animation == 0 or indice_saut == len(trajectoire_saut) - 1:
                        efface_tout()
                        if est_graphique:
                            image(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2, 'media/fond-jeux.png',
                                  largeur=LARGEUR_FENETRE, hauteur=HAUTEUR_FENETRE)

                        dessiner_blocs(lst_blocs, est_graphique)
                        dessiner_objectif(objectif, est_graphique)

                        # Points déjà accumulés des sauts précédents
                        for (pt_x, pt_y) in points_trajectoire:
                            cercle(
                                pt_x + LARGEUR_PERSO // 2,
                                pt_y + HAUTEUR_PERSO // 2,
                                3,
                                couleur='black',
                                remplissage='white',
                                tag='trajectoire'
                            )

                        # Points du saut en cours (jusqu'à l'indice courant)
                        for sous_indice in range(0, indice_saut + 1, 5):
                            pt_x, pt_y = trajectoire_saut[sous_indice]
                            cercle(
                                pt_x + LARGEUR_PERSO // 2,
                                pt_y + HAUTEUR_PERSO // 2,
                                3,
                                couleur='black',
                                remplissage='white',
                                tag='trajectoire'
                            )

                        dessiner_personnage(personnage, est_graphique)
                        texte(10, 10, f"Sauts : {nb_sauts + 1}", ancrage='nw', taille=18)
                        mise_a_jour()

                    dehors_x = position_saut[0] < -50 or position_saut[0] > LARGEUR_FENETRE + 50
                    dehors_y = position_saut[1] > HAUTEUR_FENETRE + 50
                    if dehors_x or dehors_y:
                        personnage["position"] = etat_avant_saut["position"]
                        personnage["vitesse"]  = (0, 0)
                        trajectoire_saut       = []
                        break

                # MODIFICATION v2 : accumulation des points dans la liste persistante
                # ANCIENNE VERSION : pas de liste persistante
                for point in trajectoire_saut:
                    points_trajectoire.append(point)

                trajectoire_dernier_saut = trajectoire_saut
                nb_sauts += 1
                viseur = False

        elif type_evenement == 'Touche':
            touche_appuyee = touche(evenement)

            if touche_appuyee == 'Escape':
                return "MENU", nb_sauts

            elif touche_appuyee == 'BackSpace' or touche_appuyee == 'space':
                if len(historique) > 1:
                    historique.pop()
                    etat_precedent = historique[-1]

                    personnage["position"] = etat_precedent["position"]
                    personnage["vitesse"]  = (0, 0)
                    nb_sauts = max(0, nb_sauts - 1)

                    # MODIFICATION v2 : retrait des points du dernier saut de la liste persistante
                    # ANCIENNE VERSION : pas de liste persistante à gérer
                    nb_a_retirer = len(trajectoire_dernier_saut)
                    if nb_a_retirer > 0:
                        points_trajectoire = points_trajectoire[:-nb_a_retirer]
                    trajectoire_dernier_saut = []

                    viseur = False
                    print("Retour en arrière effectué !")
                else:
                    print("Déjà à la position de départ.")

            elif touche_appuyee == 's':
                print("Appel du solveur...")
                solution = resoudre_niveau(personnage, lst_blocs, objectif, est_graphique, pas_v=10, prof_max=8)

                if solution:
                    print(f"Solution trouvée en {len(solution)} sauts : {solution}")
                    points_solveur.clear()
                    perso_copie = {"position": personnage["position"], "vitesse": (0, 0)}
                    for vitesse_solveur in solution:
                        perso_copie["vitesse"] = vitesse_solveur
                        perso_copie = simuler_saut(perso_copie, lst_blocs, objectif, est_graphique)
                        points_solveur.append(perso_copie["position"])
                else:
                    print("Pas de solution trouvée.")


if __name__ == "__main__":
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)

    continuer     = True
    meilleurs_score = {}

    while continuer:
        fichier = menu_selection(LISTE_NIVEAUX)
        if fichier == "QUITTER" or fichier is None:
            break

        chemin = "niveau/" + fichier
        perso, blocs, obj, est_graphique = charger_niveau(chemin)

        resultat, nb_sauts = boucle_jeu(perso, blocs, obj, est_graphique, meilleurs_score, fichier)

        if fichier not in meilleurs_score or nb_sauts < meilleurs_score[fichier]:
            meilleurs_score[fichier] = nb_sauts

        if resultat == "QUITTER":
            continuer = False
        elif resultat == "MENU":
            pass  # la boucle while appellera à nouveau menu_selection
        else:
            continuer = False

    ferme_fenetre()
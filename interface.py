#Shaktinath SOLEIL, David NGALULA KABONGO, Mohamed TAHAR; GROUPE TP11_10
from constantes import *
from fltk import *
import math
#Fichier principalement géré par Shaktinath
NOM_SURFACES = {
    'gray'   : 'Normal',
    'blue'   : 'Glace',
    'brown'  : 'Boue',
    'green'  : 'Élastique',
    'orange' : 'Trampoline',
    'purple' : 'Colle',
}

#Fonction fait par Shaktinath
def dessiner_objectif(objectif, est_graphique):
    """
    Gère l'affichage de l'objectif.
    En mode graphique, l'objectif est invisible.
    objectif : tuple de deux tuples définissant les coordonnées de l'objectif
    est_graphique : bool qui indique le mode (0 formes géométriques, 1 textures)
    """
    if est_graphique:
        pass
    else:
        x1, y1 = objectif[0]
        x2, y2 = objectif[1]
        rectangle(x1, y1, x2, y2, couleur='yellow', remplissage='yellow')

#Fonction fait par Shaktinath
def dessiner_blocs(lst_blocs, est_graphique):
    """
    Gère l'affichage des blocs.
    En mode graphique, les blocs sont invisibles.
    lst_blocs : liste contenant les structures de chaque bloc
    est_graphique : bool
    """
    if est_graphique:
        pass
    else:
        for bloc in lst_blocs:
            if len(bloc) == 3 and isinstance(bloc[0], tuple):
                x1, y1      = bloc[0]
                x2, y2      = bloc[1]
                couleur_bloc = bloc[2]
            else:
                x1, y1, x2, y2 = bloc[0], bloc[1], bloc[2], bloc[3]
                couleur_bloc    = bloc[4] if len(bloc) > 4 else 'gray'
            rectangle(x1, y1, x2, y2, couleur='black', remplissage=couleur_bloc)


#Fonction fait par Shaktinath
def dessiner_personnage(personnage, est_graphique):
    """
    Dessine le personnage.
    personnage : dictionnaire avec la clé 'position'
    est_graphique : bool
    >>> perso1 = {"position": (100, 100)}
    >>> x1, y1 = perso1["position"]
    >>> x1, y1
    (100, 100)
    """
    centre_x, centre_y = personnage["position"]

    if est_graphique:
        image(
            centre_x + LARGEUR_NINJA // 2,
            centre_y + HAUTEUR_NINJA // 2,
            'media/perso_ninja.png',
            largeur=40,
            hauteur=40
        )
    else:
        texte(
            centre_x + LARGEUR_PERSO // 2,
            centre_y + HAUTEUR_PERSO // 2,
            "🐑",
            ancrage='center',
            taille=18,
            tag='perso'
        )

#Fonction fait par Shaktinath
def dessiner_fleche(personnage, clic):
    """
    Dessine une vraie flèche rouge indiquant la direction et l'intensité du saut.
    personnage : dictionnaire avec la clé 'position'
    clic : tuple (x, y) des coordonnées du curseur au moment du clic gauche
    """
    efface('prevision')

    centre_x = personnage["position"][0] + LARGEUR_PERSO / 2
    centre_y = personnage["position"][1] + HAUTEUR_PERSO / 2

    clic_x, clic_y = clic
    direction_x    = clic_x - centre_x
    direction_y    = clic_y - centre_y
    longueur       = math.sqrt(direction_x**2 + direction_y**2)

    if longueur == 0:
        return
    
    bout_x = clic_x
    bout_y = clic_y

    fleche(centre_x, centre_y, bout_x, bout_y, couleur='red', epaisseur=3, tag='prevision')



#Petite modification réalisée par David
def dessiner_trajectoire(trajectoire):
    """
    Dessine les points de trajectoire du saut en cours.
    trajectoire : liste de positions (x, y)
    """

    pas_affichage = 5

    for rang in range(0, len(trajectoire), pas_affichage):
        pos_x, pos_y = trajectoire[rang]
        cercle(
            pos_x + LARGEUR_PERSO // 2,
            pos_y + HAUTEUR_PERSO // 2,
            3,
            couleur='black',
            remplissage='white',
            tag='trajectoire'
        )


#Fonction réalisée par David
def dessiner_bords(est_graphique):
    """Dessine le contour de la fenêtre (mode géométrique seulement)."""
    if not est_graphique:
        epaisseur_bord = 3
        rectangle(0, 0, LARGEUR_FENETRE, HAUTEUR_FENETRE,
                  couleur='black', remplissage='', epaisseur=epaisseur_bord)

#Fonction fait par Shaktinath
def afficher_victoire():
    """Affiche le message de victoire."""
    milieu_x = LARGEUR_FENETRE // 2
    milieu_y  = HAUTEUR_FENETRE // 2

    rectangle(milieu_x - 200, milieu_y - 50,
              milieu_x + 200, milieu_y + 50,
              couleur='black', remplissage='white',
              epaisseur=3, tag='ecran_fin')
    texte(milieu_x, milieu_y, "VICTOIRE !", ancrage='center',
          taille=40, couleur='green', tag='ecran_fin')
    texte(milieu_x, milieu_y + 35, "Cliquez pour continuer",
          ancrage='center', taille=12,
          couleur='black', tag='ecran_fin')
    mise_a_jour()

#Fonction fait par Shaktinath
def menu_selection(liste_niveaux):
    """
    Affiche les niveaux centrés et renvoie le chemin du fichier choisi.
    liste_niveaux : liste des différents niveaux.
    """
    x_min = (LARGEUR_FENETRE // 2) - (LARGEUR_BOUTON // 2)
    x_max = (LARGEUR_FENETRE // 2) + (LARGEUR_BOUTON // 2)
    selection = None

    while selection is None:
        efface_tout()
        texte(LARGEUR_FENETRE // 2, 50, "Menu des niveaux",
              ancrage='center', taille=30, couleur='darkblue')

        for rang, nom in enumerate(liste_niveaux):
            y_min = 150 + (rang * 80)
            y_max = 210 + (rang * 80)
            rectangle(x_min, y_min, x_max, y_max, couleur='black', remplissage='lightgray')
            texte(LARGEUR_FENETRE // 2, (y_min + y_max) // 2, nom, ancrage='center', taille=16)


        decalage_legende = 0
        for couleur_surface, nom_surface in NOM_SURFACES.items():
            rectangle(x_min, 450 + decalage_legende, x_min + 20, 470 + decalage_legende,
                      couleur='black', remplissage=couleur_surface)
            texte(x_min + 30, 460 + decalage_legende, nom_surface,
                  ancrage='w', taille=13, couleur='black')
            decalage_legende += 25

        mise_a_jour()
        evenement = donne_ev()

        if evenement is not None:
            type_evenement = type_ev(evenement)

            if type_evenement == 'ClicGauche':
                clic_x, clic_y = abscisse(evenement), ordonnee(evenement)
                for rang, nom in enumerate(liste_niveaux):
                    y_min = 150 + (rang * 80)
                    y_max = 210 + (rang * 80)
                    if x_min <= clic_x <= x_max and y_min <= clic_y <= y_max:
                        selection = nom

            elif type_evenement == 'Quitte':
                return "QUITTER"

    return selection


if __name__ == "__main__":
    from doctest import testmod
    testmod()
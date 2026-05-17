#Shaktinath SOLEIL, David NGALULA KABONGO, Mohamed TAHAR; GROUPE TP11_10
from constantes import *
from fltk import *
import math

def dessiner_objectif(objectif, est_graphique):
    """
    Gère l'affichage de l'objectif.
    En mode graphique, l'objectif est invisible
    objectif : tuple de deux tuples définissant les coordonnées de l'objectif
    est_graphique : bool qui indique le mode( 0 pour les formes géométrique, 1 pour les texture)
    """
    if est_graphique:
        pass
    else:
        x1, y1 = objectif[0]
        x2, y2 = objectif[1]
        rectangle(x1, y1, x2, y2, couleur='yellow', remplissage='yellow')


def dessiner_blocs(lst_blocs, est_graphique):
    """
    Gère l'affichage des blocs. 
    En mode graphique, les blocs sont invisibles.
    lst_blocs : Liste contenant les structures de chaque bloc
    est_graphique : bool qui indique le mode( 0 pour les formes géométrique, 1 pour les texture)
    """
    if est_graphique:
        pass
    else:
        for bloc in lst_blocs:
            if len(bloc) == 3 and isinstance(bloc[0], tuple):
                x1, y1 = bloc[0]
                x2, y2 = bloc[1]
                couleur_bloc = bloc[2]
            else:
                x1, y1, x2, y2 = bloc[0], bloc[1], bloc[2], bloc[3]
                couleur_bloc = bloc[4] if len(bloc) > 4 else 'gray'
            rectangle(x1, y1, x2, y2, couleur=couleur_bloc, remplissage=couleur_bloc)

def dessiner_personnage(personnage, est_graphique):
    """
    Dessine le personnage dans une couleur.
    personnage : dictionnaire avec la clé 'position'
    est_graphique : bool qui indique le mode( 0 pour les formes géométrique, 1 pour les texture)
    >>> perso1 = {"position": (100, 100)}
    >>> LARGEUR_TEST, HAUTEUR_TEST = 20, 20
    >>> x1, y1 = perso1["position"]
    >>> x2, y2 = x1 + LARGEUR_TEST, y1 + HAUTEUR_TEST
    >>> x1, y1, x2, y2
    (100, 100, 120, 120)
    """
    perso_x1, perso_y1 = personnage["position"]
    perso_x2 = perso_x1 + LARGEUR_PERSO
    perso_y2 = perso_y1 + HAUTEUR_PERSO
    
    if est_graphique :
        image(perso_x1 + LARGEUR_NINJA // 2, perso_y1 + HAUTEUR_NINJA // 2, 'media/perso_ninja.png', largeur = 40, hauteur = 40)
    else :
        rectangle(perso_x1, perso_y1, perso_x2, perso_y2, couleur='black', remplissage='white', tag='perso')
        cercle(perso_x1 + 15, perso_y1 + 10, 5, remplissage='pink')


def dessiner_fleche(personnage, clic):
    """
    Dessine une flèche rouge indiquant la direction et l'intensité du saut.
    personnage : dictionnaire avec la clé 'position'
    clic : Coordonnées (x, y) sous forme de tuple du curseur de la souris lors du ClicGauche.
    """
    efface('prevision')
    perso_x, perso_y = personnage["position"]
    start_x = perso_x + LARGEUR_PERSO / 2
    start_y = perso_y + HAUTEUR_PERSO / 2

    clic_x, clic_y = clic
    vecteur_x = clic_x - start_x
    vecteur_y = clic_y - start_y
    distance = math.sqrt(vecteur_x**2 + vecteur_y**2)

    if distance > VMAX:
        ratio = VMAX / distance
        end_x = start_x + vecteur_x * ratio
        end_y = start_y + vecteur_y * ratio
    else:
        end_x = clic_x
        end_y = clic_y
    fleche(start_x, start_y, end_x, end_y, couleur='red', epaisseur=3, tag='prevision')

def dessiner_trajectoire(trajectoire):
    """
    Dessine tous les points de la trajectoire du dernier saut.
    trajectoire : liste de positions (x, y)
    """
    efface('trajectoire')
    for (x, y) in trajectoire:
        cercle(x + LARGEUR_PERSO // 2, y + HAUTEUR_PERSO // 2, 2,
               remplissage='white', tag='trajectoire')



def afficher_victoire():
    """Affiche le message de victoire."""
    milieu_x = LARGEUR_FENETRE // 2
    milieu_y = HAUTEUR_FENETRE // 2

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
        texte(LARGEUR_FENETRE // 2, 50, "Menu des niveaux", ancrage='center', taille=30, couleur='darkblue')

        for i, nom in enumerate(liste_niveaux):
            y_min = 150 + (i * 80) 
            y_max = 210 + (i * 80)
            rectangle(x_min, y_min, x_max, y_max, couleur='black', remplissage='lightgray')
            texte(LARGEUR_FENETRE // 2, (y_min + y_max) // 2, nom, ancrage='center', taille=16)
        mise_a_jour()
        ev = donne_ev()
        if ev is not None : 
            tev = type_ev(ev)

            if tev == 'ClicGauche':
                x, y = abscisse(ev), ordonnee(ev)
                for i, nom in enumerate(liste_niveaux):
                    y_min = 150 + (i * 80)
                    y_max = 210 + (i * 80)
                    if x_min <= x <= x_max and y_min <= y <= y_max:
                        selection = nom

            elif tev == 'Quitte': 
                return "QUITTER"

    return selection

    
if __name__ == "__main__":
    from doctest import testmod
    testmod()
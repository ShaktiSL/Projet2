from constantes import *
from fltk import *
import math

def dessiner_objectif(objectif, est_graphique):
    """
    Dessine l'objectif sous forme d'un rectangle rouge.
    objectif : tuple de deux coins ((x1, y1), (x2, y2))
    >>> obj_test = ((10, 10), (50, 50))
    >>> (x1, y1), (x2, y2) = obj_test
    >>> x1, y1, x2, y2
    (10, 10, 50, 50)
    """
    (objectif_x1, objectif_y1), (objectif_x2, objectif_y2) = objectif
    if est_graphique :
        milieu_x = (objectif_x1 + objectif_x2) // 2
        milieu_y = (objectif_y1 + objectif_y2) // 2
        image(milieu_x, milieu_y, 'media/coffre.png', largeur = 140, hauteur = 90, tag='objectif')
    else :
        rectangle(objectif_x1, objectif_y1, objectif_x2, objectif_y2, couleur='red', remplissage='red', tag='objectif')


def dessiner_blocs(lst_blocs, est_graphique):
    """
    Dessine chaque bloc comme un rectangle coloré.
    lst_blocs : liste de tuples ((x1, y1), (x2, y2))
    >>> blocs = [((0, 0), (20, 20)), ((100, 100), (120, 120))]
    >>> len(blocs)
    2
    >>> blocs[0][1]
    (20, 20)
    """
    for bloc in lst_blocs:
        if est_graphique :
            pass
        else:
            (bloc_x1, bloc_y1), (bloc_x2, bloc_y2), couleur_bloc = bloc
            rectangle(bloc_x1, bloc_y1, bloc_x2, bloc_y2, couleur = 'black', remplissage = couleur_bloc, tag='bloc')

def dessiner_personnage(personnage, est_graphique):
    """
    Dessine le personnage dans une couleur.
    personnage : dictionnaire avec la clé 'position'
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
    """
    Affiche le message de victoire.
    """
    milieu_x = LARGEUR_FENETRE // 2
    milieu_y = HAUTEUR_FENETRE // 2
    rectangle(milieu_x - 200, milieu_y - 50, milieu_x + 200, milieu_y + 50, couleur='black', remplissage='white', epaisseur=3, tag='ecran_fin')
    texte(milieu_x, milieu_y, "VICTOIRE !", ancrage='center', taille=40, couleur='green', tag='ecran_fin')
    texte(milieu_x, milieu_y + 35, "Cliquez pour continuer", ancrage='center', taille=12, couleur='black', tag='ecran_fin')
    
    mise_a_jour()

    attente_clic = True
    while attente_clic:
        ev = donne_ev()
        tev = type_ev(ev)
        
        if tev in ['ClicGauche', 'ClicDroit', 'Touche', 'Quitte']:
            attente_clic = False
    efface('ecran_fin')
    while donne_ev() is not None: pass


def menu_selection(liste_niveaux):
    """
    Affiche les niveaux centrés et renvoie le chemin du fichier choisi.
    liste_niveaux : liste des différents niveaux
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
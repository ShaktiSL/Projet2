from fltk import *
from constantes_interphace import *

def menu_selection(liste_niveaux):
    """
    Affiche les niveaux centrés et renvoie le chemin du fichier choisi.
    liste_niveaux : liste des différents niveaux
    """
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
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
        tev = type_ev(ev)

        if tev == 'ClicGauche':
            x, y = abscisse(ev), ordonnee(ev)
            for i, nom in enumerate(liste_niveaux):
                y_min = 150 + (i * 80)
                y_max = 210 + (i * 80)
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    selection = nom

        elif tev == 'Quitte':
            ferme_fenetre()
            return None

    ferme_fenetre()
    return selection

if __name__ == "__main__":
    choix = menu_selection(LISTE_NIVEAUX)
    if choix:
        print(f"Lancement de : {choix}")
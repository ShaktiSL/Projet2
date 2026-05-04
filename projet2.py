# Dossier Interface 

# ===================================================================
#                       Fichier : affichage.py
# ===================================================================

from interface.fltk import *
from constantes import *

def dessiner_objectif(objectif):
    """
    Dessine l'objectif sous forme d'un rectangle rouge.
    objectif : tuple de deux coins ((x1, y1), (x2, y2))
    >>> obj_test = ((10, 10), (50, 50))
    >>> (x1, y1), (x2, y2) = obj_test
    >>> x1, y1, x2, y2
    (10, 10, 50, 50)
    """
    (objectif_x1, objectif_y1), (objectif_x2, objectif_y2) = objectif
    rectangle(objectif_x1, objectif_y1, objectif_x2, objectif_y2, couleur='red', remplissage='red', tag='objectif')


def dessiner_blocs(lst_blocs):
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
        (bloc_x1, bloc_y1), (bloc_x2, bloc_y2) = bloc
        rectangle(bloc_x1, bloc_y1, bloc_x2, bloc_y2, couleur='black', remplissage='gray', tag='bloc')

def dessiner_personnage(personnage):
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
    
    rectangle(perso_x1, perso_y1, perso_x2, perso_y2, couleur='black', remplissage='white', tag='perso')
    cercle(perso_x1 + 15, perso_y1 + 10, 5, remplissage='pink')

    
if __name__ == "__main__":
    from doctest import testmod
    testmod()

# ===================================================================
#                       Fichier : fleche.py
# ===================================================================

from interface.fltk import *
from constantes import *
import math
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


# ===================================================================
#                       Fichier : menu.py
# ===================================================================

from interface.fltk import *
from constantes import *

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
                return "QUIITER_TOTAL"

    return selection

if __name__ == "__main__":
    from doctest import testmod
    testmod() 

# ===================================================================
#                       Fichier : fltk.py
# je te le fournis directement pour eviter les erreurs 
# ===================================================================

# Dossier niveau 

# ===================================================================
#                       Fichier : clic_vers_vitesse.py
# ===================================================================
from constantes import *
from niveau.victoire import *
from niveau.creer_perso import *
import math

def clic_vers_vitesse(personnage, clic):
    """
    La fonction met à jour la vitesse du personnage par le clic de l'utilisateur.
    personnage : dictionnaire (position, vitesse)
    clic : tuple (x, y) des coordonnées du clics.
    >>> perso1 = {"position": (100, 100), "vitesse": (0, 0)}
    >>> clic1 = (130, 140)
    >>> clic_vers_vitesse(perso1, clic1)
    >>> perso1["vitesse"]
    (30.0, 40.0)
    >>> perso2 = {"position": (0, 0), "vitesse": (0, 0)}
    >>> clic2 = (300, 400)
    >>> clic_vers_vitesse(perso2, clic2)
    >>> perso2["vitesse"]
    (30.0, 40.0)
    """

    perso_x, perso_y = personnage["position"]
    clic_x, clic_y = clic
    vecteur_x = float(clic_x - perso_x)
    vecteur_y = float(clic_y - perso_y)
    norme = math.sqrt(vecteur_x**2 + vecteur_y**2)

    if norme == 0:
        personnage["vitesse"] = (0.0, 0.0)
        return
    
    if norme > VMAX : 
        coef = VMAX / norme
        vecteur_x = vecteur_x * coef
        vecteur_y = vecteur_y * coef
    
    personnage["vitesse"] = (vecteur_x, vecteur_y)

if __name__ == "__main__":
    from doctest import testmod
    testmod()

# ===================================================================
#                       Fichier : collision.py
# ===================================================================
from constantes import *
from niveau.creer_perso import *
from niveau.victoire import *

def collision(personnage, lst_blocs):
    """
    La fonction renvoie le bloc ayant eu un contact avec le personnage et None sinon.
    personnage : dictionnaire (position, vitesse)
    lst_blocs = liste de blocs ((x1,y1), (x2, y2))
    >>> perso1 = {"position": (260, 140), "vitesse": (0, 0)}
    >>> lst_bloc = [((105, 150), (300, 170))]
    >>> collision(perso1, lst_bloc)
    ((105, 150), (300, 170))
    """
    perso_x1, perso_y1 = personnage["position"]
    perso_x2 = perso_x1 + LARGEUR_PERSO
    perso_y2 = perso_y1 + HAUTEUR_PERSO

    for bloc in lst_blocs : 
        (bloc_x1, bloc_y1), (bloc_x2, bloc_y2) = bloc
        if perso_x2 > bloc_x1 and perso_x1 < bloc_x2 and perso_y2 > bloc_y1 and perso_y1 < bloc_y2 :
            return bloc
    return None


if __name__ == "__main__":
    from doctest import testmod
    testmod()


# ===================================================================
#                       Fichier : creer_perso.py
# ===================================================================
def creer_perso(x,y):
    """
    La fonction crée le personnage avec une vitesse de départ toujours à (0,0)
    x, y : position de départ
    Renvoie un dictionnaire contenant sa postion et sa vitesse.

    >>> creer_perso(500, 750)
    {'position': (500, 750), 'vitesse': (0, 0)}
    """
    return {"position" : (x,y), "vitesse" : (0,0)}

if __name__ == "__main__":
    from doctest import testmod
    testmod()

# ===================================================================
#                       Fichier : fichier_valeur_test a supprimer.txt
# Fichier : niveau1.txt
# Fichier : niveau2.txt
# Fichier : niveau3.txt
# les different fichier text pour tester le lancement.
# ===================================================================


# ===================================================================
#                       Fichier : niveaux.py
# ===================================================================
def lire_perso(lignes):
    ligne = lignes[0].split('#')[0].strip()
    parts = ligne.split(',')
    return {"position": (int(parts[0]), int(parts[1])), "vitesse": (0, 0)}

def lire_objectif(lignes):
    ligne = lignes[1].split('#')[0].strip()
    coords = ligne.split(',')
    return ((int(coords[0]), int(coords[1])), (int(coords[2]), int(coords[3])))

def lire_blocs(lignes):
    """
    Lit toutes les lignes à partir de la 3ème pour créer la liste de blocs.
    """
    lst_blocs = []
    for ligne in lignes[2:]:
        propre = ligne.split('#')[0].strip()
        points = propre.split(',')
        bloc = ((int(points[0]), int(points[1])), (int(points[2]), int(points[3])))
        lst_blocs.append(bloc)
    return lst_blocs

def charger_niveau(fichier):
    """
    Lit le fichier et renvoie (personnage, lst_blocs, objectif).
    """
    with open(fichier, 'r', encoding='utf-8') as f:
        lignes = f.readlines()
    
    perso = lire_perso(lignes)
    objectif = lire_objectif(lignes)
    blocs = lire_blocs(lignes)
    
    return perso, blocs, objectif
# ===================================================================
#                       Fichier : physique.py
# ===================================================================
from constantes import *
from niveau.collision import *




def deplacer(personnage, gravite, pas):
    x, y = personnage["position"]
    vx, vy = personnage["vitesse"]
    gx, gy = gravite

    # nouvelle position
    x = x + pas * vx
    y = y + pas * vy

    # nouvelle vitesse
    vx = vx + pas * gx
    vy = vy + pas * gy

    personnage["position"] = (x,y)
    personnage["vitesse"] = (vx, vy)


#p = {"position": (100, 100), "vitesse": (5, -10)}
#deplacer(p, (0, 1), 1)
#print(p["position"])
#print(p["vitesse"])



def placer_bord(personnage, bloc, cote):
    """
    Replace le personnage juste à l'extérieur du bloc, contre le bord indiqué.

    personnage : dictionnaire {"position": (x, y), "vitesse": (vx, vy)}
    bloc       : tuple ((x1, y1), (x2, y2))
    cote       : chaîne parmi "haut", "bas", "gauche", "droite"

    >>> p = {"position": (50, 98), "vitesse": (0, 5)}
    >>> placer_bord(p, ((0, 100), (200, 200)), "haut")
    >>> p["position"]
    (50, 80)
    """
    x, y = personnage["position"]
    (bloc_x1, bloc_y1), (bloc_x2, bloc_y2) = bloc

    if cote == "haut":
        y = bloc_y1 - HAUTEUR_PERSO
    elif cote == "bas":
        y = bloc_y2
    elif cote == "gauche":
        x = bloc_x1 - LARGEUR_PERSO
    elif cote == "droite":
        x = bloc_x2

    personnage["position"] = (x, y)

p = {"position": (50, 98), "vitesse": (0, 5)}
placer_bord(p, ((0, 100), (200, 200)), "haut")
print(p["position"])


def detecter_cote(personnage, bloc, vitesse):
    """
    Détermine par quel côté du bloc le personnage est entré en collision,
    en fonction de la direction de sa vitesse.
    Retourne "haut", "bas", "gauche" ou "droite".

    personnage : dictionnaire {"position": (x, y), "vitesse": (vx, vy)}
    bloc       : tuple ((x1, y1), (x2, y2))
    vitesse    : tuple (vx, vy) — la vitesse au moment du choc

    >>> p = {"position": (50, 95), "vitesse": (0, 5)}
    >>> detecter_cote(p, ((0, 100), (200, 200)), (0, 5))
    'haut'
    >>> p2 = {"position": (50, 205), "vitesse": (0, -5)}
    >>> detecter_cote(p2, ((0, 100), (200, 200)), (0, -5))
    'bas'
    """
    x, y = personnage["position"]
    vx, vy = vitesse
    (bloc_x1, bloc_y1), (bloc_x2, bloc_y2) = bloc

    if vy != 0 and vx == 0:
        if vy > 0:
            return "haut"
        else:
            return "bas"

    elif vx != 0 and vy == 0:
        if vx > 0:
            return "gauche"
        else:
            return "droite"

    else:  # diagonale : on compare les distances aux bords
        dist_vertical   = abs(y - bloc_y1)
        dist_horizontal = abs(x - bloc_x1)

        if dist_vertical <= dist_horizontal:
            if vy > 0:
                return "haut"
            else:
                return "bas"
        else:
            if vx > 0:
                return "gauche"
            else:
                return "droite"
    




def choc_mou(personnage, bloc):

    vx, vy = personnage["vitesse"]
    cote = detecter_cote(personnage, bloc, (vx, vy))
    placer_bord(personnage, bloc, cote)
    personnage["vitesse"] = (0, 0)
    




def choc(personnage, lst_blocs):
    """
    Orchestre la gestion d'une collision :
    trouve le bloc touché avec collision(), puis appelle choc_mou().
    Ne fait rien si le personnage n'est en collision avec aucun bloc.

    personnage : dictionnaire {"position": (x, y), "vitesse": (vx, vy)}
    lst_blocs  : liste de blocs ((x1, y1), (x2, y2))
    """
    # À compléter
    # Rappel : collision() vient de niveau.py (Dev A)
    bloc_touche = collision(personnage, lst_blocs)

    if bloc_touche is not None : 
        choc_mou(personnage, bloc_touche)



def pas(personnage, lst_blocs):
    # 1. On mémorise la position exacte avant le mouvement
    ancienne_pos = personnage["position"]
    
    deplacer(personnage, GRAVITE, PAS)
    choc(personnage, lst_blocs)

    # 2. On récupère la vitesse après le choc
    vx, vy = personnage["vitesse"]

    # CONDITION D'ARRÊT (Le secret pour ne plus freezer) :
    # Si la vitesse est (0,0) OU si la position n'a pas changé (bloqué contre un mur/sol)
    if (vx == 0 and vy == 0) or (personnage["position"] == ancienne_pos):
        return True 
    
    return False

# ===================================================================
#                       Fichier : victoire.py
# ===================================================================
from constantes import *
from niveau.creer_perso import *
from interface.fltk import *

def victoire(personnage, objectif):
    """
    La fonction renvoie True si le personnage a atteint l'objectif et False sinon.
    personnage : dictionnaire (position, vitesse)
    objectif : tuple de deux coins ((x1,y1), (x2, y2))

    >>> objectif1 = ((250,100), (270, 170))
    >>> perso1 = {"position": (260, 140), "vitesse": (0, 0)}
    >>> victoire(perso1, objectif1)
    True

    >>> perso2 = {"position": (230, 90), "vitesse": (0, 0)}
    >>> victoire(perso2, objectif1)
    False
    """
    perso_x1, perso_y1 = personnage["position"]
    perso_x2 = perso_x1 + LARGEUR_PERSO
    perso_y2 = perso_y1 + HAUTEUR_PERSO

    (objectif_x1, objectif_y1), (objectif_x2, objectif_y2) = objectif

    if perso_x2 > objectif_x1 and perso_x1 < objectif_x2 and perso_y2 > objectif_y1 and perso_y1 < objectif_y2 :
        return True
    return False

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

if __name__ == "__main__":
    from doctest import testmod
    testmod()


# Dossier Solveur 

# ===================================================================
#                       Fichier : __init__.py
# ===================================================================

# ===================================================================
#                       Fichier : generer_vitesse.py
# ===================================================================
from constantes import *

def generer_vitesses(pas_v):
    """Génère tous les sauts possibles.

    >>> vits = generer_vitesses(50)
    >>> (0, 0) in vits
    False
    >>> len(vits) > 0
    True
    """
    vitesses = []
    for vx in range(-VMAX, VMAX + 1, pas_v):
        for vy in range(-VMAX, VMAX + 1, pas_v):
            if vx != 0 or vy != 0:
                vitesses.append((vx, vy))
    return vitesses

# ===================================================================
#                       Fichier : position_approx.py
# ===================================================================
def position_approx(personnage, taille_grille):
    """Arrondit la position pour la mémoire du solveur.
    
    >>> perso = {"position": (107.8, 203.1)}
    >>> position_approx(perso, 10)
    (10, 20)
    >>> position_approx(perso, 50)
    (2, 4)
    """
    x, y = personnage["position"]
    return (int(x // taille_grille), int(y // taille_grille))
# ===================================================================
#                       Fichier : simuler_saut.py
# ===================================================================
from niveau.physique import *
from interface.affichage import *


def simuler_saut(personnage, blocs, objectif):
    en_mouvement = True
    compteur = 0
    
    print("Simulation en cours...") 

    while en_mouvement:
        if pas(personnage, blocs): 
            en_mouvement = False
        
        # --- ESSENTIEL POUR L'AFFICHAGE ---
        efface_tout()
        dessiner_blocs(blocs)
        dessiner_objectif(objectif)
        dessiner_personnage(personnage)
        mise_a_jour()
        
        # --- ESSENTIEL POUR NE PAS FREEZER ---
        donne_ev()    # Traite les événements système (Windows/Mac)
        attente(5)   # Laisse respirer le processeur
            
        compteur += 1
        # Sécurité : Si le saut dure plus de 5 secondes (500 * 10ms), on force l'arrêt
        if compteur > 500:
            print("Sécurité : Saut trop long, arrêt forcé.")
            en_mouvement = False
        
        x, y = personnage["position"]
        
        # Sécurité : Si le perso sort trop loin par le haut ou les côtés
        if y < -500 or x < -100 or x > LARGEUR_FENETRE + 100:
            print("Le personnage est perdu dans l'espace, retour au calme.")
            personnage["vitesse"] = (0, 0) # On stoppe sa course
            en_mouvement = False

    print("Fin de simulation.")
# ===================================================================
#                       Fichier : solveur.py
# ===================================================================
from niveau.victoire import *
from solveur.position_approx import *
from solveur.simuler_saut import *
from solveur.generer_vitesse import *

def resoudre(personnage, blocs, objectif, liste_vitesses, deja_explore, prof_max):
    # 1. On vérifie si on a gagné
    if victoire(personnage, objectif):
        return []

    # 2. On vérifie si on doit s'arrêter
    if prof_max <= 0:
        return None
    
    # 3. On vérifie si on est déjà passé par là
    position_grille = position_approx(personnage, 10)
    if position_grille in deja_explore:
        return None
    deja_explore.add(position_grille)
    
    # 4. On teste les sauts
    for vitesse in liste_vitesses:
        nouv_perso = simuler_saut(personnage, vitesse, blocs)
        
        chemin = resoudre(nouv_perso, blocs, objectif, liste_vitesses, deja_explore, prof_max - 1)
        
        if chemin is not None:
            return [vitesse] + chemin
            
    return None

def resoudre_niveau(personnage, blocs, objectif, pas_v, prof_max):
    """La fonction finale à appeler."""
    vitesses = generer_vitesses(pas_v)
    return resoudre(personnage, blocs, objectif, vitesses, set(), prof_max)

# Ce qui ne sont dans aucun dossier

# ===================================================================
#                       Fichier : constantes.py
# ===================================================================
LISTE_NIVEAUX = ["niveau1.txt", "niveau2.txt", "niveau3.txt"]
LARGEUR_FENETRE = 1500
HAUTEUR_FENETRE = 700
LARGEUR_BOUTON = 300
LARGEUR_PERSO = 20
HAUTEUR_PERSO = 20

LARGEUR_PERSO = 20
HAUTEUR_PERSO = 20
GRAVITE = (0, 1)  # Doit être un tuple de EXACTEMENT deux nombres
PAS = 1.2          # Doit être un seul nombre
VMAX = 30     # Puissance du saut


# ===================================================================
#                       Fichier : main.py
# ===================================================================
from interface.fltk import cree_fenetre, ferme_fenetre
from interface.menu import menu_selection
from niveau.niveaux import charger_niveau
from sautemouton import boucle_jeu
from constantes import *

if __name__ == "__main__":
    # On ouvre la fenêtre ICI et nulle part ailleurs
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    
    continuer = True
    while continuer:
        fichier = menu_selection(LISTE_NIVEAUX)
        
        if fichier is None: # Si on ferme le menu
            break
            
        chemin = "niveau/" + fichier
        perso, blocs, obj = charger_niveau(chemin)
        
        # Lance la boucle de jeu
        resultat = boucle_jeu(perso, blocs, obj)
        
        if resultat == "QUITTER_TOTAL":
            continuer = False

    ferme_fenetre()
# ===================================================================
#                       Fichier : run_doctest a supprimer.py
# ===================================================================
import doctest
import importlib.util
import sys
from pathlib import Path

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def run_file(path):
    spec = importlib.util.spec_from_file_location("mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    result = doctest.testmod(mod, verbose=False)

    if result.failed == 0:
        print(f"{GREEN}✔ PASS{RESET} {path}")
    else:
        print(f"{RED}✘ FAIL ({result.failed} failures){RESET} {path}")

if __name__ == "__main__":
    for file in sys.argv[1:]:
        run_file(file)

# ===================================================================
#                       Fichier : sautemouton.py
# ===================================================================
from interface.fltk import *
from constantes import *
from interface.affichage import *
from interface.menu import *
from interface.fleche import *
from niveau.physique import *
from niveau.collision import *
from niveau.victoire import *
from niveau.clic_vers_vitesse import *
from solveur.simuler_saut import *

def boucle_jeu(personnage, lst_blocs, objectif):
    # SUPPRIME cree_fenetre d'ici !
    viseur = False
    dernier_clic = (0, 0)

    while True:
        efface_tout()
        dessiner_blocs(lst_blocs)
        dessiner_objectif(objectif)
        dessiner_personnage(personnage)
        if viseur:
            dessiner_fleche(personnage, dernier_clic)
        mise_a_jour()

        if victoire(personnage, objectif):
            afficher_victoire()
            return "MENU" # On retourne au menu

        ev = donne_ev()
        if ev is not None:
            tev = type_ev(ev)
            if tev == 'Quitte':
                return "QUITTER_TOTAL"
            elif tev == 'ClicGauche':
                dernier_clic = (abscisse(ev), ordonnee(ev))
                # 2. On calcule la vitesse (ton calcul VMAX est bon)
                clic_vers_vitesse(personnage, dernier_clic)
                # 3. ON ACTIVE LE VISEUR
                viseur = True 
                print("Visée activée à :", dernier_clic)
            elif tev == 'ClicDroit':
                print("Clic droit reçu. État viseur :", viseur)
                if viseur:
                    # 4. On lance la simulation animée
                    simuler_saut(personnage, lst_blocs, objectif)
                    # 5. On désactive le viseur SEULEMENT après le saut
                    viseur = False
                else:
                    print("Action refusée : Vous devez d'abord viser avec le Clic Gauche !")
            elif tev == 'Touche' and touche(ev) == 'Escape':
                return "MENU"
# ===================================================================
#                       Fichier : test_global(M) a supprimer.py
# ===================================================================
from constantes import PAS
from solveur.solveur import resoudre_niveau

# 1. On crée un décor minimaliste
# Un sol de (0, 300) à (500, 400)
blocs = [((0, 300), (500, 400))]

# L'objectif est un petit carré posé sur le sol à droite
objectif = ((400, 250), (450, 300))

# 2. On crée un personnage au début du sol
perso = {"position": (50, 250), "vitesse": (0, 0)}

print("--- RECHERCHE DE SOLUTION ---")
# On lance le solveur : 
# pas_v = 25 (on teste par paliers de 25)
# prof_max = 3 (il a le droit à 3 sauts max)
solution = resoudre_niveau(perso, blocs, objectif, 50, 2)

if solution is None:
    print("❌ Le solveur n'a pas trouvé de chemin. (Vérifie la position de l'objectif)")
else:
    print("✅ SOLUTION TROUVÉE !")
    print(f"Pour gagner, fais ces sauts : {solution}")
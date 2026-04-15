# Saute Mouton

Projet de programmation L1 Info & Maths 2025-2026 — Université Gustave Eiffel.

L'objectif est d'implémenter un jeu de puzzle en 2D où un personnage doit atteindre un objectif
en effectuant le moins de sauts possible. Le jeu simule la physique des sauts (gravité, collisions)
et propose un algorithme capable de résoudre les niveaux automatiquement.

---

## Lancer le jeu

```bash
python3 sautemouton.py
```

---

## Organisation de l'équipe

Le projet est réalisé en trinôme. Chaque membre a un domaine principal, mais tout le monde
doit pouvoir expliquer l'ensemble du code à la soutenance.

- **Dev A** : Shaktinath SOLEIL — structures de données et interface graphique
- **Dev B** — chargement des niveaux et solveur
- **Dev C** — moteur physique et tests

---

## Structure des fichiers

```
sautemouton.py      # point d'entrée, boucle principale du jeu
niveau.py           # structures de données et chargement des fichiers niveaux
physique.py         # simulation physique : sauts, gravité, collisions
interface.py        # affichage FLTK, menus, gestion des clics
solveur.py          # algorithme de résolution automatique
niveaux/
    niveau1.txt     # fichiers décrivant les niveaux
    niveau2.txt
tests/
    test_niveau.py
    test_physique.py
    test_solveur.py
rapport.pdf
README.md
```

---

## Format d'un fichier niveau

Chaque niveau est un fichier texte avec ce format :

```
178,358              # position de départ du personnage (x, y)
263,173,295,208      # objectif : coin supérieur gauche puis coin inférieur droit
0,0,22,399           # bloc 1 (mur gauche)
0,376,339,399        # bloc 2 (sol)
325,49,339,399       # bloc 3 (mur droit)
70,337,127,349       # bloc 4
```

Les commentaires après `#` sont ignorés à la lecture.

---

## Planification

Le projet est découpé en 3 sprints d'une semaine.

---

### Sprint 1 — Structures de données, chargement des niveaux, moteur physique

C'est la semaine la plus importante : on pose toutes les fondations sur lesquelles le reste va
s'appuyer. Les trois développeurs travaillent en parallèle sur des parties indépendantes.

---

#### Dev A — Structures de données (`niveau.py`)

L'objectif est de définir comment le jeu représente ses objets en mémoire, et d'écrire
les fonctions de base pour les manipuler.

**1.1 — Définir le dictionnaire `personnage`**

Le personnage est un dictionnaire Python avec au minimum deux clés : sa position et sa vitesse.
On définit aussi les constantes `LARGEUR` et `HAUTEUR` qui représentent la taille du personnage
en pixels.

```python
personnage = {
    "position": (500, 750),
    "vitesse": (0, 0)
}
LARGEUR = 20
HAUTEUR = 20
```

**1.2 — Définir la structure `lst_blocs`**

Les blocs sont des rectangles. Chaque bloc est un tuple de deux coins opposés : le coin
supérieur gauche et le coin inférieur droit. L'ensemble des blocs du niveau est une liste.

```python
lst_blocs = [
    ((0, 0), (22, 399)),       # mur gauche
    ((0, 376), (339, 399)),    # sol
]
```

**1.3 — Définir la structure `objectif`**

L'objectif (porte, trésor...) est aussi un rectangle, représenté par un tuple de deux coins.

```python
objectif = ((263, 173), (295, 208))
```

**1.4 — Implémenter `victoire(personnage, objectif)`**

Renvoie `True` si le personnage se trouve à l'intérieur de la zone objectif, `False` sinon.
Utilise les constantes `LARGEUR` et `HAUTEUR` pour tenir compte de la taille du personnage.

**1.5 — Implémenter `collision(personnage, lst_blocs)`**

Renvoie le premier bloc de la liste avec lequel le personnage se superpose (c'est-à-dire qu'il
est partiellement à l'intérieur). Renvoie `None` si le personnage ne touche aucun bloc.
Cette fonction est critique : le moteur physique (Dev C) en a besoin pour fonctionner.

**1.6 — Implémenter `clic_vers_vitesse(personnage, clic)`**

Donne au personnage une vitesse dirigée vers les coordonnées du clic. Si le clic est trop
éloigné, la direction est conservée mais la norme est plafonnée à `VMAX`.

**1.7 — Écrire les doctests**

Écrire au moins 2 doctests par fonction (un cas normal, un cas limite).
python -m doctest niveaux.py

---

#### Dev B — Chargement des niveaux (`niveau.py`)

L'objectif est d'écrire la fonction qui lit un fichier `.txt` et reconstruit les structures
de données correspondantes.

**2.1 — Lire la position du personnage**

Parser la première ligne du fichier. Elle contient deux entiers séparés par une virgule.
Construire le dictionnaire `personnage` avec `"position": (x, y)` et `"vitesse": (0, 0)`.

**2.2 — Lire l'objectif**

Parser la deuxième ligne. Elle contient quatre entiers : `x1,y1,x2,y2`.
Construire le tuple `objectif = ((x1, y1), (x2, y2))`.

**2.3 — Lire les blocs**

Parser toutes les lignes suivantes. Chaque ligne contient quatre entiers.
Ignorer tout ce qui suit un `#` sur la même ligne.
Construire `lst_blocs` comme liste de tuples de coins.

**2.4 — Assembler `charger_niveau(fichier)`**

Appelle les trois fonctions précédentes et retourne le triplet
`(personnage, lst_blocs, objectif)`. C'est cette fonction qui sera appelée
depuis le reste du programme.

**2.5 — Créer des niveaux de test et écrire les doctests**

Créer au moins deux fichiers `.txt` dans `niveaux/` pour pouvoir tester.
Écrire des doctests qui vérifient que `charger_niveau` retourne bien les bonnes structures.

---

#### Dev C — Moteur physique (`physique.py`)

C'est la partie la plus complexe du projet. Elle est découpée en petites fonctions
indépendantes, chacune testable seule. L'ordre de développement est important :
chaque fonction s'appuie sur la précédente.

**3.1 — `deplacer(personnage, gravite, pas)`**

Effectue une seule étape de simulation. Met à jour la position en fonction de la vitesse,
puis met à jour la vitesse en fonction de la gravité. Pas de dépendance externe : testable seul.

```
nouvelle position :  x = x + pas × vx      y = y + pas × vy
nouvelle vitesse  :  vx = vx + pas × gx    vy = vy + pas × gy
```

```python
def deplacer(personnage, gravite, pas):
    """
    >>> p = {"position": (100, 100), "vitesse": (5, -10)}
    >>> deplacer(p, (0, 1), 1)
    >>> p["position"]
    (105, 90)
    >>> p["vitesse"]
    (5, -9)
    """
```

**3.2 — `placer_bord(personnage, bloc)`**

Quand le personnage entre en collision avec un bloc, cette fonction le replace juste à
l'extérieur du bloc, contre le bord concerné. Pas de dépendance externe : testable seule.

**3.3 — `detecter_cote(personnage, bloc, vitesse)`**

Détermine par quel côté du bloc le personnage est entré en collision, en se basant sur
la direction de sa vitesse. Retourne une chaîne parmi `"haut"`, `"bas"`, `"gauche"`, `"droite"`.
Pas de dépendance externe : testable seule.

```python
def detecter_cote(personnage, bloc, vitesse):
    """
    >>> p = {"position": (50, 95), "vitesse": (0, 5)}
    >>> detecter_cote(p, ((0, 100), (200, 200)), (0, 5))
    'haut'
    """
```

**3.4 — `choc_mou(personnage, bloc)`**

Gère le choc par défaut (choc mou) : replace le personnage hors du bloc avec `placer_bord`,
puis met sa vitesse à `(0, 0)`. Dépend de 3.2 et 3.3.

**3.5 — `choc(personnage, lst_blocs)`**

Orchestre la gestion d'une collision : appelle `collision` (écrite par Dev A) pour trouver
le bloc concerné, puis appelle `choc_mou`. Dépend de 1.5 et 3.4.
C'est ici que d'autres types de chocs (glace, caoutchouc...) seront branchés plus tard.

**3.6 — `pas(personnage, lst_blocs)`**

Effectue une étape complète de simulation : déplace le personnage avec `deplacer`,
puis résout les collisions éventuelles avec `choc`. Retourne `True` si le personnage
est au repos après cette étape, `False` sinon. Dépend de 3.1 et 3.5.

**3.7 — `simuler(personnage, lst_blocs)`**

Répète les appels à `pas` jusqu'à ce que le personnage soit au repos deux fois de suite.
Retourne la liste de toutes les positions intermédiaires (utile pour tracer la trajectoire).
Dépend de 3.6.

**3.8 — Doctests**

Écrire au moins 2 doctests par fonction. Tester les cas normaux mais aussi les cas limites :
personnage arrivant exactement sur le bord d'un bloc, vitesse nulle, collision par le dessous, etc.

> **Point d'intégration :** Dev C a besoin de `collision()` (tâche 1.5 de Dev A) pour pouvoir
> écrire et tester les fonctions 3.5, 3.6 et 3.7. Prévoir un échange en début de semaine.

---

### Sprint 2 — Interface graphique et solveur

Le jeu doit devenir jouable cette semaine. Dev A assemble l'interface, Dev B écrit le solveur,
Dev C intègre le moteur physique dans la boucle de jeu et corrige les bugs.

---

#### Dev A — Interface graphique (`interface.py`)

Toute la partie graphique utilise la bibliothèque `fltk`.

**4.1 — Menu principal**

Au lancement, afficher la liste des fichiers présents dans `niveaux/`.
Le joueur sélectionne un niveau avec la souris.

**4.2 à 4.4 — Fonctions d'affichage**

- `dessiner_blocs(lst_blocs)` : dessine chaque bloc comme un rectangle coloré
- `dessiner_personnage(personnage)` : dessine le personnage dans une couleur distincte
- `dessiner_objectif(objectif)` : dessine l'objectif (rectangle rouge)

**4.5 — `dessiner_fleche(personnage, clic)`**

Dessine une flèche rouge entre la position du personnage et le curseur,
pour indiquer la direction et l'intensité du prochain saut.

**4.6 — Boucle événements**

- Clic gauche → calcule et affiche la flèche de direction
- Clic droit → valide le saut, lance `simuler()`, met à jour l'affichage
- Touche Echap → retour au menu

**4.7 — Écran de victoire**

Quand `victoire()` retourne `True`, afficher un message et proposer de revenir au menu.

---

#### Dev B — Solveur naïf (`solveur.py`)

Le solveur explore automatiquement toutes les positions atteignables pour trouver un chemin
jusqu'à l'objectif. Il utilise une recherche récursive en profondeur (backtracking).

**5.1 — `generer_vitesses(pas_v)`**

Retourne une liste de vecteurs vitesse à tester. Par exemple avec `pas_v = 5`, on teste
toutes les combinaisons `(vx, vy)` avec `vx` et `vy` variant par pas de 5 entre `-VMAX` et `VMAX`.

**5.2 — `position_approx(personnage, a)`**

Pour éviter de visiter trop de positions quasi-identiques, on arrondit les coordonnées :
retourne `(x // a, y // a)`. Avec `a = 5`, les positions (10, 20) et (14, 24) sont
considérées comme identiques.

**5.3 à 5.5 — Algorithme récursif**

Le solveur fonctionne ainsi à chaque appel :
1. Si le personnage est sur l'objectif → succès, retourner la liste des coups joués
2. Si cette position a déjà été visitée → échec, retourner `None`
3. Sinon, tester chaque vitesse possible : simuler le saut, relancer récursivement
4. Si aucune vitesse ne mène à l'objectif → retourner `None`

**5.6 — `solveur(personnage, lst_blocs, objectif)`**

Fonction principale qui initialise l'ensemble `visite` et lance la récursion.
Retourne la liste des coups à jouer, ou `None` si le niveau est insoluble.

**5.7 — Tests de performance**

Mesurer le temps d'exécution et le nombre de positions visitées sur les niveaux de test.
Trouver de bonnes valeurs pour `a` (approximation des positions) et `pas_v` (pas des vitesses).

> **Point d'intégration :** Dev B a besoin de `simuler()` (tâche 3.7 de Dev C) pour
> simuler chaque coup dans l'algorithme.

---

### Sprint 3 — Améliorations et finalisation

Aborder les améliorations uniquement si toutes les tâches obligatoires sont terminées.
Choisir en équipe selon l'avance de chacun.

---

#### Améliorations optionnelles

**Dev A**
- (⭐) Retour en arrière : appui sur `backspace` pour revenir à la position précédente
- (⭐) Animation des sauts : déplacer le personnage progressivement le long de sa trajectoire
- (⭐⭐) Éditeur de niveau : permettre de créer et sauvegarder un nouveau niveau depuis l'interface

**Dev B**
- (⭐⭐) Solveur optimal : remplacer le backtracking par une recherche en largeur (BFS avec une file)
  pour trouver la solution en un minimum de sauts
- (⭐⭐) Affichage des positions explorées par le solveur pendant la recherche
- (⭐) Système de score : mémoriser le nombre de sauts par niveau et afficher le meilleur score

**Dev C**
- (⭐) Choc élastique (caoutchouc) : la composante de vitesse perpendiculaire au bord est inversée
- (⭐) Glissement (glace) : la composante parallèle au bord est conservée, la vitesse n'est pas annulée
- (⭐) Choc amorti : comme le choc élastique, mais la vitesse est multipliée par un coefficient < 1

---

#### Finalisation commune

- **`sautemouton.py`** : assembler tous les modules, écrire la boucle principale du jeu
- **`rapport.pdf`** : 5 pages environ — guide utilisateur, état d'avancement, description des
  fonctions importantes, difficultés rencontrées, répartition du travail en pourcentage
- **Soutenance** : préparer une présentation de 10 minutes, tous les membres doivent parler.
  Chacun identifie une partie qu'il a personnellement développée et prépare des réponses
  aux questions techniques sur cette partie
- **Archive ZIP** : rassembler tous les fichiers requis, vérifier que `python3 sautemouton.py`
  fonctionne depuis l'archive dézippée

---

## Conventions de code

Chaque fonction doit avoir :

```python
def ma_fonction(param1, param2):
    """Description claire de ce que fait la fonction.

    param1 : ce que représente param1
    param2 : ce que représente param2
    Retourne : ce que retourne la fonction

    >>> ma_fonction(cas_normal)
    resultat_attendu
    >>> ma_fonction(cas_limite)
    resultat_attendu
    """
```

Pour lancer tous les doctests d'un fichier :

```bash
python -m doctest physique.py
python -m doctest -v cheminfichier.py
```

---

## Conventions Git

```
main          # code stable uniquement — ne jamais pousser du code cassé ici
feature/xxx   # pour développer une nouvelle fonctionnalité
fix/xxx       # pour corriger un bug
```

Exemple de noms de branches : `feature/physique-deplacer`, `feature/solveur-bfs`, `fix/collision-bord`

Chaque fonctionnalité passe par une Pull Request relue par un autre membre avant d'être
fusionnée dans `main`.
from vecteur import *
from matrice import *

class Simplex:
    def __init__(self, A=None, b=None, c=None, constraint_types=None):
        """Initialise un problème de programmation linéaire pour la méthode du Simplex.
        
        Args:
            A (Matrice, optional): Matrice des coefficients des contraintes. Default is None.
            b (Vecteur, optional): Vecteur du second membre (contraintes). Default is None.
            c (Vecteur, optional): Vecteur des coûts (fonction objectif). Default is None.
            constraint_types (list, optional): Types de contraintes ("<=", ">=", "="). Default is None.
        """
        self.A = A  # Matrice des coefficients des contraintes
        self.b = b  # Vecteur des contraintes (second membre)
        self.c = c  # Vecteur des coûts (fonction objectif)
        self.constraint_types = constraint_types or []  # Types de contraintes
        
        # Variables pour stocker l'état du simplex
        self.tableau = None  # Tableau du simplex
        self.base = None  # Indices des variables de base
        self.non_base = None  # Indices des variables hors base
        self.optimal = False  # Indique si une solution optimale a été trouvée
        self.unbounded = False  # Indique si le problème est non borné
        self.solution = None  # Solution optimale
        self.valeur_optimale = None  # Valeur de la fonction objectif
        self.var_artificielles = []  # Indices des variables artificielles
    
    def initialiser(self):
        """Initialise le tableau du simplex et les ensembles de base et hors base."""
        if self.A is None or self.b is None or self.c is None:
            raise ValueError("Les données du problème ne sont pas complètes")
        
        m = len(self.A.elements)  # Nombre de contraintes
        n = len(self.c.elements)  # Nombre de variables de décision
        
        # Si aucun type de contrainte n'est spécifié, supposer "<=" pour toutes
        if not self.constraint_types:
            self.constraint_types = ["<="] * m
        
        # Compter les variables d'écart, de surplus et artificielles nécessaires
        num_slack = sum(1 for t in self.constraint_types if t == "<=")
        num_surplus = sum(1 for t in self.constraint_types if t == ">=")
        num_artificial = sum(1 for t in self.constraint_types if t in [">=", "="])
        
        # Taille totale du tableau
        total_vars = n + num_slack + num_surplus + num_artificial
        
        # Initialiser le tableau avec les contraintes et les variables additionnelles
        tableau = []
        slack_index = n
        surplus_index = n + num_slack
        artificial_index = n + num_slack + num_surplus
        self.var_artificielles = []
        
        for i in range(m):
            ligne = self.A.elements[i].elements.copy() + [0] * (total_vars - n) + [self.b.elements[i]]
            
            # Traiter selon le type de contrainte
            if self.constraint_types[i] == "<=":
                # Ajouter variable d'écart (slack)
                ligne[slack_index] = 1
                slack_index += 1
            elif self.constraint_types[i] == ">=":
                # Ajouter variable de surplus (négative)
                ligne[surplus_index] = -1
                surplus_index += 1
                # Ajouter variable artificielle
                ligne[artificial_index] = 1
                self.var_artificielles.append(artificial_index)
                artificial_index += 1
            elif self.constraint_types[i] == "=":
                # Ajouter variable artificielle
                ligne[artificial_index] = 1
                self.var_artificielles.append(artificial_index)
                artificial_index += 1
            
            tableau.append(ligne)
        
        # Ajouter la ligne de la fonction objectif (z)
        # Négation des coefficients objectifs car on maximise
        ligne_objectif = [-x for x in self.c.elements] + [0] * (total_vars - n) + [0]
        tableau.append(ligne_objectif)
        
        # Si des variables artificielles sont présentes, ajouter la fonction objectif auxiliaire (w)
        if num_artificial > 0:
            ligne_w = [0] * (total_vars + 1)  # +1 pour inclure la colonne b
            
            # Ajouter les coefficients pour les variables artificielles dans w
            for idx in self.var_artificielles:
                ligne_w[idx] = 1
            
            # Ajouter les rangs pour rendre w = 0
            for i, idx in enumerate(self.var_artificielles):
                row_idx = next(r for r, row in enumerate(tableau[:-1]) if row[idx] == 1)
                for j in range(total_vars + 1):
                    ligne_w[j] -= tableau[row_idx][j]
            
            tableau.append(ligne_w)
        
        self.tableau = tableau
        
        # Initialiser les ensembles de base et hors base
        self.base = []
        slack_idx = n
        surplus_idx = n + num_slack
        art_idx = n + num_slack + num_surplus
        
        for i in range(m):
            if self.constraint_types[i] == "<=":
                self.base.append(slack_idx)  # Variable d'écart
                slack_idx += 1
            elif self.constraint_types[i] == ">=":
                self.base.append(art_idx)  # Variable artificielle
                # Sauter la variable de surplus
                surplus_idx += 1
                art_idx += 1
            elif self.constraint_types[i] == "=":
                self.base.append(art_idx)  # Variable artificielle
                art_idx += 1
        
        # Variables hors base
        self.non_base = [j for j in range(total_vars) if j not in self.base]
        
        # Réinitialiser les autres attributs
        self.optimal = False
        self.unbounded = False
        self.solution = None
        self.valeur_optimale = None
        
        print("Tableau initial du simplex:")
        self.afficher_tableau()
    
    def afficher_tableau(self):
        """Affiche le tableau actuel du simplex."""
        if self.tableau is None:
            print("Le tableau n'a pas encore été initialisé")
            return
        
        # Déterminer la largeur des colonnes
        largeur = max(len(f"{self.tableau[i][j]:.2f}") for i in range(len(self.tableau)) for j in range(len(self.tableau[0]))) + 2
        
        # Afficher les numéros de colonnes
        print("    |", end="")
        for j in range(len(self.tableau[0]) - 1):
            print(f" x{j+1}".ljust(largeur), end="")
        print(" b")
        
        # Afficher une ligne de séparation
        print("-" * (largeur * (len(self.tableau[0]) + 1) + 5))
        
        # Afficher les variables de base et les lignes du tableau
        for i in range(len(self.tableau) - 1 - (1 if self.var_artificielles else 0)):
            var_base = f"x{self.base[i]+1}"
            print(f"{var_base} |", end="")
            for val in self.tableau[i]:
                print(f" {val:.2f}".ljust(largeur), end="")
            print()
        
        # Afficher la ligne de la fonction objectif
        print("z  |", end="")
        for val in self.tableau[-1 - (1 if self.var_artificielles else 0)]:
            print(f" {val:.2f}".ljust(largeur), end="")
        print()
        
        # Afficher la ligne de la fonction objectif auxiliaire si présente
        if self.var_artificielles:
            print("w  |", end="")
            for val in self.tableau[-1]:
                print(f" {val:.2f}".ljust(largeur), end="")
            print()
    
    def trouver_variable_entrante(self):
        """Trouve l'indice de la variable entrante (colonne pivot).
        
        Returns:
            int: Indice de la variable entrante, ou -1 si toutes les valeurs sont >= 0 (solution optimale).
        """
        # Fonction objectif z est l'avant-dernière ligne si w est présente, sinon la dernière
        ligne_z = -1 - (1 if self.var_artificielles else 0)
        derniere_ligne = self.tableau[ligne_z]
        
        # Recherche de la valeur la plus négative dans la dernière ligne (hors dernière colonne)
        min_val = 0
        min_idx = -1
        for j in range(len(derniere_ligne) - 1):
            if derniere_ligne[j] < min_val:
                min_val = derniere_ligne[j]
                min_idx = j
        
        return min_idx  # Retourne -1 si la solution est optimale
    
    def trouver_variable_entrante_phase_i(self):
        """Trouve l'indice de la variable entrante pour la Phase I."""
        # Dernière ligne = fonction objectif w
        derniere_ligne = self.tableau[-1]
        
        min_val = 0
        min_idx = -1
        for j in range(len(derniere_ligne) - 1):
            if derniere_ligne[j] < min_val:
                min_val = derniere_ligne[j]
                min_idx = j
        
        return min_idx  # Retourne -1 si la solution est optimale
    
    def trouver_variable_sortante(self, colonne_entrante):
        """Trouve l'indice de la variable sortante (ligne pivot) en utilisant le test du quotient minimum.
        
        Args:
            colonne_entrante (int): Indice de la variable entrante.
            
        Returns:
            int: Indice de la variable sortante, ou -1 si le problème est non borné.
        """
        if colonne_entrante == -1:
            return -1  # Pas de pivot nécessaire
        
        min_ratio = float('inf')
        ligne_sortante = -1
        
        # Nombre de lignes à considérer (exclut les lignes des fonctions objectif)
        num_contraintes = len(self.tableau) - 1 - (1 if self.var_artificielles else 0)
        
        for i in range(num_contraintes):  # Toutes les lignes sauf les fonctions objectif
            if self.tableau[i][colonne_entrante] > 0:
                ratio = self.tableau[i][-1] / self.tableau[i][colonne_entrante]
                if ratio < min_ratio:
                    min_ratio = ratio
                    ligne_sortante = i
        
        return ligne_sortante  # Retourne -1 si le problème est non borné
    
    def pivot(self, ligne, colonne):
        """Effectue l'opération de pivot sur le tableau du simplex.
        
        Args:
            ligne (int): Indice de la ligne pivot.
            colonne (int): Indice de la colonne pivot.
        """
        # Normaliser la ligne pivot
        element_pivot = self.tableau[ligne][colonne]
        for j in range(len(self.tableau[0])):
            self.tableau[ligne][j] /= element_pivot
        
        # Mettre à jour les autres lignes
        for i in range(len(self.tableau)):
            if i != ligne:
                facteur = self.tableau[i][colonne]
                for j in range(len(self.tableau[0])):
                    self.tableau[i][j] -= facteur * self.tableau[ligne][j]
        
        # Mettre à jour les ensembles de base et hors base
        var_sortante = self.base[ligne]
        var_entrante = colonne
        
        self.base[ligne] = var_entrante
        
        # Mettre à jour l'ensemble hors base
        self.non_base.remove(var_entrante)
        self.non_base.append(var_sortante)
        
        # Trier les variables hors base pour faciliter la lecture
        self.non_base.sort()
    
    def verifier_solution_phase_i(self):
        """Vérifie si la solution de Phase I est réalisable (w = 0)."""
        # La valeur de w est dans le coin inférieur droit du tableau
        w_value = self.tableau[-1][-1]
        
        # Si w est presque zéro (tolérance numérique)
        if abs(w_value) < 1e-10:
            print("Solution réalisable trouvée en Phase I (w ≈ 0).")
            return True
        else:
            print(f"Solution non réalisable en Phase I (w = {w_value}).")
            return False
    
    def preparer_phase_ii(self):
        """Prépare le tableau pour la Phase II en supprimant les variables artificielles."""
        # Supprimer la ligne w
        self.tableau.pop()
        
        # Les variables artificielles sont maintenant inutiles on les laisse dans le tableau mais on ne les utilisera plus
        self.var_artificielles = []
        
        print("Tableau préparé pour la Phase II:")
        self.afficher_tableau()
    
    def phase_i(self):
        """Effectue la Phase I de l'algorithme du simplex (élimination des variables artificielles)."""
        iteration = 0
        max_iterations = 100
        
        while iteration < max_iterations:
            iteration += 1
            print(f"\nItération {iteration} (Phase I):")
            
            # Fonction objectif w est la dernière ligne du tableau en phase I
            colonne_entrante = self.trouver_variable_entrante_phase_i()
            
            if colonne_entrante == -1:
                print("Phase I terminée.")
                break
            
            print(f"Variable entrante: x{colonne_entrante+1}")
            
            ligne_sortante = self.trouver_variable_sortante(colonne_entrante)
            
            if ligne_sortante == -1:
                self.unbounded = True
                print("Le problème est non borné (Phase I).")
                return False
            
            print(f"Variable sortante: x{self.base[ligne_sortante]+1}")
            
            self.pivot(ligne_sortante, colonne_entrante)
            
            print("Tableau après pivot:")
            self.afficher_tableau()
        
        return True
    
    def phase_ii(self):
        """Effectue la Phase II de l'algorithme du simplex (optimisation)."""
        iteration = 0
        max_iterations = 100
        
        while iteration < max_iterations:
            iteration += 1
            print(f"\nItération {iteration} (Phase II):")
            
            colonne_entrante = self.trouver_variable_entrante()
            
            if colonne_entrante == -1:
                self.optimal = True
                print("Solution optimale trouvée.")
                break
            
            print(f"Variable entrante: x{colonne_entrante+1}")
            
            ligne_sortante = self.trouver_variable_sortante(colonne_entrante)
            
            if ligne_sortante == -1:
                self.unbounded = True
                print("Le problème est non borné (valeur optimale: +inf)")
                break
            
            print(f"Variable sortante: x{self.base[ligne_sortante]+1}")
            
            self.pivot(ligne_sortante, colonne_entrante)
            
            print("Tableau après pivot:")
            self.afficher_tableau()
        
        # Extraire la solution optimale si elle existe
        if self.optimal:
            self.extraire_solution()
            return True
        elif iteration >= max_iterations:
            print("Nombre maximum d'itérations atteint sans convergence.")
        
        return False
    
    def resoudre(self):
        """Résout le problème de programmation linéaire en utilisant la méthode du simplex.
        
        Returns:
            bool: True si une solution optimale a été trouvée, False sinon.
        """
        self.initialiser()
        
        # Si des variables artificielles sont présentes, effectuer la Phase I
        if self.var_artificielles:
            print("\n=== PHASE I: Élimination des variables artificielles ===")
            self.phase_i()
            
            # Vérifier si la solution de Phase I est réalisable
            if not self.verifier_solution_phase_i():
                print("Le problème n'a pas de solution réalisable.")
                return False
            
            # Préparer pour la Phase II
            self.preparer_phase_ii()
        
        # Phase II: Résoudre le problème original
        print("\n=== PHASE II: Optimisation du problème original ===")
        return self.phase_ii()
    
    def extraire_solution(self):
        """Extrait la solution optimale du tableau final."""
        if not self.optimal:
            return
        
        n = len(self.c.elements)  # Nombre de variables de décision originales
        self.solution = [0] * n
        
        # Récupérer les valeurs des variables de base
        for i, var_idx in enumerate(self.base):
            if var_idx < n:  # Si la variable de base est une variable originale
                self.solution[var_idx] = self.tableau[i][-1]
        
        # Valeur optimale de la fonction objectif
        self.valeur_optimale = self.tableau[-1][-1]
    
    def afficher_solution(self):
        """Affiche la solution du problème."""
        if self.optimal:
            print("\nSolution optimale trouvée:")
            print(f"Valeur optimale de la fonction objectif: {self.valeur_optimale}")
            print("Valeurs des variables de décision:")
            for i, val in enumerate(self.solution):
                print(f"x_{i+1} = {val}")
        elif self.unbounded:
            print("\nLe problème est non borné (valeur optimale: +inf)")
        else:
            print("\nAucune solution optimale n'a été trouvée.")


def lire_simplex(filename):
    """Lit un fichier de données pour le problème du simplexe avec types de contraintes.
    
    Args:
        filename (str): Le nom du fichier à lire.

    Returns:
        tuple: Un tuple contenant la matrice des coefficients, le vecteur des contraintes,
               le vecteur des coûts et les types de contraintes.
    """
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if not line.startswith('//')]
    
    # Première ligne : coefficients de la fonction objectif
    c_values = list(map(float, lines[0].split()))
    
    # Lignes suivantes : contraintes
    A_values = []
    b_values = []
    constraint_types = []
    
    for i in range(1, len(lines)):
        parts = lines[i].split()
        
        # Trouver l'index du type de contrainte
        type_idx = -1
        for j, part in enumerate(parts):
            if part in ["<=", ">=", "="]:
                type_idx = j
                break
        
        if type_idx == -1:
            raise ValueError(f"Type de contrainte manquant à la ligne {i+1}")
        
        # Extraire les coefficients (tout avant le type de contrainte)
        coeffs = list(map(float, parts[:type_idx]))
        
        # Extraire le type de contrainte
        constraint_type = parts[type_idx]
        
        # Extraire la valeur du second membre (après le type de contrainte)
        b_value = float(parts[type_idx + 1])
        
        A_values.append(coeffs)
        b_values.append(b_value)
        constraint_types.append(constraint_type)
    
    # Créer les objets Matrice et Vecteur
    A = Matrice("A", A_values)
    b = Vecteur("b", b_values)
    c = Vecteur("c", c_values)
    
    # Afficher les données pour vérification
    print("Données lues:")
    print("Fonction objectif (c):", c.elements)
    print("Matrice des contraintes (A):")
    for row in A.elements:
        print(row.elements)
    print("Second membre (b):", b.elements)
    print("Types de contraintes:", constraint_types)
    
    return A, b, c, constraint_types


if __name__ == "__main__":
    try:
        # Mettez bien le chemin de votre fichier ici
        A, b, c, constraint_types = lire_simplex("c:/Users/User/OneDrive - Institut Catholique de Lille/Bureau/L3 SDN/S2/Method_Num_&_Sim/TP1/simplex.txt")
        simplex = Simplex(A, b, c, constraint_types)
        simplex.resoudre()
        simplex.afficher_solution()
        
    except Exception as e:
        print(f"Une erreur est survenue: {e}")
        import traceback
        traceback.print_exc()
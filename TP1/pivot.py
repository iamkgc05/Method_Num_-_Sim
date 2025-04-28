from vecteur import *
from matrice import *

def inverse(a):
    return 1/a




class Pivot:
    def __init__(self):
        pass

    def normaliser(self, matrice: Matrice, num_lignes=0, num_colonnes=0) -> Matrice:
        """Normalise une ligne de la matrice par rapport à un pivot
        
        Args:
            matrice (Matrice): La matrice à normaliser
            num_lignes (int): L'index de la ligne contenant le pivot
            num_colonnes (int): L'index de la colonne contenant le pivot
            
        Returns:
            Matrice: La matrice normalisée
            
        Raises:
            ValueError: Si le pivot est nul
        """
        # Access the pivot through the elements attribute of Vecteur
        pivot = matrice.elements[num_lignes].elements[num_colonnes]
        
        if pivot == 0:
            raise ValueError("Pivot nul")
            
        # Divide each element in the row by the pivot
        new_elements = [elt/pivot for elt in matrice.elements[num_lignes].elements]
        matrice.elements[num_lignes] = Vecteur(f"{matrice.name}_{num_lignes}", new_elements)

        
        return matrice

    def standardiser(self, matrice: Matrice, num_lignes=0, num_colonnes=0) -> Matrice:
        """Standardise les autres lignes de la matrice par rapport à une ligne pivot
        
        Args:
            matrice (Matrice): La matrice à standardiser
            num_lignes (int): L'index de la ligne pivot
            num_colonnes (int): L'index de la colonne pivot
            
        Returns:
            Matrice: La matrice standardisée
        """
        for i in range(matrice.num_ligne):
            if i != num_lignes:
                
                coeff = matrice.elements[i].elements[num_colonnes]
                
                new_elements = []
                for j in range(matrice.taille):
                    element = (matrice.elements[i].elements[j] - 
                            coeff * matrice.elements[num_lignes].elements[j])
                    new_elements.append(element)

                matrice.elements[i] = Vecteur(f"{matrice.name}_{i}", new_elements)

        
        return matrice

    def pivot_de_gauss(self, matrice: Matrice, second_membre=None) -> tuple:
        """Applique l'élimination de Gauss pour mettre la matrice sous forme échelonnée
        
        Args:
            matrice (Matrice): La matrice à transformer
            second_membre (list, optional): Le vecteur du second membre sous forme [x, y, z]. 
                                           Defaults to None.
            
        Returns:
            tuple: (Matrice, list) La matrice sous forme échelonnée et le second membre transformé
            
        Raises:
            ValueError: Si le système est impossible à résoudre (pivot nul partout)
        """
        print("Matrice initiale:")
        print(matrice)
        
        n = matrice.num_ligne
        
        # Si aucun second membre n'est fourni, on utilise un vecteur de zéros
        if second_membre is None:
            second_membre = [0] * n
        else:
            print("Second membre initial:")
            for i in range(n):
                print(f"[{second_membre[i]}]")

        if len(second_membre) != n:
            raise ValueError("Le second membre doit avoir la même taille que la matrice")
            
        # Suivi des opérations sur le système
        print("\nRésolution du système d'équations:")
        
        for i in range(n):
            # Vérifier si le pivot est nul et permuter les lignes si nécessaire
            if matrice.elements[i].elements[i] == 0:
                for j in range(i + 1, n):
                    if matrice.elements[j].elements[i] != 0:
                        print(f"Étape {i+1}: Permutation des lignes {i+1} et {j+1}")
                        # Permuter les lignes dans la matrice
                        matrice.elements[i], matrice.elements[j] = matrice.elements[j], matrice.elements[i]
                        # Permuter également les éléments correspondants dans le second membre
                        second_membre[i], second_membre[j] = second_membre[j], second_membre[i]
                        break
                else:
                    raise ValueError("Système impossible à résoudre (pivot nul partout)")
            
            print(f"Étape {i+1}: Ligne de travail {i+1}")
            
            # Normaliser la ligne du pivot
            pivot = matrice.elements[i].elements[i]
            if pivot != 0:
                print(f"  - Normalisation par le pivot {pivot}")
                # Normaliser la matrice
                self.normaliser(matrice, i, i)
                
                # Normaliser le second membre
                second_membre[i] = second_membre[i] / pivot
            
            # Standardiser les autres lignes par rapport à la ligne du pivot
            print(f"  - Standardisation des autres lignes par rapport à la ligne {i+1}")
            
            # Sauvegarde des coefficients avant standardisation
            coeffs = []
            for k in range(n):
                if k != i:
                    coeffs.append((k, matrice.elements[k].elements[i]))
            
            self.standardiser(matrice, i, i)
            
            # Standardiser le second membre en utilisant les coefficients sauvegardés
            for k, coeff in coeffs:
                second_membre[k] -= coeff * second_membre[i]
            
            print("État actuel:")
            print(matrice)
            print("Second membre:")
            for val in second_membre:
                print(f"[{val}]")
            
        
        # Convertir les valeurs du second membre en entiers si possible
        for i in range(n):
            if second_membre[i] == int(second_membre[i]):
                second_membre[i] = int(second_membre[i])
        
        return matrice, second_membre
    
    def realiser_pivot(self, matrice, second_membre, nom_inconnues=None):
        matrice_echelonnee, solution = self.pivot_de_gauss(matrice, second_membre)
        print("\nRésultat final:")
        print("Matrice échelonnée:")
        print(matrice_echelonnee)
        print("Second membre transformé:")
        for i in range(len(solution)):
            if nom_inconnues is not None:
                print(f"{nom_inconnues[i]} = {solution[i]}")
            else:
                print(f"x{i+1} = {solution[i]}")
        return matrice_echelonnee, solution, nom_inconnues
    
def utilisateur_matrice():
    nombre_inconnues = int(input("Entrez le nombre d'inconnues: "))
    noms_inconnus = []
    for i in range(nombre_inconnues):
        print(f"Entrez le nom de l'inconnue {i+1}:")
        nom = input()
        noms_inconnus.append(nom)
    nombre_equations = int(input("Entrez le nombre d'équations: "))
    nombre_ligne = nombre_equations
    matrice = Matrice("A", [[0]*nombre_inconnues for _ in range(nombre_ligne)])
    for i in range(nombre_ligne):
        print(f"Entrez les coefficients de l'équation {i+1} avec des espaces entre les valeurs:")
        coefficients = list(map(int, input().split()))
        if len(coefficients) != nombre_inconnues:
            raise ValueError("Le nombre de coefficients ne correspond pas au nombre d'inconnues")
        nom = "l" + str(i+1)
        vecteur = Vecteur(nom, coefficients)
        matrice.elements[i] = vecteur
    print("Entrez les valeurs du second membre avec des espaces entre les valeurs:")
    second_membre = list(map(int, input().split()))
    if len(second_membre) != nombre_ligne:
        raise ValueError("Le nombre de valeurs du second membre ne correspond pas au nombre d'équations")
    
    print("Matrice A:")
    print(matrice)
    print("Second membre:")
    for val in second_membre:
        print(f"[{val}]")
    
    return matrice, second_membre, noms_inconnus

def txt_en_matrice(File):
    with open(File, "r") as f:
        # Première ligne: nombre d'inconnues
        nombre_inconnues = int(f.readline().strip())
        
        # Deuxième ligne: noms des inconnues
        noms_inconnus = f.readline().strip().split()
        if len(noms_inconnus) != nombre_inconnues:
            raise ValueError(f"Le nombre de noms d'inconnues ({len(noms_inconnus)}) ne correspond pas au nombre d'inconnues ({nombre_inconnues})")
        
        # Troisième ligne: nombre d'équations
        nombre_equations = int(f.readline().strip())
        nombre_ligne = nombre_equations
        
        # Initialisation de la matrice
        matrice = Matrice("A", [[0]*nombre_inconnues for _ in range(nombre_ligne)])
        
        # Lecture des coefficients des équations
        for i in range(nombre_ligne):
            coefficients = list(map(float, f.readline().strip().split()))
            if len(coefficients) != nombre_inconnues:
                raise ValueError(f"Le nombre de coefficients pour l'équation {i+1} ({len(coefficients)}) ne correspond pas au nombre d'inconnues ({nombre_inconnues})")
            nom = "l" + str(i+1)
            vecteur = Vecteur(nom, coefficients)
            matrice.elements[i] = vecteur
        
        # Ligne n+2: composants du second membre
        second_membre = list(map(float, f.readline().strip().split()))
        if len(second_membre) != nombre_equations:
            raise ValueError(f"Le nombre de valeurs du second membre ({len(second_membre)}) ne correspond pas au nombre d'équations ({nombre_equations})")
        
        print("Lecture du fichier terminée avec succès!")
        print(f"Nombre d'inconnues: {nombre_inconnues}")
        print(f"Noms des inconnues: {noms_inconnus}")
        print(f"Nombre d'équations: {nombre_equations}")
        print("Matrice A:")
        print(matrice)
        print(f"Second membre:")
        for val in second_membre:
            print(f"[{val}]")
        
        return matrice, second_membre, noms_inconnus
    

def matrice_en_txt(matrice, second_membre, noms_inconnus, file):
    with open(file, "w") as f:
        f.write(f"{matrice.num_colonne}\n")
        f.write(" ".join(noms_inconnus) + "\n")
        f.write(f"{matrice.num_ligne}\n")
        for i in range(matrice.num_ligne):
            f.write(" ".join(map(str, matrice.elements[i].elements)) + "\n")
        f.write(" ".join(map(str, second_membre)) + "\n")
        print(f"Matrice et second membre écrits dans le fichier {file}")





    


    
    
    


if __name__=="__main__":
    """
    pivot = Pivot()
    # Exemple avec second membre
    m1 = Matrice("m1", [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]])
    b1 = [8, -11, -3]  # Second membre sous forme de vecteur simple
    matrice_echelonnee, solution = pivot.pivot_de_gauss(m1, b1)
    
    print("\nRésultat final:")
    print("Matrice échelonnée:")
    print(matrice_echelonnee)
    print("Second membre transformé:")
    for val in solution:
        print(f"[{val}]")
    
    # Affichage de la solution
    print("\nSolution du système:")
    for i in range(len(solution)):
        print(f"x{i+1} = {solution[i]}")
    """
    #Pivot = Pivot()
    #matrice, vecteur, noms_inconnus = utilisateur_matrice()
    #Pivot.realiser_pivot(matrice, vecteur, noms_inconnus)

    # Mettez le chemin complet d'acces au fichier
    chemin_fichier = "c:/Users/User/OneDrive - Institut Catholique de Lille/Bureau/L3 SDN/S2/Method_Num_&_Sim/TP1/test.txt"
    matrice, vecteur, noms_inconnus = txt_en_matrice(chemin_fichier)
    pivot = Pivot()
    n_matrice, n_vecteur, noms_inconnus = pivot.realiser_pivot(matrice, vecteur, noms_inconnus)
    matrice_en_txt(n_matrice, n_vecteur, noms_inconnus, "c:/Users/User/OneDrive - Institut Catholique de Lille/Bureau/L3 SDN/S2/Method_Num_&_Sim/TP1/test2.txt")





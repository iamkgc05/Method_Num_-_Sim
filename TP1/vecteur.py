from collections.abc import MutableSequence

class Vecteur:
    def __init__(self, name: str, elements: MutableSequence):
        """
        Initialise un vecteur avec un nom et une liste d'éléments.

        :param name: Le nom du vecteur.
        :param elements: Une liste contenant uniquement des int ou float.
        """
        if not isinstance(elements, MutableSequence) or not isinstance(elements, list):  
            raise TypeError("elements doit être une liste.")

        if not all(isinstance(x, (int, float)) for x in elements):  
            raise TypeError("Tous les éléments doivent être des int ou des float.")

        self.name = name
        self.taille = len(elements)
        self.elements = elements[:]

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères de l'objet Vecteur.
        """
        return f"(Vecteur : {self.name}, Taille : {self.taille}, Elements : {self.elements})"

    def __add__(self, other):
        """
        Ajoute deux objets Vecteur élément par élément.

        Args:
            other (Vecteur): L'autre Vecteur à ajouter.

        Returns:
            Vecteur: Un nouvel objet Vecteur avec la somme élément par élément des deux Vecteurs.
            str: Un message d'erreur si les Vecteurs ont des tailles différentes.
        """
        if self.taille != other.taille:
            return f"Erreur les tailles des vecteurs sont différentes {self.taille} != {other.taille}"
        else:
            newElements = [x + y for x, y in zip(self.elements, other.elements)]
            newName = self.name + " + " + other.name
            newVec = Vecteur(newName, newElements)
            return newVec

    def __mul__(self, coef: float | int):
        """
        Multiplie chaque élément du Vecteur par un coef ou un flottant.

        Args:
            coef (float|int): Le nombre par lequel multiplier les éléments du Vecteur.

        Returns:
            Vecteur: Un nouvel objet Vecteur avec les éléments multipliés.
            str: Un message d'erreur si l'argument n'est ni un coef ni un flottant.
        """
        if not isinstance(coef, (float | int)):
            return "Aucun coef ou flottant n'a été rentré par l'utilisateur, Erreur"
        else:
            newElements = [x * coef for x in self.elements]
            newName =  self.name + " * " + str(coef)
            newVec = Vecteur(newName, newElements)
            return newVec

    def __matmul__(self, other) -> float | int:
        """
        Calcule le produit scalaire de deux Vecteurs.

        Args:
            other (Vecteur): L'autre Vecteur pour le produit scalaire.

        Returns:
            float: Le produit scalaire des deux Vecteurs.
            str: Un message d'erreur si les Vecteurs ont des tailles différentes.
        """
        if self.taille != other.taille:
            return f"Erreur les tailles des vecteurs sont différentes {self.taille} != {other.taille}"
        else:
            newListe = [x * y for x, y in zip(self.elements, other.elements)]
            Entier = sum(newListe)
            return Entier
        
    def __rmul__(self, scalaire: int | float):
        """Permet la multiplication scalaire * vecteur"""
        return self.__mul__(scalaire)
        
    def __neg__(self):
        """
        Négative chaque élément du Vecteur.

        Returns:
            Vecteur: Un nouvel objet Vecteur avec les éléments négativés.
        """
        neg_elements = [-x for x in self.elements]
        newVec = Vecteur("-" + self.name, neg_elements)
        return newVec

    def __sub__(self, other):
        """
        Soustrait deux objets Vecteur élément par élément.

        Args:
            other (Vecteur): L'autre Vecteur à soustraire.

        Returns:
            Vecteur: Un nouvel objet Vecteur avec la différence élément par élément des deux Vecteurs.
            str: Un message d'erreur si les Vecteurs ont des tailles différentes.
        """
        if self.taille != other.taille:
            return f"Erreur les tailles des vecteurs sont différentes {self.taille} != {other.taille}"
        else:
            newVec = vecteur+(-other)
            return newVec

    

    def __eq__(self, other) -> bool:
        """
        Vérifie si deux Vecteurs sont égaux.

        Args:
            other (Vecteur): L'autre Vecteur à comparer.

        Returns:
            bool: True si les Vecteurs sont égaux, False sinon.
        """
        marge = 12-10
        if self.taille != other.taille:
            return False
        for i in range(len(self.elements)):
            if self.elements[i] != other.elements[i]:
                if abs(self.elements[i] - other.elements[i]) > abs(marge):
                    return False
        return True

    def __del__(self) -> None:
        """
        Supprime l'objet Vecteur.
        """
        print(f"Le vecteur {self.name} a été supprimé")
        del self

def ieme_canonique(taille: int, position: int) -> Vecteur:
    liste = [0] * taille
    liste[position] = 1
    name = f"Canonique {position}e position" 
    return Vecteur(name, liste)
        



if __name__=="__main__":
    ma_liste = [1, 2, 3]
    vecteur = Vecteur("A", ma_liste)
    print(vecteur)
    ma_liste[1] = 10
    print(vecteur)
    vecteur2 = Vecteur("B", [4, 5, 6])
    print(vecteur)
    print(vecteur2)
    print("\n")
    print("Addition de deux vecteurs")
    print(vecteur+vecteur2)
    print("\n")
    print("Multiplication d'un vecteur par un entier")
    print(vecteur*2)
    print("\n")
    print("Produit scalaire de deux vecteurs")
    print(vecteur@vecteur2)
    print("\n")
    print("Opposé d'un vecteur")
    print(-vecteur)
    print("\n")
    print("Soustraction de deux vecteurs")
    print(vecteur2-vecteur)
    print("\n")
    print("Comparaison de deux vecteurs")
    print(vecteur==vecteur2)
    print("\n")

    



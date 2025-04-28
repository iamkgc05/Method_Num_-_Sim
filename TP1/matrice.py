from vecteur import Vecteur
from typing import *
from vecteur import ieme_canonique

class Matrice : 
    def __init__(self, name: str, elements: List[List[int]]):
        taille = len(elements[0])
        self.name = name
        for liste in elements:
            if len(liste) != taille:
                raise ValueError("Les vecteurs n'ont pas la même taille")
        liste_vecteurs= []
        i = 0
        for liste in elements:
            liste_vecteurs.append(Vecteur(f"{name}_{i}", liste))
            i += 1 
        self.taille = taille
        self.elements = liste_vecteurs[:]
        self.num_colonne = taille
        self.num_ligne = len(liste_vecteurs)
        
    def __str__(self):
        rows = "\n".join(str(vecteur.elements) for vecteur in self.elements)
        return f"Matrice {self.name}:\n[{rows}]"

    def __add__(self, other):
        if self.taille != other.taille:
            raise "Les matrices n'ont pas la meme taille"
        new_elements = [[v1.elements[i] + v2.elements[i] for i in range(self.taille)]
                   for v1, v2 in zip(self.elements, other.elements)]
        return Matrice(f"{self.name} + {other.name}", new_elements)
    
    def __neg__(self):
        new_elements = [[-element for element in vecteur.elements] for vecteur in self.elements]
        return Matrice(f"-{self.name}", new_elements)

    def __sub__(self, other):
        if self.taille != other.taille:
            raise "Les matrices n'ont pas la meme taille"
        return self + (-other)
    
    def __mul__(self, entier: int | float): 
        """Multiplie une matrice par un scalaire"""
        if not isinstance(entier, (int, float)):
            raise TypeError("Le multiplicateur doit être un nombre")
        new_elements = [[element * entier for element in vecteur.elements] 
                   for vecteur in self.elements]
        return Matrice(f"{self.name} * {entier}", new_elements)

    def __rmul__(self, entier: int | float):
        """Permet la multiplication scalaire * matrice"""
        return self.__mul__(entier)
    
    def __matmul__(self, other):
        """Multiplication matricielle (@)
        
        Args:
            other (Matrice): La matrice à multiplier
            
        Returns:
            Matrice: Le produit des deux matrices
            
        Raises:
            ValueError: Si les dimensions ne sont pas compatibles
        """
        if self.taille != other.taille:
            raise ValueError("Les matrices ne peuvent pas être multipliées: dimensions incompatibles")
            
        new_elements = []
        for i in range(self.taille):
            # Calculate each row of the resulting matrix
            row_elements = []
            for k in range(self.taille):
                element = sum(self.elements[i].elements[j] * other.elements[j].elements[k] 
                            for j in range(self.taille))
                row_elements.append(element)
            new_elements.append(row_elements)  # Append the raw list instead of Vecteur
        
        return Matrice(f"{self.name}@{other.name}", new_elements)
    
    def mut_vec(self, vecteur: Vecteur) -> Vecteur:
        """Multiplication élément par élément du vecteur avec chaque ligne de la matrice
        
        Args:
            vecteur (Vecteur): Le vecteur à multiplier avec chaque ligne de la matrice
            
        Returns:
            Vecteur: Le vecteur résultant contenant les produits élément par élément
        """
        if self.elements[0].taille == vecteur.taille:
            
            new_elements = []
            for elt in self.elements:
                valeur = 0
                for i in range(elt.taille):
                    valeur += elt.elements[i] * vecteur.elements[i]
                new_elements.append(valeur)
            return Vecteur(f"{self.name}@{vecteur.name}", new_elements)

        else:
            raise ValueError(f"Dimensions incompatibles: matrice ({self.taille}x{self.elements[0].taille}) et vecteur ({vecteur.taille})")
    
    def __eq__(self, other) -> bool:
        if self.taille != other.taille:
            return False
        for i in range(self.taille):
            if self.elements[i] != other.elements[i]:
                return False
        return True
    
    def __del__(self) -> None:
        print(f"La matrice {self.name} a été supprimée")
        del self

    
def ieme_canonique_matrice(taille: int, name=" ") -> Matrice:
    if name == " ":
        name = f"canonique_{taille}"
    elements = [[0]*taille for _ in range(taille)]
    for i in range(taille):
        elements[i][i] = 1
    return Matrice(name, elements)

if __name__ == "__main__":
    m1 = ieme_canonique_matrice(3, "m1")
    m2 = ieme_canonique_matrice(3, "m2")
    m3 = m1 + m2
    print(m3)
    m4 = m3 @ m3
    print(m4)
    
from time import time as t
from collections.abc import Callable

fonction_numerique = Callable[[float], float]
precision = 0.00000000001


def tracer(methode_d_approximation : Callable[[], float]): 
    """@brief Cette fonction affiche une ligne contenant :
    le nom de la méthode d'approximation 
    la valeur approchée obtenue par dite méthode 
    le temps écoulé entre le lancement de la méthode et l'obtension du résultat 
    @remarks vous pourrez utiliser la fonction time du module time."""

    debut = t()
    valeur_approx = methode_d_approximation()
    fin = t()
    print(f"{methode_d_approximation.__name__} : {valeur_approx} en {fin-debut:.10f} secondes")

    return valeur_approx


def fonction_a_annuler(x: float) -> float :
    """Il s'agit d'une fonction continue vérifiant 
    il existe un intervalle I = [a, b] sur lequel 
    ° f est continue sur I ; 
    ° f monotone sur I ; 
    ° f(sqrt(2)) = 0.
    """

    return x**2 - 2


def dichotomie(a : float, b : float, f : fonction_numerique) -> float: 
    """Approche dichotomique pour résoudre le pb. 
    @param a : le début de l'intervalle de recherche ;
    @param b : la fin de l'intervalle de recherche ; 
    @param f : la fonction présentant toutes les propriétés voulues.
    """

    while b - a > precision:
        m = (a + b)/2
        if f(a) * f(m) <= 0:
            b = m
        else :
            a = m 

    return (a+b)/2


def methode_par_dichotomie() -> float: 
    """Application de la méthode par dichotomie sur l'intervalle [1 ; 2] avec la fonction 
    à annuler définie plus tôt."""
    return dichotomie(1, 2, fonction_a_annuler)




def fonction_contractante(x:float) -> float:
    return -0.1 * x**2 + 1.0 * x + 0.2

def suite_recurrente(premier_terme: float, f: fonction_numerique) -> float:
    x = premier_terme
    while True:
        xs = f(x)
        if abs(xs-x) < precision:
            return xs
        x = xs
    
def methode_du_point_fixe():
    return suite_recurrente(1.0, fonction_contractante)


def derivee_de_la_fonction_a_annuler(x: float) -> float :
    return 2*x

def Newton(f: fonction_numerique, df: fonction_numerique, a: float) -> float :
    a0 = a
    while True:
        f_a = f(a0)
        fda = df(a0)

        if fda == 0:
            print ("Null")
            return
        a1 = a0 - f_a/fda

        if abs(a1 - a0) < precision:
            return a1
        
        a0 = a1



def methode_par_Newton() -> float:
    return Newton(fonction_a_annuler, derivee_de_la_fonction_a_annuler, 2)


def serie_racine_un_plus_x(x: float) -> float:
    terme = 1.0 
    somme = terme
    n = 0
    while abs(terme) > precision:
        n += 1
        terme *= (0.5 - (n - 1)) / n * x
        somme += terme
    return somme

def methode_de_serie1() -> float : 
    x = 1.0
    resultat = serie_racine_un_plus_x(x)
    return resultat

def methode_de_serie2() -> float:
    x = -0.25/2.25
    facteur = 1.5
    resultat = facteur * serie_racine_un_plus_x(x)
    return resultat

def methode_de_serie3() -> float:
    x = 0.04/1.96
    facteur = 1.4
    resultat = facteur * serie_racine_un_plus_x(x)

    return resultat





if __name__ == "__main__":
    tracer(methode_par_dichotomie)
    tracer(methode_du_point_fixe)
    tracer(methode_par_Newton)
    tracer(methode_de_serie1)
    tracer(methode_de_serie2)
    tracer(methode_de_serie3)

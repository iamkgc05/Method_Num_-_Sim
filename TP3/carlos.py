# h = f(a) + f(b) / 2 + somme de i = 1 à n-1 de f(ai)
# h(somme de i = 0 a n - 1 de f(ai))


from math import sqrt,radians, cos
import matplotlib.pyplot as plt
from collections.abc import Callable


g = 9.8
lf = 1.0
precision = 0.0001

def subdiv_reg(a,b,n):
    liste = []
    nbre_div = (b-a)/n
    x = a
    for i in range(n):
        liste.append(x)
        x+=nbre_div
    liste.append(b)
    return liste


def add(x, zero=0):
    return x 



def int_rectangle(fonction, liste):
    somme = 0
    h = liste[1] - liste[0]
    for i in range (len(liste)-1):
        somme+= fonction(liste[i]) 
    somme*= h

    return somme


def int_trapeze(fonction, liste):
    somme = 0 
    h = liste[1] - liste[0]
    ab = liste[0]+liste[-1]
    final = ab/2
    

    for i in range(1, len(liste) -1):
        somme+= fonction(liste[i]) 
    somme+= final
    somme*= h

    return somme 

def fonctionq5(x): 
    reponse  = sqrt(1 - (x**2))
    return reponse

def estimation_periode(tm, n=1):
    ancienne_estimation = 0 
    erreur = 1
    while erreur > precision: 
        n*=2
        pas = tm/n
        somme = 0
        for i in range(n):
            t = i*pas
            somme += 1/sqrt(cos(t)- cos(tm))
        estimation = 2 * sqrt(2*lf/g) * somme * pas 
        erreur = abs(ancienne_estimation - estimation)
        #print(erreur)
        #print("--------------")
        #print(estimation)
        ancienne_estimation = estimation
    return estimation
    

def init_theta(thmin=1.0, thmax=3.14, n_points=500):

    theta_vals = []
    for i in range(n_points):
        # calcul de chaque theta
        theta = thmin + (thmax - thmin) * i / (n_points - 1)
        theta_vals.append(theta)
    
    return theta_vals

def tracer_periode():
    theta_vals = init_theta()
    T_vals = [estimation_periode(theta) for theta in theta_vals]

    plt.plot(theta_vals, T_vals)
    plt.xlabel(r'$\theta_{\max}$ (radians)')
    plt.ylabel('Période T (secondes)')
    plt.title('Période T en fonction de θ_max pour un pendule')
    plt.show()

def methode_Euler(x0 : float, y0 : float, xN : float, N : int, g : Callable[[float, float], float]) -> list:
    pass





#print(subdiv_reg(1,2,1))
print("Reponse pour n = 100")
l = subdiv_reg(0,1,100)
print(int_rectangle(fonctionq5, l))
print("oooooo")
print(int_trapeze(fonctionq5,l))

print("\n")
print("Reponse pour n = 1000")
l = subdiv_reg(0,1,1000)
print(int_rectangle(fonctionq5, l))
print("oooooo")
print(int_trapeze(fonctionq5,l))

print("\n")
print("Reponse pour n = 10000")
l = subdiv_reg(0,1,10000)
print(int_rectangle(fonctionq5, l))
print("oooooo")
print(int_trapeze(fonctionq5,l))


# theta_max

theta_max = radians(30)
T = estimation_periode(theta_max)
print(f"Période : {T:.6f} s")



# h = f(a) + f(b) / 2 + somme de i = 1 à n-1 de f(ai)
# h(somme de i = 0 a n - 1 de f(ai))


from math import sqrt

g = 9.8
l = 1.0

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




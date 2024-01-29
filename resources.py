def indicator(i):
    return 1 if i else 0


def fonction_Phi_R(n, C):
    resultat = 1
    for j in range(1, n):
        resultat = resultat * min(j, C)
    return resultat
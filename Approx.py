from tkinter import *
from math import factorial
from resources import fonction_Phi_R
import numpy as np

NOMBRE_ITERATIONS = 10


def calcul_approche_1(lh, uh, ur, ud, C, p, N):
    mu = [uh, ur, ud]
    gamma = [lh, lh/p, (1-p)*lh/p]
    rho = [g/u for g, u in zip(gamma, mu)]
    rr = rho[1]
    somme = sum([rr**(i)/fonction_Phi_R(i, C) for i in range(1, NOMBRE_ITERATIONS)])
    pr0 = 1/somme
    
    req_nb_r = sum([i*pr0*rr**i/fonction_Phi_R(i, C) for i in range(1, NOMBRE_ITERATIONS)])
    requetes_nb = [rho[0]/(1-rho[0]), req_nb_r, rho[2]/(1-rho[2])] 
    temps_sejour = [c/g for c, g in zip(requetes_nb, gamma)]
    (temps_sejour_h, temps_sejour_r, temps_sejour_d) = tuple(temps_sejour)
    temps_sejour_r_d = (temps_sejour_r + (1-p)*temps_sejour_d) / p
    temps_sejour_moyen = temps_sejour_h + temps_sejour_r_d
    return (requetes_nb, temps_sejour_moyen, temps_sejour)

def calcul_approche_2(lh, uh, ur, ud, C, p, N):
    mu_h_d = [uh, ud]
    gamma_h_d = [lh, (1-p)*lh/p]
    gamma = [lh, lh/p, (1-p)*lh/p]
    rho_h_d = [g/u for g, u in zip(gamma_h_d, mu_h_d)]
    rho_r = gamma[1]/(C*ur)
    r_nb_h_d = [r/(1-r) for r in rho_h_d]
    req_nb_r = sum([(1-rho_r)*rho_r**i*i for i in range(1, NOMBRE_ITERATIONS)])
    requetes_nb = [r_nb_h_d[0], req_nb_r, r_nb_h_d[1]]
    temps_sejour = [c/g for c, g in zip(requetes_nb, gamma)]
    (temps_sejour_h, temps_sejour_r, temps_sejour_d) = tuple(temps_sejour)
    temps_sejour_moyen = temps_sejour_h + (temps_sejour_r + (1-p)*temps_sejour_d) / p
    return (requetes_nb, temps_sejour_moyen, temps_sejour)

def calcul_approche_3(lh, uh, ur, ud, C, p, N):
    mu = [uh, ur, ud]
    gamma = [lh, lh/p, (1-p)*lh/p]
    rho = [g/u for g, u in zip(gamma, mu)]
    r_nb_h_d = [r/(1-r) for r in [rho[0], rho[2]]]
    rr = rho[1]
    req_nb_r = sum([(np.exp(-rr))*rr**i/factorial(i)*i for i in range(1, NOMBRE_ITERATIONS)])
    requetes_nb = [r_nb_h_d[0], req_nb_r, r_nb_h_d[1]]
    temps_sejour = [requetes_nb[0]/gamma[0], 1/ur, requetes_nb[2]/gamma[2]]
    (temps_sejour_h, temps_sejour_r, temps_sejour_d) = tuple(temps_sejour)
    temps_sejour_moyen = temps_sejour_h + (temps_sejour_r + (1-p)*temps_sejour_d) / p
    return (requetes_nb, temps_sejour_moyen, temps_sejour)

def calcul_et_affichage(fonction_approche):
    lh = float(lh_entry.get())
    uh = float(uh_entry.get())
    ur = float(ur_entry.get())
    ud = float(ud_entry.get())
    C = float(C_entry.get())
    p = float(p_entry.get())
    N = float(N_entry.get())

    resultats = fonction_approche(lh, uh, ur, ud, C, p, N)

    texte_resultat = (
        f"Nombre moyen de requêtes : {resultats[0]}\n"
        f"Temps moyen de séjour : {resultats[1]}\n"
        f"Temps moyen de séjour dans chaque nœud : {resultats[2]}\n"
    )

    result_label.config(text=texte_resultat)

def mise_a_jour_et_calcul(fonction_approche, nom_approche):
    approximation_label.config(text=f"Approximation sélectionnée : {nom_approche}")
    calcul_et_affichage(fonction_approche)

# Create the main window
root = Tk()
root.title("Résultats du Modèle de File d'Attente")

# Create labels and entry fields for parameters
lh_label = Label(root, text="λh:")
lh_label.pack(pady=5)
lh_entry = Entry(root)
lh_entry.pack()

uh_label = Label(root, text="μH:")
uh_label.pack(pady=5)
uh_entry = Entry(root)
uh_entry.pack()

ur_label = Label(root, text="μR:")
ur_label.pack(pady=5)
ur_entry = Entry(root)
ur_entry.pack()

ud_label = Label(root, text="μD:")
ud_label.pack(pady=5)
ud_entry = Entry(root)
ud_entry.pack()

C_label = Label(root, text="C:")
C_label.pack(pady=5)
C_entry = Entry(root)
C_entry.pack()

p_label = Label(root, text="p:")
p_label.pack(pady=5)
p_entry = Entry(root)
p_entry.pack()

N_label = Label(root, text="N:")
N_label.pack(pady=5)
N_entry = Entry(root)
N_entry.pack()
button_frame = Frame(root)
button_frame.pack(pady=10)

# Créer un label pour afficher l'approximation sélectionnée
approximation_label = Label(button_frame, text="Approximation sélectionnée : Aucune", justify=LEFT)
approximation_label.grid(row=1, columnspan=3, pady=5)

button_approche_1 = Button(button_frame, text="Approche 1", command=lambda: mise_a_jour_et_calcul(calcul_approche_1, "Approche 1"), bg="lightblue")
button_approche_1.grid(row=0, column=0, padx=5)

button_approche_2 = Button(button_frame, text="Approche 2", command=lambda: mise_a_jour_et_calcul(calcul_approche_2, "Approche 2"), bg="lightgreen")
button_approche_2.grid(row=0, column=1, padx=5)

button_approche_3 = Button(button_frame, text="Approche 3", command=lambda: mise_a_jour_et_calcul(calcul_approche_3, "Approche 3"), bg="lightcoral")
button_approche_3.grid(row=0, column=2, padx=5)

# Créer un label pour afficher les résultats
result_label = Label(root, text="", justify=LEFT)
result_label.pack(pady=10)

# Lancer la boucle principale
root.mainloop()
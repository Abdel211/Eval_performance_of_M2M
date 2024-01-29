import random
import numpy as np
import tkinter as tk
from resources import indicator
from tkinter import Label, Entry, Button, Frame, Text, Scrollbar

def compute_open_net(l_h, u_h, u_r, u_d, c, p, n):
   
   

    X = [n, 0, 0, 0]
    tours = 100000

    temps_total = 0
    k = 0
    requete_gen = 0
    cust_nb = [0, 0, 0, 0]
    throughput = [0, 0, 0, 0]

    for _ in range(1, tours):
        u = random.uniform(0.0, 1.0)
        max_rate = l_h + u_h * indicator(X[1] > 0) + min(X[2], c) * u_r + u_d * indicator(X[3])
        duree = np.random.exponential(1 / max_rate)
        temps_total += duree
        proba_T_to_H = l_h / max_rate
        proba_H_to_R = u_h * indicator(X[1] > 0) / max_rate
        proba_R_to_D = (1 - p) * u_r * min(X[2], c) / max_rate
        proba_R_to_T = p * u_r * min(X[2], c) / max_rate
        proba_D_to_R = u_d * indicator(X[3] > 0) / max_rate

        cust_nb = [nb + x * duree for nb, x in zip(cust_nb, X)]

        if u <= proba_T_to_H:
            requete_gen += 1
            if X[0] == 0:
                k += 1
            else:
                X[1] += 1
                X[0] -= 1
                throughput[1] += 1
        elif proba_T_to_H <= u <= proba_H_to_R + proba_T_to_H:
            X[2] += 1
            X[1] -= 1
            throughput[2] += 1
        elif proba_H_to_R + proba_T_to_H <= u <= proba_H_to_R + proba_T_to_H + proba_R_to_D:
            X[3] += 1
            X[2] -= 1
            throughput[3] += 1
        elif proba_H_to_R + proba_T_to_H + proba_R_to_D <= u <= proba_H_to_R + proba_T_to_H + proba_R_to_D + proba_R_to_T:
            X[0] += 1
            X[2] -= 1
            throughput[0] += 1
        elif proba_H_to_R + proba_T_to_H + proba_R_to_D + proba_R_to_T <= u <= proba_H_to_R + proba_T_to_H + proba_R_to_D + proba_R_to_T + proba_D_to_R:
            X[2] += 1
            X[3] -= 1
            throughput[2] += 1
        else:
            print("gros souci" + str(u))
            exit()

    p_rejec = k / requete_gen
    cust_nb = [nb / temps_total for nb in cust_nb]
    throughput = [nb / temps_total for nb in throughput]
    sojourns = [c / r if r != 0 else 0 for c, r in zip(cust_nb, throughput)]
    sojourn_h, sojourn_r, sojourn_d = tuple(sojourns[1:])
    sojourn_r_d = (sojourn_r + (1 - p) * sojourn_d) / p
    mean_sojourn = sojourn_h + sojourn_r_d
    return p_rejec, cust_nb, throughput, mean_sojourn, sojourns

def display_open_net_results(p_rejec, cust_nb, mean_sojourn):
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, "Simulation Results (Open Network):\n\n")
    result_text.insert(tk.END, "Probability of Rejection: {:.4f}\n".format(p_rejec))
    result_text.insert(tk.END, "Average number of requests:\n")
    for i, value in enumerate(cust_nb):
        result_text.insert(tk.END, "Customers[{}]: {:.4f}\n".format(i, value))
    result_text.insert(tk.END, "Mean sojourn time: {:.4f}\n".format(mean_sojourn))

def run_open_net_simulation():
    l_h_value = float(entries[0].get())
    u_h_value = float(entries[1].get())
    u_r_value = float(entries[2].get())
    u_d_value = float(entries[3].get())
    c_value = float(entries[4].get())
    p_value = float(entries[5].get())
    n_value = float(entries[6].get())

    (p_rejec, cust_nb, _, mean_sojourn, _) = compute_open_net(l_h_value, u_h_value, u_r_value, u_d_value, c_value, p_value, n_value)
    display_open_net_results(p_rejec, cust_nb, mean_sojourn)
################################################################################################################################################
                                                        # Tkinter # 
root = tk.Tk()
root.title("Open Network Simulation")
main_frame = Frame(root, padx=20, pady=20, bg='#E6E6FA')
main_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
labels = [ "λh:", "μH:", "μR:", "μD:", "C:", "P:","N:"]
for i, label_text in enumerate(labels):
    Label(main_frame, text=label_text, font=('Helvetica', 12), bg='#E6E6FA').grid(row=i, column=0, sticky='w', pady=5)
entries = {}
for i in range(len(labels)):
    entries[i] = Entry(main_frame, font=('Helvetica', 12))
    entries[i].grid(row=i, column=1, pady=5)
Button(main_frame, text="Run Open Network Simulation", font=('Helvetica', 12), command=run_open_net_simulation, bg='red').grid(row=len(labels), columnspan=2, pady=10)
result_text_frame = Frame(root, padx=20, pady=20, bg='#E6E6FA')
result_text_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
result_text = Text(result_text_frame, wrap=tk.WORD, font=('Helvetica', 12), height=20, width=80)
result_text.grid(row=0, column=0)
scrollbar = Scrollbar(result_text_frame, command=result_text.yview)
scrollbar.grid(row=0, column=1, sticky='nsew')
result_text['yscrollcommand'] = scrollbar.set
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
root.geometry('+%d+%d' % ((root.winfo_screenwidth() - root.winfo_reqwidth()) / 2, (root.winfo_screenheight() - root.winfo_reqheight()) / 2))
root.mainloop()

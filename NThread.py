import random
import numpy as np
import tkinter as tk
from resources import indicator
from tkinter import Label, Entry, Button, Frame, Text, Scrollbar


def simulate_closed_system(lambd_h, mu_h, mu_r, mu_d, capacity, probability, initial_threads):

    threads = [initial_threads, 0, 0, 0]
    num_iterations = 10000

    total_time = 0
    rejection_time = 0
    customer_counts = [0, 0, 0, 0]
    request_counts = [0, 0, 0, 0]

    for _ in range(1, num_iterations):
        random_value = random.uniform(0.0, 1.0)
        max_rate = lambd_h * indicator(threads[0] > 0) + mu_h * indicator(threads[1] > 0) + min(threads[2], capacity) * mu_r + mu_d * indicator(threads[3])

        duration = np.random.exponential(1 / max_rate)
        total_time += duration

        prob_t_to_h = lambd_h * indicator(threads[0] > 0) / max_rate
        prob_h_to_r = mu_h * indicator(threads[1] > 0) / max_rate
        prob_r_to_d = (1 - probability) * mu_r * min(threads[2], capacity) / max_rate
        prob_r_to_t = probability * mu_r * min(threads[2], capacity) / max_rate
        prob_d_to_r = mu_d * indicator(threads[3] > 0) / max_rate
        rejection_time += indicator(threads[0] == 0) * duration
        customer_counts = [count + thread * duration for count, thread in zip(customer_counts, threads)]
        if random_value <= prob_t_to_h:
            threads[1] += 1
            threads[0] -= 1
            request_counts[1] += 1
        elif prob_t_to_h < random_value <= prob_h_to_r + prob_t_to_h:
            threads[2] += 1
            threads[1] -= 1
            request_counts[2] += 1
        elif prob_h_to_r + prob_t_to_h < random_value <= prob_h_to_r + prob_t_to_h + prob_r_to_d:
            threads[3] += 1
            threads[2] -= 1
            request_counts[3] += 1
        elif prob_h_to_r + prob_t_to_h + prob_r_to_d < random_value <= prob_h_to_r + prob_t_to_h + prob_r_to_d + prob_r_to_t:
            threads[0] += 1
            threads[2] -= 1
            request_counts[0] += 1
        elif prob_h_to_r + prob_t_to_h + prob_r_to_d + prob_r_to_t < random_value <= prob_h_to_r + prob_t_to_h + prob_r_to_d + prob_r_to_t + prob_d_to_r:
            threads[2] += 1
            threads[3] -= 1
            request_counts[2] += 1
        else:
            print("Unexpected value: " + str(random_value))
            exit()

    rejection_probability = rejection_time / total_time
    avg_customer_counts = [count / total_time for count in customer_counts]
    throughput = [count / total_time for count in request_counts]
    sojourn_times = [customer / rate if rate != 0 else 0 for customer, rate in zip(avg_customer_counts, throughput)]
    (sojourn_h, sojourn_r, sojourn_d) = tuple(sojourn_times[1:])
    sojourn_r_d = (sojourn_r + (1 - probability) * sojourn_d) / probability
    mean_sojourn = sojourn_h + sojourn_r_d

    return rejection_probability, avg_customer_counts, throughput, mean_sojourn, sojourn_times


def display_simulation_results(rejection_probability, avg_customer_counts, mean_sojourn):
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, "Simulation Results:\n")
    result_text.insert(tk.END, "-" * 40 + "\n")
    result_text.insert(tk.END, f"Probability of Rejection: {rejection_probability:.4f}\n")
    result_text.insert(tk.END, "-" * 40 + "\n")
    result_text.insert(tk.END, "Average number of requests:\n")
    for i, value in enumerate(avg_customer_counts):
        result_text.insert(tk.END, f"Customers[{i}]: {value:.4f}\n")
    result_text.insert(tk.END, "-" * 40 + "\n")
    result_text.insert(tk.END, f"Mean sojourn time: {mean_sojourn:.4f}\n")
    result_text.insert(tk.END, "-" * 40 + "\n")
def run_simulation():
    lambd_h_value = float(entries[0].get())
    mu_h_value = float(entries[1].get())
    mu_r_value = float(entries[2].get())
    mu_d_value = float(entries[3].get())
    capacity_value = float(entries[4].get())
    probability_value = float(entries[5].get())
    initial_threads_value = float(entries[6].get())

    (rejection_probability, avg_customer_counts, _, mean_sojourn, _) = simulate_closed_system(
        lambd_h_value, mu_h_value, mu_r_value, mu_d_value, capacity_value, probability_value, initial_threads_value
    )
    display_simulation_results(rejection_probability, avg_customer_counts, mean_sojourn)

#############################################################################################################################################""
                                                            # Tkinter
root = tk.Tk()
root.title("Closed Net Simulation ")
main_frame = Frame(root, padx=20, pady=20, bg='#E6E6FA')
main_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
labels = [ "λh:", "μH:", "μR:", "μD:", "C:", "P:","N:"]

for i, label_text in enumerate(labels):
    Label(main_frame, text=label_text, font=('Helvetica', 12), bg='#E6E6FA').grid(row=i, column=0, sticky='w', pady=5)
entries = {}
for i in range(len(labels)):
    entries[i] = Entry(main_frame, font=('Helvetica', 12))
    entries[i].grid(row=i, column=1, pady=5)
Button(main_frame, text="Run  Closed Net Simulation", font=('Helvetica', 12), command=run_simulation, bg='red').grid(row=len(labels), columnspan=2, pady=10)
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

import random
import time
import numpy as np
from scheptk.scheptk import FlowShop

# Carregamento da instância 
instance = FlowShop("P1.txt")

# Parâmetros da instância 
jobs = instance.jobs
machines = instance.machines
pt_matriz = np.array(instance.pt)

def tempo_processamento(m, j):
    return pt_matriz[m][j]

# Heurística NEH 
def neh(flowshop):
    total_proc_tempo = [(j, sum(tempo_processamento(m, j) for m in range(machines))) for j in range(jobs)]
    jobs_aleatorios = [j for j, _ in sorted(total_proc_tempo, key=lambda x: -x[1])]

    sequence = jobs_aleatorios[:5] 
    if flowshop.Cmax(sequence[::-1]) < flowshop.Cmax(sequence):
        sequence = sequence[::-1]

    for job in jobs_aleatorios[5:]:
        melhor_seq, melhor_cmax = None, float('inf')
        for i in range(len(sequence) + 1):
            trial = sequence[:i] + [job] + sequence[i:]
            cmax = flowshop.Cmax(trial)
            if cmax < melhor_cmax:
                melhor_cmax, melhor_seq = cmax, trial
        sequence = melhor_seq

    return sequence

# Busca local com inserção
def busca_local(flowshop, sequence):
    improved = True
    while improved:
        improved = False
        melhor_cmax = flowshop.Cmax(sequence)

        # Inserção
        for i in range(len(sequence)):
            for j in range(len(sequence)):
                if i != j:
                    new_seq = sequence[:]
                    job = new_seq.pop(i)
                    new_seq.insert(j, job)
                    new_cmax = flowshop.Cmax(new_seq)
                    if new_cmax < melhor_cmax:
                        sequence = new_seq
                        melhor_cmax = new_cmax
                        improved = True

    return sequence

#  Algoritmo Iterated Greedy
def iterated_greedy(flowshop, d=4, T=0.4, tempo_max=60):
    tempo_inicial = time.time()
    sequencia_atual = neh(flowshop)
    melhor = sequencia_atual[:]
    melhor_cmax = flowshop.Cmax(melhor)

    tempo_total = sum(tempo_processamento(m, j) for m in range(machines) for j in range(jobs))
    media_PT = tempo_total / (jobs * machines)
    temperature = T * media_PT / 10

    iter = 0

    while time.time() - tempo_inicial < tempo_max:
        # Destruição
        indices = sorted(random.sample(range(len(sequencia_atual)), d))
        removed_jobs = [sequencia_atual[i] for i in indices]
        pacial = [j for j in sequencia_atual if j not in removed_jobs]

        # Reconstrução
        for job in removed_jobs:
            melhor_pos = None
            melhor_val = float('inf')
            for i in range(len(pacial) + 1):
                trial = pacial[:i] + [job] + pacial[i:]
                cmax = flowshop.Cmax(trial)
                if cmax < melhor_val:
                    melhor_val = cmax
                    melhor_pos = trial
            pacial = melhor_pos

        # Busca local
        improved = busca_local(flowshop, pacial)

        # Critério de aceitação
        delta = flowshop.Cmax(improved) - flowshop.Cmax(sequencia_atual)
        if delta < 0 or random.random() < np.exp(-delta / temperature):
            sequencia_atual = improved[:]
            if flowshop.Cmax(sequencia_atual) < melhor_cmax:
                melhor = sequencia_atual[:]
                melhor_cmax = flowshop.Cmax(melhor)

        iter += 1

        # Log de progresso
        if iter % 100 == 0: 
            print(f"Iteração {iter}: Makespan = {flowshop.Cmax(sequencia_atual)} | Sequência = {sequencia_atual}")

    return melhor, melhor_cmax, iter, time.time() - tempo_inicial

# --- Executa o algoritmo ---
tempo_maximo_segundos = 60
melhor_sequence, melhor_makespan, total_iters, total_time = iterated_greedy(instance, d=4, T=0.4, tempo_max=tempo_maximo_segundos)

# --- Exibe resultado final ---
print("\n========== RESULTADO FINAL ==========")
instance.print_schedule(melhor_sequence)
print(f"\nMelhor makespan encontrado: {melhor_makespan}")
print(f"Melhor sequência: {melhor_sequence}" + str(sum(melhor_sequence)))
print(f"Tempo total: {total_time:.2f} segundos")
print(f"Total de iterações: {total_iters}")

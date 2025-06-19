import random
import time
import numpy as np
from scheptk.scheptk import FlowShop

# Carregamento da instância
instance = FlowShop("P1.txt")

# Parâmetros gerais
tempo_max = 60            # tempo máximo de execução (segundos)
d = 4                     # número de jobs a serem removidos na destruição
T = 0.4                   # parâmetro de temperatura

# Parâmetros da instância
jobs = instance.jobs
machines = instance.machines
pt_matriz = np.array(instance.pt)

def neh(flowshop):
    # Soma dos tempos de cada job (coluna)
    somas = pt_matriz.sum(axis=0)
    jobs_ordenados = [int(i) for i in np.argsort(-somas)]

    # Inicializa sequência com os dois primeiros jobs
    sequence = jobs_ordenados[:2]
    if flowshop.Cmax(sequence[::-1]) < flowshop.Cmax(sequence):
        sequence = sequence[::-1]

    # Insere os demais jobs na melhor posição
    for job in jobs_ordenados[2:]:
        melhor_seq = None
        melhor_cmax = float('inf')
        for i in range(len(sequence) + 1):
            tentativa = sequence[:i] + [job] + sequence[i:]
            cmax = flowshop.Cmax(tentativa)
            if cmax < melhor_cmax:
                melhor_cmax = cmax
                melhor_seq = tentativa
        sequence = melhor_seq

    return sequence

def busca_local(flowshop, sequence):
    improved = True
    while improved:
        improved = False
        melhor_cmax = flowshop.Cmax(sequence)

        for i in range(len(sequence)):
            for j in range(len(sequence)):
                if i != j:
                    nova_seq = sequence[:]
                    job = nova_seq.pop(i)
                    nova_seq.insert(j, job)
                    new_cmax = flowshop.Cmax(nova_seq)

                    if new_cmax < melhor_cmax:
                        sequence = nova_seq
                        melhor_cmax = new_cmax
                        improved = True

    return sequence

def iterated_greedy(flowshop, d=4, T=0.4, tempo_max=60):
    inicio = time.time()

    # Solução inicial com NEH
    sequencia_atual = neh(flowshop)
    melhor = sequencia_atual[:]
    melhor_cmax = flowshop.Cmax(melhor)

    # Cálculo da temperatura inicial
    tempo_total = pt_matriz.sum()
    media_PT = tempo_total / (jobs * machines)
    temperatura = T * media_PT / 10

    iteracao = 0

    while time.time() - inicio < tempo_max:
        # Destruição
        indices_removidos = sorted(random.sample(range(len(sequencia_atual)), d))
        jobs_removidos = [sequencia_atual[i] for i in indices_removidos]
        parcial = [job for job in sequencia_atual if job not in jobs_removidos]

        # Reconstrução
        for job in jobs_removidos:
            melhor_pos = None
            melhor_val = float('inf')

            for i in range(len(parcial) + 1):
                tentativa = parcial[:i] + [job] + parcial[i:]
                cmax = flowshop.Cmax(tentativa)

                if cmax < melhor_val:
                    melhor_val = cmax
                    melhor_pos = tentativa

            parcial = melhor_pos

        # Busca local
        melhorado = busca_local(flowshop, parcial)

        # Critério de aceitação
        delta = flowshop.Cmax(melhorado) - flowshop.Cmax(sequencia_atual)
        if delta < 0 or random.random() < np.exp(-delta / temperatura):
            sequencia_atual = melhorado[:]
            if flowshop.Cmax(sequencia_atual) < melhor_cmax:
                melhor = sequencia_atual[:]
                melhor_cmax = flowshop.Cmax(melhor)

        iteracao += 1

        # Log de progresso
        print(f"Iteração {iteracao:>3}: Makespan = {flowshop.Cmax(sequencia_atual)} | Sequência = {sequencia_atual}")

    duracao = time.time() - inicio
    return melhor, melhor_cmax, iteracao, duracao

melhor_sequence, melhor_makespan, total_iters, total_time = iterated_greedy(
    instance, d=d, T=T, tempo_max=tempo_max)

print("\n========== RESULTADO FINAL ==========")
instance.print_schedule(melhor_sequence)
print(f"\nMelhor makespan encontrado: {melhor_makespan}")
print(f"Melhor sequência: {melhor_sequence}")
print(f"Tempo total: {total_time:.2f} segundos")
print(f"Total de iterações: {total_iters}")

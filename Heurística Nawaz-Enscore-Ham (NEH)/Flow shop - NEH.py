import numpy as np
from scheptk.scheptk import FlowShop

# Algoritmo NEH (Nawaz-Enscore-Ham) para o problema de Flow Shop
instance = FlowShop('P1.txt')
num_jobs = instance.jobs
num_machines = instance.machines

# PASSO 1: soma dos tempos de cada job em todas as máquinas
pt_matriz = np.array(instance.pt)
somas = pt_matriz.sum(axis=0)  # Soma dos tempos de cada job (coluna)

# PASSO 2: ordenar jobs por ordem descrescente de soma
ordem_jobs = list(np.argsort(-somas))

# FUNÇÃO: inserção com o melhor makespan
def melhor_insercao(sequencia, job):
    melhor_seq = None
    melhor_cmax = float('inf')

    for i in range(len(sequencia) + 1):
        nova_seq = sequencia[:i] + [job] + sequencia[i:]
        cmax = instance.Cmax(nova_seq)

        if cmax < melhor_cmax:
            melhor_cmax = cmax
            melhor_seq = nova_seq

    return melhor_seq

# PASSO 3: inicialização com os dois primeiros jobs na melhor ordem
seq_atual = ordem_jobs[:2]
if instance.Cmax(seq_atual[::-1]) < instance.Cmax(seq_atual):
    seq_atual = seq_atual[::-1]

# PASSO 4: inserção dos demais jobs
for job in ordem_jobs[2:]:
    seq_atual = melhor_insercao(seq_atual, job)

# Resultado final
makespan_final = instance.Cmax(seq_atual)
instance.print_schedule(seq_atual)

print("\n========== RESULTADO FINAL ==========")
print(f"Melhor sequência encontrada (NEH): {list(map(int, seq_atual))}")
print(f"Makespan final: {makespan_final}")
import numpy as np
from scheptk.scheptk import FlowShop

# Carrega a instânciak
instance = FlowShop('C:/Users/atila/OneDrive/Área de Trabalho/VScode - Flow shop/Instâncias/P1.txt')
num_jobs = instance.jobs
num_machines = instance.machines

# Passo 1: Calcular soma dos tempos de processamento de cada job em todas as máquinas
pt_matriz = np.array(instance.pt)  
somas = pt_matriz.sum(axis=0)  # soma por coluna (job)

# Passo 2: Ordenar os jobs por soma decrescente
ordem_jobs = list(np.argsort(-somas))  # índices ordenados decrescentemente

# Passo 3: Inicializar sequência com os dois primeiros jobs na melhor ordem
def melhor_insercao(seq, job):
    # insere 'job' em todas as posições de 'seq' e retorna a melhor sequência (menor makespan).
    melhor_seq = None
    melhor_cmax = float('inf')
    for i in range(len(seq) + 1):
        nova_seq = seq[:i] + [job] + seq[i:]
        cmax = instance.Cmax(nova_seq)
        if cmax < melhor_cmax:
            melhor_cmax = cmax
            melhor_seq = nova_seq
    return melhor_seq

# Inicialização com os 5 primeiros
seq_atual = ordem_jobs[:2] 
# Testa as duas possíveis ordens
if instance.Cmax(seq_atual[::-1]) < instance.Cmax(seq_atual):
    seq_atual = seq_atual[::-1]

# Passo 4: Inserir os demais jobs um por um na melhor posição
for job in ordem_jobs[2:]: 
    seq_atual = melhor_insercao(seq_atual, job)

# Resultado final
instance.print_schedule(seq_atual)
makespan_final = instance.Cmax(seq_atual)
seq_atual = [int(x) for x in seq_atual]

print("\n========== RESULTADO FINAL ==========")
print(f'Melhor sequência encontrada (NEH): {seq_atual}')
print(f'Makespan final: {makespan_final}')
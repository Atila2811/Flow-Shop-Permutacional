import time
from random import randint, shuffle
from scheptk.scheptk import FlowShop

# Carregar instância
instance = FlowShop('P1.txt')

# Função para calcular o makespan
def makespan(seq):
    return instance.Cmax(seq)

# Parâmetro de tempo
tempo_limite = 60
inicio = time.time()

# Melhor resultado global
melhor_seq_global = None
melhor_makespan_global = float('inf')
contador_tentativas = 0

# Loop até atingir o tempo limite
while time.time() - inicio < tempo_limite:
    # Gera uma sequência aleatória
    seq_aleatoria = list(range(instance.jobs))
    shuffle(seq_aleatoria)
    melhor_seq = seq_aleatoria.copy()
    melhor_makespan = makespan(melhor_seq)

    # Busca local simples com trocas aleatórias
    for i in range(1000):  # quantidade de trocas aleatórias por lista
        nova_seq = melhor_seq.copy()
        i, j = randint(0, instance.jobs - 1), randint(0, instance.jobs - 1)
        while i == j:
            j = randint(0, instance.jobs - 1)
        nova_seq[i], nova_seq[j] = nova_seq[j], nova_seq[i]
        nova_makespan = makespan(nova_seq)

        if nova_makespan < melhor_makespan:
            melhor_seq = nova_seq
            melhor_makespan = nova_makespan

    contador_tentativas += 1
    print(f"Tentativa {contador_tentativas}: Makespan = {melhor_makespan}")

    # Atualiza o melhor global
    if melhor_makespan < melhor_makespan_global:
        melhor_makespan_global = melhor_makespan
        melhor_seq_global = melhor_seq

# Resultado final
print("\n========== RESULTADO FINAL ==========")
print("Melhor sequência encontrada:", melhor_seq_global)
print("Melhor makespan:", melhor_makespan_global)
print("Número de tentativas executadas:", contador_tentativas)

import time
processo_atual = None
tempo_acesso = None
fila_espera = []

def requisitar_acesso(processo):
    global processo_atual
    global tempo_acesso
    global fila_espera

    # Adiciona o processo à fila de espera se a região crítica já estiver sendo acessada
    if processo_atual != None:
        fila_espera.append(processo)
        print(f"Processo {processo} adicionado à fila de espera.")
        return

    # Atribui o processo atual e o tempo de acesso
    processo_atual = processo
    tempo_acesso = time.time()
    print(f"Processo {processo} acessando a região crítica.")

def liberar_acesso(processo):
    global processo_atual
    global tempo_acesso
    global fila_espera

    # Verifica se o processo atual é o mesmo que está liberando o acesso
    if processo_atual != processo:
        print(f"Processo {processo} tentou liberar acesso indevidamente.")
        return

    print(f"Processo {processo} liberou acesso à região crítica após {time.time() - tempo_acesso} segundos.")

    # Atribui o próximo processo da fila de espera à variável processo_atual
    if len(fila_espera) > 0:
        processo_atual = fila_espera.pop(0)
        tempo_acesso = time.time()
        print(f"Processo {processo_atual} acessando a região crítica a partir da fila de espera.")
    else:
        processo_atual = None

class ContaBancaria:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial

    def depositar(self, valor, processo):
        requisitar_acesso(processo)
        print(f"Processo {processo} realizando depósito no valor de {valor}.")
        self.saldo += valor
        print(f"saldo atual: {self.saldo}")
        time.sleep(2)
        liberar_acesso(processo)

    def retirar(self, valor, processo):
        if valor > self.saldo:
            print(f"Processo {processo} tentou retirar {valor} mas o saldo é de {self.saldo}.")
            print("Saldo insuficiente")
        else:
            requisitar_acesso(processo)
            print(f"Processo {processo} realizando retirada no valor de {valor}.")
            self.saldo -= valor
            print(f"saldo atual: {self.saldo}")
            time.sleep(4)
            liberar_acesso(processo)

conta = ContaBancaria(1000)
conta.depositar(500, "P1")
conta.retirar(200, "P2")
conta.retirar(200, "P3")
conta.retirar(1200, "P4")

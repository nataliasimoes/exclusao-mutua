import time
from threading import Thread, Lock


class ContaBancaria:
    # Inicializa a conta bancária com um saldo inicial
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial

        self.processo_atual = None

        # Fila de espera para os processos como dicionários. Ex: {'func': func, 'args': args}
        self.fila_espera = []

        # Variável que indica se o monitor deve continuar verificando a fila de espera
        self.continuar_observando = True
        self.esperando = False
        # Inicia a thread que observa a fila de espera
        Thread(target=self.observar_fila).start()

    def fechar(self):
        print("Fechando a conta...")
        self.continuar_observando = False

    def observar_fila(self):
        while self.continuar_observando:
            # a cada 1 segundo verifica se a fila de espera não está vazia
            time.sleep(1)
            # Se a fila de espera não estiver vazia e não houver nenhum processo sendo executado
            if len(self.fila_espera) > 0:
                self.esperando = False  # Indica que não está mais esperando
                if not self.processo_atual or not self.processo_atual.is_alive():
                    # Se não houver nenhum processo sendo executado, pega o próximo da fila de espera e executa
                    proximo = self.fila_espera.pop(0)
                    self.execute(proximo)

            elif not self.esperando:
                self.esperando = True
                print("Aguardando Movimentações...")

    def execute(self, proximo):
        self.processo_atual = Thread(
            target=proximo['func'], args=proximo['args'])
        self.processo_atual.start()

    def add_a_fila(self, func, args):
        self.fila_espera.append({'func': func, 'args': args})

    def depositar(self, valor, processo):
        self.add_a_fila(self._depositar, (valor, processo))

    def retirar(self, valor, processo):
        self.add_a_fila(self._retirar, (valor, processo))

    def _depositar(self, valor, processo):
        print(f"Processo {processo} realizando depósito no valor de {valor}.")
        self.saldo += valor
        print(f"saldo atual: {self.saldo}")
        time.sleep(2)

    def _retirar(self, valor, processo):
        if valor > self.saldo:
            print(
                f"Processo {processo} tentou retirar {valor} mas o saldo é de {self.saldo}.")
            print("Saldo insuficiente")
        else:
            print(
                f"Processo {processo} realizando retirada no valor de {valor}.")
            self.saldo -= valor
            print(f"saldo atual: {self.saldo}")
            time.sleep(4)


conta = ContaBancaria(1000)
time.sleep(3)
conta.depositar(500, "P1")
conta.retirar(200, "P2")
conta.retirar(200, "P3")
conta.retirar(1200, "P4")

input()
conta.fechar()

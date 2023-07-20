from abc import ABC, abstractmethod
from datetime import datetime

# Classe Cliente representa um cliente que pode ter várias contas associadas a ele.
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    # Método para registrar uma transação em uma conta específica.
    def registrar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    # Método para incluir uma nova conta associada ao cliente.
    def incluir_conta(self, conta):
        self.contas.append(conta)


# Classe PessoaFisica é uma subclasse de Cliente e representa um cliente do tipo pessoa física.
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


# Classe Conta representa uma conta bancária genérica.
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    # Método estático para criar uma nova conta para um cliente.
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    # Propriedade que retorna o saldo da conta.
    @property
    def saldo(self):
        return self._saldo

    # Propriedade que retorna o número da conta.
    @property
    def numero(self):
        return self._numero

    # Propriedade que retorna a agência da conta.
    @property
    def agencia(self):
        return self._agencia

    # Propriedade que retorna o cliente associado à conta.
    @property
    def cliente(self):
        return self._cliente

    # Propriedade que retorna o histórico da conta.
    @property
    def historico(self):
        return self._historico

    # Método para sacar um valor da conta.
    def sacar_valor(self, valor):
        saldo = self._saldo
        sem_saldo = valor > saldo

        if sem_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif valor > 0:
            self._saldo -= saldo
            print("\n=== O saque foi realizado com sucesso! ===")
            return True
        else:
            print("Houve uma falha na operação, informe um valor válido")

        return False

    # Método para depositar um valor na conta.
    def depositar_valor(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Seu depósito foi realizado com sucesso! ===")
        else:
            print("Houve uma falha na operação, informe um valor válido")
            return False

        return True


# Classe ContaCorrente é uma subclasse de Conta e representa uma conta corrente específica.
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    # Método para sacar um valor da conta corrente, levando em consideração o limite de saques e limite de saldo.
    def sacar_valor(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] ==
            Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar_valor(valor)

        return False

    # Método que retorna uma representação em formato de string da conta corrente.
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


# Classe Historico representa o histórico de transações de uma conta.
class Historico:
    def __init__(self):
        self._transacoes = []

    # Propriedade que retorna a lista de transações do histórico.
    @property
    def transacoes(self):
        return self._transacoes

    # Método para inserir uma transação no histórico.
    def inserir_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


# Classe abstrata Transacao é uma classe base para transações genéricas.
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass


# Classe Saque é uma subclasse de Transacao e representa uma transação de saque.
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    # Método para registrar um saque na conta.
    def registrar(self, conta):
        sucesso_transacao = conta.sacar_valor(self.valor)
        if sucesso_transacao:
            conta.historico.inserir_transacao(self)


# Classe Deposito é uma subclasse de Transacao e representa uma transação de depósito.
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    # Método para registrar um depósito na conta.
    def registrar(self, conta):
        sucesso_transacao = conta.depositar_valor(self.valor)
        if sucesso_transacao:
            conta.historico.inserir_transacao(self)

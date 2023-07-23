"""
Projeto com sqlalchemy com SQlite
Marcos Aurélio Leonel
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import select

Base = declarative_base()

class Client(Base):
    """
    Classe que representa a tabela 'client' (cliente) no banco de dados.

    Atributos:
    id (int): Chave primária para o cliente.
    name (str): Nome do cliente.
    cpf (str): CPF do cliente.
    address (str): Endereço do cliente.

    Métodos:
    __repr__(): Retorna uma representação em string do cliente.
    """
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String(9), unique=True, autoincrement=True)
    address = Column(String(100))

    def __repr__(self) -> str:
        return f"""
                    Cliente

        Nome: {self.name} - ID: {self.id}
        CPF: {self.cpf}
        ENDEREÇO(s): {self.address}

        """


class Account(Base):
    """
    Classe que representa a tabela 'account' (conta) no banco de dados.

    Atributos:
    id (int): Chave primária para a conta.
    acc_type (str): Tipo da conta (e.g., conta corrente, conta poupança).
    agency (str): Agência da conta (padrão é "0001").
    acc_num (int): Número da conta (deve ser único).
    credit (float): Saldo da conta.
    id_client (int): Chave estrangeira referenciando o ID do cliente associado a esta conta.

    Métodos:
    __repr__(): Retorna uma representação em string da conta.
    """
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    acc_type = Column(String, autoincrement=True)
    agency = Column(String, default="0001")
    acc_num = Column(Integer, unique=True)
    credit = Column(Float)
    id_client = Column(Integer, ForeignKey("client.id"), nullable=False)

    def __repr__(self) -> str:
        return f"""
                    Conta

        TIPO DA CONTA: {self.acc_type} - ID: {self.id}
        AGÊNCIA: {self.agency} - NUM. DA CONTA: {self.acc_num}

        SALDO: {self.credit}    ID DO CLIENTE: {self.id_client}

        """


engine = create_engine("sqlite://")
Base.metadata.create_all(engine)

with Session(engine) as session:
    marcos = Client(
        name="Marcos Aurélio",
        cpf="123456789",
        address="Rua Desembarcador Juliano Alves 400, Pirangi Natal/RN",
    )

    mayara = Client(
        name="Mayara Maia",
        cpf="10111213141",
        address="Rua Jogador Alberi 1400, Candelaria Natal/RN",
    )

    marcos_acc = Account(
        acc_type="conta corrente",
        agency="0001",
        acc_num=7415876329,
        credit=500.0,
        id_client=1,
    )

    mayara_acc = Account(
        acc_type="conta poupança",
        agency="0001",
        acc_num=369852147,
        credit=1000.0,
        id_client=2,
    )

    session.add(marcos)
    session.add(mayara)
    session.add(marcos_acc)
    session.add(mayara_acc)
    session.commit()

    # Consultas

    # Consulta 1
    client_id_statement = select(Client.id).where(Client.name == "Marcos Aurélio")
    client_id = session.scalar(client_id_statement)

    acc_corrente_statement = select(Account).where(Account.acc_type == "conta corrente").where(
        Account.id_client == client_id)
    acc_corrente = session.scalar(acc_corrente_statement)

    print(f"\nConta corrente do cliente {marcos.name}:\n{acc_corrente}")

    # Consulta 2
    acc_poupanca_statement = select(Account).where(
                             Account.acc_type == "conta poupança").where(Account.id_client == 2)
    acc_poupanca = session.scalar(acc_poupanca_statement)

    print(f"Conta poupança do cliente {mayara.name}:\n{acc_poupanca}")

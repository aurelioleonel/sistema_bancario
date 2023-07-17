"""
 Fomos contratados por um grande banco para desenvolver o seu novo sistema.
 Esse banco deseja modernizar suas operações e para isso escolheu a linguagem Python.
 Para a primeira versão do sistema devemos implementar apenas 3 operações: depósito, saque e extrato.

 Marcos Aurélio Leonel
"""

import datetime

menu = """
[ D ] Depositar
[ S ] Sacar
[ E ] Extrato
[ Q ] Sair
"""

saldo = 0
limite = float(500)
extratos_bancarios = {
    "Extrato de Deposito": [],
    "Extrato de Saques": [],
    "Extrato Geral": []
}
numeros_saques = 0
LIMITE_SAQUES = 3
data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # DATA atual e hora

while True:
    opcao = input(menu)

    if opcao.upper() == "D":
        valor_deposito = float(input("Valor de deposito: R$ "))  # Solicita o valor do depósito
        if valor_deposito > 0:
            saldo += valor_deposito  # Atualiza o saldo com o valor do depósito
            extratos_bancarios["Extrato de Deposito"].append(f"Data: {str(data)} - Deposito: R$ {valor_deposito:.2f}")  # Adiciona o registro do depósito ao extrato
            extratos_bancarios["Extrato Geral"].append(f"Data: {str(data)} - Deposito: R$ {valor_deposito:.2f}")  # Adiciona o registro do depósito ao extrato geral
        else:
            print("Operação falhou!, Depositar acima de R$ 0")

    elif opcao.upper() == "S":
        if numeros_saques < LIMITE_SAQUES:
            valor_saque = float(input("Valor de saque: R$ "))  # Solicita o valor do saque
            if valor_saque > 0:
                if valor_saque <= limite and valor_saque <= saldo:  # Verifica se o valor do saque é válido
                    extratos_bancarios["Extrato de Saques"].append(f"Data: {str(data)} - Saque: R$ {valor_saque:.2f}")  # Adiciona o registro do saque ao extrato de saques
                    extratos_bancarios["Extrato Geral"].append(f"Data: {str(data)} - Saque: R$ {valor_saque:.2f}")  # Adiciona o registro do saque ao extrato geral
                    print("Saque Realizado com Sucesso!")
                    numeros_saques += 1
                    saldo -= valor_saque  # Decrementa o saldo a cada saque
                elif valor_saque > saldo:
                    print("O cliente não tem valor suficiente para o saque.")
                    print("Por favor retire um extrato para verificar seu saldo atual")
                else:
                    print(f"O limite de saque é de {limite:.2f}")
            else:
                print("Você deve informar um valor de saque válido!")
        else:
            print("Você não pode efetuar o saque, você excedeu o limite diário (3 saques)")

    elif opcao.upper() == "E":  # Sub menu da opção extrato
        while True:
            opcao_de_estrato = int(input("""
    ESCOLHA UMA OPÇÃO DE EXTRATO        
    [ 1 ] Geral
    [ 2 ] Saques
    [ 3 ] Depósitos
    [ 4 ] Sair
    """))

            if opcao_de_estrato == 1:
                if len(extratos_bancarios["Extrato Geral"]) == 0:
                    print(f'Não ha extratos na data {data}')

                for extrato_geral in extratos_bancarios["Extrato Geral"]:
                    print(extrato_geral)

            if opcao_de_estrato == 2:
                if len(extratos_bancarios["Extrato de Saques"]) == 0:
                    print(f'Não ha saques na data {data}')

                for extrato_saque in extratos_bancarios["Extrato de Saques"]:
                    print(extrato_saque)

            if opcao_de_estrato == 3:
                if len(extratos_bancarios["Extrato de Deposito"]) == 0:
                    print(f'Não ha depositos na data {data}')

                for extrato_deposito in extratos_bancarios["Extrato de Deposito"]:
                    print(extrato_deposito)

            if opcao_de_estrato == 4:
                break
            print(f"Seu saldo atual é R$ {saldo:.2f} em {data}")
    elif opcao.upper() == "Q":
        break

    else:
        print("Operação inválida, por favor digite uma opção válida.")
print("Obrigado por usar nosso sistema. Volte sempre!")




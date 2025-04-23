import sys
from datetime import datetime
import time


banco = "Banco Lone"  # Aqui seu dinheiro neinguém come!
option_1 = "Digite [d] para depositar"
option_2 = "Digite [s] para sacar"
option_3 = "Digite [e] para ver o extrato"
option_4 = "Digite [x] para sair"

banco, option_1, option_2, option_3, option_4 = banco.center(29, "."), option_1.center(29), option_2.center(
    29), option_3.center(29), option_4.center(29)
option_1, option_2, option_3, option_4 = option_1.lstrip(), option_2.lstrip(), option_3.lstrip(), option_4.lstrip()

nome_usuario = input("Qual é o seu nome?").strip().title()
nome_usuario = "Olá {nome}, seja bem vindo!".format(nome=nome_usuario)
saldo = 10.0
limite_saque = 500
limite_transacoes_diarias = 10
qtd_transacoes_do_dia = 0
limite_saque_diario = 3
qtd_saques_do_dia = 0
extrato = []

menu = """
    %s \n
    #############################
    %s

    %s
    %s
    %s
    %s

    %s
    #############################

""" % (nome_usuario, banco, option_1, option_2, option_3, option_4, "." * 29)

menu_apenas_com_extrato = """
    %s \n
    #############################
    %s
    
    %s
    %s
    
    %s
    #############################
""" % (nome_usuario, banco, option_3, option_4, "." * 29)


def depositar_dinheiro(** saldo):
    while True:
        valor_deposito = int(input("Qual valor você deseja depositar?"))

        if type(valor_deposito) != int or valor_deposito <= 0:
            print("\nOpção invalida, por favor escolha novamente\n")
            continue

        saldo_anterior = saldo
        saldo += valor_deposito
        escrever_extrato("deposito", (saldo_anterior, saldo))
        print("Tudo certo! Seu saldo aumentou R${1}.00, seu saldo atual é de: R${0}".format(saldo, valor_deposito))
        return saldo


def sacar_dinheiro(saldo, /):
    while True:
        valor_sacar = int(input("Qual valor você deseja sacar?"))

        if saldo < valor_sacar:
            print("Saldo insuficiente (seu saldo é de R${}), por favor, escolha outro valor!".format(saldo))
            continue
        elif valor_sacar >= limite_saque:
            print("Limite de saque de R$%d.00 atingido, por favor, escolha um valor menor!" % limite_saque)
            continue
        elif type(valor_sacar) != int or valor_sacar <= 0:
            print("\nOpção invalida, por favor escolha novamente\n")
            continue
        else:
            saldo_anterior = saldo
            saldo -= valor_sacar
            print("Saque de R$%d.00 concluido com sucesso!" % valor_sacar)
            escrever_extrato("saque", valores=(saldo_anterior, saldo), valor_sacar=valor_sacar)
            return saldo


def escrever_extrato(transacao, /, valores: tuple, *, valor_sacar=0) -> None:
    saldo_anterior, saldo_atual = valores
    data_e_hora = datetime.now().strftime("%d/%m/%Y às %H:%M")
    dic = {"saque": valor_sacar, "data": data_e_hora, "saldo_anterior": round(saldo_anterior),
           "saldo_atual": round(saldo_atual)} if transacao == "saque" else {
        "deposito": int(saldo_atual - saldo_anterior), "data": data_e_hora, "saldo_anterior": round(saldo_anterior),
        "saldo_atual": round(saldo_atual)}
    extrato_texto = "saque de R${saque}.00 realizado no dia {data}, seu saldo foi de R${saldo_anterior}.00 para R${saldo_atual}.00".format(
        **dic) if transacao == "saque" else "deposito de R${deposito}.00 realizado no dia {data}, seu saldo foi de R${saldo_anterior}.00 para R${saldo_atual}.00".format(
        **dic)
    extrato.append(extrato_texto)


def sair_do_programa_ou_voltar_ao_menu(mostrar_opcao__extrato=True):
    option_1 = "Digite [q] para voltar ao menu anterior".center(29)
    option_2 = "Digite [e] para abrir o extrato".center(
        29) if mostrar_opcao__extrato is True else "Digite [x] para fechar o programa".center(29)
    option_3 = "Digite [x] para fechar o programa".center(29) if mostrar_opcao__extrato is True else ""

    menu = """
        {pergunta} \n
        #############################
        {banco}

        {option_1}
        {option_2}
        {option_3}

        {pontos}
        #############################

    """.format(**{"pergunta": "Você deseja voltar para ao menu anterior ou fechar o programa?", "banco": banco,
                  "option_1": option_1, "option_2": option_2, "option_3": option_3, "pontos": "." * 29})

    while True:
        escolha_menu = input(menu)

        if escolha_menu == "q" or escolha_menu == "e" or escolha_menu == "x":
            return escolha_menu
        else:
            print("Opção invalida, por favor escolha novamente")
            continue


while True:
    limite_transacoes_diarias_atingido = qtd_transacoes_do_dia >= limite_transacoes_diarias
    if limite_transacoes_diarias_atingido:
        print("Desculpe, mas você já ultrapassou o limite de transações diárias de hoje, volte novamente amanhã!")
        escolha = input(menu_apenas_com_extrato)
    else:
        escolha = input(menu)

    if escolha == "d" and not limite_transacoes_diarias_atingido:
        saldo = depositar_dinheiro(saldo=saldo)
        qtd_transacoes_do_dia += 1

        escolha_2 = sair_do_programa_ou_voltar_ao_menu()
        if escolha_2 == "q":
            continue
        elif escolha_2 == "e":
            escolha = "e"
        else:
            escolha = "x"

    elif escolha == "s" and not limite_transacoes_diarias_atingido:
        if qtd_saques_do_dia >= limite_saque_diario:
            print("Limite de saque diario atingido, por favor, volte amanhã!")
            continue

        saldo = sacar_dinheiro(saldo)
        qtd_saques_do_dia += 1
        qtd_transacoes_do_dia += 1

        escolha_2 = sair_do_programa_ou_voltar_ao_menu()
        if escolha_2 == "q":
            continue
        elif escolha_2 == "e":
            escolha = "e"
        else:
            escolha = "x"

    if escolha == "e":
        if not extrato:
            print("Ops, pelo jeito você ainda não vez nenhuma transação, volte aqui quando fazer uma!")
            continue

        extrato_texto = ""
        for i in extrato:
            extrato_texto += "\n" + "|"
            extrato_texto += (" " * 7) + i

        print("Aqui está seu extato: %s" % extrato_texto)
        escolha_2 = sair_do_programa_ou_voltar_ao_menu(mostrar_opcao__extrato=False)
        if escolha_2 == "q":
            continue
        else:
            escolha = "x"

    if escolha == "x":
        print("Fechando o sistema.")
        time.sleep(1)
        print("Fechando o sistema..")
        time.sleep(1)
        print("Fechando o sistema...")
        time.sleep(1)
        sys.exit()

    else:
        print("Opção invalida, por favor escolha novamente")
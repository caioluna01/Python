clientes = []
agendamentos = []

while True:
    print("\nAGENDA")
    print("1 - Cadastrar cliente")
    print("2 - listar clientes")
    print("3 - sair")

    opcao = input("Escolha: ")

    if opcao == "1":
        nome = input("Digite o seu nome: ")
        telefone = input("Digite o seu telefone: ")
        cpf = input("Digite o seu cpf: ")
        cliente = {"Nome":  nome, "telefone": telefone, "cpf": cpf}
        clientes.append(cliente)  
        print("Cliente cadastrado com sucesso!") 
    

    elif opcao == "2":
        if not clientes:
            print("Nenhum cliente cadastrado")
        else:
            print("\nLISTA DE CLIENTES:")
            for cliente in clientes:
                print(f"Nome: {cliente['Nome']}")
                print(f"Telefone: {cliente['telefone']}")
                print(f"CPF: {cliente['cpf']}")
                
    elif opcao == "3":
        break 

    else:
        print("opção invalida:")

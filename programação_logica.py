print('Bem vindo ao Aki, empresa segurada em desenvolvimento web, realize o cadastro para se inscrever no curso')

# NOME
while True:
    nome = input('Escreva o seu nome: ')
    if nome.replace(' ', '').isalpha():
        break
    else:
        print('Digite apenas letras para o nome.')

# CPF 
while True:
    cpf = input('Escreva o seu CPF (11 números): ')
    if cpf.isdigit() and len(cpf) == 11:
        
        cpf_formatado = cpf[:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:]
        break
    else:
        print('CPF inválido. Digite exatamente 11 números.')

# ENDEREÇO
while True:
    endereco = input('Escreva o seu endereço: ')
    if endereco.replace(' ', '').isalpha():
        break
    else:
        print('Digite apenas letras para o endereço.')

# IDADE
while True:
    try:
        idade = int(input('Escreva sua idade: '))
        if idade > 0 and idade < 150:  
            break
        else:
            print('Idade inválida.')
    except ValueError:
        print('Digite apenas números.')

# ALTURA
while True:
    try:
        altura = float(input('Escreva sua altura (ex: 1.75): '))
        if altura > 0 and altura < 3:
            break
        else:
            print('Altura inválida.')
    except ValueError:
        print('Use ponto (ex: 1.75)')

# TELEFONE 
    telefone = input('Escreva seu telefone (10 ou 11 números): ')
    if telefone.isdigit() and (len(telefone) == 10 or len(telefone) == 11):
        if len(telefone) == 10:
            tel_formatado = '(' + telefone[:2] + ') ' + telefone[2:6] + '-' + telefone[6:]
        else:
            tel_formatado = '(' + telefone[:2] + ') ' + telefone[2:7] + '-' + telefone[7:]
        break
    else:
        print('Telefone inválido.')

print('Seu nome cadastrado é:', nome)
print('Seu CPF registrado é:', cpf_formatado)
print('Seu endereço é:', endereco)
print('Sua idade registrada é:', idade, 'anos')
print('Sua altura registrada é:', altura, 'metros')
print('Seu telefone registrado é:', tel_formatado)
print('Muito obrigado por se cadastrar!')
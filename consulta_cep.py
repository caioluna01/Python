import requests
import json
import os
from datetime import datetime

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def consultar_cep(cep):
    cep_limpo = cep.replace('-', '').replace('.', '').strip()
    
    if not cep_limpo.isdigit() or len(cep_limpo) != 8:
        return {'erro': 'CEP inválido. Digite 8 números.'}
    
    url = f'https://viacep.com.br/ws/{cep_limpo}/json/'
    
    try:
        resposta = requests.get(url, timeout=10)
        dados = resposta.json()
        
        if 'erro' in dados:
            return {'erro': 'CEP não encontrado.'}
        
        return {
            'cep': dados['cep'],
            'logradouro': dados.get('logradouro', 'Não informado'),
            'bairro': dados.get('bairro', 'Não informado'),
            'cidade': dados.get('localidade', 'Não informado'),
            'estado': dados.get('uf', 'Não informado')
        }
    
    except requests.ConnectionError:
        return {'erro': 'Sem conexão com a internet.'}
    except requests.Timeout:
        return {'erro': 'Tempo limite excedido.'}
    except Exception as e:
        return {'erro': f'Erro inesperado: {str(e)}'}

def salvar_historico(cep, resultado):
    try:
        with open('historico_cep.json', 'r') as arquivo:
            historico = json.load(arquivo)
    except FileNotFoundError:
        historico = []
    
    registro = {
        'cep': cep,
        'data_consulta': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'resultado': resultado
    }
    
    historico.append(registro)
    
    with open('historico_cep.json', 'w') as arquivo:
        json.dump(historico, arquivo, indent=2, ensure_ascii=False)

def ver_historico():
    try:
        with open('historico_cep.json', 'r') as arquivo:
            historico = json.load(arquivo)
        
        if not historico:
            print('Nenhuma consulta realizada ainda.')
            return
        
        print('\n=== HISTÓRICO DE CONSULTAS ===')
        for item in historico[-10:]:
            print(f'Data: {item["data_consulta"]}')
            print(f'CEP: {item["cep"]}')
            if 'erro' not in item['resultado']:
                print(f'Endereço: {item["resultado"]["logradouro"]}')
                print(f'Cidade: {item["resultado"]["cidade"]}/{item["resultado"]["estado"]}')
            else:
                print(f'Erro: {item["resultado"]["erro"]}')
            print('-' * 30)
    
    except FileNotFoundError:
        print('Nenhum histórico encontrado.')

def menu():
    while True:
        limpar_tela()
        print('=== CONSULTA DE CEP ===')
        print('1. Consultar CEP')
        print('2. Ver histórico de consultas')
        print('3. Sair')
        
        opcao = input('Escolha: ')
        
        if opcao == '1':
            cep = input('Digite o CEP (apenas números): ')
            resultado = consultar_cep(cep)
            
            print('\n=== RESULTADO ===')
            if 'erro' in resultado:
                print(f'Erro: {resultado["erro"]}')
            else:
                print(f'CEP: {resultado["cep"]}')
                print(f'Logradouro: {resultado["logradouro"]}')
                print(f'Bairro: {resultado["bairro"]}')
                print(f'Cidade: {resultado["cidade"]}')
                print(f'Estado: {resultado["estado"]}')
                
                salvar_historico(cep, resultado)
            
            input('\nPressione Enter para continuar...')
        
        elif opcao == '2':
            ver_historico()
            input('\nPressione Enter para continuar...')
        
        elif opcao == '3':
            print('Saindo...')
            break
        
        else:
            print('Opção inválida!')
            input('Pressione Enter para continuar...')

if __name__ == '__main__':
    menu()

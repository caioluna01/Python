import sqlite3
from datetime import datetime

def criar_banco():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT DEFAULT 'pendente',
            data_criacao TEXT
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_tarefa(titulo, descricao):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO tarefas (titulo, descricao, data_criacao)
        VALUES (?, ?, ?)
    ''', (titulo, descricao, data))
    conn.commit()
    conn.close()
    print(f'Tarefa "{titulo}" adicionada com sucesso!')

def listar_tarefas(filtro='todas'):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    if filtro == 'pendentes':
        cursor.execute('SELECT * FROM tarefas WHERE status = "pendente"')
    elif filtro == 'concluidas':
        cursor.execute('SELECT * FROM tarefas WHERE status = "concluida"')
    else:
        cursor.execute('SELECT * FROM tarefas')
    
    tarefas = cursor.fetchall()
    conn.close()
    
    if not tarefas:
        print('Nenhuma tarefa encontrada.')
        return
    
    for tarefa in tarefas:
        print(f'ID: {tarefa[0]}')
        print(f'Título: {tarefa[1]}')
        print(f'Descrição: {tarefa[2]}')
        print(f'Status: {tarefa[3]}')
        print(f'Criada em: {tarefa[4]}')
        print('-' * 30)

def atualizar_status(tarefa_id, novo_status):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tarefas SET status = ? WHERE id = ?
    ''', (novo_status, tarefa_id))
    conn.commit()
    conn.close()
    print(f'Tarefa {tarefa_id} atualizada para "{novo_status}"')

def deletar_tarefa(tarefa_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tarefas WHERE id = ?', (tarefa_id,))
    conn.commit()
    conn.close()
    print(f'Tarefa {tarefa_id} deletada.')

def menu():
    criar_banco()
    
    while True:
        print('\n=== SISTEMA DE TAREFAS ===')
        print('1. Adicionar tarefa')
        print('2. Listar todas as tarefas')
        print('3. Listar tarefas pendentes')
        print('4. Listar tarefas concluídas')
        print('5. Concluir tarefa')
        print('6. Deletar tarefa')
        print('7. Sair')
        
        opcao = input('Escolha uma opção: ')
        
        if opcao == '1':
            titulo = input('Título: ')
            descricao = input('Descrição: ')
            adicionar_tarefa(titulo, descricao)
        
        elif opcao == '2':
            listar_tarefas()
        
        elif opcao == '3':
            listar_tarefas('pendentes')
        
        elif opcao == '4':
            listar_tarefas('concluidas')
        
        elif opcao == '5':
            tarefa_id = int(input('ID da tarefa: '))
            atualizar_status(tarefa_id, 'concluida')
        
        elif opcao == '6':
            tarefa_id = int(input('ID da tarefa: '))
            deletar_tarefa(tarefa_id)
        
        elif opcao == '7':
            print('Saindo...')
            break
        
        else:
            print('Opção inválida!')

if __name__ == '__main__':
    menu()

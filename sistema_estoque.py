# sistema_estoque_v1.py

class Produto:
    def __init__(self, id, nome, preco, quantidade):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
    
    def __str__(self):
        return f"ID: {self.id} | {self.nome} | R${self.preco:.2f} | Estoque: {self.quantidade}"


class GerenciadorEstoque:
    def __init__(self):
        self.produtos = {}
        self.proximo_id = 1
    
    def adicionar_produto(self, nome, preco, quantidade):
        """Adiciona um novo produto"""
        produto = Produto(self.proximo_id, nome, preco, quantidade)
        self.produtos[self.proximo_id] = produto
        self.proximo_id += 1
        print(f" Produto '{nome}' adicionado com sucesso!")
    
    def listar_produtos(self):
        """Lista todos os produtos"""
        if not self.produtos:
            print(" Nenhum produto cadastrado.")
            return
        print("\n" + "="*50)
        print(" LISTA DE PRODUTOS")
        print("="*50)
        for produto in self.produtos.values():
            print(produto)
    
    def buscar_produto(self, id):
        """Busca produto por ID"""
        return self.produtos.get(id)
    
    def atualizar_estoque(self, id, quantidade):
        """Atualiza a quantidade em estoque"""
        produto = self.buscar_produto(id)
        if produto:
            produto.quantidade = quantidade
            print(f" Estoque de '{produto.nome}' atualizado para {quantidade}")
        else:
            print(" Produto não encontrado!")
    
    def remover_produto(self, id):
        """Remove um produto"""
        if id in self.produtos:
            nome = self.produtos[id].nome
            del self.produtos[id]
            print(f" Produto '{nome}' removido!")
        else:
            print(" Produto não encontrado!")
    
    def produtos_baixo_estoque(self, limite=5):
        """Mostra produtos com estoque baixo"""
        baixos = [p for p in self.produtos.values() if p.quantidade <= limite]
        if baixos:
            print(f"\n PRODUTOS COM ESTOQUE BAIXO (≤ {limite}):")
            for p in baixos:
                print(f"   • {p.nome} - apenas {p.quantidade} unidades")
        else:
            print(" Todos os produtos têm estoque adequado!")


# Interface do usuário
def menu():
    print("\n" + "="*50)
    print("   SISTEMA DE GESTÃO DE ESTOQUE")
    print("="*50)
    print("1️⃣  Adicionar produto")
    print("2️⃣  Listar produtos")
    print("3️⃣  Atualizar estoque")
    print("4️⃣  Remover produto")
    print("5️⃣  Ver produtos com estoque baixo")
    print("6️⃣  Sair")
    print("="*50)


def main():
    sistema = GerenciadorEstoque()
    
    while True:
        menu()
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            nome = input("Nome do produto: ")
            preco = float(input("Preço: R$"))
            quantidade = int(input("Quantidade em estoque: "))
            sistema.adicionar_produto(nome, preco, quantidade)
        
        elif opcao == "2":
            sistema.listar_produtos()
        
        elif opcao == "3":
            id = int(input("ID do produto: "))
            quantidade = int(input("Nova quantidade: "))
            sistema.atualizar_estoque(id, quantidade)
        
        elif opcao == "4":
            id = int(input("ID do produto a remover: "))
            sistema.remover_produto(id)
        
        elif opcao == "5":
            limite = int(input("Limite mínimo de estoque: "))
            sistema.produtos_baixo_estoque(limite)
        
        elif opcao == "6":
            print(" Saindo do sistema...")
            break
        
        else:
            print(" Opção inválida!")


if __name__ == "__main__":
    main()

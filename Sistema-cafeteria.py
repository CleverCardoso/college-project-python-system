from tabulate import tabulate
import json
import re

def linha(tam=42):
    return '-' *tam

def cabeçalho(txt):
    print(linha())
    print(txt.center(42))
    print(linha())
    
class produtos:
    def __init__(self):
        self.lista_produto = []
    
       
    def Cadastrar_produto(self):
        nome = input("Nome do Produto: ")
        preco = input("Preço do Produto: ")
        ingredientes_input = input("Digite os ingredientes separados por vírgula: ")
        ingredientes = [item.strip() for item in ingredientes_input.split(",")]
        promocao_input = input("Está em promoção? [S/N]: ").strip().upper()  

        if promocao_input == "S":
            promocao = True
        elif promocao_input == "N":
            promocao = False
        else:
            print("Entrada inválida para promoção. Definindo como False.")
            promocao = False

    
        self.lista_produto.append({"nome": nome, "preco": preco, "ingredientes": ingredientes, "promocao": promocao})
        
    def Ver_produtos(self):
        cabeçalho("Cardapio")
        print("-" * 80)
        print(f"{'Nome':<20} {'Preço':<10} {'Ingredientes':<30} {'Promoção':<10}")
        print("-" * 80)
        for produto in self.lista_produto:
            nome = produto["nome"]
            preco = f"R${produto['preco']}"
            ingredientes = ", ".join(produto["ingredientes"])
            promocao = "Sim" if produto["promocao"] else "Não"
            print(f"{nome:<20} {preco:<10} {ingredientes:<30} {promocao:<10}")
            print("-" * 80)
    
    


class Clientes:
    
    def __init__(self):
        self.lista_clientes = []

    def cadastrar_cliente(self):
        nome = input("Nome do cliente: ")
        tel = input("Telefone do cliente: ")

        while True:
            email = input("Email do cliente: ")
            if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                print("Cliente cadastrado")
                break
            else:
                print("Email inválido. Tente novamente.")

        self.lista_clientes.append({"nome": nome, "tel": tel, "email": email})


def menu_produtos():
    while True:
                print("==== PRODUTOS ====")
                print("1. Cadastrar produto")
                print("2. Ver lista de produtos")
                print("3. Sair")
                opcao = input("Escolha uma opção: ")
                
                if opcao == "1":
                    p.Cadastrar_produto()
                elif opcao == "2":
                    p.Ver_Cardapio()
                elif opcao == "3":
                    break
                else:
                    print("Opção inválida")
                    
class pedido:
    def __init__(self):
        pass

def Ver_cardapio(self):
        cabeçalho("Cardapio")
        print("-" * 80)
        print(f"{'Nome':<20} {'Preço':<10} {'Ingredientes':<30} {'Promoção':<10}")
        print("-" * 80)
        for produto in self.lista_produto:
            nome = produto["nome"]
            preco = f"R${produto['preco']}"
            ingredientes = ", ".join(produto["ingredientes"])
            promocao = "Sim" if produto["promocao"] else "Não"
            print(f"{nome:<20} {preco:<10} {ingredientes:<30} {promocao:<10}")
            print("-" * 80)
p = produtos()
c = Clientes()    

def main_menu():       
    while True:
        print("==== COFFEE SHOPS TIA ROSA ====")
        print("1. Cadastrar produto")
        print("2. Clientes")
        print("3. Fazer pedido")
        print("4. Ver cardápio")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            menu_produtos()
        elif opcao == "2":
            Clientes
        elif opcao == "3":
            pass
        elif opcao == "4":
            pass
        elif opcao == "5":
            break
        else:
            print("Opção inválida")
            
            
main_menu()
        
    
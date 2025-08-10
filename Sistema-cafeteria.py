from tabulate import tabulate
import json
import re
from datetime import datetime
from pathlib import Path

ARQUIVO_DADOS = "dados_tiarosa.json"


#Utilidades

def linha(tam=42):
    return '-' *tam

def cabecalho(txt):
    print(linha())
    print(txt.center(42))
    print(linha())

def input_nao_vazio(msg):
    while True:
        v = input(msg).strip()
        if v:
            return v
        print("Entrada vazia. Tente novamente.")

#COLOCANDO EM JSON AS LISTAS

def carregar_dados():
    p = Path(ARQUIVO_DADOS)
    if not p.exists():
        return{"produtos":[], "clientes":[], "pedidos": []}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"produtos": [], "clientes": [], "pedidos": []}
    
def salvar_dados(dados):
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

#PRODUTOS

class produtos:
    
    def __init__(self, dados):
        self.lista_produto = dados["produtos"]
        self.proximo_ID = self.recalcula_proximo_ID()
     
        
    def recalcula_proximo_ID(self):
           if not self.lista_produto:
               return 1
           return max(p["id"] for p in self.lista_produto) + 1
    
    
    def get_lista_produto(self):
        return self.lista_produto
        
               
    def Cadastrar_produto(self):
        cabecalho("Cadastro de Produto")
        
        nome = input_nao_vazio("Nome do Produto: ")
        
        while True:
            preco_str = input_nao_vazio("Preço do Produto (ex: 12.50): ").replace(",", ".")
            try:
                preco = float(preco_str)
                if preco <= 0:
                    print("Preço deve ser maior que 0.")
                    continue
                break
            except ValueError:
                print("Preço inválido.")
        
        ingredientes_input = input("Digite os ingredientes separados por vírgula: ")
        ingredientes = [item.strip() for item in ingredientes_input.split(",")]
        
        promocao_input = input("Está em promoção? [S/N]: ").strip().upper()  
        promocao = True if promocao_input == "S" else False

        novo = {
            "id": self.proximo_ID,
            "nome": nome,
            "preco": preco,
            "ingredientes": ingredientes,
            "promocao": promocao
        }
    
        self.lista_produto.append(novo)
        self.proximo_ID += 1
        print("Produto Castrado com sucesso!")
        
    
    
    def ver_tabela(self, registros):
        headers = ["ID", "Nome", "Preço (R$)", "Ingredientes", "Promoção"]
        linhas = []
        for p in registros:
            linhas.append([
                p["id"], p["nome"], f"{p['preco']:.2f}",
                ", ".join(p["ingredientes"]),
                "Sim" if p["promocao"] else "Não"
            ])
        try:
            print(tabulate(linhas, headers=headers, tablefmt="grid", stralign="left"))
        except Exception:
            # fallback simples
            print(f"{'ID':<5} {'Nome':<25} {'Preço':<10} {'Ingredientes':<30} {'Promoção':<9}")
            print(linha())
            for l in linhas:
                print(f"{str(l[0]):<5} {l[1]:<25} {l[2]:<10} {l[3]:<30} {l[4]:<9}")
    
    def ver_produtos(self):
        cabecalho("Lista de Produtos")
        if not self.lista_produto:
            print("Sem produtos cadastrados.")
            return
        self.ver_tabela(self.lista_produto)
        
    def ver_promocoes(self):
        cabecalho("Produtos em Promoçao")
        promo = [p for p in self.lista_produto if p["promocao"]]
        if not promo:
            print("Nenhum produto em promoção")
            return
        self.ver_tabela(promo)
        
    def buscar_por_nome(self,termo):
        termo = termo.lower().strip()
        return [p for p in self.lista_produto if termo in p["nome"].lower()]
        
    
    def obter_por_id(self,pid):
        for p in self.lista_produto:
            if p["id"] == pid:
                return p 
            
        return None
    
        
        
#CLIENTES

class Clientes:
    
    def __init__(self, dados):
        self.lista_clientes = dados["clientes"]

    def cadastrar_cliente(self):
        cabecalho("Cadastro de Cliente")
        nome = input_nao_vazio("Nome do cliente: ")
        tel = input_nao_vazio("Telefone do cliente: ")

        
        #Validar Email
        while True:
            email = input_nao_vazio("Email do cliente: ") 
            if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                print("Cliente cadastrado")
                break
            else:
                print("Email inválido. Tente novamente.")

        #Evita duplicacao de email
        if any(cl["Email"].lower() == email.lower() for cl in self.lista_clientes):
            print("Ja existe um Usuario com esse email. Cadastro cancelado.")
            return
        
        self.lista_clientes.append({"nome": nome, "tel": tel, "email": email})
        print("Cliente cadastrado!")
        
    def ver_clientes(self):
        cabecalho("Lista de Clientes")
        if not self.lista_clientes:
            print("Sem clientes cadastrados.")
            return
        headers = ["#", "Nome", "Telefone", "Email"]
        linhas = []
        for i, c in enumerate(self.lista_clientes, start=1):
            linhas.append([i, c["nome"], c["tel"], c["email"]])
        try:
            print(tabulate(linhas, headers=headers, tablefmt="grid", stralign="left"))
        except Exception:
            print(f"{'#':<3} {'Nome':<25} {'Telefone':<15} {'Email':<30}")
            print(linha())
            for l in linhas:
                print(f"{str(l[0]):<3} {l[1]:<25} {l[2]:<15} {l[3]:<30}") 
                
    def buscar(self, termo):
        termo = termo.lower().strip()
        return [
            c for c in self.lista_clientes
            if termo in c["nome"].lower() or termo in c["tel"].lower() or termo in c["email"].lower()
        ]
            
class pedido:
    
    desconto_produto = 0.10
    
    def __init__(self, dados, clientes: Clientes, produtos: produtos):
        self.pedidos = dados["pedidos"]  # lista de dicts
        self.clientes = clientes
        self.produtos = produtos
    
    def escolher_cliente(self):
        while True:
            print("\n1) Listar Clientes  2) Buscar Clientes  3) Cancelar")
            op = input("Opção: ").strip()
            if op == "1":
                self.clientes.ver_clientes()
                idx = input("Digite o # do cliente: ").strip()
                if not idx.isdigit():
                    print("Indice invalido")
                    continue
                return self.clientes.lista_clientes[idx - 1]
            elif op == "2":
                termo = input_nao_vazio("Buscar por nome/telefone/email: ")
                achados = self.clientes.buscar(termo)
                if not achados:
                    print("Nenhum cliente encontrado")
                    continue
                for i, c in enumerate(achados, start=1):
                    print(f"{i}. {c['nome']} | {c['tel']} | {c['email']}")
                idx = input("Escolha (número): ").strip()
                if not idx.isdigit():
                    print("Índice inválido.")
                    continue
                idx = int(idx)
                if idx < 1 or idx > len(achados):
                    print("Fora do intervalo.")
                    continue
                return achados[idx - 1]
            elif op == "3":
                return None
            else:
                print("Opção inválida.")
                
    
    def escolher_itens(self):
        itens = []
        while True:
            self.produtos.ver_produtos()
            pid_str = input("ID do produto (ou 'fim' para terminar): ").strip().lower()
            if pid_str == "fim":
                break
            if not pid_str.isdigit():
                print("ID inválido. ")
                continue
            pid = int(pid_str)
            prod = self.produtos.obter_por_id(pid)
            if not prod:
                print("Produto não encontrado.")
                continue
            
            while True:
                qtd_str = input("Quantidade: ").strip()
                if qtd_str.isdigit() and int(qtd_str) > 0:
                    qtd = int(qtd_str)
                    break
                print("Quantidade inválida.")
                itens.append({"id": prod["id"], "nome": prod["nome"], "preco": prod["preco"], "promocao": prod["promocao"], "qtd": qtd})
                return itens
            
            
    def calcular_total(self,itens):
        subtotal = 0.0
        desconto = 0.0
        for it in itens:
            valor = it["preco"] * it["qtd"]
            subtotal += valor
            if it["promocao"]:
                desconto += valor * self.desconto_promo
        total = subtotal - desconto
        return subtotal, desconto, total
    
    
    def novo_pedido(self):
        cabecalho("Novo Pedido")
        if not self.clientes.lista_clientes:
            print("Cadastre um cliente primeiro.")
            return
        if not self.produtos.lista_produto:
            print("Cadastre produtos primeiro.")
            return

        cliente = self._escolher_cliente()
        if not cliente:
            print("Pedido cancelado.")
            return

        itens = self._escolher_itens()
        if not itens:
            print("Nenhum item selecionado. Pedido cancelado.")
            return

        subtotal, desconto, total = self._calcula_total(itens)
        
        pedido = {
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cliente": cliente,  # salva snapshot simples
            "itens": itens,
            "subtotal": round(subtotal, 2),
            "desconto": round(desconto, 2),
            "total": round(total, 2)
        }
        self.pedidos.append(pedido)
        
        print("\nResumo do Pedido")
        print(linha())
        for it in itens:
            flag = " (PROMO)" if it["promocao"] else ""
            print(f"{it['qtd']}x {it['nome']}{flag} - R$ {it['preco']:.2f} cada")
        print(linha())
        print(f"Subtotal: R$ {subtotal:.2f}")
        print(f"Desconto : R$ {desconto:.2f}")
        print(f"TOTAL    : R$ {total:.2f}")
        print("✅ Pedido registrado!")
        
    
        
dados = carregar_dados()                
p = produtos(dados)
c = Clientes(dados) 
pp = pedido()   

def main_menu():       
    while True:
        print("\n==== COFFEE SHOPS TIA ROSA ====")
        print("1. Produtos")
        print("2. Clientes")
        print("3. Ver cardápio")
        print("4. Fazer pedido")
        print("5. Sair")
        opcao = input_nao_vazio("Escolha uma opção: ")
        
        if opcao == "1":
            p.Cadastrar_produto()
        elif opcao == "2":
            c.cadastrar_cliente()
        elif opcao == "3":
            p.ver_produtos()
        elif opcao == "4":
            pp.pedido()
        elif opcao == "5":
            # salva antes de sair
            salvar_dados({"produtos": p.get_lista_produto(),
                          "clientes": c.lista_clientes,
                          "pedidos": pp.pedidos})
            break
        else:
            print("Opção inválida")
            
            
main_menu()
        
    
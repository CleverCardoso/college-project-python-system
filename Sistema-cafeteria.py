from tabulate import tabulate
import json
import re
from datetime import datetime
from pathlib import Path
import os

ARQUIVO_DADOS = "dados_tiarosa.json"


# =========================
# Utilidades 
# =========================

def limpar_tela():
    """Limpa a tela do terminal (Windows: cls | Linux/Mac: clear)."""
    
    os.system('cls' if os.name == 'nt' else 'clear')

def linha(tam=42):
    """Retorna uma linha horizontal com o tamanho informado."""
    
    return '-' *tam


def cabecalho(txt):
    """Limpa a tela e imprime um cabeçalho padrão centralizado."""
    limpar_tela()
    print(linha())
    print(txt.center(42))
    print(linha())

def input_nao_vazio(msg):
    """Força o usuário a digitar algo não vazio."""
    
    while True:
        v = input(msg).strip()
        if v:
            return v
        print("Entrada vazia. Tente novamente.")

def pausa(msg="\nPressione Enter para voltar..."):
    input(msg)


# =========================
# Persistência (JSON)
# =========================

def carregar_dados():
    """
    Carrega os dados do arquivo JSON.
    Se não existir ou der erro, retorna estrutura vazia.
    
    """
    p = Path(ARQUIVO_DADOS)
    if not p.exists():
        return{"produtos":[], "clientes":[], "pedidos": []}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"produtos": [], "clientes": [], "pedidos": []}
    
def salvar_dados(dados):
    """Salva o dicionário de dados no JSON com indentação legível."""
    
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


# =========================
# PRODUTOS
# =========================

class Produtos:
    """Gerencia o catálogo de produtos (CRUD básico)."""
    
    def __init__(self, dados):
        self.lista_produto = dados["produtos"]
        self.proximo_ID = self.recalcula_proximo_ID()
     
        
    def recalcula_proximo_ID(self):
        """Calcula o próximo ID com base no maior ID existente."""
        
        if not self.lista_produto:
            return 1
        return max(p["id"] for p in self.lista_produto) + 1
    
    
    def get_lista_produto(self):
        """Retorna a lista interna (para salvar)."""
        
        return self.lista_produto
        
               
    def Cadastrar_produto(self):
        """Cadastra um novo produto com validações simples."""
        
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
        """Renderiza uma tabela de produtos usando tabulate (com fallback)."""
        
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
        """Lista todos os produtos cadastrados."""
        
        cabecalho("Lista de Produtos")
        if not self.lista_produto:
            print("Sem produtos cadastrados.")
            return
        self.ver_tabela(self.lista_produto)
        pausa()
        
        
    def ver_promocoes(self):
        """Lista somente produtos que estão em promoção."""
        
        cabecalho("Produtos em Promoçao")
        promo = [p for p in self.lista_produto if p["promocao"]]
        if not promo:
            print("Nenhum produto em promoção")
            return
        self.ver_tabela(promo)
        pausa()
        
    def buscar_por_nome(self,termo):
        """Busca por nome (case-insensitive, contém)."""
        
        termo = termo.lower().strip()
        return [p for p in self.lista_produto if termo in p["nome"].lower()]
        
    
    def obter_por_id(self,pid):
        """Retorna o produto pelo ID (ou None)."""
        for p in self.lista_produto:
            if p["id"] == pid:
                return p 
            
        return None
    
        
# =========================
# CLIENTES
# =========================

class Clientes:
    """Gerencia cadastro e busca de clientes."""
    
    def __init__(self, dados):
        self.lista_clientes = dados["clientes"]

    def cadastrar_cliente(self):
        """Cadastra cliente com validação básica de e-mail e duplicidade."""
        cabecalho("Cadastro de Cliente")
        nome = input_nao_vazio("Nome do cliente: ")
        tel = input_nao_vazio("Telefone do cliente: ")

        
        # Valida e-mail simples via regex
        while True:
            email = input_nao_vazio("Email do cliente: ") 
            if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                break
            else:
                print("Email inválido. Tente novamente.")

        # Evita duplicação por e-mail
        if any(cl["email"].lower() == email.lower() for cl in self.lista_clientes):
            print("Ja existe um Usuario com esse email. Cadastro cancelado.")
            return
        
        self.lista_clientes.append({"nome": nome, "tel": tel, "email": email})
        print("Cliente cadastrado!")
        
    def ver_clientes(self):
        """Lista clientes em tabela (ou fallback)."""
        
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
        pausa()
                
    def buscar(self, termo):
        """Busca cliente por nome, telefone ou e-mail (contains, case-insensitive)."""
        termo = termo.lower().strip()
        return [
            c for c in self.lista_clientes
            if termo in c["nome"].lower() or termo in c["tel"].lower() or termo in c["email"].lower()
        ]
            
            
# =========================
# PEDIDOS
# =========================

class pedido:
    """Registra pedidos, calcula totais e gera relatórios."""
    
    desconto_produto = 0.10 # 10% de desconto para itens em promoção
    
    def __init__(self, dados, clientes: Clientes, produtos: Produtos):
        self.pedidos = dados["pedidos"] 
        self.clientes = clientes
        self.produtos = produtos
    
    def escolher_cliente(self):
        """Permite listar/buscar e selecionar um cliente, ou cancelar."""
        
        while True:
            print("\n1) Listar Clientes  2) Buscar Clientes  3) Cancelar")
            op = input("Opção: ").strip()
            if op == "1":
                self.clientes.ver_clientes()
                idx = input("Digite o # do cliente: ").strip()
                if not idx.isdigit():
                    print("Índice inválido.")
                    continue
                idx = int(idx)
                if idx < 1 or idx > len(self.clientes.lista_clientes):
                    print("Fora do intervalo.")
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
        """Monta a lista de itens do pedido"""
        
        itens = []
        while True:
            self.produtos.ver_produtos()
            pid_str = input("ID do produto (ou 'fim' para terminar): ").strip().lower()
            if pid_str == "fim":
                break
            if not pid_str.isdigit():
                print("ID inválido.")
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

            itens.append({
                "id": prod["id"], "nome": prod["nome"], "preco": prod["preco"],
                "promocao": prod["promocao"], "qtd": qtd
            })
        return itens
            
            
    def calcular_total(self,itens):
        """Calcula subtotal, desconto (apenas itens em promoção) e total."""
        
        subtotal = 0.0
        desconto = 0.0
        for it in itens:
            valor = it["preco"] * it["qtd"]
            subtotal += valor
            if it["promocao"]:
                desconto += valor * self.desconto_produto
        total = subtotal - desconto
        return subtotal, desconto, total
    
    
    def novo_pedido(self):
        """Fluxo completo de novo pedido, com resumo final."""
        
        cabecalho("Novo Pedido")
        if not self.clientes.lista_clientes:
            print("Cadastre um cliente primeiro.")
            return
        if not self.produtos.lista_produto:
            print("Cadastre produtos primeiro.")
            return

        cliente = self.escolher_cliente()
        if not cliente:
            print("Pedido cancelado.")
            return

        itens = self.escolher_itens()
        if not itens:
            print("Nenhum item selecionado. Pedido cancelado.")
            return

        subtotal, desconto, total = self.calcular_total(itens)
        
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
        print("Pedido registrado!")
        
    def listar_pedidos(self):
        """Lista todos os pedidos já registrados com seus totais."""
        
        cabecalho("Pedidos Registrados")
        if not self.pedidos:
            print("Nenhum pedido ainda")
            return
        for i,p in enumerate(self.pedidos, start=1):
            print(linha())
            print(f"#{i} | {p['data_hora']} | Cliente: {p['cliente']['nome']} ({p['cliente']['email']})")
            for it in p["itens"]:
                flag = " (PROMO)" if it["promocao"] else ""
                print(f"  - {it['qtd']}x {it['nome']}{flag} @ R$ {it['preco']:.2f}")
            print(f"Subtotal: R$ {p['subtotal']:.2f} | Desconto: R$ {p['desconto']:.2f} | TOTAL: R$ {p['total']:.2f}")
        print(linha())
        pausa()
        
        
    def relatorio_venda_dia(self):
        """Mostra quantidade de pedidos e total do dia atual."""
        
        hoje = datetime.now().strftime("%Y-%m-%d")
        total = 0.0
        qtd_pedidos = 0
        for p in self.pedidos:
            if p["data_hora"].startswith(hoje):
                qtd_pedidos += 1
                total += p["total"]
        cabecalho(f"Relatório de Vendas - {hoje}")
        print(f"Pedidos: {qtd_pedidos}")
        print(f"Total arrecadado: R$ {total:.2f}")
        pausa()
        
    
    def relatorio_pedidos_por_cliente(self):
        """Filtra e soma pedidos por termo (nome/email/telefone)."""
        
        termo = input_nao_vazio("Buscar cliente (nome/email/telefone): ").lower()
        resultados = []
        for p in self.pedidos:
            c = p["cliente"]
            pac = f"{c['nome']} {c['email']} {c['tel']}".lower()
            if termo in pac:
                resultados.append(p)
                
        cabecalho("Pedidos por cliente (busca)")
        if not resultados:
            print("Nenhum pedido encontrado para este cliente.")
            return
        soma = 0.0
        for i, p in enumerate(resultados, start=1):
            print(f"{i}. {p['data_hora']} | {p['cliente']['nome']} | TOTAL: R$ {p['total']:.2f}")
            soma += p["total"]
        print(linha())
        print(f"Total acumulado: R$ {soma:.2f}")
        pausa()
        
        
# =========================
# MENUS
# =========================
       
def menu_produtos(produtos: Produtos):
    """Menu de gerenciamento de produtos."""
    
    while True:
        print("\n==== PRODUTOS ====")
        print("1. Cadastrar produto")
        print("2. Ver lista de produtos")
        print("3. Ver apenas promoções")
        print("4. Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            produtos.Cadastrar_produto()
        elif op == "2":
            produtos.ver_produtos()
        elif op == "3":
            produtos.ver_promocoes()
        elif op == "4":
            break
        else:
            print("Opção inválida.")


def menu_clientes(clientes: Clientes):
    """Menu de gerenciamento de clientes."""
    
    while True:
        print("\n==== CLIENTES ====")
        print("1. Cadastrar cliente")
        print("2. Ver lista de clientes")
        print("3. Buscar clientes")
        print("4. Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            clientes.cadastrar_cliente()
        elif op == "2":
            clientes.ver_clientes()
        elif op == "3":
            termo = input_nao_vazio("Termo de busca: ")
            achados = clientes.buscar(termo)
            if not achados:
                print("Nenhum cliente encontrado.")
            else:
                for i, c in enumerate(achados, start=1):
                    print(f"{i}. {c['nome']} | {c['tel']} | {c['email']}")
        elif op == "4":
            break
        else:
            print("Opção inválida.")
            
def menu_pedidos(pedidos: pedido):
    """Menu de pedidos e relatórios."""
    
    while True:
        print("\n==== PEDIDOS ====")
        print("1. Novo pedido")
        print("2. Listar pedidos")
        print("3. Relatório - Vendas do dia")
        print("4. Relatório - Pedidos por cliente")
        print("5. Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            pedidos.novo_pedido()
        elif op == "2":
            pedidos.listar_pedidos()
        elif op == "3":
            pedidos.relatorio_venda_dia()  
        elif op == "4":
            pedidos.relatorio_pedidos_por_cliente()
        elif op == "5":
            break
        else:
            print("Opção inválida.")
            
            
# =========================
# MAIN LOOP
# =========================            
            
def main():
    """Loop principal do sistema."""
    
    dados = carregar_dados()

    produtos_obj = Produtos(dados)    
    clientes_obj = Clientes(dados)
    pedidos_obj  = pedido(dados, clientes_obj, produtos_obj)  
           
    while True:
        limpar_tela()
        print("\n==== COFFEE SHOPS TIA ROSA ====")
        print("1. Produtos")
        print("2. Clientes")
        print("3. Ver cardápio")
        print("4. Pedidos")
        print("5. Salvar & Sair")
        opcao = input_nao_vazio("Escolha uma opção: ").strip()
        
        if opcao == "1":
            menu_produtos(produtos_obj)
        elif opcao == "2":
            menu_clientes(clientes_obj)
        elif opcao == "3":
            produtos_obj.ver_produtos()
        elif opcao == "4":
             menu_pedidos(pedidos_obj)
        elif opcao == "5":
            # salva antes de sair
            salvar_dados({
                "produtos": produtos_obj.get_lista_produto(),
                "clientes": clientes_obj.lista_clientes,
                "pedidos":  pedidos_obj.pedidos
            })
            print("Dados salvos. Até mais!")
            break
        else:
            print("Opção inválida.")
            
if __name__ == "__main__":
    main()
        
    
# COFFEE SHOPS TIA ROSA --- Sistema de Console (Python)

Sistema de terminal para gerenciar **Produtos**, **Clientes** e **Pedidos** de uma cafeteria. Dados são persistidos em arquivos **JSON** e as listagens são formatadas com a biblioteca **Tabulate**.

## Funcionalidades

-   **Produtos**: Cadastrar, listar e listar itens em promoção.
-   **Clientes**: Cadastrar (com validação simples de e-mail e bloqueio de duplicados), listar e buscar.
-   **Pedidos**: Escolher cliente, adicionar itens, calcular subtotal, aplicar **desconto de 10%** em itens promocionais e exibir o total.
-   **Relatórios**: Gerar relatórios de **vendas do dia** e **pedidos por cliente**.
-   **UX**: Limpa a tela do terminal a cada etapa para uma leitura mais agradável.

## Requisitos

-   Python 3.10+
-   Biblioteca: `tabulate`

## Como Rodar

1.  **Crie e ative o ambiente virtual:**
    ```bash
    # Comando para criar o ambiente
    python -m venv venv

    # Ative o ambiente
    # No Windows: .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

2.  **Instale as dependências:**
    ```bash
    pip install tabulate
    ```

3.  **Execute o programa:**
    ```bash
    python Sistema-cafeteria.py
    ```

## Autor

Cleverlandio Cardoso de Oliveira Junior

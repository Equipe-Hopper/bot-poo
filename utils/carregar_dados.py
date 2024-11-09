# utils/carregar_dados.py

import pandas as pd
from modules.produto import Produto
from modules.pedido import Pedido
from modules.gestor_de_pedidos import GestorDePedidos

def carregar_pedidos_do_excel(caminho_arquivo, gestor: GestorDePedidos):
    # Carrega a planilha
    df = pd.read_excel(caminho_arquivo)  # Supondo que a planilha seja um arquivo Excel
    
    for _, row in df.iterrows():
        # Extrai os dados da linha
        cliente = row['Cliente']
        status = row['Status']
        
        # Cria uma lista de produtos
        produtos = []
        quantidade_produtos = {}
        
        # Cria uma instância de Produto com os dados da linha
        produto = Produto(nome=row['Produto'], preco=row['Preco'], categoria=row['Categoria'])
        produtos.append(produto)
        
        # Define a quantidade do produto
        quantidade_produtos[produto] = row['Quantidade']
        
        # Cria o pedido com os produtos e quantidade
        pedido = Pedido(produtos=produtos, quantidade=quantidade_produtos, cliente=cliente, status=status)
        
        # Adiciona o pedido ao gestor
        gestor.adicionar_pedido(pedido)
        
    print("Pedidos carregados com sucesso a partir do Excel.")
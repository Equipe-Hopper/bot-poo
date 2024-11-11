"""EQUIPE HOPPER
ALUNOS: ARMANDO DE OLIVEIRA GONÇALVES NETO
        MARCIO BRENER CANTUARIA SANTOS
        CLICIA MARIA SILVA
        VICTOR FLAVIO ARANTES
        KAMILA DOS SANTOS SOUZA""" 

from modules.produto import Produto
from modules.pedido import Pedido
from modules.gestor_de_pedidos import GestorDePedidos
from bot.bot_de_pedidos import BotDePedidos
from exeption.exeptions import ValorInvalidoError, QuantidadeInvalidaError

def main():
    gestor = GestorDePedidos()
    bot = BotDePedidos()

    try:
        # Criação de produtos
        produto1 = Produto("Camiseta", 50.0, "Vestuario")
        produto2 = Produto("Calça", 100.0, "Vestuario")

        # Criação de pedido com produtos e quantidades válidas
        pedido = Pedido([produto1, produto2], {produto1: 2, produto2: 1}, "Cliente A")
        gestor.adicionar_pedido(pedido)

        caminho_arquivo = "C:/Users/kliss/OneDrive/Área de Trabalho/projetos/LG/Bot_poo/data/planilha_de_produtos.xlsx"
        bot.carregar_pedidos_planilha(caminho_arquivo, gestor)

        # Exibir todos os pedidos carregados
        print("Pedidos carregados no sistema:")
        gestor.listar_pedidos()

        # Integrar com o Bot para preencher o formulário
        #bot = BotDePedidos()
        bot.preencher_pedidos(gestor)

         # Salvar dados em JSON e binário
        gestor.salvar_dados_json("data/pedidos.json")
        gestor.salvar_dados_binario("data/pedidos.pkl")

        # Carregar dados de JSON e binário
        gestor.carregar_dados_json("data/pedidos.json")
        gestor.carregar_dados_binario("data/pedidos.pkl")

        # Listar pedidos com status "Novo" e formatar a saída
        pedidos_novos = gestor.listar_pedidos_por_status("Novo")
        print("Pedidos com status 'Novo':")
        for pedido in pedidos_novos:
            print(f"Cliente: {pedido.cliente}, Status: {pedido.status}, Total: {pedido.total_pedido():.2f}")

    except ValorInvalidoError as ve:
        print(f"Erro: {ve}")
    except QuantidadeInvalidaError as qe:
        print(f"Erro: {qe}")

if __name__ == "__main__":
    main()

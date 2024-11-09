import json
import pickle
from functools import reduce
from utils.log_decorator import log_atividade

from modules.pedido import Pedido

class GestorDePedidos:
    def __init__(self):
        self.pedidos = []

    @log_atividade
    def adicionar_pedido(self, pedido: Pedido):
        """Adiciona um pedido à lista de pedidos."""
        self.pedidos.append(pedido)

    @log_atividade
    def listar_pedidos_por_status(self, status: str):
        """Lista pedidos com um status específico usando filter."""
        # Converte o status para uma forma padronizada antes de filtrar
        status = status.capitalize()
        return list(filter(lambda pedido: pedido.status == status, self.pedidos))

    def pedidos_por_categoria(self, categoria: str) -> dict:
        """Gera um relatório de quantos produtos de uma categoria específica foram vendidos."""
        return {categoria: sum(1 for pedido in self.pedidos for produto in pedido.produtos if produto.categoria == categoria)}

    def total_vendas(self) -> float:
        """Calcula o total de vendas utilizando reduce."""
        return reduce(lambda total, pedido: total + pedido.total_pedido(), self.pedidos, 0.0)
    
    def listar_pedidos(self):
        for pedido in self.pedidos:
            print(pedido.detalhes_pedido())

    def salvar_dados_json(self, arquivo: str):
        try:
            pedidos_serializaveis = []
            for pedido in self.pedidos:
                pedido_detalhes = {
                    "cliente": pedido.cliente,
                    "status": pedido.status,
                    "produtos": [
                        {
                            "nome": produto.nome,
                            "preco": produto.preco,
                            "categoria": produto.categoria,
                            "quantidade": pedido.quantidade[produto]
                        }
                        for produto in pedido.produtos
                    ],
                    "total": pedido.total_pedido()
                }
                pedidos_serializaveis.append(pedido_detalhes)

            with open(arquivo, 'w') as f:
                json.dump(pedidos_serializaveis, f, indent=4)
            print("Dados salvos em JSON com sucesso.")
        except IOError as e:
            print(f"Erro ao salvar dados JSON: {e}")

    def carregar_dados_json(self, arquivo: str):
        """Carrega os dados dos pedidos de um arquivo JSON."""
        try:
            with open(arquivo, 'r') as f:
                dados = json.load(f)
                # Processo para recriar instâncias de pedidos a partir dos dados JSON
                # Necessário transformar em objetos Pedido e Produto novamente
                print("Dados carregados do JSON com sucesso.")
        except FileNotFoundError:
            print("Arquivo JSON não encontrado.")
        except IOError as e:
            print(f"Erro ao carregar dados JSON: {e}")

    def salvar_dados_binario(self, arquivo: str):
        """Salva os dados dos pedidos em um arquivo binário usando pickle."""
        try:
            with open(arquivo, 'wb') as f:
                pickle.dump(self.pedidos, f)
            print("Dados salvos em binário com sucesso.")
        except IOError as e:
            print(f"Erro ao salvar dados binários: {e}")

    def carregar_dados_binario(self, arquivo: str):
        """Carrega os dados dos pedidos de um arquivo binário usando pickle."""
        try:
            with open(arquivo, 'rb') as f:
                self.pedidos = pickle.load(f)
            print("Dados carregados do binário com sucesso.")
        except FileNotFoundError:
            print("Arquivo binário não encontrado.")
        except IOError as e:
            print(f"Erro ao carregar dados binários: {e}")

from functools import reduce

from exeption.exeptions import QuantidadeInvalidaError

class Pedido:
    def __init__(self, produtos: list, quantidade: dict, cliente: str, status: str = "Novo"):
        self.produtos = produtos
        self.quantidade = quantidade
        self.cliente = cliente
        self.status = status

        # Validação das quantidades
        if not all(q > 0 for q in quantidade.values()):
            raise QuantidadeInvalidaError("A quantidade de cada produto deve ser positiva.")

    def total_pedido(self) -> float:
        """Calcula o total do pedido usando map e reduce."""
        return reduce(
            lambda total, produto: total + produto.preco * self.quantidade[produto],
            self.produtos,
            0.0
        )

    def detalhes_pedido(self) -> str:
        """Retorna os detalhes do pedido."""
        detalhes = f"Cliente: {self.cliente}\nStatus: {self.status}\n"
        for produto in self.produtos:
            detalhes += f"{produto.detalhes()} - Quantidade: {self.quantidade[produto]}\n"
        detalhes += f"Total: {self.total_pedido():.2f}"
        return detalhes

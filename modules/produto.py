from exeption.exeptions import ValorInvalidoError


class Produto:
    def __init__(self, nome: str, preco: float, categoria: str):
        if preco <= 0:
            raise ValorInvalidoError("O preço do produto deve ser positivo.")
        self.nome = nome
        self.preco = preco
        self.categoria = categoria

    def detalhes(self) -> str:
        return f"Produto: {self.nome}, Categoria: {self.categoria}, Preço: {self.preco:.2f}"

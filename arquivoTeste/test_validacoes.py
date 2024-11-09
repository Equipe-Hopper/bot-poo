import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from modules.produto import Produto
from modules.pedido import Pedido
from exeption.exeptions import ValorInvalidoError, QuantidadeInvalidaError
from modules.produto import Produto

class TestValidacoesProdutoPedido(unittest.TestCase):

    def test_produto_preco_invalido(self):
        """Teste para verificar se ValorInvalidoError é lançado para preços negativos ou zero"""
        with self.assertRaises(ValorInvalidoError):
            Produto(nome="Produto Teste", preco=-10, categoria="Teste")

        with self.assertRaises(ValorInvalidoError):
            Produto(nome="Produto Teste", preco=0, categoria="Teste")

    def test_pedido_quantidade_invalida(self):
        """Teste para verificar se QuantidadeInvalidaError é lançado para quantidades inválidas"""
        # Criar um produto válido para usar no pedido
        produto = Produto(nome="Produto Teste", preco=50, categoria="Teste")

        # Tentar criar um pedido com quantidade negativa
        with self.assertRaises(QuantidadeInvalidaError):
            Pedido(produtos=[produto], quantidade={produto: -1}, cliente="Cliente Teste")

        # Tentar criar um pedido com quantidade zero
        with self.assertRaises(QuantidadeInvalidaError):
            Pedido(produtos=[produto], quantidade={produto: 0}, cliente="Cliente Teste")

# Executa os testes
if __name__ == "__main__":
    unittest.main()

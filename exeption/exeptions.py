class ValorInvalidoError(Exception):
    """Exceção para valores inválidos, como preços não positivos em produtos."""
    pass

class QuantidadeInvalidaError(Exception):
    """Exceção para quantidade inválida, como valores negativos ou zero."""
    pass

import functools

def log_atividade(func):
    """Decorator para registrar a execução de métodos."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"[LOG] Executando {func.__name__} com argumentos {args} {kwargs}. Retorno: {resultado}")
        return resultado
    return wrapper

from botcity.web import WebBot
from modules.gestor_de_pedidos import GestorDePedidos
# Import for the Web Botcls
from botcity.web import WebBot, Browser, By
# Import for integration with BotCity Maestro SDK
from botcity.maestro import *
import pandas as pd
from modules.pedido import Pedido
from modules.produto import Produto
from utils.carregar_dados import carregar_pedidos_do_excel

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

from webdriver_manager.chrome import ChromeDriverManager

class BotDePedidos(WebBot):

    def start_browser(self):
        # Configura o caminho do ChromeDriver usando o ChromeDriverManager
        self.driver_path = ChromeDriverManager().install()
        self.browser = Browser.CHROME
        self.headless = False  # Defina como True se desejar rodar sem abrir a janela
        super().start_browser()

    def preencher_pedidos(self, gestor: GestorDePedidos):
        # Abre o navegador e vai para a URL do formulário
        url_formulario = "https://forms.gle/H7rN167s6XLKiGXw6"
        
        for pedido in gestor.pedidos:
            # Abre o navegador e vai para a URL do formulário para cada pedido
            self.browse(url_formulario)
            self.maximize_window()
            self.wait(5000)  # Aguarda o carregamento do formulário
                
            # Localize e preencha o campo do cliente usando XPath
            cliente_field = self.find_element('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input', By.XPATH)
            self.wait(10000)

            if cliente_field:
                print("Campo 'Cliente' encontrado. Tentando clicar e preencher...")
                try:
                    cliente_field.click()  # Clicar no campo
                    cliente_field.send_keys(pedido.cliente)  # Preenche o nome do cliente
                except Exception as e:
                    print(f"Erro ao interagir com o campo 'Cliente': {e}")
                    continue  # Pule para o próximo pedido em caso de erro
            else:
                print("Campo 'Cliente' não disponível para interação.")
                continue  # Pule para o próximo pedido se o campo não for encontrado

            # Selecionar o campo STATUS
            try:
                if pedido.status.lower() == 'novo':
                    campo_novo = self.find_element('//*[@id="i11"]/div[3]/div', By.XPATH)
                    if campo_novo:
                        campo_novo.click()
                elif pedido.status.lower() == 'processando':
                    campo_processando = self.find_element('//*[@id="i14"]/div[3]/div', By.XPATH)
                    if campo_processando:
                        campo_processando.click()
                elif pedido.status.lower() == 'enviado':
                    campo_enviado = self.find_element('//*[@id="i17"]/div[3]/div', By.XPATH)
                    if campo_enviado:
                        campo_enviado.click()
                else:
                    print(f"Status não reconhecido: {pedido.status}")
                self.wait(1000)
            except Exception as e:
                print(f"Erro ao selecionar o status: {e}")
                
            # Preenche os produtos e quantidades
            for produto in pedido.produtos:
                produto_field = self.find_element('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input', By.XPATH)
                if produto_field:
                    produto_field.click()
                    produto_field.send_keys(produto.nome)

                quantidade_field = self.find_element('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input', By.XPATH)
                if quantidade_field:
                    quantidade_field.click()
                    quantidade_field.send_keys(str(pedido.quantidade[produto]))

            # Preencha o total do pedido usando XPath
            total_field = self.find_element('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input', By.XPATH)
            if total_field:
                total_field.click()
                total_field.send_keys(str(pedido.total_pedido()))
            
            # Enviar o formulário (botão de envio) usando XPath
            submit_button = self.find_element('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span', By.XPATH)
            if submit_button:
                submit_button.click()
            
            print("PEDIDO ENVIADO COM SUCESSO!")

            # Aguarde alguns segundos antes de passar para o próximo pedido
            self.wait(2000)  # Ajuste conforme necessário
    
    ## Método que atende ao requisito de "extrair os dados de pedidos de uma interface externa e carregar na aplicação"
    def carregar_pedidos_planilha(self, caminho_arquivo, gestor):
        
        try:
           
            df = pd.read_excel(caminho_arquivo)

            for _, row in df.iterrows():
                # Extrai e padroniza os dados do pedido
                produto = Produto(nome=row['Produto'], preco=row['Preco'], categoria=row['Categoria'])
                quantidade = {produto: row['Quantidade']}
                status = row['Status'].capitalize()  # Padroniza para a primeira letra maiúscula

                pedido = Pedido(produtos=[produto], quantidade=quantidade, cliente=row['Cliente'], status=status)
                gestor.adicionar_pedido(pedido)

            print("Pedidos carregados com sucesso a partir da planilha.")
        
        except FileNotFoundError:
            print(f"Erro: o arquivo '{caminho_arquivo}' não foi encontrado.")
        except Exception as e:
            print(f"Erro ao carregar pedidos da planilha: {e}")
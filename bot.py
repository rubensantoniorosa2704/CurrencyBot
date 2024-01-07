import csv
import platform
from datetime import datetime
import logging

from botcity.web import WebBot, Browser
from botcity.maestro import BotMaestroSDK, AutomationTaskFinishStatus

from selenium.webdriver.firefox.options import Options

# Configuração para evitar exceções ao interagir com o BotMaestroSDK
BotMaestroSDK.RAISE_NOT_CONNECTED = False

class CotacaoBot:
    """
    Classe para interagir com o bot de navegação web.
    """
    def __init__(self, headless: bool, full_driver_path: str = None):
        """
        Inicializa o bot e aplica as configurações.

        :param headless: Um booleano indicando se o navegador deve ser executado em modo headless.
        :param full_driver_path: O caminho completo para o driver do navegador. Informar None usa o driver padrão no PATH
        """
        firefox_options = Options()
        firefox_options.headless = headless

        self.bot = WebBot()
        
        # Check if running on Windows and set Firefox binary path accordingly
        if platform.system() == 'Windows':
            firefox_binary_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
            firefox_options.binary_location = firefox_binary_path
            self.bot.options = firefox_options
        
        if full_driver_path:
            self.bot.driver_path = full_driver_path

        self.bot.headless = headless
        self.bot.browser = Browser.FIREFOX


    def browse_and_get_cotacao(self, moeda) -> str:
        """
        Navega até a página do Google e extrai a moeda e a cotação.

        Args:
            moeda (str): Nome da moeda.

        Returns:
            Tuple[str, str]: Retorna a moeda e a cotação.
        """
        try:
            self.bot.browse(f"https://www.google.com/search?q=cotação+{moeda}")
            script_moeda = 'return document.querySelector("span.vLqKYe").textContent;'
            script_cotacao = 'return document.querySelector(".SwHCTb").textContent;'
            temp_moeda = self.bot.execute_javascript(script_moeda)
            temp_cotacao = self.bot.execute_javascript(script_cotacao)
            return temp_moeda, temp_cotacao
        except Exception as e:
            print(f"Error browsing and extracting data for {moeda}: {str(e)}")

    def stop_browser(self):
        """
        Para o navegador web.
        """
        try:
            self.bot.stop_browser()
        except Exception as e:
            print(f"Error stopping the browser: {str(e)}")

class LogFile:
    """
    Classe para gerenciar o arquivo de log.
    """
    def __init__(self, filename='cotacoes.log'):
        """
        Inicializa o arquivo de log.

        Args:
            filename (str): Nome do arquivo de log.
        """
        logging.basicConfig(filename=filename, level=logging.INFO, encoding='UTF-8')

    def write(self, message):
        """
        Escreve uma mensagem no arquivo de log.

        Args:
            message (str): Mensagem a ser escrita.
        """
        try:
            logging.info(message)
        except Exception as e:
            print(f"Error writing to log file: {str(e)}")

class CsvFile:
    """
    Classe para gerenciar o arquivo CSV.
    """
    def __init__(self, filename='cotacoes.csv'):
        """
        Inicializa o arquivo CSV.

        Args:
            filename (str): Nome do arquivo CSV.
        """
        self.filename = filename

    def setup_file(self):
        """
        Configura o arquivo CSV, adicionando cabeçalho se o arquivo estiver vazio.
        """
        try:
            with open(self.filename, 'a', newline='', encoding='UTF-8') as file:
                writer = csv.writer(file, delimiter=';')
                if file.tell() == 0:
                    writer.writerow(["Data", "Moeda", "Cotação"])
        except Exception as e:
            print(f"Error setting up CSV file: {str(e)}")

    def write(self, data, moeda, cotacao):
        """
        Escreve uma linha no arquivo CSV.

        Args:
            data (str): Data da cotação.
            moeda (str): Nome da moeda.
            cotacao (str): Valor da cotação.
        """
        try:
            with open(self.filename, 'a', newline='', encoding='UTF-8') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([data, moeda, cotacao])
        except Exception as e:
            print(f"Error writing to CSV file: {str(e)}")

def data_e_hora_atual() -> datetime:
    """
    Retorna a data e a hora atual no formato '%d/%m/%Y %H:%M'.

    Returns:
        str: Data e hora formatadas.
    """
    try:
        data_e_hora = datetime.now()
        return data_e_hora.strftime('%d/%m/%Y %H:%M')
    except Exception as e:
        print(f"Error getting current date and time: {str(e)}")
        return None

def not_found(label):
    """
    Imprime uma mensagem indicando que um elemento não foi encontrado.

    Args:
        label (str): Rótulo do elemento.
    """
    try:
        print(f"Element not found: {label}")
    except Exception as e:
        print(f"Error printing 'not found' message: {str(e)}")
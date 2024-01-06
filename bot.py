import csv
from datetime import datetime
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from botcity.web import WebBot, Browser
from botcity.maestro import *

BotMaestroSDK.RAISE_NOT_CONNECTED = False

def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()
    bot.headless = False
    bot.browser = Browser.FIREFOX

    pesquisa_cotacao(bot, 'dolar', 'euro', 'libra', 'iene')
    bot.stop_browser()

    maestro.finish_task(
        task_id=execution.task_id,
        status=AutomationTaskFinishStatus.SUCCESS,
        message="Task Finished OK."
    )

def not_found(label):
    print(f"Element not found: {label}")

def data_e_hora_atual() -> str:
        data_e_hora = datetime.now()
        return data_e_hora.strftime('%d/%m/%Y %H:%M')

def pesquisa_cotacao(bot, *args):
    logging.basicConfig(filename='cotacoes.log', level=logging.INFO)

    with open('cotacoes.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')

        if file.tell() == 0:
            writer.writerow(["Data", "Moeda", "Cotacao"])

        for moeda in args:
            temp_data = data_e_hora_atual()
            temp_moeda = moeda

            bot.browse(f"https://www.google.com/search?q=cotação+{moeda}")

            script_moeda = 'return document.querySelector("span.vLqKYe").textContent;'
            script_cotacao = 'return document.querySelector(".SwHCTb").textContent;'

            temp_moeda = bot.execute_javascript(script_moeda)
            temp_cotacao = bot.execute_javascript(script_cotacao)

            if temp_moeda and temp_cotacao:
                writer.writerow([temp_data, temp_moeda, temp_cotacao])

                resultado_log = f'[{temp_data}] MOEDA: {temp_moeda.upper()}; COTAÇÃO: {temp_cotacao}.'
                logging.info(resultado_log)
            else:
                not_found(f'Moeda: {moeda}')

if __name__ == '__main__':
    main()
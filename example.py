# -*- coding: UTF-8 -*-
import PySimpleGUI as sg
from bot import *

def main():
    sg.theme('LightGrey1')

    layout = [
        [sg.Text('Selecione as moedas para pesquisa:')],
        [sg.Checkbox('Dólar', key='dolar'), sg.Checkbox('Euro', key='euro'),
         sg.Checkbox('Libra', key='libra'), sg.Checkbox('Iene', key='iene')],
        [sg.Checkbox('Modo Headless', key='headless')],
        [sg.Button('Iniciar Pesquisa')],
    ]

    window = sg.Window('Cotação de Moedas', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == 'Iniciar Pesquisa':
            selected_currencies = [currency for currency in ['dolar', 'euro', 'libra', 'iene'] if values[currency]]
            headless_mode = values['headless']

            if not selected_currencies:
                sg.popup('Selecione pelo menos uma moeda para pesquisa.')
                continue  # Volta ao início do loop para esperar uma seleção válida

            maestro = BotMaestroSDK.from_sys_args()
            execution = maestro.get_execution()

            cotacao_bot = CotacaoBot(headless=headless_mode)
            log_file = LogFile()
            csv_file = CsvFile()

            csv_file.setup_file()

            for temp_moeda in selected_currencies:
                temp_data = data_e_hora_atual()
                temp_moeda, temp_cotacao = cotacao_bot.browse_and_get_cotacao(temp_moeda)

                if temp_moeda and temp_cotacao:
                    csv_file.write(temp_data, temp_moeda, temp_cotacao)

                    resultado_log = f'[{temp_data}] MOEDA: {temp_moeda.upper()}; COTAÇÃO: {temp_cotacao}.'
                    log_file.write(resultado_log)
                else:
                    not_found(f'Moeda: {temp_moeda}')
                    sg.popup(f'Não foi possível extrair a cotação. Verifique sua conexão com a internet e tente novamente')

            cotacao_bot.stop_browser()

            maestro.finish_task(
                task_id=execution.task_id,
                status=AutomationTaskFinishStatus.SUCCESS,
                message="Task Finished OK."
            )

    window.close()

if __name__ == '__main__':
    main()
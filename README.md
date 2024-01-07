# CurrencyBot
Cotação de moedas em tempo real, inspirado no [ConversorSelenium](https://github.com/CastroMurilo/ConversorSelenium) de CastroMurilo.

## Funcionalidades

### 1. Classe `CotacaoBot`

A classe `CotacaoBot` é responsável por interagir com o bot de navegação web. Ela possui os seguintes métodos:

- `__init__(self, headless:bool)`: Inicializa o bot de navegação web com a opção de modo headless.
- `browse_and_get_cotacao(self, moeda) -> Tuple[str, str]`: Navega até a página do Google e extrai a moeda e a cotação.
- `stop_browser(self)`: Para o navegador web.

### 2. Classe `LogFile`

A classe `LogFile` gerencia o arquivo de log. Ela possui os seguintes métodos:

- `__init__(self, filename='cotacoes.log')`: Inicializa o arquivo de log com um nome padrão ou especificado.
- `write(self, message)`: Escreve uma mensagem no arquivo de log.

### 3. Classe `CsvFile`

A classe `CsvFile` gerencia o arquivo CSV. Ela possui os seguintes métodos:

- `__init__(self, filename='cotacoes.csv')`: Inicializa o arquivo CSV com um nome padrão ou especificado.
- `setup_file(self)`: Configura o arquivo CSV, adicionando cabeçalho se o arquivo estiver vazio.
- `write(self, data, moeda, cotacao)`: Escreve uma linha no arquivo CSV.

### 4. Função `data_e_hora_atual()`

Retorna a data e a hora atual no formato '%d/%m/%Y %H:%M'.

### 5. Função `not_found(label)`

Imprime uma mensagem indicando que um elemento não foi encontrado.

## Executando um exemplo

Para executar o CurrencyBot, utilize o script `example.py`. O programa permite selecionar as moedas desejadas para pesquisa, escolher o modo headless e exibe os resultados na interface gráfica.

Certifique-se de ter as dependências do projeto instaladas antes de executar. Utilize o seguinte comando para instalar as dependências:

```bash
pip install -r requirements.txt

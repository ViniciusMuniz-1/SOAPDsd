# Projeto SOAP para Jogo de Avatar

Este projeto demonstra a comunicação entre um cliente JavaScript e um servidor Python utilizando SOAP (Simple Object Access Protocol). O cliente faz perguntas ao usuário, envia as respostas para o servidor SOAP e o servidor retorna o personagem correspondente com base nas respostas.

## Estrutura do Projeto

- `server.py`: Implementação do servidor SOAP em Python.
- `client.mjs`: Implementação do cliente SOAP em JavaScript.
- `wsdl.xml`: Arquivo WSDL descrevendo o serviço SOAP.

## Pré-requisitos

Antes de começar, certifique-se de que você tem o seguinte instalado:

- **Python** (versão 3.6 ou superior)
- **Node.js** (versão 14 ou superior)

## Configuração do Servidor

1. **Instale as dependências do Python:**

   Crie um ambiente virtual e instale as bibliotecas necessárias com `pip`:

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   pip install flask lxml zeep

- **Node.js** (versão 14 ou superior)

2. **Inicie o servidor:**

    python server.py

## Configuração do Cliente

1. **Clone o repositório ou faça o download do código:**

   Certifique-se de que o arquivo `client.mjs` está no diretório de trabalho.

2. **Instale as dependências necessárias:**

   Navegue até o diretório onde o `client.mjs` está localizado e instale os pacotes necessários com o `npm`:

   ```bash
   npm install xml2js node-fetch readline-sync

3. **Execute o cliente:**

    node client.mjs
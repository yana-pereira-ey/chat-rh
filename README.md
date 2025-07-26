# Assistente Virtual

## Descrição
Este é um projeto de um agente ChatBot desenvolvido para auxiliar os funcionários do cliente no entendimento de questões corporativas. 
O ChatBot lê a pergunta do usuário, explica seu pensamento e retorna uma resposta clara e abrangente. 
O pensamento do ChatBot pode ser acessado através de um botão que abre um pop-up no front-end.

## Arquitetura
A arquitetura do projeto é composta pelos seguintes componentes:

### Frontend
- Desenvolvido com Python Flask, JavaScript, HTML e CSS.
- Tela de autenticação com SSO.

### Backend
- Desenvolvido em Python.
- Soluções Azure utilizadas:
  - Microsoft Entra ID para administrar os usuários.
  - Azure AISearch para armazenamento dos vetores.
  - CosmoDB para armazenar o histórico e conversas dos usuários.
  - Azure Key Vault para armazenamento das credenciais e variáveis de ambiente.
  - Modelo de linguagem baseado no Azure OpenAI.

- LangChain utilizado como orquestrador para integrar o modelo de linguagem com o OpenSearch.


## Instalação
Para instalar e executar o projeto localmente, siga os passos abaixo:

1. Clone o repositório:
   ```bash
   git clone git@github.com:EYLatamSouth/talent_ai_chatbot.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd talent_ai_chatbot
   ```

3. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```

4. Criar um arquivo .env na raiz do projeto contendo as seguintes credenciais:
```
   # Azure OpenAI
   AZURE_OPENAI_API_KEY = ""
   AZURE_OPENAI_ENDPOINT= ""
   AZURE_OPENAI_API_VERSION= ""
   AZURE_OPENAI_CHAT_DEPLOYMENT_NAME= ""
   AZURE_MODEL_NAME=""
   EMBEDDING_MODEL=""

   # Azure AI Search
   AZURE_SEARCH_ENDPOINT=""
   AZURE_SEARCH_ADMIN_KEY=""

   # Azure Blob Storage
   AZURE_STORAGE_CONNECTION_STRING=""
   AZURE_STORAGE_ACCOUNT_NAME=""
   AZURE_STORAGE_ACCOUNT_KEY=""

   # Auth using Microsfot ENTRA ID
   CLIENT_ID=""
   CLIENT_SECRET=""
   AUTHORITY=""

   FLASK_SECRET_KEY=""
```

## Uso
Para iniciar o servidor, execute:
```bash
python main_app.py
```

## Observação:Caso ocorra algum erro relacionado a  "werkzeug" excute o comando abaixo
```bash
pip install --upgrade flask werkzeug
```

## Autores 
* **Juliana Araújo** - *Manager* - [julianac.araujo@br.ey.com](mailto:julianac.araujo@br.ey.com)
* **Marcelo Claro** - *Tech Lead* - [marcelo.claro@br.ey.com](mailto:marcelo.claro@br.ey.com)
* **Paulo Jarbas Camurça** - *Data Scientist* - [paulo.camurca@br.ey.com](mailto:paulo.camurca@br.ey.com)
* **Luiz Hoffmann** - *Data Scientist* - [luiz.hoffmann@br.ey.com](mailto:luiz.hoffmann@br.ey.com)

## Status do Projeto
O projeto está em andamento e novas funcionalidades estão sendo continuamente adicionadas. 
Estamos abertos a sugestões e colaborações para melhorar o ChatBot.
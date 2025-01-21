# LimpAeh - Back-end

Bem-vindo ao repositório do back-end do sistema LimpAeh, desenvolvido para gerenciar atividades de limpeza em instituições públicas de ensino. Este sistema permite o registro, monitoramento e automação das solicitações e atividades de limpeza, melhorando a comunicação entre administradores, supervisores e funcionários.

## Tecnologias Utilizadas
- Flask
- Flask-RESTful
- Flask-Migrate
- PostgreSQL

## Pré-requisitos
Antes de começar, certifique-se de ter o seguinte instalado:
- PostgreSQL
- Git

## Instalação
1. Clone este repositório:
   ```bash
   git clone https://github.com/vivaldovitor/limpaeh-backend.git
   cd limpaeh-backend
   ```

2. Crie um ambiente virtual:
    ```bash
    virtualenv venv
    source venv/bin/activate  # Linux/MacOS
    venv\Scripts\activate # Windows
    ```

3. Instale as dependências
    ```bash
    pip install -r requirements.txt
    ```

4. Configure o banco de dados no arquivo .env.

5. Rode o projeto
    ```bash
    python app.py
    ```
# Utilizando MyWorkbench

Este é um guia passo a passo para configurar e executar o script `MyWorkbench.py`, uma aplicação de consulta e salvamento de dados em um banco de dados MySQL, usando o script de instalação `executar_myworkbench.sh`.

## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes pré-requisitos instalados em seu sistema:

- Python 3
- Git (para clonar o repositório)

## Instalação e Execução

1. **Clone o repositório**

   Abra o terminal e clone o repositório `MyWorkbench`:

   ```bash
   git clone https://github.com/jean-nathan/MyWorkbench.git
   ```

2. **Navegue até o diretório do projeto**

   Vá para o diretório `MyWorkbench`:

   ```bash
   cd MyWorkbench
   ```

3. **Execute o script de instalação**

   Execute o script `executar_myworkbench.sh` para configurar o ambiente e iniciar o `MyWorkbench`:

   ```bash
   ./executar_myworkbench.sh
   ```

   Este script realizará as seguintes etapas:
   - Verificar se o ambiente virtual está ativado. Se não estiver, ele será criado e ativado automaticamente.
   - Verificar e instalar o Python3 e o `pip` se não estiverem instalados.
   - Instalar as dependências necessárias (`mysql-connector-python`, `pandas`).
   - Executar o script `MyWorkbench.py` dentro do ambiente virtual.

4. **Interagindo com MyWorkbench**

   Após a execução bem-sucedida do script `executar_myworkbench.sh`, o `MyWorkbench` estará pronto para uso. Você pode iniciar o `MyWorkbench` sempre que necessário executando:

   ```bash
   ./executar_myworkbench.sh
   ```

   Isso ativará automaticamente o ambiente virtual, instalará as dependências e iniciará o `MyWorkbench.py`.

5. **Imagens**

   **Configuração Conexão:**

   <img width="535" alt="image" src="https://github.com/jean-nathan/MyWorkbench/assets/118441482/773429ac-1696-4e46-bef9-f605cc700651">

   **Consulta Dados:**

   <img width="536" alt="image" src="https://github.com/jean-nathan/MyWorkbench/assets/118441482/fe41ae89-8485-46ef-b598-4e7bde67bca2">

Este é um guia passo a passo para configurar e executar o script `MyWorkbench.py`, uma aplicação de consulta e salvamento de dados em um banco de dados MySQL.

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

3. **Permissões de execução**

   Antes de executar o script `executar_myworkbench.sh`, certifique-se de que ele possui permissões de execução:

   ```bash
   chmod +x executar_myworkbench.sh
   ```

4. **Execute o script de instalação**

   Execute o script `executar_myworkbench.sh` para configurar o ambiente e iniciar o `MyWorkbench`:

   ```bash
   ./executar_myworkbench.sh
   ```

   Este script realizará as seguintes etapas:
   - Verificará se o ambiente virtual está ativado. Se não estiver, será criado e ativado automaticamente.
   - Verificará e instalará o Python3 e o `pip` se não estiverem instalados.
   - Instalará as dependências necessárias (`mysql-connector-python`, `pandas`).
   - Executará o script `MyWorkbench.py` dentro do ambiente virtual.

5. **Interagindo com MyWorkbench**

   Após a execução bem-sucedida do script `executar_myworkbench.sh`, o `MyWorkbench` estará pronto para uso. Você pode iniciar o `MyWorkbench` sempre que necessário executando:

   ```bash
   ./executar_myworkbench.sh
   ```

   Isso ativará automaticamente o ambiente virtual, instalará as dependências e iniciará o `MyWorkbench.py`.

## Capturas de tela

### Configuração de Conexão:

<img width="535" alt="Configuração de Conexão" src="assets/configuracao_conexao.png">

### Consulta de Dados:

<img width="536" alt="Consulta de Dados" src="assets/consulta_dados.png">
```

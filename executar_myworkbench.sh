#!/bin/bash

set -e  # Abortar imediatamente se um comando falhar

# Diretório de logs
LOG_DIR="logs"
mkdir -p "$LOG_DIR"

# Função para registrar mensagens no log
log() {
    local timestamp
    timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] $1" >> "$LOG_DIR/myworkbench.log"
}

# Verificar se o ambiente virtual está ativado
if [ -z "$VIRTUAL_ENV" ]; then
    log "Criando e ativando ambiente virtual..."

    # Verificar e instalar python3-venv se necessário (Linux)
    if command -v apt-get &> /dev/null; then
        log "Instalando python3-venv..."
        sudo apt-get update >> "$LOG_DIR/apt_update.log"  # Logar saída do apt-get update
        sudo apt-get install -y python3-venv >> "$LOG_DIR/python3-venv_install.log"  # Logar saída do apt-get install

    # Verificar e instalar python3-venv se necessário (macOS)
    elif command -v brew &> /dev/null; then
        log "Instalando python3-venv..."
        brew install python3 >> "$LOG_DIR/brew_install.log"  # Logar saída do brew install

    else
        log "Gerenciador de pacotes não suportado. Instale manualmente python3-venv."
        exit 1
    fi

    # Criar e ativar o ambiente virtual
    python3 -m venv myenv
    source myenv/bin/activate
fi

# Verificar e instalar dependências necessárias dentro do ambiente virtual
if ! command -v pip &> /dev/null; then
    log "pip não encontrado. Instalando pip..."
    python3 -m ensurepip --upgrade >> "$LOG_DIR/ensurepip.log"  # Logar saída do ensurepip
fi

# Instalar ou atualizar as dependências
log "Instalando/atualizando dependências..."
pip install --upgrade mysql-connector-python pandas >> "$LOG_DIR/pip_install.log"  # Logar saída do pip install

# Executar o script Python dentro do ambiente virtual
log "Executando MyWorkbench..."
python3 MyWorkbench.py >> "$LOG_DIR/myworkbench_execution.log"  # Logar saída do script Python

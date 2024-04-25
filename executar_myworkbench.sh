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

# Verificar qual é o sistema operacional
if [[ "$OSTYPE" == "darwin"* ]]; then
    log "Sistema operacional detectado: macOS"

    # Verificar se o ambiente virtual está ativado
    if [ -z "$VIRTUAL_ENV" ]; then
        log "Criando e ativando ambiente virtual..."

        # Verificar e instalar python3-venv se necessário
        if ! command -v python3-venv &> /dev/null; then
            log "Instalando python3-venv..."
            # Baixar o instalador do Python
            curl -o python-installer.pkg https://www.python.org/ftp/python/3.10.6/python-3.10.6-macos11.pkg
            # Instalar o Python a partir do instalador baixado
            sudo installer -pkg python-installer.pkg -target /
            rm python-installer.pkg  # Remover o instalador após a instalação
        fi

        # Criar e ativar o ambiente virtual
        python3 -m venv myenv
        source myenv/bin/activate
    fi

    # Verificar e instalar dependências necessárias dentro do ambiente virtual
    if ! command -v pip &> /dev/null; then
        log "pip não encontrado. Instalando pip..."
        # Instalar pip manualmente
        sudo easy_install pip
    fi

    # Instalar ou atualizar as dependências
    log "Instalando/atualizando dependências..."
    pip install --upgrade mysql-connector-python pandas >> "$LOG_DIR/pip_install.log"  # Logar saída do pip install

    # Executar o script Python dentro do ambiente virtual
    log "Executando MyWorkbench..."
    python3 MyWorkbench.py >> "$LOG_DIR/myworkbench_execution.log"  # Logar saída do script Python
else
    log "Sistema operacional não suportado. Instale manualmente as dependências."
    exit 1
fi

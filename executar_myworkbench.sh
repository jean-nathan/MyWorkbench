#!/bin/bash

# Verificar se o ambiente virtual está ativado
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Criando e ativando ambiente virtual..."
    
    # Verificar e instalar python3-venv se necessário
    if ! command -v python3-venv &> /dev/null; then
        echo "Instalando python3-venv..."
        sudo apt-get update
        sudo apt-get install -y python3-venv
    fi
    
    # Criar e ativar o ambiente virtual
    python3 -m venv myenv
    source myenv/bin/activate
fi

# Verificar e instalar dependências necessárias
if ! command -v python3 &> /dev/null; then
    echo "Python3 não encontrado. Instalando Python..."
    sudo apt-get update
    sudo apt-get install -y python3
fi

if ! command -v pip &> /dev/null; then
    echo "pip não encontrado. Instalando pip..."
    sudo apt-get install -y python3-pip
fi

# Instalar as dependências necessárias no ambiente virtual
echo "Instalando dependências..."
source myenv/bin/activate  # Ativar o ambiente virtual antes de instalar as dependências
pip install mysql-connector-python pandas

# Executar o script Python
echo "Executando MyWorkbench..."
python3 MyWorkbench.py

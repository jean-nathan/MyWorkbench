#!/bin/bash

# Verificar se o ambiente virtual está ativado
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Criando e ativando ambiente virtual..."
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

echo "Instalando dependências..."
pip install mysql-connector-python pandas

# Executar o script Python
echo "Executando MyWorkbench..."
python3 MyWorkbench.py

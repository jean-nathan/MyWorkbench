#!/bin/bash

# Verificar se o ambiente virtual está ativado
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Criando e ativando ambiente virtual..."
    python3 -m venv myenv
    source myenv/bin/activate
fi

# Função para instalar o pacote python3-venv no Ubuntu/Debian
install_python3_venv_ubuntu() {
    echo "Instalando python3-venv no Ubuntu/Debian..."
    sudo apt update
    sudo apt install -y python3-venv
}

# Função para instalar o pacote python3-venv no macOS usando Homebrew
install_python3_venv_macos() {
    echo "Instalando python3-venv no macOS..."
    brew update
    brew install python3
}

# Verificar e instalar o pacote python3-venv se não estiver disponível
if ! [ -x "$(command -v python3 -m venv)" ]; then
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        install_python3_venv_ubuntu
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        install_python3_venv_macos
    else
        echo "Sistema operacional não suportado."
        exit 1
    fi
fi

# Verificar e instalar dependências necessárias
if ! command -v python3 &> /dev/null; then
    echo "Python3 não encontrado. Instalando Python..."
    sudo apt update
    sudo apt install -y python3
fi

if ! command -v pip &> /dev/null; then
    echo "pip não encontrado. Instalando pip..."
    sudo apt install -y python3-pip
fi

echo "Instalando dependências..."
pip install mysql-connector-python pandas

# Executar o script Python
echo "Executando MyWorkbench..."
python3 MyWorkbench.py

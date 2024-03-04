#!/bin/bash

sudo apt install python3-pip python3-venv -y

# Configurar ambiente virtual venv
echo -e '[CONFIGURAÇÃO] Criando ambiente virtual.'
[ -d "venv" ] && rm -rf ./venv && python3 -m venv ./venv  || python3 -m venv ./venv

if [ $? -eq 0 ]; then
    echo -e '[CONFIGURAÇÃO] Ativando o ambiente virtual.'
    source venv/bin/activate
    pip3 install --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt
else
    echo -e '[ERRO] Falha ao criar o ambiente virtual.'
    exit 1
fi

# Zaproxy
echo -e "[CONFIGURAÇÃO] Baixando o Zap Proxy"
versao="2.14.0"
if [ -d "ZAP_$versao" ]; then
    echo -e "Zap Proxy já está instalado."
    exit 0
else
    wget https://github.com/zaproxy/zaproxy/releases/download/v$versao/ZAP_$versao.tar.gz
    tar -zxvf ZAP_$versao.tar.gz
    unlink ZAP_$versao.tar.gz 
fi

echo -e "[CONFIGURAÇÃO] finalizada!"

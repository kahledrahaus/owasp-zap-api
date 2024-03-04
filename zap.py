###################################################################
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Script Name: zap.py
# Description: Automação de testes usando zap proxy
# Date: 03/04/2022
# Author: @kahledrahaus
# Encode: UTF8
###################################################################

from zapv2 import ZAPv2
from pprint import pprint
import time
import sys
import os
import datetime

def run_zap_scan(target):
    zap = ZAPv2(apikey='2e04c978070fb9756cde6a684a')
    
    # Fecha a sessão anterior antes de criar uma nova sessão
    zap.core.new_session()

    # Abrindo a url informada no prompt
    zap.urlopen(target)

    # Executando scanner passivo spider
    scanID = zap.spider.scan(target)

    print('Executando varredura Spider...')
    time.sleep(1)
    
    # Faça um loop até que o scanner termine
    while int(zap.spider.status(scanID)) < 100:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'Executando varredura Spider...')
        print('Progresso da varredura Spider: {}'.format(zap.spider.status(scanID)), '%')
        time.sleep(5)
    
    print('Varredura Spider concluído.')
    time.sleep(3)
    os.system('cls' if os.name == 'nt' else 'clear')

    # Executando varredura Ajax Spider
    print('Executando varredura Ajax Spider...')
    scanID = zap.ajaxSpider.scan(target)

    timeout = time.time() + 60*2   
    while zap.ajaxSpider.status == 'running':
        if time.time() > timeout:
            break
        print('Ajax Spider status ' + zap.ajaxSpider.status)
        time.sleep(2)

    print('Varredura Ajax Spider concluida...')
    time.sleep(3)
    os.system('cls' if os.name == 'nt' else 'clear')

    # Executando scanner ativo
    scanID = zap.ascan.scan(target)
    
    print(f'Executando varredura ativa...')
    time.sleep(1)
    
    # Faça um loop até que o scanner termine
    while int(zap.ascan.status(scanID)) < 100:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'Executando varredura ativa...')
        print('Progresso da varredura ativa: {}'.format(zap.ascan.status(scanID)), '%')
        time.sleep(5)

    print('Varredura ativa concluída.')
    time.sleep(3)
    os.system('cls' if os.name == 'nt' else 'clear')

    # Mostra as vulnerabilidades encontradas pela verificação no formato json no terminal
    # print('Hosts: {}'.format(', '.join(zap.core.hosts)))
    # print('Alerts: ')
    # pprint(zap.core.alerts(baseurl=target_url))

    # Exibe os resultados
    hosts = zap.core.hosts
    print(f'Hosts escaneados: {len(hosts)}')
    time.sleep(1)
    for host in hosts:
        print(f' - {host}')

    alerts = zap.core.alerts()
    print(f'Número de alertas encontrados: {len(alerts)}')
    time.sleep(1)

    # Gera relatório em HTML
    report_html = zap.core.htmlreport()   
    with open(f'Reports/{report_file_name}_report.html', 'w', encoding='utf-8') as f:
        f.write(report_html)
    print(f'\nRelatório gerado com sucesso e salvo em Reports/{report_file_name}_report.html.')

    # Gera relatório em JSON
    report_json = zap.core.jsonreport()
    with open(f'Reports/{report_file_name}_report.json', 'w') as f:
        f.write(report_json)
    print(f'\nRelatório gerado com sucesso e salvo em Reports/{report_file_name}_report.json.')

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Argumentos insuficientes. Informe o URL do alvo.')
        sys.exit(1)

    target = sys.argv[1]
    
    # Extrai o nome do domínio do URL do alvo
    host_name = target.split('/')[2]
    host_name = host_name.replace('.', '_')
    
    now = datetime.datetime.now()
    date_str = now.strftime('%Y-%m-%d_%H-%M-%S')
    
    # Define o nome do arquivo com a data atual e o nome do host
    report_file_name = f'{date_str}_{host_name}_report.html'
    
    # Executa a varredura e gera o relatório
    run_zap_scan(target)

# Subdomain IP Resolver

## Descrição
Este script em Python automatiza a busca por subdomínios de um domínio específico, resolve seus respectivos endereços IP e verifica quais estão ativos com código HTTP 200. Os resultados são armazenados em um arquivo de texto contendo informações importantes sobre a análise realizada.

## Funcionalidades
Coleta de subdomínios a partir das fontes públicas crt.sh e RapidDNS.

Resolução de IP dos subdomínios encontrados.

Verificação de status HTTP, identificando quais subdomínios respondem com código 200.

Filtragem de resultados, removendo subdomínios não resolvidos e e-mails.

Armazenamento dos resultados em um arquivo de texto, incluindo estatísticas da análise.

Execução multithread para melhorar o desempenho.

## Uso
python script.py exemplo.com

O script salvará os resultados no arquivo exemplo.com_subdomains.txt e exibirá o caminho do arquivo gerado.

## Dependências
Python 3.x
Bibliotecas: requests, socket, re, sys, os, time, concurrent.futures

Instale as dependências com:
pip install requests

### Exemplo de saída:
[+] Iniciando busca de subdomínios para exemplo.com...

[+] Foram encontrados 120 subdomínios. Resolvendo IPs...

[>] Resolvendo: sub1.exemplo.com -> 192.168.1.1

[>] Resolvendo: sub2.exemplo.com -> Não resolvido

[+] Verificando status HTTP...

[>] Checando: sub1.exemplo.com -> Status 200

[✔] Resultados salvos em: /caminho/para/exemplo.com_subdomains.txt

[✔] Subdomínios ativos (código 200) salvos: 85


Este projeto está licenciado sob a GNU General Public License v3.0 (GPLv3).  
Você pode modificar e distribuir este código, mas qualquer versão derivada deve ser distribuída sob a mesma licença.  
Veja a licença completa em: https://www.gnu.org/licenses/gpl-3.0.html


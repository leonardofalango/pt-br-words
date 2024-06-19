import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

letters = [chr(chr_code).lower() for chr_code in range(97, 123)]  # Letras de 'a' a 'z'
base_url = 'https://www.dicio.com.br/palavras-com-'

def parse_url(url):
    try:
        print("Requisição para", url)
        response = requests.get(url)
        
        if response.status_code == 200:
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')
            
            paragrafos = soup.find_all('p')
            paragrafos_filtrados = []
            
            for p in paragrafos:
                if "Dicio, Dicionário Online de Português" not in p.text and "Lista com" not in p.text and 'Palavras populare' not in p.text:
                    filter = str(p).replace("<br/>", "\n").replace("<p>", "").replace("</p>", "").replace(" ", "")
                    paragrafos_filtrados.append(filter)
            return paragrafos_filtrados
        else:
            print(f'A requisição retornou um erro: {response.status_code}')
    except Exception as e:
        print(f'Erro ao processar a URL {url}: {e}')
        return None

# Usar ThreadPoolExecutor para processar múltiplas URLs simultaneamente
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(parse_url, base_url + letter) for letter in letters]
    
    # Iterar sobre os resultados conforme eles forem completados
    for future in as_completed(futures):
        try:
            paragrafos = future.result()
            if paragrafos:
                with open("dic.txt", 'a', encoding='utf-8') as f:
                    for p in paragrafos:
                        f.write(p + '\n')  # Escrever o texto do parágrafo no arquivo com quebra de linha
        except Exception as e:
            print(f'Erro ao processar um resultado: {e}')

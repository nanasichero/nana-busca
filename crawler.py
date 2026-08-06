import requests
from bs4 import BeautifulSoup
import sqlite3

def crawl_page(url):
    try:
        # 1. Acessa a página
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. Extrai o título e o texto limpo (sem tags HTML)
        title = soup.title.string if soup.title else 'Sem título'
        
        # Remove scripts e estilos para pegar só o texto útil
        for script in soup(["script", "style"]):
            script.extract()
        content = soup.get_text(separator=' ', strip=True)
        
        # 3. Salva no nosso índice (Banco de Dados)
        conn = sqlite3.connect('search_engine.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pages (url, title, content) VALUES (?, ?, ?)", 
                       (url, title, content))
        conn.commit()
        conn.close()
        
        print(f"Indexado com sucesso: {url}")
        
    except Exception as e:
        print(f"Erro ao indexar {url}: {e}")

# Teste com uma página simples (ex: Wikipedia)
crawl_page("https://pt.wikipedia.org/wiki/Python")

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sqlite3

app = FastAPI()

# Rota para a API de busca
@app.get("/search")
def search(q: str):
    conn = sqlite3.connect('search_engine.db')
    cursor = conn.cursor()
    
    query = """
        SELECT url, title, snippet(pages, 2, '<b>', '</b>', '...', 20) as preview
        FROM pages 
        WHERE pages MATCH ? 
        ORDER BY rank 
        LIMIT 10
    """
    cursor.execute(query, (q,))
    results = cursor.fetchall()
    conn.close()
    
    formatted_results = [
        {"url": row[0], "title": row[1], "preview": row[2]} 
        for row in results
    ]
    
    return {"query": q, "results": formatted_results}

# Serve a pasta 'static' para exibir o index.html na raiz (http://127.0.0.1:8000/)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

import sqlite3

def setup_database():
    conn = sqlite3.connect('search_engine.db')
    cursor = conn.cursor()
    
    # Cria uma tabela virtual FTS5 para busca textual ultra-rápida
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS pages USING fts5(
            url, 
            title, 
            content
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    print("Banco de dados criado com sucesso!")

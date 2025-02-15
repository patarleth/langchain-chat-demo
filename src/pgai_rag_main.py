import os
import psycopg2
from pgvector.psycopg2 import register_vector

# Shamelessly 'borrowed' from https://github.com/timescale/private-rag-example/

def connect_db(ollama_host, postgresql_host, postgresql_port, user, password, db_name):
    conn = psycopg2.connect( # use the credentials of your postgresql database 
        host = postgresql_host,
        database = db_name,
        user = user,
        password = password,
        port = postgresql_port
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute(f"select set_config('ai.ollama_host', '{ollama_host}', false);")
    return conn

def create_documents_table(conn):
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS pgai_documents (
                        id SERIAL PRIMARY KEY,
                        title TEXT,
                        content TEXT,
                        embedding VECTOR(3072)
                    );
                """)
    return conn

def insert_documents(conn, document_data):
    with create_documents_table(conn):
        with conn.cursor() as cur:
            cur.execute(f"select count(*) from pgai_documents")
            rows = cur.fetchall()
            docCount = rows[0][0]
            if docCount == 0:
                with conn.cursor() as cur:
                    # use the port at which your ollama service is running.
                    # nomic-embed-text
                    for doc in document_data:
                        cur.execute("""
                            INSERT INTO pgai_documents (title, content, embedding)
                            VALUES (
                                %(title)s,
                                %(content)s,
                                ai.ollama_embed('llama3.2', %(content)s)
                            )
                        """, doc)

def fetch_documents_by_vector_similarity(conn, llm_query) -> str:
    context=''
    with conn:
        with conn.cursor() as cur:
            # Embed the query using the ollama_embed function
            cur.execute(f"SELECT ai.ollama_embed('llama3.2', %s);", (llm_query,))
            query_embedding = cur.fetchone()[0]

            # Retrieve relevant documents based on cosine distance
            cur.execute(f"SELECT title, content, 1 - (embedding <=> %s) AS similarity FROM pgai_documents ORDER BY similarity LIMIT 300", (query_embedding,))

            rows = cur.fetchall()
            for row in rows:
              title = row[0]
              content = row[1]
              context = context + title + ' - ' + content + '\n'                
    return context


def build_and_execute_ollama_generate(conn, context, query):
    # print(f"query: {query}\n")

    with conn.cursor() as cur:
        genStr = """DOCUMENT: {1}

QUESTION: {0}

INSTRUCTIONS:
Answer the users QUESTION using the DOCUMENT text above.
Keep your answer ground in the facts of the DOCUMENT.
If the DOCUMENT doesn’t contain the facts to answer the QUESTION then please say so.
""".format(query, context)
        print(f"\n\n\n{genStr}\n\n")

        cur.execute("SELECT ai.ollama_generate('llama3.2', %s)",
                    (genStr, ))
            
        model_response = cur.fetchone()[0]
        print(model_response['response'])

# here is some fakey data for the documents table
document_data_korea = [
    {"title": "Seoul Tower", "content": "Seoul Tower is a communication and observation tower located on Namsan Mountain in central Seoul, South Korea."},
    {"title": "Gwanghwamun Gate", "content": "Gwanghwamun is the main and largest gate of Gyeongbokgung Palace, in Jongno-gu, Seoul, South Korea."},
    {"title": "Bukchon Hanok Village", "content": "Bukchon Hanok Village is a Korean traditional village in Seoul with a long history."},
    {"title": "Myeong-dong Shopping Street", "content": "Myeong-dong is one of the primary shopping districts in Seoul, South Korea."},
    {"title": "Dongdaemun Design Plaza", "content": "The Dongdaemun Design Plaza is a major urban development landmark in Seoul, South Korea."}
]

ollama_host=os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
psql_host=os.environ.get('POSTGRESQL_HOST', 'localhost')
psql_port=os.environ.get('POSTGRESQL_PORT', '5432')
psql_user=os.environ.get('POSTGRES_USER', 'postgres')
psql_password=os.environ.get('POSTGRES_PASSWORD', 'postgres')
psql_db=os.environ.get('POSTGRES_DB', 'postgres')

query = "Tell me about landmarks in Seoul"

conn = connect_db(ollama_host, psql_host, psql_port, psql_user, psql_password, psql_db)
# Register the vector type with psycopg2
register_vector(conn)

try:
    insert_documents(conn, document_data_korea)
    context = fetch_documents_by_vector_similarity(conn, query)
    build_and_execute_ollama_generate(conn, context, query)
finally:
    conn.close()
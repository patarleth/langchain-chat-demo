from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings

from langchain_core.documents import Document

from langchain_postgres.vectorstores import PGVector
# https://github.com/langchain-ai/langchain-postgres/blob/main/examples/vectorstore.ipynb

from sqlalchemy import create_engine, text, URL;

import os, logging

# https://python.langchain.com/docs/integrations/chat/ollama/
# when running from inside docker -
# In Dockerfile ENV is set with OLLAMA_HOST=http://host.docker.internal:111434 
# my tailnet ollama http://spicynoodleM4.taild54a2.ts.net:11434
# my tailnet postgressql host snp-connections.taild54a2.ts.net

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

logger = logging.getLogger('postgresql_pgvector')
logger.setLevel(level=logging.INFO)

ollama_base_url=os.environ.get('OLLAMA_HOST', 'http://spicynoodleM4.taild54a2.ts.net:11434')
psql_host=os.environ.get('POSTGRESQL_HOST', 'snp-containers.taild54a2.ts.net')
psql_port=os.environ.get('POSTGRESQL_PORT', '5432')
psql_user=os.environ.get('POSTGRES_USER', 'postgres')
psql_password=os.environ.get('POSTGRES_PASSWORD', 'postgres')
psql_db=os.environ.get('POSTGRES_DB', 'postgres')

docs = [
    Document(page_content='there are cats in the pond', metadata={"id": 1, "location": "pond", "topic": "animals"}),
    Document(page_content='ducks are also found in the pond', metadata={"id": 2, "location": "pond", "topic": "animals"}),
    Document(page_content='fresh apples are available at the market', metadata={"id": 3, "location": "market", "topic": "food"}),
    Document(page_content='the market also sells fresh oranges', metadata={"id": 4, "location": "market", "topic": "food"}),
    Document(page_content='the new art exhibit is fascinating', metadata={"id": 5, "location": "museum", "topic": "art"}),
    Document(page_content='a sculpture exhibit is also at the museum', metadata={"id": 6, "location": "museum", "topic": "art"}),
    Document(page_content='a new coffee shop opened on Main Street', metadata={"id": 7, "location": "Main Street", "topic": "food"}),
    Document(page_content='the book club meets at the library', metadata={"id": 8, "location": "library", "topic": "reading"}),
    Document(page_content='the library hosts a weekly story time for kids', metadata={"id": 9, "location": "library", "topic": "reading"}),
    Document(page_content='a cooking class for beginners is offered at the community center', metadata={"id": 10, "location": "community center", "topic": "classes"})
]

# this is not necessary for this demo. I include it for demonstration purposes.
llm = ChatOllama(
    model="llama3.2",
    temperature=0,
    base_url=ollama_base_url,
    # other params...
)

# create url connection string directly
print(f"\n  psql_host {psql_host}\n  psql_port {psql_port}\n  psql_user {psql_user}\n  psql_password {psql_password}\n  psql_db {psql_db}\n")
connection = f"postgresql+psycopg://{psql_user}:{psql_password}@{psql_host}:{psql_port}/{psql_db}"
print(f"  postgresql connection {connection}\n")

# create url connection string using SQLAlchemy URL object
url_object = URL.create(
    "postgresql+psycopg",
    username="postgres",
    password="postgres",  # plain (unescaped) text
    host=psql_host,
    database="postgres",
)
print(f"sqlalchemy url object {url_object}\n")

collection_name = "langchaindocs"
embeddings = OllamaEmbeddings(model="llama3.2", base_url=ollama_base_url)

db_engine = create_engine(url_object)
db_engine.logger.info("Connected to PostgreSQL database")

# exec_options = db_engine.get_execution_options()
#print(f"exec options size {len(exec_options)}")
#for key,value in exec_options:
#    print(f"  key: {key}, value: {value}")

vectorstore = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=db_engine,
    use_jsonb=True,
    create_extension=True,
    logger=logger,
)

# it is not necessary to recreate the collection, I leave it commented out to show it can be done
# vectorstore.delete_collection()
# vectorstore.create_collection()

vectorstore.add_documents(docs, ids=[doc.metadata['id'] for doc in docs])

# use the embedding class to create a vector based on the search string passed
# first query is retrieve documents with their score
similar_docs_relevance = vectorstore.max_marginal_relevance_search_with_score('kitty', k=4)
print("max_marginal_relevance_search_with_score results")
for doc_w_rel in similar_docs_relevance:
    doc = doc_w_rel[0]
    rel = doc_w_rel[1]
    print(f"  ----> {rel} - {doc.id} - {doc.page_content}")

print("---")

# next ONLY returns the docs sans score
similar_docs = vectorstore.similarity_search('kitty', k=4)
print("similarity_search results")
for doc in similar_docs:
    print(f"  ----> {doc.id} - {doc.page_content}")
    # print(f"  ----> {doc}")

print("---")

# perfrom the same search using the embedding directly, just to show it can be done

# test printing first 10 embeddings from the OllamaEmbeddings model
test_embedding_text = "kitty"
kitty_vector = embeddings.embed_query(test_embedding_text)
print(kitty_vector[:10])

search_by_vector_docs = vectorstore.similarity_search_by_vector(kitty_vector, k=4)

print("direct search_by_vector_docs results")
for doc in search_by_vector_docs:
    print(f"  ----> {doc.id} - {doc.page_content}")

# sample raw query using sqlalchemy just for fun
# with db_engine.connect() as connection:
#    # result = connection.execute(text(f"select id from {collection_name}"))
#    result = connection.execute(text(f"show search_path"))
#    for row in result:
#        print(f"{row.search_path}")

print(f"done")
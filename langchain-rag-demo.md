# langchain-rag-demo

## SQLAlchemy 

The langchain-postgres library leverges SQLAlchemy core to manage all PGVector column in the public.langchain_pg_embedding table. This table is joined to the collection table to provide a separation between the embedding and the collection metadata.

Select all documents from the public.langchain_pg_embedding table in the collection angchaindocs

    select id, collection.name, document from public.langchain_pg_embedding docs join public.langchain_pg_collection collection on docs.collection_id = collection.uuid and collection.name = 'langchaindocs';

langchain PGVector docs -

    [langchain_postgres.vectorstores.PGVector](https://python.langchain.com/api_reference/postgres/vectorstores/langchain_postgres.vectorstores.PGVector.html#langchain_postgres.vectorstores.PGVector)

## tables

    langchain_pg_collection 
        uuid 
        name - collection name passed from python code
        cmetadata - null in demo project

    langchain_pg_embedding - 
        id - document id
        collection_id - fk to the collection_table above
        document - source text used for embedding
        embedding - the actual vector col for similarity search, 
        cmetadata - json metadata object passed in for each document on insert

    Yes, you have to join these tables two together to return documents for a specifc collection.
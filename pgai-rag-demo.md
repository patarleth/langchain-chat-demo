# pgai rag using pgvector and postgresql

This demo code is shamelessly lifted from timescale

    https://github.com/timescale/private-rag-example/

This demo uses psycopg2 to connect to postgresql, using pgai to generate vector 'embeddings' and pgvector to enable storing the embeddings in a column of type vector.

The code creates a table named documents. Documents stores both the text of a given document along with its 'embedding'. The embeddings are stored as vectors using pgvector extension in PostgreSQL. This column type allows for executing similarity queries.

To run this demo you will need to have installed and prepared both PostgreSQL (I recommend running the docker container below) and Ollama

## Setup

1. Install [Ollama](https://ollama.ai/) then pull the llama3.2 model as referenced in [pgai-rag-demo.py](pgai-rag-demo.py)
2. Install [pgai](https://github.com/timescale/pgai) and [pgvector](https://github.com/pgvector/pgvector) extensions in your PostgreSQL database.

Not going to lie - setting the db up is a bit of a nightmare, but it's worth it and it's required for this demo heh ;)

To ease the process, timescale/timescaledb-ha:pg17 can be used in a [docker-compose.yaml](postgres_docker-compose.yaml) which will install all necessary dependencies for you. Yes it's slower than a native db, yes the file Volumn can't reallly be sped up but hey this works.

I also set the timescale postgres database image as the core of the hasura project to add graphql and rest apis automatically for your tables. [Hasura](https://hasura.io/pricing) is great and free for individuals.

READ THE DOCKER-COMPOSE and note: the docker-compose file above references a volumn named db_data. This volume needs to be created in docker desktop.

Having the db created, WILL NOT actually enable the extensions for each db -

```
  psql -U postgres -d postgres -c "CREATE EXTENSION IF NOT EXISTS pgvector;"
  psql -U postgres -d postgres -c "CREATE EXTENSION IF NOT EXISTS pgai;"
```

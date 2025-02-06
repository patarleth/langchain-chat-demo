# embeddings abstraction in LLM RAG

In this project I offer two competing philosophies on where to put the embeddings logic in an LLM vector based RAG?

    /pgai-rag-demo.py

    Pgai, or just ‘ai’ in the postgres extension parlance, adds code to postgres db server which allows the database to connect to your llm model directly and create ‘embeddings’ on insert. This strat enables ingest applications to be unaware of the model specific embeddings for the vector column. Simply build procedures in the db to call out and create the vector col.

And 

    /langchain-rag-demo.py

    Next is the potentially much higher performant solution offered by langchain-postgres - Inserts to the given collections vector column are managed by [sqlalchemy](https://docs.sqlalchemy.org/en/20/). Sqlalchemy manages the db connection and vector column inserts as raw & the application must create the embeddings through the ‘Document’ framework.  The app must be aware of the model and how to build the embeddings for cosine similarity selects.  

Pgai makes everything very simple. You can write selects that create the bindings for search on demand and you don’t need an app to play with the vector store

The langchain-postgress framework approach is annoying to debug and setup. Feels like every ORM I’ve ever used. Completely magic by design, a noob like me has no idea whats going on under the covers.

---

## the big problem 

Your RAG app will be stuck with the abtraction and a total refactor will be required if you change your mind.

My experience with pgai is that it makes everything, so, so, so easy. BUT the perf clearly will always suck under any real load. great, great prototypes, easy to use db abstractions, both insert and query.

From the couple days I've used the langchain community over engineered offerings is that their magic solution requires you become an expert using sqlalchemy to do anything. And doing anything with the vector column sure seems like it will require an app or a cli tool.

Which would you pick?

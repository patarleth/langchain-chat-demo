# langchain visual code w/ docker

Simple tests of using a docker dev container, built and configured using docker-compose.yml

Dev container based on the MS managed image (for now)

	* mcr.microsoft.com/vscode/devcontainers/python

docker compose creates and runs a postgres db and the Dev Container for VSCode.

https://github.com/microsoft/vscode-dev-containers

Dockerfile RUNs pip and installs the various langchain and langgraph reqs along with environment variables that points to OLLAMA running on the host.

## how to instal if new to dev containers in VSCode -

* New Window
* F1 (hold fn and press f1)
* Search for "Dev Containers: Open Folder in Container..."
* Wait
* Click Rebuild if the ext prompts.  (this only needs to be done once)

If code prompts you more than once, click ignore.

## test containers

[langchain_main](langchain_main.md) 
	
	- langchain used to generate a prompt and print.

<hr />

[pgai_rag_main](pgai_rag_main.md)

	- pgai/pgvector rag using postgresql to generate a prompt and print. 

<hr />

[langchain_rag_main](langchain_rag_main.md)

	- langchain-postgres.PGVector used to generate document embeddings and print similarities.

<hr />

[date_prompt_main](date_prompt_main.md)

	- langchain-postgres.PGVector used to generate document embeddings and print similarities.

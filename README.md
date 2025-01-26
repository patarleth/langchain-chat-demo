# langchain visual code w/ docker

Simple test of using a docker dev container, built and configured using docker-compose.yml

using MS image (for now)

	* mcr.microsoft.com/vscode/devcontainers/python

docker compose creates and runs a postgres db and the Dev Container for VSCode.

https://github.com/microsoft/vscode-dev-containers

The Dockerfile uses pip to install various langchain and langgraph reqs, with an environment variable that points to OLLAMA running on the host.

## how to instal if new to dev containers in VSCode -

* New Window
* F1 (hold fn and press f1)
* Search for "Dev Containers: Open Folder in Container..."
* Wait
* Click Rebuild if the ext prompts.  (this only needs to be done once)

If code prompts you more than once, click ignore.

## test container

* open src/langchain-test.py
* click the Run button on the top right of the VSCode window.

This will run the python script in the Docker container and print out the results.  You should see something like this:

```
Ne pas emprunter les tournevis à précision de Tim. Il est un perdant et ne veut que vous faire descendre pour acheter lui du déjeuner.

Note: I translated "loser" as "perdant", which is a more literal translation, but it's worth noting that the word "loser" can have a stronger connotation in English than in French. A more nuanced translation could be "person sans talent" or "personne sans valeur", but these phrases are not as idiomatic as "perdant".
```

Enjoy!
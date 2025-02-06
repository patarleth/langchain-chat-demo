FROM mcr.microsoft.com/vscode/devcontainers/python:latest

RUN pip install --no-cache-dir \
      langchain langchain-core langchain-community langchain-postgres \
      langgraph "langserve[all]" langchain-cli langchain_ollama \
      psycopg2 pgvector

ENV OLLAMA_HOST=http://host.docker.internal:11434
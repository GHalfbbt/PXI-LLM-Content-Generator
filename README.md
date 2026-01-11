# PXI LLM Content Generator

## Overview
This project is an academic and technical initiative focused on building a modular content generation system using Large Language Models (LLMs).

The goal is to generate high-quality, platform-adapted content (blogs and social media posts) through a web interface, with an architecture designed to be extensible toward advanced features such as RAG, multi-LLM support, image generation, and multi-agent systems.

## Current Status
🚧 Project in active development.

The current phase focuses on:
- Project structure and environment setup
- Core content generation pipeline using LangChain
- Streamlit-based user interface

## Tech Stack
- **Language:** Python 3.11
- **Frontend:** Streamlit
- **LLM Framework:** LangChain
- **LLM Providers:** Groq (Mixtral), Ollama (planned)
- **Observability:** LangSmith (planned)
- **Containerization:** Docker (planned)

## Project Structure

The project follows a modular and extensible architecture designed to support future features such as RAG, multi-LLM support, image generation, and multi-agent systems.

```text
PXI-LLM-Content-Generator/
│
├── app/
│   ├── main.py                  # Streamlit entry point (UI orchestration only)
│   │
│   ├── ui/                      # Streamlit UI components
│   │   ├── sidebar.py           # User inputs (topic, platform, tone, etc.)
│   │   └── output.py            # Output rendering
│   │
│   ├── core/                    # Core business logic
│   │   ├── prompts/             # Prompt templates by content type
│   │   │   ├── blog.py
│   │   │   ├── twitter.py
│   │   │   ├── instagram.py
│   │   │   └── linkedin.py
│   │   │
│   │   ├── chains/              # LangChain chains
│   │   │   └── content_chain.py
│   │   │
│   │   ├── postprocess/         # Output formatting and cleanup
│   │   │   └── formatter.py
│   │   │
│   │   └── rag/                 # Retrieval-Augmented Generation (future)
│   │
│   ├── llms/                    # LLM providers and factory
│   │   ├── base.py              # Abstract LLM interface
│   │   ├── groq_llm.py          # Groq (Mixtral) implementation
│   │   └── ollama_llm.py        # Ollama (Llama3) implementation
│   │
│   ├── storage/                 # Persistence layer
│   │   ├── json_store.py        # JSON-based storage
│   │   └── postgres.py          # PostgreSQL integration (future)
│   │
│   ├── config/                  # Configuration and settings
│   │   └── settings.py
│   │
│   └── utils/                   # Shared utilities
│       └── validators.py
│
├── docker/                      # Docker configuration
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── docs/                        # Project documentation
│   ├── architecture.md
│   └── setup.md
│
├── tests/                       # Tests (to be implemented)
│
├── .github/
│   └── ISSUE_TEMPLATE/          # GitHub issue templates
│
├── .env.example                 # Environment variables example
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE




## Development Workflow
- GitFlow-inspired branching strategy
- Feature-based branches
- Pull Requests into `develop`
- Protected `main` branch

## License
MIT License


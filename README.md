# PXI LLM Content Generator

## Overview
This project is an academic and technical initiative focused on building a modular content generation system using Large Language Models (LLMs).

The goal is to generate high-quality, platform-adapted content (blogs and social media posts) through a web interface, with an architecture designed to be extensible toward advanced features such as RAG, multi-LLM support, image generation, and multi-agent systems.

## Current Status
✅ **Core features implemented and functional**

### Implemented Features

#### ✅ Core Functionality
- **Content Generation Pipeline**: Complete LangChain-based content generation chain for blog posts
- **Multi-LLM Support**: Factory pattern implementation supporting both Groq (cloud) and Ollama (local) providers
- **LLM Provider Factory**: Centralized LLM instantiation with validation and error handling
- **Configuration Management**: Centralized settings with environment variable validation

#### ✅ User Interface
- **Streamlit Web Application**: Fully functional UI with modern gradient-based styling
- **Internationalization (i18n)**: Multi-language UI support (English, Spanish, French, Italian)
- **Interactive Sidebar**: Comprehensive input controls for topic, audience, tone, language, and LLM provider selection
- **Content Output Display**: Formatted output with word/character count and copy functionality
- **Error Handling**: User-friendly error messages with troubleshooting suggestions
- **Empty States**: Guided onboarding experience for new users
- **Loading States**: Visual feedback during content generation

#### ✅ LLM Providers
- **Groq Integration**: Cloud-based LLM provider using Groq API (default model: llama-3.3-70b-versatile)
- **Ollama Integration**: Local LLM provider support with connection validation and error handling

#### ✅ Architecture
- **Modular Design**: Clean separation of concerns (UI, core logic, LLM providers, configuration)
- **Extensible Structure**: Ready for future features (RAG, multi-platform content, image generation)

### Planned Features
- Social media platform-specific content generation (Twitter, LinkedIn, Instagram)
- Content persistence and history (JSON storage implementation started)
- PostgreSQL integration for advanced storage
- Retrieval-Augmented Generation (RAG) capabilities
- LangSmith observability integration
- Docker containerization
- Unit and integration tests

## Tech Stack
- **Language:** Python 3.11
- **Frontend:** Streamlit with custom CSS styling
- **LLM Framework:** LangChain (LCEL - LangChain Expression Language)
- **LLM Providers:** 
  - ✅ Groq (Cloud) - llama-3.3-70b-versatile
  - ✅ Ollama (Local) - llama3.2
- **Internationalization:** Custom i18n module with 4 languages
- **Configuration:** python-dotenv for environment management
- **Observability:** LangSmith (planned)
- **Containerization:** Docker (planned)

## Project Structure

The project follows a modular and extensible architecture designed to support future features such as RAG, multi-LLM support, image generation, and multi-agent systems.

```
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
│   │   ├── factory.py           # LLM factory pattern implementation
│   │   ├── groq_llm.py          # Groq (llama-3.3-70b-versatile) implementation
│   │   └── ollama_llm.py        # Ollama (llama3.2) implementation
│   │
│   ├── storage/                 # Persistence layer
│   │   ├── json_store.py        # JSON-based storage (structure ready)
│   │   └── postgres.py          # PostgreSQL integration (future)
│   │
│   ├── config/                  # Configuration and settings
│   │   └── settings.py          # Centralized config with validation
│   │
│   └── utils/                   # Shared utilities
│       ├── i18n.py              # Internationalization module (4 languages)
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
```



## Key Features

### 🌐 Multi-Language Support
The application supports multiple languages for both the user interface and content generation:
- **UI Languages**: English, Spanish, French, Italian
- **Content Languages**: English, Spanish, French, Italian
- Users can interact with the interface in their preferred language while generating content in any supported language

### 🤖 Flexible LLM Provider Selection
Choose between cloud and local LLM providers:
- **Groq (Cloud)**: Fast, cloud-based inference using high-performance models
- **Ollama (Local)**: Privacy-focused local inference, no API costs

### 🎨 Modern User Interface
- Beautiful gradient-based design with custom CSS styling
- Intuitive sidebar with organized input sections
- Real-time content statistics (word count, character count)
- Responsive layout optimized for content reading

### ⚙️ Configuration & Validation
- Environment-based configuration using `.env` files
- Automatic validation of LLM provider availability
- Clear error messages with troubleshooting guidance
- Support for custom model names and parameters

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Groq API key (for cloud provider) OR Ollama installed locally (for local provider)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PXI-LLM-Content-Generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   # For Groq (Cloud provider)
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL_NAME=llama-3.3-70b-versatile
   
   # For Ollama (Local provider - optional)
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL_NAME=llama3.2
   ```

4. **Run the application**
   ```bash
   streamlit run app/main.py
   ```

### Usage

1. **Select UI Language**: Choose your preferred interface language from the sidebar
2. **Enter Topic**: Specify the main subject for your blog post
3. **Define Audience**: Describe your target audience
4. **Choose Tone**: Select the writing style (Professional, Casual, Friendly, Technical)
5. **Select Content Language**: Choose the language for content generation
6. **Choose LLM Provider**: Select between Groq (Cloud) or Ollama (Local)
7. **Generate**: Click the "Generate Blog Post" button
8. **Review & Copy**: Read the generated content and use the text area controls to copy

## Architecture Highlights

### Factory Pattern for LLM Providers
The application uses a factory pattern to manage LLM provider instantiation, making it easy to add new providers in the future.

### Separation of Concerns
- **UI Layer** (`app/ui/`): Streamlit components and rendering logic
- **Core Logic** (`app/core/`): Content generation chains and prompt templates
- **LLM Layer** (`app/llms/`): Provider implementations and factory
- **Configuration** (`app/config/`): Centralized settings management
- **Utilities** (`app/utils/`): Shared helpers like i18n and validators

### LangChain Integration
Uses LangChain Expression Language (LCEL) for clean, composable chains:
```python
chain = prompt | llm
result = chain.invoke({"topic": "...", "audience": "...", ...})
```

## Development Workflow
- GitFlow-inspired branching strategy
- Feature-based branches
- Pull Requests into `develop`
- Protected `main` branch

## License
MIT License


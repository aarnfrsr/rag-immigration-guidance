# Project Structure

Complete directory structure and file organization for the Immigration Guidance RAG System.

## Directory Tree

```
rag-immigration-guidance/
│
├── 📁 Core Application
│   ├── app.py                      # Streamlit web interface (main application)
│   ├── run.bat                     # Windows startup script
│   └── run.sh                      # Unix/Mac startup script
│
├── 📁 notebooks/                   # Jupyter notebooks for development
│   ├── claude_rag.ipynb           # Main implementation (Claude Sonnet 4.5)
│   ├── phase1.ipynb               # Alternative implementation (Ollama/Llama3)
│   └── chroma_db/                 # Vector database (generated, gitignored)
│
├── 📁 data/
│   └── raw/                       # Source USCIS policy PDFs (25 documents)
│       ├── Chapter 1 - Purpose and Background.pdf
│       ├── Chapter 2 - Becoming a U.S. Citizen.pdf
│       ├── ... (23 more PDFs)
│       └── re-entrypermits2026.pdf
│
├── 📁 assets/                     # Images and screenshots for documentation
│   └── README.md                  # Instructions for adding assets
│
├── 📁 scripts/                    # Utility scripts (currently empty)
│
├── 📁 .github/
│   └── copilot-instructions.md   # AI agent development guidelines
│
├── 📄 Configuration Files
│   ├── requirements.txt           # Python package dependencies
│   ├── .env.example              # Environment variable template
│   ├── .env                      # Local environment (gitignored)
│   └── .gitignore                # Git ignore rules
│
└── 📄 Documentation
    ├── README.md                  # Main project documentation
    ├── LICENSE                    # MIT License
    ├── CONTRIBUTING.md            # Contribution guidelines
    └── PROJECT_STRUCTURE.md       # This file
```

## File Descriptions

### Core Application

#### `app.py` (298 lines)
Streamlit web interface for the RAG system.

**Features:**
- Chat interface with message history
- Source citation display
- Configurable retrieval settings (sidebar)
- Error handling and loading states
- Cached RAG system initialization

**Key Functions:**
- `initialize_rag_system()`: Loads embeddings, vectorstore, and LLM
- `display_sources()`: Shows source documents with excerpts
- `main()`: Main Streamlit application logic

#### `run.bat` / `run.sh`
Automated startup scripts that:
1. Check for virtual environment
2. Activate virtual environment
3. Install missing dependencies
4. Launch Streamlit app

### Notebooks

#### `notebooks/claude_rag.ipynb`
**Primary implementation** using Claude Sonnet 4.5.

**Sections:**
1. Setup and Dependencies
2. Document Loading (PyPDF)
3. Text Chunking (RecursiveCharacterTextSplitter)
4. Embeddings & Vector DB (HuggingFace + Chroma)
5. LLM Setup (Claude via Anthropic API)
6. RAG Chain (LangChain LCEL)
7. Query Functions
8. Example Queries

**Output:** Creates `notebooks/chroma_db/` with embedded documents

#### `notebooks/phase1.ipynb`
**Alternative implementation** using Ollama/Llama3.

**Purpose:** Demonstrates local LLM option (free, privacy-focused)

**Key Difference:** Uses Llama3 instead of Claude for generation

### Data

#### `data/raw/`
Contains 25 USCIS Policy Manual PDF documents:
- Citizenship & Naturalization (Chapters 2, 3)
- Filing & Documentation (Chapters 3, 4)
- Interview Guidelines (Chapter 5)
- Adjudicative Review (Chapter 6)
- Child Status Protection Act (Chapter 7)
- Legal Analysis & Discretion (Chapter 10)
- Plus 13 other specialized policy documents

**Total:** ~203 pages of official immigration policy

### Configuration

#### `requirements.txt`
Python dependencies organized by category:

```
Core LangChain:
- langchain >= 0.1.0
- langchain-anthropic >= 0.1.0
- langchain-community >= 0.0.20

Document Processing:
- pypdf >= 3.17.0

Embeddings & Vectorstore:
- sentence-transformers >= 2.2.2
- chromadb >= 0.4.22

Utilities:
- python-dotenv >= 1.0.0

Web UI:
- streamlit >= 1.30.0

Development (optional):
- jupyter >= 1.0.0
- ipykernel >= 6.29.0
```

#### `.env.example`
Template for environment variables:
```
ANTHROPIC_API_KEY=your_api_key_here
```

#### `.gitignore`
Excludes from version control:
- Virtual environments (`.venv-1/`)
- Environment files (`.env`)
- Vector database (`chroma_db/`)
- Python cache (`__pycache__/`)
- IDE files (`.vscode/`, `.idea/`)
- Jupyter checkpoints

### Documentation

#### `README.md`
Main project documentation including:
- Project overview and features
- Setup instructions
- Usage examples
- Architecture details
- Optimization tips
- Troubleshooting

#### `LICENSE`
MIT License with acknowledgment of third-party licenses

#### `CONTRIBUTING.md`
Guidelines for contributors:
- Development setup
- Project structure
- Areas for improvement
- Code style
- Testing procedures

## Technology Stack

### Frontend
- **Streamlit** 1.30.0+ - Web interface framework

### Backend
- **LLM**: Claude Sonnet 4.5 (via Anthropic API)
- **Framework**: LangChain 0.1.0+
- **Embeddings**: HuggingFace sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB 0.4.22+
- **Document Processing**: PyPDF 3.17.0+

### Development
- **Notebooks**: Jupyter + ipykernel
- **Environment**: python-dotenv for config management

## Generated Files (Gitignored)

These files are created during runtime and excluded from git:

```
notebooks/chroma_db/              # Vector database
├── chroma.sqlite3               # SQLite database
└── <uuid>/                      # Collection data
    ├── data_level0.bin
    ├── header.bin
    ├── index_metadata.pickle
    ├── length.bin
    └── link_lists.bin
```

## Workflow

1. **Initial Setup**
   ```bash
   python -m venv .venv-1
   source .venv-1/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with ANTHROPIC_API_KEY
   ```

2. **Generate Vector Database**
   - Open `notebooks/claude_rag.ipynb`
   - Run all cells to create `notebooks/chroma_db/`

3. **Run Web Interface**
   ```bash
   streamlit run app.py
   # Or: run.bat (Windows) / ./run.sh (Unix)
   ```

## Future Organization

Potential additions for scaling:

```
rag-immigration-guidance/
├── src/                         # Python package
│   ├── __init__.py
│   ├── embeddings.py           # Embedding logic
│   ├── retrieval.py            # Retrieval functions
│   ├── generation.py           # LLM generation
│   └── utils.py                # Helper functions
├── tests/                       # Unit tests
│   ├── test_retrieval.py
│   └── test_generation.py
├── docs/                        # Additional documentation
│   ├── ARCHITECTURE.md
│   └── API.md
└── docker/                      # Containerization
    ├── Dockerfile
    └── docker-compose.yml
```

## Key Principles

1. **Separation of Concerns**: Notebooks for development, app.py for production
2. **Environment Isolation**: All secrets in .env, never committed
3. **Reproducibility**: requirements.txt pins versions, vectorstore persisted
4. **Documentation**: Every file has a clear purpose and documentation
5. **Git Hygiene**: .gitignore excludes generated files, environments, and secrets

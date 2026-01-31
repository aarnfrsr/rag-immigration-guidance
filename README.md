# Immigration Guidance RAG System

> A production-ready Retrieval-Augmented Generation (RAG) system for USCIS immigration policy guidance, featuring both local (Ollama) and cloud (Claude) implementations with a user-friendly Streamlit web interface.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://python.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone <your-repo-url>
cd rag-immigration-guidance
python -m venv .venv-1
source .venv-1/bin/activate  # Windows: .venv-1\Scripts\activate

# 2. Install and configure
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 3. Generate vectorstore (run notebook first)
# Open notebooks/claude_rag.ipynb and run all cells

# 4. Launch web interface
streamlit run app.py
# Or use: run.bat (Windows) / ./run.sh (Unix)
```

## 📸 Screenshots

<!-- Add screenshots here after generating them -->
> **Note**: See [assets/README.md](assets/README.md) for instructions on adding screenshots.

## Overview

This system allows you to ask questions about U.S. immigration policies and receive accurate, citation-backed answers from official USCIS documentation.

### ✨ Key Features

- 🎯 **Dual LLM Support**: Compare local (Ollama/Llama3) vs cloud (Claude Sonnet 4.5) implementations
- 🌐 **Web Interface**: Beautiful Streamlit frontend with chat history and source visualization
- 📚 **Source Attribution**: All answers include references to specific USCIS documents and page numbers
- ⚡ **Production-Ready**: Persisted vectorstore, error handling, and optimized retrieval
- 💰 **Cost-Effective**: Free local embeddings with optional API-based generation
- 📖 **Comprehensive Coverage**: 25 USCIS policy documents (~203 pages)

### 🛠️ Skills Demonstrated

This project showcases proficiency in:

- **LLM Integration**: Working with both local (Ollama) and API-based (Claude/Anthropic) models
- **RAG Architecture**: Complete pipeline from document loading → chunking → embedding → retrieval → generation
- **Vector Databases**: Chroma with persistence and efficient similarity search
- **Web Development**: Streamlit for interactive ML/AI applications
- **Python Best Practices**: Virtual environments, dependency management, documentation
- **Real-world Application**: Domain-specific (legal/immigration) question-answering system

## Architecture

- **LLM**: Claude Sonnet 4.5 (Anthropic API)
- **Embeddings**: HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
- **Vectorstore**: Chroma (persisted locally)
- **Framework**: LangChain

## Setup Instructions

### 1. Prerequisites

- Python 3.13+ (or 3.11+)
- Anthropic API key ([Get one here](https://console.anthropic.com/settings/keys))

### 2. Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using uv (faster)
uv pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
ANTHROPIC_API_KEY=your_actual_api_key_here
```

Alternatively, set the environment variable directly:

```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY="your_api_key_here"

# Windows CMD
set ANTHROPIC_API_KEY=your_api_key_here

# Linux/Mac
export ANTHROPIC_API_KEY="your_api_key_here"
```

### 4. Run the Notebook

Open and run [notebooks/claude_rag.ipynb](notebooks/claude_rag.ipynb):

```bash
jupyter notebook notebooks/claude_rag.ipynb
```

Or use VS Code with the Jupyter extension.

## Usage

### Basic Query

```python
# Ask a question
result = ask_question("What are the key requirements for U.S. citizenship?")
```

### Custom Retrieval

```python
# More control over number of retrieved chunks
custom_result = ask_with_custom_retrieval(
    "How does the Child Status Protection Act work?",
    num_chunks=6
)
```

## Document Coverage

The system includes the following USCIS Policy Manual chapters:

1. Chapter 1 - General Policies
2. Chapter 2 - Eligibility Requirements
3. Chapter 3 - Filing Instructions
4. Chapter 4 - Documentation
5. Chapter 5 - Interview Guidelines
6. Chapter 6 - Adjudicative Review
7. Chapter 7 - Child Status Protection Act
8. Chapter 10 - Legal Analysis and Use of Discretion

## Project Structure

```
rag-immigration-guidance/
├── data/
│   └── raw/                    # Source PDF documents
├── notebooks/
│   ├── phase1.ipynb           # Original Ollama implementation
│   └── claude_rag.ipynb       # New Claude implementation
├── chroma_db/                 # Persisted vectorstore (created on first run)
├── .env                       # API keys (create from .env.example)
├── .env.example              # Template for environment variables
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Optimization Tips

### Improve Retrieval Quality

- **Adjust chunk parameters**: Modify `chunk_size` and `chunk_overlap` in the text splitter
- **Change number of chunks**: Increase/decrease `k` in retriever configuration
- **Try different search types**: Use `mmr` (maximal marginal relevance) instead of `similarity`

### Improve Answer Quality

- **Refine prompts**: Customize the prompt template for more specific guidance
- **Adjust temperature**: Lower (0) for factual answers, higher (0.5-1.0) for creative responses
- **Upgrade model**: Use Claude Opus 4.5 for complex legal reasoning

### Cost Optimization

- **Use Claude Haiku 4**: Faster and cheaper for simpler queries
- **Reduce max_tokens**: Set lower limits if answers are too verbose
- **Cache vectorstore**: Reuse the persisted Chroma database to avoid re-embedding

## Cost Estimates

### Claude API Costs (as of January 2026)

- **Sonnet 4.5**: ~$3 per million input tokens, ~$15 per million output tokens
- **Typical query**: ~2,000-4,000 input tokens, ~500-1,000 output tokens
- **Estimated cost per query**: $0.01-0.02

### Embedding Costs

- **HuggingFace Sentence Transformers**: FREE (runs locally)

## Troubleshooting

### "ANTHROPIC_API_KEY not found"

Make sure you've either:
1. Created a `.env` file with your API key, or
2. Set the environment variable in your shell

### "Module not found" errors

Install all dependencies:
```bash
pip install -r requirements.txt
```

### Vectorstore creation is slow

This is normal on first run. The vectorstore is persisted to `./chroma_db` and will load instantly in future sessions.

### Out of memory errors

Reduce the number of documents or chunk size:
```python
chunk_size = 500  # Instead of 1000
search_kwargs={"k": 2}  # Instead of 4
```

## Migration from Ollama

The original implementation used Ollama with Llama2. Key differences:

| Feature | Old (Ollama) | New (Claude) |
|---------|-------------|--------------|
| LLM | Llama2 (local) | Claude Sonnet 4.5 (API) |
| Cost | Free | ~$0.01-0.02 per query |
| Quality | Good | Excellent |
| Speed | Fast (local) | Fast (API, ~2-3s) |
| Setup | Requires Ollama server | Just API key |

## 📁 Project Structure

```
rag-immigration-guidance/
├── app.py                      # Streamlit web interface
├── run.bat / run.sh           # Startup scripts
├── notebooks/
│   ├── claude_rag.ipynb       # Main implementation (Claude)
│   └── phase1.ipynb           # Alternative implementation (Ollama)
├── data/raw/                  # USCIS policy PDFs (25 documents)
├── assets/                    # Screenshots and images
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
└── docs/
    ├── README.md             # This file
    ├── PROJECT_STRUCTURE.md  # Detailed structure documentation
    ├── CONTRIBUTING.md       # Contribution guidelines
    └── LICENSE               # MIT License
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed documentation.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup instructions
- Code style guidelines
- Areas for improvement
- Testing procedures

**Quick contribution ideas:**
- ✅ Add more USCIS documents
- ✅ Implement semantic caching for common queries
- ✅ Add conversation memory for follow-up questions
- ✅ Create unit tests for RAG components
- ✅ Add evaluation metrics

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

USCIS documents are in the public domain as works of the U.S. Government.

## Resources

- [Claude API Documentation](https://docs.anthropic.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [USCIS Policy Manual](https://www.uscis.gov/policy-manual)

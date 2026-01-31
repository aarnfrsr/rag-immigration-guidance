# Contributing to Immigration Guidance RAG System

Thank you for your interest in contributing! This is primarily a portfolio/educational project, but suggestions and improvements are welcome.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd rag-immigration-guidance
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv-1
   source .venv-1/bin/activate  # On Windows: .venv-1\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

5. **Generate the vector database**
   - Open and run `notebooks/claude_rag.ipynb`
   - This creates the `chroma_db/` folder with embedded documents

6. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   # Or use: run.bat (Windows) / ./run.sh (Unix/Mac)
   ```

## Project Structure

```
rag-immigration-guidance/
├── app.py                  # Streamlit web application
├── notebooks/              # Jupyter notebooks
│   ├── claude_rag.ipynb   # Main RAG implementation (Claude)
│   └── phase1.ipynb       # Alternative implementation (Ollama)
├── data/raw/               # Source PDF documents
├── assets/                 # Screenshots and images
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variable template
└── README.md              # Project documentation
```

## Areas for Improvement

### High Priority
- [ ] Add unit tests for RAG pipeline components
- [ ] Implement caching for frequently asked questions
- [ ] Add conversation history/memory for follow-up questions
- [ ] Improve error handling and user feedback

### Medium Priority
- [ ] Add support for document upload (user-provided PDFs)
- [ ] Implement query rewriting for better retrieval
- [ ] Add evaluation metrics (retrieval precision, answer quality)
- [ ] Create Docker containerization

### Low Priority
- [ ] Add support for multiple languages
- [ ] Implement user authentication for deployed version
- [ ] Add analytics/usage tracking
- [ ] Create API endpoints (REST/GraphQL)

## Code Style

- Follow PEP 8 for Python code
- Use type hints where applicable
- Add docstrings for functions and classes
- Keep functions focused and under 50 lines when possible

## Testing

Currently, testing is manual. To test:
1. Run the Streamlit app
2. Try example questions
3. Verify source citations are correct
4. Check for errors in different scenarios

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Questions or Ideas?

Feel free to open an issue to discuss potential changes or improvements!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

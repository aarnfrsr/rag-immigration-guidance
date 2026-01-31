# Copilot / AI Agent Instructions — RAG Immigration Guidance

Purpose: Help AI coding agents become immediately productive in this repository.

- **Project layout (quick):**
  - `data/raw/` — source documents used for embeddings and retrieval.
  - `notebooks/` — exploratory RAG notebooks; primary integration code lives here (example: [notebooks/phase1.ipynb](notebooks/phase1.ipynb#L35-L47)).
  - `scripts/` — utility scripts (small tooling and ETL helpers).

- **Big picture / architecture:**
  - This repo implements a prototype RAG (retrieval-augmented generation) workflow in notebooks: embed documents, store in a vectorstore, then build a RetrievalQA chain that uses a locally-hosted LLM via Ollama.
  - Embeddings are created using `HuggingFaceEmbeddings` (see `notebooks/phase1.ipynb` where `sentence-transformers/all-MiniLM-L6-v2` is referenced).
  - LLM integration uses `langchain_community.llms.Ollama` (the notebook constructs `Ollama(model="llama3")`) — the agent should assume a running Ollama server and the `llama3` model present when testing LLM calls.
  - Vectorstore usage is referenced as an abstract `vectorstore` object (not fixed to a specific implementation in the notebook). Look for where `vectorstore` is constructed in `scripts/` or other notebooks; typical implementations are Chroma/FAISS — treat `vectorstore.as_retriever()` as the expected API.

- **Developer workflows & commands (Windows-focused):**
  - Notebooks show package checks like `!pip list | findstr langchain` — use PowerShell or CMD on Windows for the same commands.
  - To run notebooks interactively, open `notebooks/phase1.ipynb` in Jupyter/VS Code. Ensure required packages (`langchain`, `langchain_community`, `sentence-transformers`, `faiss`/`chromadb` if used) are installed in the active kernel.
  - Ollama: before running LLM calls, ensure Ollama is installed and running locally; confirm the `llama3` model is available. If Ollama is remote or uses different env vars, document them in repo README (none found — ask maintainers).

- **Project-specific conventions & patterns:**
  - Prototype-first: most core logic lives in notebooks rather than a packaged app. Expect exploratory code and inline dependency checks.
  - Minimal abstraction: the notebooks construct the RAG chain inline (see `build_rag_chain(vectorstore)` in [notebooks/phase1.ipynb](notebooks/phase1.ipynb#L35-L47)). When converting to scripts, preserve `retriever = vectorstore.as_retriever(search_kwargs={"k": 4})` semantics.
  - Return of source documents is enabled on RetrievalQA chains (`return_source_documents=True`) — downstream code expects explicit source docs for provenance.

- **Integration points & external dependencies to watch for:**
  - Ollama local LLM server and the `llama3` model.
  - HuggingFace sentence-transformers model `all-MiniLM-L6-v2` used for embeddings.
  - An unspecified `vectorstore` implementation — search repo for `.as_retriever(` to find vectorstore creation code before editing.

- **What a Copilot-like agent should do first when editing code here:**
  1. Open `[notebooks/phase1.ipynb](notebooks/phase1.ipynb#L1)` and locate the `build_rag_chain` cell to understand how embeddings, retriever, and LLM are wired together.
  2. Search the repo for `vectorstore` and `.as_retriever(` to find the concrete vectorstore implementation before changing retrieval semantics.
  3. Do not change the `search_kwargs={"k": 4}` default without checking downstream expectations for the number of source docs returned.
  4. When adding code that calls Ollama, include a short runtime check (e.g., safe try/except with a clear error message about Ollama being unreachable).

- **Examples to reference in edits:**
  - `notebooks/phase1.ipynb` — `get_embeddings()` using `HuggingFaceEmbeddings` and `build_rag_chain(vectorstore)` constructing `RetrievalQA`.

- **When to leave TODOs or open questions in PRs:**
  - If the vectorstore implementation is not found, leave a TODO asking maintainers which vectorstore (Chroma vs FAISS) they intend to use.
  - If Ollama configuration (host/port/model name) is unclear, add a short README note and a TODO in code pointing to maintainers for the canonical setup.

If any section is unclear or you want more detail about `vectorstore` usage or Ollama setup, tell me which area to expand and I will iterate.

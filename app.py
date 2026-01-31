"""
Immigration Guidance RAG System - Streamlit Frontend
Uses Claude Sonnet 4.5 with LangChain for answering USCIS policy questions.
"""

import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Page configuration
st.set_page_config(
    page_title="Immigration Guidance Assistant",
    page_icon="🗽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 0.5rem;
        border-radius: 0.3rem;
        margin-top: 0.5rem;
        font-size: 0.85rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load environment variables
load_dotenv()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_initialized" not in st.session_state:
    st.session_state.rag_initialized = False


@st.cache_resource
def initialize_rag_system(num_chunks: int = 4):
    """
    Initialize the RAG system components.
    Cached to avoid reloading on every interaction.
    """
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        st.error("⚠️ ANTHROPIC_API_KEY not found in environment variables!")
        st.info("Please set your API key in a .env file or environment variables.")
        st.stop()

    # Initialize embeddings
    with st.spinner("Loading embeddings model..."):
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

    # Load vectorstore
    with st.spinner("Loading vectorstore..."):
        # Check both possible locations
        chroma_db_path = Path("chroma_db")
        notebooks_chroma_path = Path("notebooks/chroma_db")

        if chroma_db_path.exists():
            db_path = "./chroma_db"
        elif notebooks_chroma_path.exists():
            db_path = "./notebooks/chroma_db"
        else:
            st.error("⚠️ Vectorstore not found!")
            st.info("Please run the claude_rag.ipynb notebook first to create the vectorstore.")
            st.stop()

        vectorstore = Chroma(
            persist_directory=db_path,
            embedding_function=embeddings
        )

    # Initialize Claude
    llm = ChatAnthropic(
        model="claude-sonnet-4-5-20250929",
        temperature=0,
        max_tokens=4096
    )

    # Create prompt template
    prompt_template = """You are an expert immigration law assistant with deep knowledge of USCIS policies and procedures.
Use the following context from official USCIS documentation to answer the question accurately and comprehensively.

IMPORTANT:
- Cite specific sources by referencing the document chapter and page numbers
- If the context doesn't contain enough information to fully answer the question, acknowledge this
- Provide clear, actionable guidance when applicable
- Use precise legal terminology from the source documents

Context:
{context}

Question: {question}

Answer:"""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    # Create retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": num_chunks}
    )

    # Helper function to format documents
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Create RAG chain
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | PROMPT
        | llm
        | StrOutputParser()
    )

    return rag_chain, retriever, vectorstore


def display_sources(sources):
    """Display source documents in a formatted box."""
    if sources:
        with st.expander("📚 View Sources", expanded=False):
            for i, doc in enumerate(sources, 1):
                source_file = Path(doc.metadata.get("source", "Unknown")).name
                page_num = doc.metadata.get("page", "Unknown")

                st.markdown(f"""
                **Source {i}:** {source_file} - Page {page_num}

                *Excerpt:* {doc.page_content[:200]}...

                ---
                """)


def main():
    # Header
    st.title("🗽 Immigration Guidance Assistant")
    st.markdown("Ask questions about USCIS policies and procedures based on official documentation.")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        # Number of chunks to retrieve
        num_chunks = st.slider(
            "Number of document chunks to retrieve",
            min_value=2,
            max_value=8,
            value=4,
            help="More chunks provide more context but may include less relevant information"
        )

        st.markdown("---")

        # About section
        st.subheader("About")
        st.markdown("""
        This assistant uses:
        - **LLM**: Claude Sonnet 4.5
        - **Embeddings**: HuggingFace MiniLM
        - **Vectorstore**: Chroma
        - **Framework**: LangChain

        **Data Source**: 25 USCIS policy manuals covering citizenship, naturalization, documentation, and more.
        """)

        st.markdown("---")

        # Clear conversation button
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        # Statistics
        if st.session_state.rag_initialized:
            st.markdown("---")
            st.subheader("📊 Stats")
            st.metric("Messages", len(st.session_state.messages))

    # Initialize RAG system
    try:
        rag_chain, retriever, vectorstore = initialize_rag_system(num_chunks)
        st.session_state.rag_initialized = True

        # Display success message only once
        if len(st.session_state.messages) == 0:
            st.success(f"✓ System initialized with {vectorstore._collection.count()} document chunks")

    except Exception as e:
        st.error(f"Error initializing RAG system: {str(e)}")
        st.stop()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Display sources for assistant messages
            if message["role"] == "assistant" and "sources" in message:
                display_sources(message["sources"])

    # Chat input
    if prompt := st.chat_input("Ask a question about immigration policies..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Searching documents and generating answer..."):
                try:
                    # Get relevant documents
                    source_docs = retriever.invoke(prompt)

                    # Get answer from RAG chain
                    response = rag_chain.invoke(prompt)

                    # Display answer
                    st.markdown(response)

                    # Display sources
                    display_sources(source_docs)

                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "sources": source_docs
                    })

                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

    # Example questions (shown when chat is empty)
    if len(st.session_state.messages) == 0:
        st.markdown("### 💡 Example Questions")

        col1, col2 = st.columns(2)

        example_questions = [
            "What are the requirements for U.S. citizenship?",
            "What documentation is needed for a naturalization application?",
            "How does the Child Status Protection Act work?",
            "What happens during an immigration interview?"
        ]

        for i, question in enumerate(example_questions):
            col = col1 if i % 2 == 0 else col2
            with col:
                if st.button(question, key=f"example_{i}", use_container_width=True):
                    # Simulate user asking the question
                    st.session_state.messages.append({"role": "user", "content": question})
                    st.rerun()


if __name__ == "__main__":
    main()

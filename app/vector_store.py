
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from app.ingestion import ingest_directory

INDEX_DIR = Path("data/faiss_index")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_vector_store(
    documents: list[Document],
    index_dir: str | Path = INDEX_DIR,
) -> FAISS:
    if not documents:
        raise ValueError("Cannot build a vector store from empty documents.")

    embeddings = get_embeddings()
    store = FAISS.from_documents(documents, embeddings)

    path = Path(index_dir)
    path.mkdir(parents=True, exist_ok=True)
    store.save_local(str(path))

    return store


def load_vector_store(
    index_dir: str | Path = INDEX_DIR,
) -> FAISS:
    path = Path(index_dir)

    if not (path / "index.faiss").is_file():
        raise FileNotFoundError(
            f"No FAISS index found at {path}. Build the index first."
        )

    return FAISS.load_local(
        str(path),
        embeddings=get_embeddings(),
        allow_dangerous_deserialization=True,
    )


def search_documents(
    question: str,
    store: FAISS,
    k: int = 4,
) -> list[tuple[Document, float]]:
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if k < 1:
        raise ValueError("k must be at least 1.")

    return store.similarity_search_with_relevance_scores(
        question.strip(),
        k=k,
    )


def index_knowledge_base(
    knowledge_dir: str | Path = "knowledge_base",
    index_dir: str | Path = INDEX_DIR,
) -> FAISS:
    chunks = ingest_directory(knowledge_dir)

    store = build_vector_store(chunks, index_dir)

    print(f"Indexed {len(chunks)} document chunks.")
    print(f"FAISS index saved to: {Path(index_dir).resolve()}")

    return store

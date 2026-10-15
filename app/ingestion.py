
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def load_document(file_path: str | Path) -> list[Document]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    if not path.is_file():
        raise ValueError(f"Expected a file, got: {path}")

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension}")

    if extension == ".pdf":
        loader = PyPDFLoader(str(path))
    else:
        loader = TextLoader(
            str(path),
            encoding="utf-8",
            autodetect_encoding=True,
        )

    documents = loader.load()

    for document in documents:
        document.metadata.update({
            "source": path.name,
            "file_path": str(path.resolve()),
            "file_type": extension.lstrip("."),
        })

    return [
        document for document in documents
        if document.page_content.strip()
    ]


def load_directory(directory: str | Path) -> list[Document]:
    root = Path(directory)

    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {root}")

    if not root.is_dir():
        raise ValueError(f"Expected a directory, got: {root}")

    documents = []

    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            documents.extend(load_document(path))

    return documents


def split_documents(
    documents: list[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> list[Document]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be >= 0 and less than chunk_size"
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    return splitter.split_documents(documents)


def ingest_file(
    file_path: str | Path,
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> list[Document]:
    documents = load_document(file_path)
    return split_documents(documents, chunk_size, chunk_overlap)


def ingest_directory(
    directory: str | Path = "knowledge_base",
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[Document]:
    documents = load_directory(directory)

    if not documents:
        raise ValueError(f"No supported documents found in {directory}")

    return split_documents(documents, chunk_size, chunk_overlap)

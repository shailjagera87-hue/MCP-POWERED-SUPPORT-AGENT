
from app.vector_store import index_knowledge_base, search_documents


def main():
    store = index_knowledge_base()

    question = "How long does shipping take?"
    results = search_documents(question, store, k=3)

    print(f"\nQuestion: {question}\n")

    for i, (document, score) in enumerate(results, start=1):
        print(f"--- Result {i} (score: {score:.4f}) ---")
        print(f"Source: {document.metadata.get('source')}")
        print(document.page_content)
        print()


if __name__ == "__main__":
    main()

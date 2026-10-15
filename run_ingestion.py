
from pathlib import Path
import traceback

from app.ingestion import ingest_directory


def main():
    project_root = Path(__file__).resolve().parent
    knowledge_dir = project_root / "knowledge_base"

    print(f"Project root: {project_root}")
    print(f"Knowledge directory: {knowledge_dir}")
    print(f"Directory exists: {knowledge_dir.is_dir()}")

    if knowledge_dir.is_dir():
        print("Files found:")
        for path in sorted(knowledge_dir.rglob("*")):
            if path.is_file():
                print(f"  - {path.name}")

    try:
        chunks = ingest_directory(knowledge_dir)

        print(f"\nCreated {len(chunks)} chunks.\n")

        for i, chunk in enumerate(chunks[:5], start=1):
            print(f"--- Chunk {i} ---")
            print(f"Source: {chunk.metadata.get('source')}")
            print(f"Metadata: {chunk.metadata}")
            print(chunk.page_content)
            print()

    except Exception:
        print("\nIngestion failed. Full error:")
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()

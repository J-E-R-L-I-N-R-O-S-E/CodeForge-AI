from __future__ import annotations

from typing import Any

import chromadb


class MemoryService:
    """
    ChromaDB-based persistent memory for CodeForge AI.

    Stores project information in a persistent local ChromaDB
    collection and provides simple store/retrieve operations.
    """

    COLLECTION_NAME = "codeforge_project_memory"

    def __init__(
        self,
        db_path: str = "memory/chroma_db",
    ) -> None:

        self.client = chromadb.PersistentClient(
            path=db_path
        )

        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME
        )

    # =========================================================
    # Store memory
    # =========================================================

    def store(
        self,
        memory_id: str,
        text: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Store or replace one memory item.
        """

        if not memory_id.strip():
            raise ValueError(
                "memory_id cannot be empty."
            )

        if not text.strip():
            raise ValueError(
                "Memory text cannot be empty."
            )

        safe_metadata = metadata or {}

        self.collection.upsert(
            ids=[memory_id],
            documents=[text],
            metadatas=[safe_metadata],
        )

    # =========================================================
    # Retrieve memory
    # =========================================================

    def search(
        self,
        query: str,
        n_results: int = 5,
        project_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search relevant memories using ChromaDB.

        When project_id is provided, only memories belonging
        to that project are retrieved.
        """

        if not query.strip():
            raise ValueError(
                "Search query cannot be empty."
            )

        if n_results <= 0:
            raise ValueError(
                "n_results must be greater than zero."
            )

        query_kwargs = {
            "query_texts": [query],
            "n_results": n_results,
        }

        if project_id:
            query_kwargs["where"] = {
                "project_id": project_id
            }

        result = self.collection.query(
            **query_kwargs
        )

        memories: list[dict[str, Any]] = []

        ids = result.get("ids", [[]])[0]
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]

        for index, memory_id in enumerate(ids):

            memories.append(
                {
                    "id": memory_id,
                    "text": documents[index],
                    "metadata": metadatas[index],
                    "distance": (
                        distances[index]
                        if index < len(distances)
                        else None
                    ),
                }
            )

        return memories
        """
        Search relevant memories using ChromaDB.
        """

        if not query.strip():
            raise ValueError(
                "Search query cannot be empty."
            )

        if n_results <= 0:
            raise ValueError(
                "n_results must be greater than zero."
            )

        result = self.collection.query(
            query_texts=[query],
            n_results=n_results,
        )

        memories: list[dict[str, Any]] = []

        ids = result.get("ids", [[]])[0]
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]

        for index, memory_id in enumerate(ids):

            memories.append(
                {
                    "id": memory_id,
                    "text": documents[index],
                    "metadata": metadatas[index],
                    "distance": (
                        distances[index]
                        if index < len(distances)
                        else None
                    ),
                }
            )

        return memories

    # =========================================================
    # Get all memories
    # =========================================================

    def get_all(self) -> list[dict[str, Any]]:
        """
        Return all stored memories.
        """

        result = self.collection.get(
            include=[
                "documents",
                "metadatas",
            ]
        )

        memories: list[dict[str, Any]] = []

        ids = result.get("ids", [])
        documents = result.get("documents", [])
        metadatas = result.get("metadatas", [])

        for index, memory_id in enumerate(ids):

            memories.append(
                {
                    "id": memory_id,
                    "text": documents[index],
                    "metadata": (
                        metadatas[index]
                        if index < len(metadatas)
                        else {}
                    ),
                }
            )

        return memories

    # =========================================================
    # Delete one memory
    # =========================================================

    def delete(
        self,
        memory_id: str,
    ) -> None:
        """Delete a memory item."""

        self.collection.delete(
            ids=[memory_id]
        )
        # =========================================================
    # CodeForge-specific memory helpers
    # =========================================================

    def store_project_idea(
        self,
        project_id: str,
        project_idea: str,
    ) -> None:
        """Store the original project idea."""

        self.store(
            memory_id=f"{project_id}_idea",
            text=project_idea,
            metadata={
                "type": "project_idea",
                "project_id": project_id,
            },
        )

    def store_clarification(
        self,
        project_id: str,
        round_number: int,
        answer: str,
    ) -> None:
        """Store a user's clarification answer."""

        self.store(
            memory_id=(
                f"{project_id}_clarification_{round_number}"
            ),
            text=answer,
            metadata={
                "type": "clarification_answer",
                "project_id": project_id,
                "round_number": round_number,
            },
        )

    def store_requirements(
        self,
        project_id: str,
        requirements: list[str],
    ) -> None:
        """Store confirmed requirements."""

        text = "\n".join(
            f"- {item}"
            for item in requirements
        )

        self.store(
            memory_id=f"{project_id}_requirements",
            text=text,
            metadata={
                "type": "final_requirements",
                "project_id": project_id,
            },
        )

    def store_srs(
        self,
        project_id: str,
        srs: str,
    ) -> None:
        """Store the generated SRS."""

        self.store(
            memory_id=f"{project_id}_srs",
            text=srs,
            metadata={
                "type": "final_srs",
                "project_id": project_id,
            },
        )

    def get_project_memory(
        self,
        project_id: str,
    ) -> list[dict[str, Any]]:
        """Retrieve all memory belonging to one project."""

        memories = self.get_all()

        return [
            memory
            for memory in memories
            if memory.get("metadata", {}).get(
                "project_id"
            ) == project_id
        ]

if __name__ == "__main__":

    memory = MemoryService()

    memory.store(
        memory_id="demo_project",
        text=(
            "Hospital Management System for managing "
            "patients, doctors, appointments, and "
            "medical records."
        ),
        metadata={
            "type": "project_idea",
        },
    )

    results = memory.search(
        "Hospital Management System"
    )

    print("\n" + "=" * 60)
    print("CHROMADB MEMORY TEST")
    print("=" * 60)

    for item in results:
        print("\nID:", item["id"])
        print("Text:", item["text"])
        print("Metadata:", item["metadata"])
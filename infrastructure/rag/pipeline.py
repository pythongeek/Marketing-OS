"""
AgenticMarketingPro — RAG Pipeline (Chroma + LlamaIndex)
=========================================================
Handles:
- Markdown parsing & chunking from the vault
- Embedding generation (OpenAI / local alternatives)
- ChromaDB vector storage + retrieval
- Query routing with metadata filters

Usage:
    from rag.pipeline import VaultRAG
    rag = VaultRAG()
    rag.ingest_vault()          # One-time full ingestion
    results = rag.query("How do we handle brand voice?", top_k=5)
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any, Iterator
from datetime import datetime
from dataclasses import dataclass

from config import Config

logger = logging.getLogger("amp.rag")


@dataclass
class Chunk:
    """A document chunk with metadata."""
    text: str
    source_path: str
    source_type: str  # e.g., "persona", "brief", "profit_plan"
    title: str
    section: str
    chunk_index: int
    total_chunks: int
    word_count: int
    tags: List[str]
    last_modified: float


class VaultRAG:
    """
    RAG pipeline for the AgenticMarketingPro vault.
    Uses ChromaDB for local vector storage + LlamaIndex for indexing.
    """

    def __init__(
        self,
        collection_name: str = None,
        persist_dir: Path = None,
        embedding_model: str = None,
    ):
        self.collection_name = collection_name or Config.CHROMA_COLLECTION_NAME
        self.persist_dir = persist_dir or Config.CHROMA_PERSIST_DIR
        self.embedding_model = embedding_model or Config.EMBEDDING_MODEL
        self.vault_root = Config.VAULT_ROOT

        self._chroma_client = None
        self._collection = None
        self._index = None
        self._embedding_model = None

        self._init_chroma()
        self._init_embeddings()

    # ── Initialization ──────────────────────────────────────────────────

    def _init_chroma(self):
        """Initialize ChromaDB persistent client."""
        try:
            import chromadb
            from chromadb.config import Settings

            self.persist_dir.mkdir(parents=True, exist_ok=True)
            self._chroma_client = chromadb.PersistentClient(
                path=str(self.persist_dir),
                settings=Settings(anonymized_telemetry=False),
            )
            self._collection = self._chroma_client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
            )
            logger.info(f"ChromaDB initialized: {self.persist_dir}/{self.collection_name}")
        except ImportError:
            logger.error("chromadb not installed. Run: pip install chromadb")
            raise
        except Exception as e:
            logger.error(f"ChromaDB init failed: {e}")
            raise

    def _init_embeddings(self):
        """Initialize embedding model."""
        try:
            from llama_index.embeddings.openai import OpenAIEmbedding

            if Config.OPENAI_API_KEY:
                self._embedding_model = OpenAIEmbedding(
                    model=self.embedding_model,
                    api_key=Config.OPENAI_API_KEY,
                )
                logger.info(f"OpenAI embeddings initialized: {self.embedding_model}")
            else:
                logger.warning("No OPENAI_API_KEY. Embeddings will fail.")
                # TODO: Add fallback to local embeddings (e.g., sentence-transformers)
        except ImportError:
            logger.error("llama-index-embeddings-openai not installed.")
            raise

    # ── Chunking ──────────────────────────────────────────────────────

    def _parse_markdown(self, file_path: Path) -> Iterator[Chunk]:
        """
        Parse a markdown file into semantic chunks.
        Strategy: Split by H2 headers, then by paragraph if too long.
        """
        try:
            text = file_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.warning(f"Failed to read {file_path}: {e}")
            return

        # Extract frontmatter
        frontmatter = {}
        content = text
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                try:
                    import yaml
                    frontmatter = yaml.safe_load(parts[1])
                except ImportError:
                    pass
                content = parts[2].strip()

        title = frontmatter.get("title", file_path.stem.replace("-", " ").title())
        tags = frontmatter.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]

        # Determine source type from path
        source_type = self._infer_source_type(file_path)

        # Split by H2 headers
        import re
        h2_pattern = re.compile(r'^##\s+(.+)$', re.MULTILINE)
        sections = h2_pattern.split(content)

        if len(sections) == 1:
            # No H2 headers — treat whole file as one section
            sections = ["content", sections[0]]

        chunks = []
        chunk_idx = 0

        for i in range(1, len(sections), 2):
            section_name = sections[i].strip() if i < len(sections) else "content"
            section_text = sections[i + 1] if i + 1 < len(sections) else ""

            # Further split long sections by paragraph
            paragraphs = [p.strip() for p in section_text.split("\n\n") if p.strip()]
            current_chunk = ""
            current_words = 0
            max_words = 500  # Target chunk size

            for para in paragraphs:
                para_words = len(para.split())
                if current_words + para_words > max_words and current_chunk:
                    # Emit current chunk
                    chunk = Chunk(
                        text=f"# {title}\n## {section_name}\n\n{current_chunk}",
                        source_path=str(file_path.relative_to(self.vault_root)),
                        source_type=source_type,
                        title=title,
                        section=section_name,
                        chunk_index=chunk_idx,
                        total_chunks=-1,  # Updated later
                        word_count=current_words,
                        tags=tags,
                        last_modified=file_path.stat().st_mtime,
                    )
                    chunks.append(chunk)
                    chunk_idx += 1
                    current_chunk = para
                    current_words = para_words
                else:
                    current_chunk += "\n\n" + para if current_chunk else para
                    current_words += para_words

            # Emit remaining chunk for this section
            if current_chunk:
                chunk = Chunk(
                    text=f"# {title}\n## {section_name}\n\n{current_chunk}",
                    source_path=str(file_path.relative_to(self.vault_root)),
                    source_type=source_type,
                    title=title,
                    section=section_name,
                    chunk_index=chunk_idx,
                    total_chunks=-1,
                    word_count=current_words,
                    tags=tags,
                    last_modified=file_path.stat().st_mtime,
                )
                chunks.append(chunk)
                chunk_idx += 1

        # Update total_chunks
        for chunk in chunks:
            chunk.total_chunks = len(chunks)
            yield chunk

    def _infer_source_type(self, file_path: Path) -> str:
        """Infer the source type from the file path."""
        path_str = str(file_path).lower()
        if "persona" in path_str or "writer" in path_str:
            return "persona"
        elif "brief" in path_str or "content" in path_str:
            return "content_brief"
        elif "profit" in path_str or "forecast" in path_str:
            return "profit_plan"
        elif "competitor" in path_str or "intel" in path_str:
            return "competitor_intel"
        elif "keyword" in path_str:
            return "keyword_universe"
        elif "report" in path_str or "analytics" in path_str:
            return "report"
        elif "audit" in path_str or "health" in path_str:
            return "audit"
        elif "playbook" in path_str or "sop" in path_str:
            return "playbook"
        elif "ops" in path_str or "log" in path_str:
            return "ops"
        else:
            return "general"

    # ── Ingestion ───────────────────────────────────────────────────

    def ingest_vault(self, force: bool = False) -> Dict[str, int]:
        """
        Ingest all markdown files from the vault into ChromaDB.
        Returns stats: {files_processed, chunks_created, errors}
        """
        stats = {"files_processed": 0, "chunks_created": 0, "errors": 0}

        # Collect all .md files
        md_files = list(self.vault_root.rglob("*.md"))
        logger.info(f"Found {len(md_files)} markdown files in vault")

        # Check which files are already indexed (if not force)
        if not force and self._collection.count() > 0:
            existing_ids = set(self._collection.get()["ids"])
            logger.info(f"Collection has {len(existing_ids)} existing chunks")
        else:
            existing_ids = set()
            if force:
                self._collection.delete(where={})
                logger.info("Cleared existing collection for force re-ingest")

        for file_path in md_files:
            try:
                # Generate a deterministic ID prefix from file path
                file_id = str(file_path.relative_to(self.vault_root)).replace("\\", "/")

                for chunk in self._parse_markdown(file_path):
                    chunk_id = f"{file_id}#{chunk.chunk_index}"

                    if chunk_id in existing_ids and not force:
                        continue

                    # Generate embedding
                    embedding = self._get_embedding(chunk.text)
                    if embedding is None:
                        stats["errors"] += 1
                        continue

                    # Store in ChromaDB
                    self._collection.add(
                        ids=[chunk_id],
                        embeddings=[embedding],
                        documents=[chunk.text],
                        metadatas=[{
                            "source_path": chunk.source_path,
                            "source_type": chunk.source_type,
                            "title": chunk.title,
                            "section": chunk.section,
                            "chunk_index": chunk.chunk_index,
                            "total_chunks": chunk.total_chunks,
                            "word_count": chunk.word_count,
                            "tags": json.dumps(chunk.tags),
                            "last_modified": chunk.last_modified,
                        }],
                    )
                    stats["chunks_created"] += 1

                stats["files_processed"] += 1

            except Exception as e:
                logger.error(f"Failed to ingest {file_path}: {e}")
                stats["errors"] += 1

        logger.info(f"Ingestion complete: {stats}")
        return stats

    def _get_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for a text chunk."""
        if not self._embedding_model:
            logger.error("Embedding model not initialized")
            return None
        try:
            return self._embedding_model.get_text_embedding(text)
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            return None

    # ── Query ─────────────────────────────────────────────────────────

    def query(
        self,
        query_text: str,
        top_k: int = 5,
        source_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_word_count: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Query the vault with semantic search + optional filters.
        
        Args:
            query_text: Natural language query
            top_k: Number of results to return
            source_type: Filter by source type (e.g., "persona", "content_brief")
            tags: Filter by tags (all must match)
            min_word_count: Minimum chunk size
        """
        if not self._embedding_model:
            logger.error("Embedding model not initialized")
            return []

        # Generate query embedding
        query_embedding = self._get_embedding(query_text)
        if query_embedding is None:
            return []

        # Build where clause
        where = {}
        if source_type:
            where["source_type"] = source_type

        # Execute query
        try:
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k * 2,  # Over-fetch for filtering
                where=where if where else None,
                include=["documents", "metadatas", "distances"],
            )
        except Exception as e:
            logger.error(f"ChromaDB query failed: {e}")
            return []

        # Process and filter results
        output = []
        if results and results["ids"]:
            for i, doc_id in enumerate(results["ids"][0]):
                metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                
                # Tag filter (post-filter since Chroma doesn't support array contains well)
                if tags and metadata:
                    chunk_tags = json.loads(metadata.get("tags", "[]"))
                    if not all(t in chunk_tags for t in tags):
                        continue

                # Word count filter
                if metadata and metadata.get("word_count", 0) < min_word_count:
                    continue

                output.append({
                    "id": doc_id,
                    "text": results["documents"][0][i] if results["documents"] else "",
                    "metadata": metadata,
                    "distance": results["distances"][0][i] if results["distances"] else 0.0,
                    "relevance_score": round(1 - results["distances"][0][i], 4) if results["distances"] else 0.0,
                })

                if len(output) >= top_k:
                    break

        return output

    def query_by_source(self, source_type: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Retrieve all chunks of a specific source type."""
        try:
            results = self._collection.get(
                where={"source_type": source_type},
                include=["documents", "metadatas"],
                limit=top_k,
            )
            return [
                {
                    "id": results["ids"][i],
                    "text": results["documents"][i],
                    "metadata": results["metadatas"][i],
                }
                for i in range(len(results["ids"]))
            ]
        except Exception as e:
            logger.error(f"Query by source failed: {e}")
            return []

    # ── Stats & Maintenance ─────────────────────────────────────────

    def stats(self) -> Dict[str, Any]:
        """Get collection statistics."""
        count = self._collection.count()
        
        # Get source type distribution
        try:
            all_meta = self._collection.get(include=["metadatas"])
            source_types = {}
            for meta in all_meta.get("metadatas", []):
                st = meta.get("source_type", "unknown")
                source_types[st] = source_types.get(st, 0) + 1
        except Exception:
            source_types = {}

        return {
            "collection_name": self.collection_name,
            "total_chunks": count,
            "persist_dir": str(self.persist_dir),
            "embedding_model": self.embedding_model,
            "source_type_distribution": source_types,
        }

    def delete_by_source(self, source_type: str) -> int:
        """Delete all chunks of a specific source type."""
        try:
            self._collection.delete(where={"source_type": source_type})
            return self._collection.count()
        except Exception as e:
            logger.error(f"Delete failed: {e}")
            return -1


if __name__ == "__main__":
    # Test initialization
    try:
        rag = VaultRAG()
        print("RAG Pipeline initialized successfully")
        print("Stats:", rag.stats())
    except Exception as e:
        print(f"Initialization failed: {e}")
        print("Make sure requirements are installed: pip install -r requirements.txt")

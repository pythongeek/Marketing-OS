"""
AgenticMarketingPro RAG Pipeline
=================================

ChromaDB + LlamaIndex-based retrieval for the vault.

Usage:
    from rag.pipeline import VaultRAG
    rag = VaultRAG()
    rag.ingest_vault()
    results = rag.query("How do we handle brand voice?", top_k=5)
"""

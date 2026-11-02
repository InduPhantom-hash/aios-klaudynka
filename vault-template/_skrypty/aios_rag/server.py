"""Read-only MCP interface: indexing remains an explicit CLI operation."""
import asyncio

from .engine import Config, Rag


def serve(config: Config):
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("rag-vault")

    @mcp.tool()
    async def rag_search(query: str, namespace: str | None = None, type: str | None = None, k: int = 5) -> dict:
        """Wyszukaj lokalne fragmenty z cytatami. Odczytaj plik źródłowy przed przyjęciem ustalenia."""
        return await asyncio.to_thread(lambda: Rag(Config.load(config.vault)).query(query, namespace, type, k))

    @mcp.tool()
    async def rag_namespaces() -> dict:
        """Lista obszarów indeksu, bez modelu i bez połączenia sieciowego."""
        return await asyncio.to_thread(lambda: Rag(Config.load(config.vault)).namespaces())

    mcp.run()

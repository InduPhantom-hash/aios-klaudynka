"""Read-only MCP interface: indexing remains an explicit CLI operation."""
from .engine import Config, Rag


def serve(config: Config):
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("rag-vault")

    @mcp.tool()
    def rag_search(query: str, namespace: str | None = None, type: str | None = None, k: int = 5) -> dict:
        """Wyszukaj lokalne fragmenty z cytatami. Odczytaj plik źródłowy przed przyjęciem ustalenia."""
        return Rag(Config.load(config.vault)).query(query, namespace, type, k)

    @mcp.tool()
    def rag_namespaces() -> dict:
        """Lista obszarów indeksu, bez modelu i bez połączenia sieciowego."""
        return Rag(Config.load(config.vault)).namespaces()

    mcp.run()

"""ハイスクールPython - コード解析ツール MCP サーバー.

FastAPI バックエンドを呼び出す MCP ツールを提供.
"""

from typing import Any

from fastmcp import FastMCP

from .client import get_client

# MCPサーバーインスタンスの作成
mcp = FastMCP("ハイスクール Python - コード解析ツール")


@mcp.tool()
async def analyze_python_code(code: str) -> dict[str, Any]:
    """Python コードを静的解析する.

    Args:
        code: 解析する Python コード

    Returns:
        解析結果 (構造、警告、エラーなど)
    """
    client = await get_client()

    return await client.analyze_code(code)


@mcp.tool()
async def visualize_code_structure(
    code: str,
    highlight_line: int = 0,
    show_flow: bool = True,  # noqa: FBT001, FBT002
) -> dict[str, Any]:
    """コードの構造を可視化する.

    Args:
        code: 可視化する Python コード
        highlight_line: ハイライトする行番号
        show_flow: フロー図を表示するか

    Returns:
        可視化結果 (ステップ、フロー図、説明)
    """
    client = await get_client()

    return await client.visualize_code(code, highlight_line, show_flow)


@mcp.tool()
async def analyze_error(code: str, error_message: str) -> dict[str, Any]:
    """エラーを教育的に分析・説明する.

    Args:
        code: エラーが発生したコード
        error_message: エラーメッセージ

    Returns:
        エラー解析結果 (説明、修正提案、学習リソース)
    """
    client = await get_client()

    return await client.analyze_error(code, error_message)


if __name__ == "__main__":
    # MCP サーバーを起動
    mcp.run()

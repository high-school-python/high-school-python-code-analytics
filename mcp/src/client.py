"""MCP クライアント.

FastAPI バックエンドを呼び出すクライアント実装.
"""

import os

import httpx

# FastAPI サーバーの URL (環境変数で設定可能)
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class HighSchoolPythonClient:
    """ハイスクールPython - コード解析ツール API クライアント."""

    def __init__(self, base_url: str = API_BASE_URL) -> None:
        """初期化."""
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    async def close(self) -> None:
        """クライアントを閉じる."""
        await self.client.aclose()

    async def health_check(self) -> dict:
        """ヘルスチェック."""
        res = await self.client.get("/")
        res.raise_for_status()
        return res.json()

    async def analyze_code(self, code: str, options: dict | None = None) -> dict:
        """コードを解析.

        Args:
            code: Python コード
            options: 解析オプション

        Returns:
            解析結果
        """
        res = await self.client.post(
            "/api/v1/analyze",
            json={"code": code, "options": options},
        )
        res.raise_for_status()

        return res.json()

    async def visualize_code(
        self,
        code: str,
        highlight_line: int = 0,
        show_flow: bool = True,  # noqa: FBT001, FBT002
    ) -> dict:
        """コードを可視化.

        Args:
            code: Python コード
            highlight_line: ハイライトする行
            show_flow: フロー図を表示するか

        Returns:
            可視化結果
        """
        res = await self.client.post(
            "/api/v1/visualize",
            json={
                "code": code,
                "highlight_line": highlight_line,
                "show_flow": show_flow,
            },
        )
        res.raise_for_status()

        return res.json()

    async def analyze_error(self, code: str, error_message: str) -> dict:
        """エラーを解析.

        Args:
            code: エラーが発生したコード
            error_message: エラーメッセージ

        Returns:
            解析結果
        """
        res = await self.client.post(
            "/api/v1/analyze-error",
            json={
                "code": code,
                "error_message": error_message,
            },
        )
        res.raise_for_status()

        return res.json()


# グローバルクライアントインスタンス
_client: HighSchoolPythonClient | None = None


async def get_client() -> HighSchoolPythonClient:
    """クライアントインスタンスを取得."""
    global _client  # noqa: PLW0603

    if _client is None:
        _client = HighSchoolPythonClient()

    return _client

"""ハイスクールPython - コード解析ツール API - メインアプリケーション.

共通バックエンドとして動作
"""

import logging
import traceback

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# ログレベルをDEBUGに設定
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# ルーターのインポート
from .routers import analysis, error_analysis, visualization

# FastAPIアプリケーションの初期化
app = FastAPI(
    title="ハイスクールPython - コード解析ツール API",
    description="高校生向け Python 学習を支援する共通バックエンド API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS設定（将来のWebフロントエンド対応）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(analysis.router, prefix="/api/v1", tags=["analysis"])
app.include_router(visualization.router, prefix="/api/v1", tags=["visualization"])
app.include_router(error_analysis.router, prefix="/api/v1", tags=["error"])


# ヘルスチェックモデル
class HealthResponse(BaseModel):
    """ヘルスチェックレスポンスモデル."""

    status: str
    version: str
    message: str


# ルートエンドポイント
@app.get("/")
async def root() -> HealthResponse:
    """API のヘルスチェックエンドポイント."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        message="ハイスクールPython - コード解析ツール API は正常に動作しています",
    )


# グローバル例外ハンドラー
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """全ての例外をキャッチしてトレースバックをログ出力."""
    logger.error("Unhandled exception occurred: %s", exc)
    logger.error("Request URL: %s", request.url)
    logger.error("Request method: %s", request.method)
    logger.error("Traceback: %s", traceback.format_exc())

    return JSONResponse(
        status_code=500,
        content={
            "error": "内部サーバーエラーが発生しました",
            "detail": str(exc),
            "status": 500,
        },
    )


# エラーハンドラー
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: object) -> JSONResponse:
    """404エラーハンドラー.

    Args:
        request: FastAPIリクエストオブジェクト
        exc: 例外オブジェクト

    Returns:
        エラーレスポンス
    """
    logger.warning("404 Not Found: %s", request.url)
    return JSONResponse(
        status_code=404,
        content={"error": "エンドポイントが見つかりません", "status": 404},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")  # noqa: S104

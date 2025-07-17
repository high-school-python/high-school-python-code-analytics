"""コード解析エンドポイント."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..services.analyzer import analyze_code

router = APIRouter()


class AnalyzeRequest(BaseModel):
    """コード解析リクエストモデル."""

    code: str
    options: dict | None = None


class AnalyzeResponse(BaseModel):
    """コード解析レスポンスモデル."""

    success: bool
    error: str | None = None
    message: str | None = None
    line: int | None = None
    offset: int | None = None
    text: str | None = None
    structure: dict | None = None
    style_issues: list[dict] | None = None
    improvements: list[dict] | None = None
    stats: dict | None = None
    summary: dict | None = None


@router.post("/analyze")
async def analyze_python_code(request: AnalyzeRequest) -> AnalyzeResponse:
    """Pythonコードを静的解析.

    - ASTによる構文解析
    - コード構造の抽出
    - 警告の生成
    """
    try:
        result = await analyze_code(request.code)
        return AnalyzeResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

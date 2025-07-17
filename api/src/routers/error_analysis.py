"""エラー解析エンドポイント."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..services.error_analyzer import analyze_error

router = APIRouter()


class ErrorAnalyzeRequest(BaseModel):
    """エラー解析リクエストモデル."""

    code: str
    error_message: str


class SimilarExample(BaseModel):
    """類似例モデル."""

    wrong: str
    correct: str
    explanation: str


class ErrorAnalyzeResponse(BaseModel):
    """エラー解析レスポンスモデル."""

    success: bool
    error_type: str
    line_number: int
    column_number: int
    simple_explanation: str
    detailed_explanation: str
    common_causes: list[str]
    fix_suggestions: list[str]
    similar_examples: list[SimilarExample]
    learning_resources: list[str]


@router.post("/analyze-error")
async def analyze_python_error(request: ErrorAnalyzeRequest) -> ErrorAnalyzeResponse:
    """Pythonエラーを教育的に解析.

    - エラーの分類と説明
    - 修正提案
    - 学習リソースの提供
    """
    try:
        result = await analyze_error(request.code, request.error_message)
        return ErrorAnalyzeResponse(success=True, **result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

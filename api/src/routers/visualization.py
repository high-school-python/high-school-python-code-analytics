"""可視化エンドポイント."""

from fastapi import APIRouter
from pydantic import BaseModel

from ..services.visualizer import visualize_code

router = APIRouter()


class VisualizeRequest(BaseModel):
    """可視化リクエストモデル."""

    code: str
    highlight_line: int = 0
    show_flow: bool = True


class SimulatedStep(BaseModel):
    """シミュレーションステップモデル."""

    line_number: int
    code: str
    action: str
    description: str
    scope: str


class VisualizeResponse(BaseModel):
    """可視化レスポンスモデル."""

    success: bool
    steps: list[SimulatedStep]
    structure: dict
    flow_diagram: str
    explanation: str
    error: str | None = None


@router.post("/visualize")
async def visualize_python_code(request: VisualizeRequest) -> VisualizeResponse:
    """Python コードの構造を可視化.

    - 静的解析によるフロー図生成
    - コード構造の説明
    - SVG形式のダイアグラム
    """
    try:
        result = visualize_code(
            request.code,
            highlight_line=request.highlight_line,
            show_flow=request.show_flow,
        )
        
        # 結果を期待される形式に変換
        if result.get("success", False):
            # ステップを期待される形式に変換
            steps = []
            for step in result.get("steps", []):
                steps.append(SimulatedStep(
                    line_number=step["line"],
                    code=step["description"],
                    action=step["operation"],
                    description=step.get("description", ""),
                    scope="global"  # シンプルにglobalとする
                ))
            
            # 構造情報を構築
            structure = {
                "variables": result.get("final_variables", {}),
                "flow_edges": result.get("flow_edges", [])
            }
            
            # 説明を生成
            explanation_parts = []
            for exp in result.get("explanations", []):
                explanation_parts.append(f"行{exp['line']}: {exp['explanation']}")
            
            return VisualizeResponse(
                success=True,
                steps=steps,
                structure=structure,
                flow_diagram=result.get("flowchart", ""),
                explanation="\n".join(explanation_parts) if explanation_parts else "コードの説明",
                error=None
            )
        else:
            return VisualizeResponse(
                success=False,
                steps=[],
                structure={},
                flow_diagram="",
                explanation="",
                error=result.get("message", "可視化エラー")
            )
    except Exception as e:
        return VisualizeResponse(
            success=False,
            steps=[],
            structure={},
            flow_diagram="",
            explanation="",
            error=str(e),
        )

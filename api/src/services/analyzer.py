"""コード解析サービス.

静的解析による Python コードの構造解析
"""

import ast
import logging
import traceback
from typing import Any

logger = logging.getLogger(__name__)


class CodeStructureAnalyzer(ast.NodeVisitor):
    """コード構造を解析するASTビジター.

    Attributes:
        structure: コード構造
        current_scope: 現在のスコープ
    """

    def __init__(self) -> None:
        """コンストラクタ."""
        self.structure: dict[str, Any] = {
            "imports": [],
            "functions": [],
            "classes": [],
            "variables": [],
            "loops": [],
            "conditionals": [],
            "complexity": 0,
        }
        self.current_scope = []

    def visit_Import(self, node: ast.Import) -> None:
        """Import 文を処理."""
        for alias in node.names:
            self.structure["imports"].append(
                {
                    "type": "import",
                    "name": alias.name,
                    "alias": alias.asname,
                    "line": node.lineno,
                },
            )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """From import 文を処理."""
        module = node.module or ""
        for alias in node.names:
            self.structure["imports"].append(
                {
                    "type": "from_import",
                    "module": module,
                    "name": alias.name,
                    "alias": alias.asname,
                    "line": node.lineno,
                },
            )
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """関数定義を処理."""
        func_info = {
            "name": node.name,
            "line": node.lineno,
            "args": [arg.arg for arg in node.args.args],
            "decorators": [self._get_decorator_name(d) for d in node.decorator_list],
            "docstring": ast.get_docstring(node),
            "complexity": self._calculate_complexity(node),
        }
        self.structure["functions"].append(func_info)
        self.structure["complexity"] += func_info["complexity"]

        self.current_scope.append(node.name)
        self.generic_visit(node)
        self.current_scope.pop()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """クラス定義を処理."""
        class_info = {
            "name": node.name,
            "line": node.lineno,
            "bases": [self._get_name(base) for base in node.bases],
            "decorators": [self._get_decorator_name(d) for d in node.decorator_list],
            "docstring": ast.get_docstring(node),
            "methods": [],
        }

        # メソッドを抽出
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                class_info["methods"].append(
                    {
                        "name": item.name,
                        "line": item.lineno,
                        "is_static": any(self._is_staticmethod(d) for d in item.decorator_list),
                        "is_class": any(self._is_classmethod(d) for d in item.decorator_list),
                    },
                )

        self.structure["classes"].append(class_info)

        self.current_scope.append(node.name)
        self.generic_visit(node)
        self.current_scope.pop()

    def visit_Assign(self, node: ast.Assign) -> None:
        """代入文を処理."""
        for target in node.targets:
            if isinstance(target, ast.Name) and not self.current_scope:
                self.structure["variables"].append(
                    {
                        "name": target.id,
                        "line": node.lineno,
                        "type": self._infer_type(node.value),
                    },
                )
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        """For ループを処理."""
        try:
            logger.debug("Processing For loop at line %d", node.lineno)
            logger.debug("For loop target: %s", node.target)
            logger.debug("For loop iter: %s", node.iter)

            target_name = self._get_name(node.target)
            iter_name = self._get_name(node.iter)

            loop_info = {
                "type": "for",
                "line": node.lineno,
                "target": target_name,
                "iter": iter_name,
                "has_else": node.orelse != [],
            }
            self.structure["loops"].append(loop_info)
            self.structure["complexity"] += 1
            self.generic_visit(node)
        except Exception as e:
            logger.error("Error in visit_For: %s", str(e))
            logger.error("Node details - target: %s, iter: %s", node.target, node.iter)
            raise

    def visit_While(self, node: ast.While) -> None:
        """While ループを処理."""
        self.structure["loops"].append(
            {
                "type": "while",
                "line": node.lineno,
                "has_else": node.orelse != [],
            },
        )
        self.structure["complexity"] += 1
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        """If 文を処理."""
        self.structure["conditionals"].append(
            {
                "type": "if",
                "line": node.lineno,
                "has_else": node.orelse != [],
                "elif_count": self._count_elifs(node),
            },
        )
        self.structure["complexity"] += 1 + self._count_elifs(node)
        self.generic_visit(node)

    def _get_name(self, node: ast.AST) -> str:
        """ノードから名前を取得."""
        if node is None:
            return "unknown"
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            value_name = self._get_name(node.value)
            return f"{value_name}.{node.attr}"
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                return f"{node.func.id}()"
            if isinstance(node.func, ast.Attribute):
                return f"{self._get_name(node.func)}()"
        if isinstance(node, ast.Constant):
            return repr(node.value)
        if isinstance(node, ast.List):
            return "list"
        if isinstance(node, ast.Dict):
            return "dict"
        if isinstance(node, ast.Tuple):
            return "tuple"
        return "unknown"

    def _get_decorator_name(self, decorator: ast.AST) -> str:
        """デコレータ名を取得."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        if isinstance(decorator, ast.Attribute):
            return f"{self._get_name(decorator.value)}.{decorator.attr}"
        return "unknown"

    def _is_staticmethod(self, decorator: ast.AST) -> bool:
        """スタティックメソッドか判定."""
        return isinstance(decorator, ast.Name) and decorator.id == "staticmethod"

    def _is_classmethod(self, decorator: ast.AST) -> bool:
        """クラスメソッドか判定."""
        return isinstance(decorator, ast.Name) and decorator.id == "classmethod"

    def _infer_type(self, node: ast.AST) -> str:  # noqa: PLR0911
        """値から型を推論."""
        if isinstance(node, ast.Constant):
            return type(node.value).__name__
        if isinstance(node, ast.List):
            return "list"
        if isinstance(node, ast.Dict):
            return "dict"
        if isinstance(node, ast.Set):
            return "set"
        if isinstance(node, ast.Tuple):
            return "tuple"
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            return node.func.id
        return "unknown"

    def _calculate_complexity(self, node: ast.AST) -> int:
        """サイクロマティック複雑度を計算."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    def _count_elifs(self, node: ast.If) -> int:
        """elifの数をカウント."""
        count = 0
        while node.orelse:
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                count += 1
                node = node.orelse[0]
            else:
                break
        return count


def check_style_issues(code: str) -> list[dict[str, Any]]:
    """スタイルの問題をチェック."""
    issues = []
    lines = code.split("\n")

    for i, line in enumerate(lines, 1):
        # 行の長さチェック
        if len(line) > 79:
            issues.append(
                {
                    "line": i,
                    "type": "line_too_long",
                    "message": f"行が長すぎます ({len(line)} 文字)。PEP 8では79文字以内が推奨されます。",
                    "severity": "warning",
                },
            )

        # タブの使用チェック
        if "\t" in line:
            issues.append(
                {
                    "line": i,
                    "type": "tab_usage",
                    "message": "タブ文字が使用されています。PEP 8ではスペース4つが推奨されます。",
                    "severity": "warning",
                },
            )

        # 末尾の空白チェック
        if line.rstrip() != line:
            issues.append(
                {
                    "line": i,
                    "type": "trailing_whitespace",
                    "message": "行末に不要な空白があります。",
                    "severity": "info",
                },
            )

    return issues


def suggest_improvements(structure: dict[str, Any]) -> list[dict[str, str]]:
    """コード改善の提案."""
    suggestions = []

    # 複雑度のチェック
    if structure["complexity"] > 10:
        suggestions.append(
            {
                "type": "high_complexity",
                "message": "コードの複雑度が高いです。関数を分割することを検討してください。",
            },
        )

    # 関数の長さチェック
    for func in structure["functions"]:
        if func["complexity"] > 5:
            suggestions.append(
                {
                    "type": "complex_function",
                    "message": f"関数 '{func['name']}' が複雑です。より小さな関数に分割することを検討してください。",
                },
            )

        if not func["docstring"]:
            suggestions.append(
                {
                    "type": "missing_docstring",
                    "message": f"関数 '{func['name']}' にdocstringがありません。関数の目的を説明するdocstringを追加してください。",
                },
            )

    # クラスのチェック
    for cls in structure["classes"]:
        if not cls["docstring"]:
            suggestions.append(
                {
                    "type": "missing_docstring",
                    "message": f"クラス '{cls['name']}' にdocstringがありません。クラスの目的を説明するdocstringを追加してください。",
                },
            )

    # 変数名のチェック
    for var in structure["variables"]:
        if len(var["name"]) == 1 and var["name"] not in ["i", "j", "k", "n", "x", "y", "z"]:
            suggestions.append(
                {
                    "type": "short_variable_name",
                    "message": f"変数名 '{var['name']}' が短すぎます。より説明的な名前を使用してください。",
                },
            )

    return suggestions


async def analyze_code(code: str) -> dict:
    """コードを解析.

    Args:
        code: Pythonコード

    Returns:
        解析結果
    """
    logger.info("Starting code analysis")
    logger.debug("Code to analyze: %s", code)

    try:
        # ASTの解析
        logger.debug("Parsing AST...")
        tree = ast.parse(code)
        logger.debug("AST parsed successfully")

        # 構造解析
        logger.debug("Analyzing code structure...")
        analyzer = CodeStructureAnalyzer()
        analyzer.visit(tree)
        structure = analyzer.structure
        logger.debug("Structure analysis complete: %s", structure)

        # スタイルチェック
        logger.debug("Checking style issues...")
        style_issues = check_style_issues(code)
        logger.debug("Style issues found: %d", len(style_issues))

        # 改善提案
        logger.debug("Generating improvement suggestions...")
        improvements = suggest_improvements(structure)
        logger.debug("Improvement suggestions: %d", len(improvements))

        # 統計情報
        logger.debug("Calculating statistics...")
        stats = {
            "total_lines": len(code.split("\n")),
            "code_lines": len([line for line in code.split("\n") if line.strip() and not line.strip().startswith("#")]),
            "import_count": len(structure["imports"]),
            "function_count": len(structure["functions"]),
            "class_count": len(structure["classes"]),
            "complexity_score": structure["complexity"],
        }

        return {
            "success": True,
            "structure": structure,
            "style_issues": style_issues,
            "improvements": improvements,
            "stats": stats,
            "summary": {
                "total_issues": len(style_issues),
                "total_suggestions": len(improvements),
                "quality_score": max(0, 100 - len(style_issues) * 5 - len(improvements) * 10),
            },
        }

    except SyntaxError as e:
        logger.error("Syntax error in code: %s", str(e))
        logger.debug("Syntax error details - Line: %s, Offset: %s, Text: %s", e.lineno, e.offset, e.text)
        return {
            "success": False,
            "error": "syntax_error",
            "message": str(e),
            "line": e.lineno,
            "offset": e.offset,
            "text": e.text,
        }
    except Exception as e:
        logger.error("Unexpected error during analysis: %s", str(e))
        logger.error("Error type: %s", type(e).__name__)
        logger.error("Traceback:\n%s", traceback.format_exc())
        return {
            "success": False,
            "error": "analysis_error",
            "message": str(e),
        }

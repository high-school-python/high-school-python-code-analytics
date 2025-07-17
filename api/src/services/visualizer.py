"""可視化サービス
静的解析によるコード構造の可視化
"""

import ast


class ExecutionFlowSimulator(ast.NodeVisitor):
    """静的解析による実行フローのシミュレーション"""

    def __init__(self) -> None:
        self.steps = []
        self.variables = {}
        self.flow_edges = []
        self.current_step = 0
        self.branch_stack = []

    def add_step(self, line: int, operation: str, description: str, variables: dict | None = None) -> None:
        """実行ステップを追加."""
        step = {
            "step": self.current_step,
            "line": line,
            "operation": operation,
            "description": description,
            "variables": variables or self.variables.copy(),
        }
        self.steps.append(step)

        # フローエッジを追加
        if self.current_step > 0:
            self.flow_edges.append({
                "from": self.current_step - 1,
                "to": self.current_step,
                "type": "sequential",
            })

        self.current_step += 1

    def visit_Module(self, node: ast.Module) -> None:
        """Moduleノードを訪問."""
        for stmt in node.body:
            self.visit(stmt)

    def visit_Assign(self, node: ast.Assign) -> None:
        """代入文を処理."""
        for target in node.targets:
            if isinstance(target, ast.Name):
                # 変数の値をシミュレート
                var_name = target.id
                value_desc = self._get_value_description(node.value)

                self.variables[var_name] = value_desc
                self.add_step(
                    node.lineno,
                    "assign",
                    f"{var_name} = {value_desc}",
                )

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        """複合代入文を処理."""
        if isinstance(node.target, ast.Name):
            var_name = node.target.id
            op = self._get_operator_symbol(node.op)
            value_desc = self._get_value_description(node.value)

            current_value = self.variables.get(var_name, "?")
            self.variables[var_name] = f"{current_value} {op} {value_desc}"

            self.add_step(
                node.lineno,
                "augassign",
                f"{var_name} {op}= {value_desc}",
            )

    def visit_If(self, node: ast.If) -> None:
        """if文を処理."""
        condition_desc = self._get_value_description(node.test)
        
        # 条件を評価してみる
        condition_result = self._evaluate_condition(node.test)
        
        self.add_step(
            node.lineno,
            "condition",
            f"if {condition_desc}: → {condition_result}",
        )

        if condition_result == "True":
            # Trueブランチを実行
            self.add_step(
                node.lineno,
                "branch_taken",
                "条件が真のため、ifブロックを実行",
            )
            for stmt in node.body:
                self.visit(stmt)
                
            # elseブランチはスキップ
            if node.orelse:
                self.add_step(
                    node.lineno,
                    "branch_skipped",
                    "elseブロックはスキップ",
                )
        elif condition_result == "False":
            # Trueブランチをスキップ
            self.add_step(
                node.lineno,
                "branch_skipped",
                "条件が偽のため、ifブロックをスキップ",
            )
            
            # Falseブランチを実行
            if node.orelse:
                self.add_step(
                    node.lineno,
                    "branch_taken",
                    "elseブロックを実行",
                )
                for stmt in node.orelse:
                    self.visit(stmt)
        else:
            # 評価できない場合は両方のブランチを表示
            self.add_step(
                node.lineno,
                "branch_unknown",
                "条件の評価結果が不明（実行時に決定）",
            )
            
            # Trueブランチ
            branch_start = self.current_step
            for stmt in node.body:
                self.visit(stmt)

            # Falseブランチ
            if node.orelse:
                else_start = self.current_step
                self.flow_edges.append({
                    "from": branch_start - 1,
                    "to": else_start,
                    "type": "branch",
                    "label": "False",
                })
                for stmt in node.orelse:
                    self.visit(stmt)

    def visit_For(self, node: ast.For) -> None:
        """forループを処理."""
        target = self._get_name(node.target)
        iter_desc = self._get_value_description(node.iter)
        
        # イテレータの値を取得して実際の反復を表現
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name):
            if node.iter.func.id == "range":
                # range関数の引数を解析
                if len(node.iter.args) == 1:
                    # range(n)
                    end = self._get_value_description(node.iter.args[0])
                    try:
                        end_val = int(end)
                        iter_values = list(range(end_val))[:3]  # 最初の3つを表示
                        iter_desc = f"range({end}) → {iter_values}{'...' if end_val > 3 else ''}"
                    except:
                        pass
                elif len(node.iter.args) >= 2:
                    # range(start, end)
                    start = self._get_value_description(node.iter.args[0])
                    end = self._get_value_description(node.iter.args[1])
                    try:
                        start_val = int(start)
                        end_val = int(end)
                        iter_values = list(range(start_val, end_val))[:3]
                        iter_desc = f"range({start}, {end}) → {iter_values}{'...' if end_val - start_val > 3 else ''}"
                    except:
                        pass

        self.add_step(
            node.lineno,
            "loop_start",
            f"for {target} in {iter_desc}:",
        )

        loop_start = self.current_step

        # ループの最初の数回を展開して表示
        max_iterations = 3
        current_iteration = 0
        
        # 実際のイテレーション値を取得
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == "range":
            try:
                if len(node.iter.args) == 1:
                    iter_values = list(range(int(self._get_value_description(node.iter.args[0]))))
                elif len(node.iter.args) >= 2:
                    iter_values = list(range(
                        int(self._get_value_description(node.iter.args[0])),
                        int(self._get_value_description(node.iter.args[1]))
                    ))
                else:
                    iter_values = []
                    
                # 最初の数回分を実行
                for i, value in enumerate(iter_values[:max_iterations]):
                    self.variables[target] = str(value)
                    self.add_step(
                        node.lineno,
                        "loop_iteration",
                        f"ループ {i+1}回目: {target} = {value}",
                    )
                    
                    # ループ本体を実行
                    for stmt in node.body:
                        self.visit(stmt)
                
                # 残りの反復がある場合
                if len(iter_values) > max_iterations:
                    self.add_step(
                        node.lineno,
                        "loop_continue",
                        f"... (残り {len(iter_values) - max_iterations} 回の反復)",
                    )
            except:
                # エラーが発生した場合は通常の処理
                for stmt in node.body:
                    self.visit(stmt)
        else:
            # range以外の場合は通常の処理
            for stmt in node.body:
                self.visit(stmt)

        self.add_step(
            node.lineno,
            "loop_end",
            f"ループ終了",
        )

    def visit_While(self, node: ast.While) -> None:
        """whileループを処理."""
        condition_desc = self._get_value_description(node.test)

        self.add_step(
            node.lineno,
            "loop",
            f"while {condition_desc}:",
        )

        loop_start = self.current_step

        # ループ本体をシミュレート
        for stmt in node.body:
            self.visit(stmt)

        # ループエッジを追加
        self.flow_edges.append({
            "from": self.current_step - 1,
            "to": loop_start - 1,
            "type": "loop",
            "label": "check condition",
        })

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """関数定義を処理."""
        args_desc = ", ".join(arg.arg for arg in node.args.args)
        self.add_step(
            node.lineno,
            "function_def",
            f"def {node.name}({args_desc}):",
        )

        # 関数内部はスキップ（定義のみ表示）
        self.add_step(
            node.lineno,
            "skip",
            f"[関数 {node.name} の内部定義]",
        )

    def visit_Return(self, node: ast.Return) -> None:
        """return文を処理."""
        if node.value:
            value_desc = self._get_value_description(node.value)
            self.add_step(
                node.lineno,
                "return",
                f"return {value_desc}",
            )
        else:
            self.add_step(
                node.lineno,
                "return",
                "return",
            )

    def visit_Expr(self, node: ast.Expr) -> None:
        """式文を処理."""
        # 式文（printなど）
        if isinstance(node.value, ast.Call):
            self.visit_Call(node.value, node.lineno)

    def visit_Call(self, node: ast.Call, line: int | None = None) -> None:
        """関数呼び出しを処理."""
        if line is None:
            line = node.lineno

        func_name = self._get_name(node.func)
        args_desc = ", ".join(self._get_value_description(arg) for arg in node.args)

        self.add_step(
            line,
            "call",
            f"{func_name}({args_desc})",
        )

    def _get_name(self, node: ast.AST) -> str:
        """ノードから名前を取得."""
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return "..."

    def _get_value_description(self, node: ast.AST) -> str:
        """値の説明を取得."""
        if isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return f'"{node.value}"'
            return str(node.value)
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.List):
            elements = [self._get_value_description(e) for e in node.elts[:3]]
            if len(node.elts) > 3:
                elements.append("...")
            return f"[{', '.join(elements)}]"
        if isinstance(node, ast.Dict):
            return "{...}"
        if isinstance(node, ast.Call):
            func_name = self._get_name(node.func)
            return f"{func_name}(...)"
        if isinstance(node, ast.BinOp):
            left = self._get_value_description(node.left)
            right = self._get_value_description(node.right)
            op = self._get_operator_symbol(node.op)
            return f"{left} {op} {right}"
        if isinstance(node, ast.Compare):
            left = self._get_value_description(node.left)
            ops = [self._get_comparison_symbol(op) for op in node.ops]
            comparators = [self._get_value_description(c) for c in node.comparators]
            parts = [left]
            for op, comp in zip(ops, comparators, strict=False):
                parts.extend([op, comp])
            return " ".join(parts)
        return "..."

    def _get_operator_symbol(self, op: ast.AST) -> str:
        """演算子のシンボルを取得."""
        op_map = {
            ast.Add: "+",
            ast.Sub: "-",
            ast.Mult: "*",
            ast.Div: "/",
            ast.FloorDiv: "//",
            ast.Mod: "%",
            ast.Pow: "**",
        }
        return op_map.get(type(op), "?")

    def _get_comparison_symbol(self, op: ast.AST) -> str:
        """比較演算子のシンボルを取得."""
        op_map = {
            ast.Eq: "==",
            ast.NotEq: "!=",
            ast.Lt: "<",
            ast.LtE: "<=",
            ast.Gt: ">",
            ast.GtE: ">=",
            ast.Is: "is",
            ast.IsNot: "is not",
            ast.In: "in",
            ast.NotIn: "not in",
        }
        return op_map.get(type(op), "?")
    
    def _evaluate_condition(self, node: ast.AST) -> str:
        """条件式を評価して結果を返す."""
        if isinstance(node, ast.Compare):
            # 比較演算子の場合
            left = self._get_value_description(node.left)
            op = node.ops[0] if node.ops else None
            right = self._get_value_description(node.comparators[0]) if node.comparators else None
            
            # 変数の値を取得
            if isinstance(node.left, ast.Name) and node.left.id in self.variables:
                left_val = self.variables[node.left.id]
                try:
                    left = int(left_val)
                except:
                    left = left_val
            
            try:
                # 数値として評価を試みる
                if isinstance(op, ast.Gt) and isinstance(left, int) and isinstance(right, str):
                    right_val = int(right)
                    return "True" if left > right_val else "False"
                elif isinstance(op, ast.Lt) and isinstance(left, int) and isinstance(right, str):
                    right_val = int(right)
                    return "True" if left < right_val else "False"
                elif isinstance(op, ast.GtE) and isinstance(left, int) and isinstance(right, str):
                    right_val = int(right)
                    return "True" if left >= right_val else "False"
                elif isinstance(op, ast.LtE) and isinstance(left, int) and isinstance(right, str):
                    right_val = int(right)
                    return "True" if left <= right_val else "False"
                elif isinstance(op, ast.Eq):
                    return "True" if str(left) == str(right) else "False"
                elif isinstance(op, ast.NotEq):
                    return "True" if str(left) != str(right) else "False"
            except:
                pass
                
        elif isinstance(node, ast.Constant):
            # 定数の場合
            return "True" if node.value else "False"
            
        elif isinstance(node, ast.Name):
            # 変数の場合
            if node.id in self.variables:
                val = self.variables[node.id]
                return "True" if val and val != "0" and val != "False" else "False"
        
        return "Unknown"


def create_flowchart_svg(steps: list[dict], edges: list[dict], highlight_line: int = 0) -> str:
    """フローチャートのSVGを生成."""
    # SVGの初期設定
    width = 800
    height = max(600, len(steps) * 100)
    node_width = 200
    node_height = 60
    x_center = width // 2
    y_spacing = 100

    svg_parts = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        "<defs>",
        '<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">',
        '<polygon points="0 0, 10 3.5, 0 7" fill="#333" />',
        "</marker>",
        "</defs>",
        "<style>",
        ".node { fill: #f0f0f0; stroke: #333; stroke-width: 2; }",
        ".node-highlight { fill: #ffeb3b; }",
        ".node-condition { fill: #e1f5fe; }",
        ".node-loop { fill: #f3e5f5; }",
        ".text { font-family: monospace; font-size: 12px; text-anchor: middle; }",
        ".edge { stroke: #333; stroke-width: 2; fill: none; marker-end: url(#arrowhead); }",
        ".edge-label { font-family: sans-serif; font-size: 10px; fill: #666; }",
        "</style>",
    ]

    # ノードの位置を計算
    node_positions = {}
    for i, step in enumerate(steps):
        node_positions[step["step"]] = {
            "x": x_center,
            "y": 50 + i * y_spacing,
        }

    # エッジを描画
    for edge in edges:
        from_pos = node_positions.get(edge["from"])
        to_pos = node_positions.get(edge["to"])

        if from_pos and to_pos:
            if edge["type"] == "sequential":
                # 直線のエッジ
                svg_parts.append(
                    f'<line class="edge" x1="{from_pos["x"]}" y1="{from_pos["y"] + node_height//2}" '
                    f'x2="{to_pos["x"]}" y2="{to_pos["y"] - node_height//2}" />',
                )
            elif edge["type"] in ["branch", "loop"]:
                # 曲線のエッジ
                control_x = from_pos["x"] + 150 if edge["type"] == "branch" else from_pos["x"] - 150
                control_y = (from_pos["y"] + to_pos["y"]) // 2

                path = f'M {from_pos["x"]} {from_pos["y"] + node_height//2} '
                path += f'Q {control_x} {control_y} {to_pos["x"]} {to_pos["y"] - node_height//2}'

                svg_parts.append(f'<path class="edge" d="{path}" />')

                # ラベルを追加
                if "label" in edge:
                    label_x = (from_pos["x"] + control_x) // 2
                    label_y = (from_pos["y"] + control_y) // 2
                    svg_parts.append(
                        f'<text class="edge-label" x="{label_x}" y="{label_y}">{edge["label"]}</text>',
                    )

    # ノードを描画
    for step in steps:
        pos = node_positions[step["step"]]
        x = pos["x"] - node_width // 2
        y = pos["y"] - node_height // 2

        # ノードのスタイルを決定
        node_class = "node"
        if step["line"] == highlight_line:
            node_class += " node-highlight"
        elif step["operation"] == "condition":
            node_class += " node-condition"
        elif step["operation"] == "loop":
            node_class += " node-loop"

        # ノードの矩形
        svg_parts.append(
            f'<rect class="{node_class}" x="{x}" y="{y}" '
            f'width="{node_width}" height="{node_height}" rx="5" />',
        )

        # テキスト
        text_lines = step["description"].split("\n")
        for i, line in enumerate(text_lines[:2]):  # 最大2行まで
            text_y = pos["y"] + (i - 0.5) * 15
            svg_parts.append(
                f'<text class="text" x="{pos["x"]}" y="{text_y}">{line[:30]}</text>',
            )

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


def visualize_code(code: str, *, highlight_line: int = 0, show_flow: bool = True) -> dict:
    """コードを可視化.

    Args:
        code: Pythonコード
        highlight_line: ハイライトする行
        show_flow: フロー図を生成するか

    Returns:
        可視化結果
    """
    try:
        # ASTを解析
        tree = ast.parse(code)

        # 実行フローをシミュレート
        simulator = ExecutionFlowSimulator()
        simulator.visit(tree)

        result = {
            "success": True,
            "steps": simulator.steps,
            "final_variables": simulator.variables,
            "flow_edges": simulator.flow_edges,
        }

        # フローチャートを生成
        if show_flow and simulator.steps:
            result["flowchart"] = create_flowchart_svg(
                simulator.steps,
                simulator.flow_edges,
                highlight_line,
            )

        # 実行ステップの説明を生成
        explanations = []
        for step in simulator.steps:
            explanation = {
                "line": step["line"],
                "operation": step["operation"],
                "description": step["description"],
                "explanation": _get_step_explanation(step),
            }
            if step["variables"]:
                explanation["variables_after"] = step["variables"]
            explanations.append(explanation)

        result["explanations"] = explanations

        return result

    except SyntaxError as e:
        return {
            "success": False,
            "error": "syntax_error",
            "message": str(e),
            "line": e.lineno,
        }
    except Exception as e:
        return {
            "success": False,
            "error": "visualization_error",
            "message": str(e),
        }


def _get_step_explanation(step: dict) -> str:
    """ステップの教育的説明を生成."""
    op = step["operation"]

    explanations = {
        "assign": "変数に値を代入しています。",
        "augassign": "変数の値を更新しています。",
        "condition": "条件をチェックして、結果に応じて処理を分岐します。",
        "branch_taken": "条件に基づいて、このブロックを実行します。",
        "branch_skipped": "条件に基づいて、このブロックはスキップされます。",
        "branch_unknown": "実行時に条件が評価され、どちらかのブロックが実行されます。",
        "loop_start": "繰り返し処理を開始します。",
        "loop_iteration": "ループの各反復で変数が更新されます。",
        "loop_continue": "ループはまだ続きますが、表示は省略されています。",
        "loop_end": "繰り返し処理が完了しました。",
        "loop": "繰り返し処理を実行します。",
        "function_def": "関数を定義しています。この時点では実行されません。",
        "call": "関数を呼び出しています。",
        "return": "関数から値を返します。",
        "skip": "この部分はスキップされます。",
    }

    return explanations.get(op, "このステップを実行します。")

"""エラー解析サービス.

静的解析によるエラーの教育的説明を提供.
"""

import ast
import re
from typing import Any


def parse_error_location(error_message: str) -> tuple[int, int]:
    """エラーメッセージから行番号と列番号を抽出."""
    # より多様なパターンに対応
    patterns = [
        r"line (\d+)(?:, column (\d+))?",  # 標準的なパターン
        r"\((\d+):(\d+)\)",  # (line:column) 形式
        r"at line (\d+)",  # at line X 形式
    ]

    for pattern in patterns:
        match = re.search(pattern, error_message)
        if match:
            line = int(match.group(1))
            column = int(match.group(2)) if len(match.groups()) > 1 and match.group(2) else 0
            return line, column
    return 0, 0


def get_educational_explanation(error_type: str, context: dict[str, Any]) -> dict[str, Any]:
    """エラータイプに応じた教育的説明を生成."""
    explanations = {
        "SyntaxError": {
            "simple": "コードの書き方に間違いがあります",
            "detail": "Pythonの文法ルールに従っていない部分があります。括弧の対応やコロンの位置を確認してください。",
            "tips": [
                "括弧 (), [], {} の対応を確認",
                "if文やfor文の後にコロン(:)があるか確認",
                "インデントが正しいか確認",
                "文字列のクォートが閉じているか確認",
                "予約語（if, for, def等）のスペルを確認",
            ],
            "concept": "構文エラーは、Pythonがコードを理解できない時に発生します。料理のレシピのように、正しい順序と形式が必要です。",
            "difficulty_level": 1,
        },
        "NameError": {
            "simple": "存在しない名前を使っています",
            "detail": f"'{context.get('name', '変数')}' という名前が定義されていません。変数名のスペルミスか、定義し忘れの可能性があります。",
            "tips": [
                "変数名のスペルを確認",
                "変数を使う前に定義しているか確認",
                "大文字・小文字の違いに注意",
                "変数のスコープ（有効範囲）を確認",
                "インポートし忘れていないか確認",
            ],
            "concept": "変数は値を保存する箱のようなものです。使う前に必ず箱を用意（定義）する必要があります。",
            "difficulty_level": 1,
        },
        "TypeError": {
            "simple": "データの種類が合っていません",
            "detail": "異なる種類のデータを一緒に使おうとしています。数値と文字列など、種類の違うデータは直接計算できません。",
            "tips": [
                "int()やstr()で型変換を行う",
                "変数の中身を確認する",
                "関数の引数の数や種類を確認",
                "演算子が使えるデータ型か確認",
                "type()関数でデータ型を調べる",
            ],
            "concept": "Pythonでは数値は数値同士、文字列は文字列同士でしか計算できません。りんご＋みかんは計算できないのと同じです。",
            "difficulty_level": 2,
        },
        "IndentationError": {
            "simple": "インデント（字下げ）が正しくありません",
            "detail": "Pythonではインデントでコードのブロックを表現します。スペースの数を揃えましょう。",
            "tips": [
                "同じブロック内では同じ数のスペースを使う",
                "タブとスペースを混在させない",
                "通常は4つのスペースを使う",
                "エディタの空白文字表示機能を使う",
                "自動インデント機能を活用する",
            ],
            "concept": "インデントは段落のようなものです。同じ話題（ブロック）は同じ深さで書く必要があります。",
            "difficulty_level": 1,
        },
        "IndexError": {
            "simple": "リストの範囲外にアクセスしています",
            "detail": "存在しない位置の要素を取得しようとしています。リストの長さを確認してください。",
            "tips": [
                "リストのインデックスは0から始まる",
                "len()関数でリストの長さを確認",
                "負のインデックスは後ろから数える",
                "スライスを使って安全にアクセス",
                "try-exceptで例外処理を行う",
            ],
            "concept": "リストは0番から始まる番号付きの箱です。3個の箱がある場合、番号は0, 1, 2となります。",
            "difficulty_level": 2,
        },
        "ValueError": {
            "simple": "値が適切ではありません",
            "detail": "関数に渡された値が期待される形式と異なります。値の内容や形式を確認してください。",
            "tips": [
                "入力値の形式を確認",
                "空文字列や特殊文字に注意",
                "数値変換時は数字のみか確認",
                "範囲外の値でないか確認",
                "ドキュメントで正しい使い方を確認",
            ],
            "concept": "関数は特定の形式の入力を期待します。自動販売機にお札を入れる向きが決まっているのと同じです。",
            "difficulty_level": 2,
        },
        "AttributeError": {
            "simple": "そのオブジェクトにその属性やメソッドはありません",
            "detail": "オブジェクトに存在しない属性やメソッドにアクセスしようとしています。",
            "tips": [
                "属性名・メソッド名のスペルを確認",
                "dir()関数で利用可能な属性を確認",
                "オブジェクトの型を確認",
                "ドキュメントを参照",
                "IDEの自動補完を活用",
            ],
            "concept": "オブジェクトはそれぞれ異なる機能（メソッド）を持っています。車には走る機能がありますが、飛ぶ機能はありません。",
            "difficulty_level": 3,
        },
    }

    error_info = explanations.get(
        error_type,
        {
            "simple": "エラーが発生しました",
            "detail": "コードに問題があります。エラーメッセージを確認してください。",
            "tips": ["エラーメッセージを読んで原因を特定する"],
            "concept": "プログラミングのエラーは学習のチャンスです。エラーメッセージは問題を解決するヒントを教えてくれます。",
            "difficulty_level": 1,
        },
    )

    return error_info


def analyze_code_context(code: str, line: int, error_type: str) -> dict[str, Any]:
    """コードのコンテキストを解析して詳細な情報を取得."""
    context = {
        "problematic_line": "",
        "surrounding_lines": [],
        "indentation_level": 0,
        "in_function": False,
        "in_loop": False,
        "in_condition": False,
        "undefined_vars": [],
        "defined_vars": set(),
    }

    lines = code.split("\n")
    if 0 < line <= len(lines):
        context["problematic_line"] = lines[line - 1]

        # 前後の行を取得
        start = max(0, line - 3)
        end = min(len(lines), line + 2)
        context["surrounding_lines"] = lines[start:end]

        # インデントレベルを計算
        context["indentation_level"] = len(context["problematic_line"]) - len(context["problematic_line"].lstrip())

    # ASTを使った詳細解析
    try:
        tree = ast.parse(code)

        # 定義された変数を収集
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        context["defined_vars"].add(target.id)
            elif isinstance(node, ast.FunctionDef):
                context["defined_vars"].add(node.name)
                # 関数の引数も定義済み変数として追加
                for arg in node.args.args:
                    context["defined_vars"].add(arg.arg)

        # 使用されている未定義変数を検出
        if error_type == "NameError":
            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                    if node.id not in context["defined_vars"] and node.id not in __builtins__:
                        context["undefined_vars"].append(node.id)
    except:
        pass  # パースエラーの場合は無視

    return context


def suggest_fix(code: str, error_type: str, line: int, error_message: str = "") -> list[str]:
    """エラーに対する修正提案を生成."""
    suggestions = []
    context = analyze_code_context(code, line, error_type)

    if error_type == "SyntaxError":
        problem_line = context["problematic_line"]

        # 特定のエラーメッセージに基づく提案
        if "expected ':'" in error_message:
            suggestions.append("コロン(:)が必要です")
            # if, for, while, def, classなどの後にコロンが必要
            for keyword in ["if", "for", "while", "def", "class", "elif", "else", "try", "except", "finally"]:
                if keyword in problem_line and not problem_line.strip().endswith(":"):
                    suggestions.append(f"{keyword}文の後にはコロン(:)を付けてください")
                    suggestions.append(f"修正例: {problem_line.strip()}:")
                    break

        elif "was never closed" in error_message:
            # 括弧が閉じられていない
            match = re.search(r"'(.)'", error_message)
            if match:
                unclosed_char = match.group(1)
                if unclosed_char == "(":
                    suggestions.append("開き括弧 '(' が閉じられていません")
                    suggestions.append("対応する閉じ括弧 ')' を追加してください")
                    # 複数行にまたがる可能性があるため、前の行もチェック
                    suggestions.append("前の行から続いている括弧がないか確認してください")
                elif unclosed_char == "[":
                    suggestions.append("開き角括弧 '[' が閉じられていません")
                    suggestions.append("対応する閉じ角括弧 ']' を追加してください")
                elif unclosed_char == "{":
                    suggestions.append("開き波括弧 '{' が閉じられていません")
                    suggestions.append("対応する閉じ波括弧 '}' を追加してください")

        elif "unexpected EOF" in error_message:
            suggestions.append("ファイルが予期せず終了しています")
            suggestions.append("以下を確認してください：")
            suggestions.append("・開いた括弧がすべて閉じられているか")
            suggestions.append("・文字列がすべて閉じられているか")
            suggestions.append("・if文やループのブロックが完成しているか")

        else:
            # 従来の一般的なチェック
            # コロンの欠落チェック
            if any(
                keyword in problem_line
                for keyword in ["if ", "for ", "while ", "def ", "class ", "elif ", "else", "try", "except"]
            ):
                if not problem_line.strip().endswith(":"):
                    suggestions.append("行末にコロン(:)を追加してください")
                    suggestions.append(f"修正例: {problem_line.strip()}:")

            # 括弧の不一致
            open_parens = problem_line.count("(")
            close_parens = problem_line.count(")")
            if open_parens != close_parens:
                diff = abs(open_parens - close_parens)
                if open_parens > close_parens:
                    suggestions.append(f"閉じ括弧 ')' が{diff}個不足しています")
                else:
                    suggestions.append(f"開き括弧 '(' が{diff}個不足しています")

            # クォートの不一致
            single_quotes = problem_line.count("'")
            double_quotes = problem_line.count('"')
            if single_quotes % 2 != 0:
                suggestions.append("シングルクォート(')が閉じられていません")
            if double_quotes % 2 != 0:
                suggestions.append('ダブルクォート(")が閉じられていません')

    elif error_type == "NameError":
        # エラーメッセージから変数名を抽出
        match = re.search(r"name '(\w+)' is not defined", error_message)
        if match:
            var_name = match.group(1)
            suggestions.append(f"変数 '{var_name}' が定義されていません")

            # タイポの可能性をチェック
            for defined_var in context["defined_vars"]:
                if abs(len(var_name) - len(defined_var)) <= 2:
                    # 簡易的な類似度チェック
                    if sum(c1 == c2 for c1, c2 in zip(var_name, defined_var, strict=False)) >= len(var_name) * 0.7:
                        suggestions.append(f"もしかして: '{defined_var}' のつもりでしたか？")

            suggestions.append(f"使用する前に変数を定義してください: {var_name} = 値")

    elif error_type == "IndentationError":
        # 特定のエラーメッセージに基づく提案
        if "expected an indented block" in error_message:
            suggestions.append("インデントされたブロックが必要です")
            suggestions.append("if文、for文、関数定義などの後は、次の行をインデント（字下げ）してください")
            suggestions.append("通常は4つのスペースを使用します")

            # 前の行を確認
            if line > 1 and len(context["surrounding_lines"]) > 0:
                prev_idx = min(line - 2, len(context["surrounding_lines"]) - 1)
                if prev_idx >= 0:
                    prev_line = context["surrounding_lines"][prev_idx]
                    if prev_line.strip().endswith(":"):
                        suggestions.append(f"前の行 '{prev_line.strip()}' の後にインデントが必要です")
                        suggestions.append(f"修正例:\n{prev_line}\n    {context['problematic_line'].strip()}")
        else:
            suggestions.append("インデントが正しくありません")

            # 前の行との比較
            if len(context["surrounding_lines"]) > 1:
                prev_line = context["surrounding_lines"][-2] if line > 1 else ""
                if any(keyword in prev_line for keyword in ["if ", "for ", "while ", "def ", "class "]):
                    suggestions.append("前の行の後はインデントを増やしてください（通常4スペース）")
                else:
                    suggestions.append("同じブロック内では同じインデントレベルを保ってください")

            suggestions.append("タブとスペースを混在させないでください")

    elif error_type == "TypeError":
        suggestions.append("データ型が一致していません")
        if "unsupported operand type" in error_message:
            suggestions.append("異なる型のデータを演算しようとしています")
            suggestions.append("int()やstr()で型変換を行ってください")
        elif "missing" in error_message and "argument" in error_message:
            suggestions.append("関数に必要な引数が不足しています")

    elif error_type == "IndexError":
        suggestions.append("リストの範囲外にアクセスしています")
        suggestions.append("len()でリストの長さを確認してください")
        suggestions.append("インデックスは0から始まることに注意してください")

    return suggestions


async def analyze_error(code: str, error_message: str) -> dict:
    """エラーを解析して教育的な説明を提供.

    Args:
        code: エラーが発生したコード
        error_message: エラーメッセージ

    Returns:
        解析結果
    """
    # エラータイプの抽出（より柔軟に）
    error_type = "UnknownError"
    error_detail = ""

    # 一般的なPythonエラーのパターンをチェック
    error_patterns = {
        r"SyntaxError": "SyntaxError",
        r"NameError": "NameError",
        r"TypeError": "TypeError",
        r"IndentationError": "IndentationError",
        r"IndexError": "IndexError",
        r"ValueError": "ValueError",
        r"AttributeError": "AttributeError",
        r"KeyError": "KeyError",
        r"ZeroDivisionError": "ZeroDivisionError",
        r"ImportError": "ImportError",
        r"EOFError": "EOFError",
        r"invalid syntax": "SyntaxError",
        r"unexpected indent": "IndentationError",
        r"unindent does not match": "IndentationError",
        r"list index out of range": "IndexError",
        r"string index out of range": "IndexError",
        # 特定のSyntaxErrorパターン
        r"expected an indented block": "IndentationError",
        r"expected ':'": "SyntaxError",
        r"was never closed": "SyntaxError",
        r"unexpected EOF while parsing": "SyntaxError",
        r"unterminated string": "SyntaxError",
    }

    for pattern, etype in error_patterns.items():
        if re.search(pattern, error_message, re.IGNORECASE):
            error_type = etype
            break

    # エラーの詳細部分を抽出
    if ":" in error_message:
        parts = error_message.split(":", 1)
        if len(parts) > 1:
            error_detail = parts[1].strip()

    # エラー位置の解析
    line, column = parse_error_location(error_message)

    # コンテキスト情報の抽出
    context = analyze_code_context(code, line, error_type)

    # NameErrorの場合、未定義変数名を特定
    if error_type == "NameError":
        match = re.search(r"name '(\w+)' is not defined", error_message)
        if match:
            context["name"] = match.group(1)

    # 教育的説明の生成
    explanation = get_educational_explanation(error_type, context)

    # 修正提案の生成（エラーメッセージも渡す）
    suggestions = suggest_fix(code, error_type, line, error_message)

    # 関連する学習リソース
    resources = [
        {
            "title": f"Python {error_type} について学ぶ",
            "url": f"https://docs.python.org/ja/3/tutorial/errors.html#{error_type.lower()}",
        },
    ]

    # 類似例の生成（エラーに応じてより具体的に）
    similar_examples = []
    if error_type == "SyntaxError":
        # expected ':' のエラー
        if "expected ':'" in error_message:
            similar_examples.append(
                {
                    "wrong": "if x > 5\n    print('大きい')",
                    "correct": "if x > 5:\n    print('大きい')",
                    "explanation": "if文の後にはコロン(:)が必要です",
                },
            )
            similar_examples.append(
                {
                    "wrong": "for i in range(10)\n    print(i)",
                    "correct": "for i in range(10):\n    print(i)",
                    "explanation": "for文の後にもコロン(:)が必要です",
                },
            )
        # was never closed のエラー
        elif "was never closed" in error_message:
            if "'('" in error_message:
                similar_examples.append(
                    {
                        "wrong": "print('Hello World'",
                        "correct": "print('Hello World')",
                        "explanation": "開き括弧には必ず対応する閉じ括弧が必要です",
                    },
                )
                similar_examples.append(
                    {
                        "wrong": "result = (1 + 2\nprint(result)",
                        "correct": "result = (1 + 2)\nprint(result)",
                        "explanation": "複数行にまたがる場合も括弧を閉じる必要があります",
                    },
                )
        # unexpected EOF
        elif "unexpected EOF" in error_message:
            similar_examples.append(
                {
                    "wrong": "if True:\n    print('開始'",
                    "correct": "if True:\n    print('開始')",
                    "explanation": "文字列やブロックが完成していません",
                },
            )
        # 従来の一般的な例
        elif ":" not in context.get("problematic_line", "") and any(
            kw in context.get("problematic_line", "") for kw in ["if", "for", "while", "def", "class"]
        ):
            similar_examples.append(
                {
                    "wrong": "if x > 5\n    print('大きい')",
                    "correct": "if x > 5:\n    print('大きい')",
                    "explanation": "制御構造の後にはコロン(:)が必要です",
                },
            )

    elif error_type == "NameError":
        if context.get("name"):
            var_name = context["name"]
            similar_examples.append(
                {
                    "wrong": f"print({var_name})\n{var_name} = 10",
                    "correct": f"{var_name} = 10\nprint({var_name})",
                    "explanation": "変数は使用する前に定義する必要があります",
                },
            )
        # 組み込み関数のタイポ
        if context.get("name") in ["pirnt", "prnt", "prin"]:
            similar_examples.append(
                {
                    "wrong": "pirnt('Hello')",
                    "correct": "print('Hello')",
                    "explanation": "組み込み関数名のスペルに注意してください",
                },
            )

    elif error_type == "IndentationError":
        if "expected an indented block" in error_message:
            similar_examples.append(
                {
                    "wrong": "if x > 5:\nprint('大きい')",
                    "correct": "if x > 5:\n    print('大きい')",
                    "explanation": "if文の後のブロックはインデントが必要です",
                },
            )
            similar_examples.append(
                {
                    "wrong": "def hello():\nprint('Hello')",
                    "correct": "def hello():\n    print('Hello')",
                    "explanation": "関数定義の後のブロックもインデントが必要です",
                },
            )
        else:
            similar_examples.append(
                {
                    "wrong": "if x > 5:\n  print('大きい')\n    print('とても大きい')",
                    "correct": "if x > 5:\n    print('大きい')\n    print('とても大きい')",
                    "explanation": "同じブロック内では同じインデントレベルを保ってください",
                },
            )
            similar_examples.append(
                {
                    "wrong": "def func():\n\treturn 1  # タブ\n    return 2  # スペース",
                    "correct": "def func():\n    return 1\n    return 2",
                    "explanation": "タブとスペースを混在させないでください",
                },
            )

    elif error_type == "TypeError":
        if "unsupported operand" in error_message:
            similar_examples.append(
                {
                    "wrong": "result = '5' + 3",
                    "correct": "result = int('5') + 3  # または '5' + str(3)",
                    "explanation": "異なる型の値を演算する場合は型変換が必要です",
                },
            )
        elif "missing" in error_message and "argument" in error_message:
            similar_examples.append(
                {
                    "wrong": "print()",
                    "correct": "print('Hello')",
                    "explanation": "関数には必要な引数を渡す必要があります",
                },
            )

    elif error_type == "IndexError":
        similar_examples.append(
            {
                "wrong": "lst = [1, 2, 3]\nprint(lst[3])",
                "correct": "lst = [1, 2, 3]\nprint(lst[2])  # 最後の要素",
                "explanation": "リストのインデックスは0から始まり、長さ-1で終わります",
            },
        )

    # 学習リソースの整形
    learning_resources = [resource["title"] for resource in resources]

    # エラー解決のステップバイステップガイド
    step_by_step_guide = generate_step_by_step_guide(error_type, context, line)

    # 視覚的な説明（アスキーアートやダイアグラム）
    visual_explanation = generate_visual_explanation(error_type, context)

    return {
        "error_type": error_type,
        "line_number": line,
        "column_number": column,
        "simple_explanation": explanation.get("simple", "エラーが発生しました"),
        "detailed_explanation": explanation.get("detail", "コードに問題があります"),
        "concept_explanation": explanation.get("concept", ""),
        "difficulty_level": explanation.get("difficulty_level", 1),
        "common_causes": explanation.get("tips", []),
        "fix_suggestions": suggestions,
        "step_by_step_guide": step_by_step_guide,
        "similar_examples": similar_examples,
        "visual_explanation": visual_explanation,
        "learning_resources": learning_resources,
        "context": {
            "problematic_line": context.get("problematic_line", ""),
            "surrounding_lines": context.get("surrounding_lines", []),
            "indentation_level": context.get("indentation_level", 0),
        },
    }


def generate_step_by_step_guide(error_type: str, context: dict[str, Any], line: int) -> list[dict[str, Any]]:
    """エラー解決のステップバイステップガイドを生成."""
    guides = {
        "SyntaxError": [
            {"step": 1, "action": "エラーメッセージの行番号を確認", "detail": f"{line}行目を見てください"},
            {"step": 2, "action": "その行の文法をチェック", "detail": "コロン、括弧、クォートなどを確認"},
            {"step": 3, "action": "前後の行も確認", "detail": "前の行から続く構文エラーの可能性もあります"},
            {"step": 4, "action": "修正して再実行", "detail": "一つずつ修正して動作を確認"},
        ],
        "NameError": [
            {
                "step": 1,
                "action": "エラーで表示された名前を確認",
                "detail": f"'{context.get('name', '変数')}'というキーワードを探す",
            },
            {
                "step": 2,
                "action": "その名前が定義されているか確認",
                "detail": "変数の定義、関数の定義、インポート文を探す",
            },
            {"step": 3, "action": "スペルミスをチェック", "detail": "大文字・小文字の違いも確認"},
            {"step": 4, "action": "定義の位置を確認", "detail": "使用する前に定義されているか"},
        ],
        "TypeError": [
            {"step": 1, "action": "エラーが発生した演算や関数呼び出しを特定", "detail": f"{line}行目の演算を確認"},
            {"step": 2, "action": "関係する変数の型を確認", "detail": "type()関数やprint()で中身を確認"},
            {"step": 3, "action": "必要な型変換を特定", "detail": "int(), str(), float()などの使用を検討"},
            {"step": 4, "action": "型変換を適用", "detail": "適切な場所で型変換を行う"},
        ],
        "IndentationError": [
            {"step": 1, "action": "エラー行のインデントを確認", "detail": f"{line}行目の空白を数える"},
            {"step": 2, "action": "前後の行と比較", "detail": "同じブロックは同じインデント"},
            {"step": 3, "action": "タブとスペースの混在を確認", "detail": "エディタの空白文字表示をONに"},
            {"step": 4, "action": "一貫したインデントに修正", "detail": "通常は4スペースに統一"},
        ],
        "IndexError": [
            {"step": 1, "action": "リストやタプルのアクセス部分を特定", "detail": f"{line}行目の[]を探す"},
            {"step": 2, "action": "リストの長さを確認", "detail": "len()関数で要素数を調べる"},
            {"step": 3, "action": "インデックスの値を確認", "detail": "0から始まることを忘れずに"},
            {"step": 4, "action": "範囲チェックを追加", "detail": "if文で範囲内かチェック"},
        ],
    }

    return guides.get(
        error_type,
        [
            {"step": 1, "action": "エラーメッセージを読む", "detail": "エラーの種類と発生場所を確認"},
            {"step": 2, "action": "該当行を確認", "detail": "問題のあるコードを特定"},
            {"step": 3, "action": "修正を試みる", "detail": "エラーメッセージのヒントに従う"},
        ],
    )


def generate_visual_explanation(error_type: str, context: dict[str, Any]) -> dict[str, str]:
    """エラーの視覚的な説明を生成."""
    visuals = {
        "SyntaxError": {
            "type": "diagram",
            "content": """
構文エラーの例：
─────────────────────────
❌ if x > 5
     print("大きい")

✅ if x > 5:  ← コロンが必要
     print("大きい")
─────────────────────────
""",
        },
        "NameError": {
            "type": "flow",
            "content": f"""
変数の使用フロー：
─────────────────────────
1. 定義 → x = 10
2. 使用 → print(x)  ✅

❌ 使用 → print({context.get("name", "y")})
   定義 → {context.get("name", "y")} = 20
─────────────────────────
""",
        },
        "TypeError": {
            "type": "comparison",
            "content": """
型の不一致：
─────────────────────────
❌ "5" + 3
   文字列 + 数値 = エラー！

✅ int("5") + 3 = 8
   数値 + 数値 = OK!

✅ "5" + str(3) = "53"
   文字列 + 文字列 = OK!
─────────────────────────
""",
        },
        "IndentationError": {
            "type": "alignment",
            "content": """
インデントの例：
─────────────────────────
❌ 不揃いなインデント
if True:
  x = 1
    y = 2  ← 揃っていない！

✅ 正しいインデント
if True:
    x = 1
    y = 2  ← 揃っている！
─────────────────────────
""",
        },
        "IndexError": {
            "type": "array",
            "content": """
リストのインデックス：
─────────────────────────
lst = ["A", "B", "C"]
      [0]  [1]  [2]

✅ lst[0] = "A"
✅ lst[2] = "C"
❌ lst[3] = エラー！

長さ: len(lst) = 3
有効な範囲: 0〜2
─────────────────────────
""",
        },
    }

    return visuals.get(
        error_type,
        {
            "type": "text",
            "content": "エラーの詳細な視覚的説明は準備中です。",
        },
    )

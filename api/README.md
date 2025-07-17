# ハイスクール Python - コード解析ツール - API サーバー

高校生が Python プログラミングを学ぶためのバックエンド API です。FastAPI で構築され、AST を使用した静的解析により安全な学習環境を提供します。

## URL

- Local: [http://localhost:8080](http://localhost:8080)
- Production: [https://api.code-analytics.high-school-python.jp](https://api.code-analytics.high-school-python.jp)

## 機能概要

### 1. コード構造解析

- Python AST を使用した静的解析
- 関数、クラス、変数、ループ、条件分岐の抽出
- コード複雑度の計算
- スタイルチェックと改善提案

### 2. 実行フロー可視化

- 静的解析による実行フローのシミュレーション
- ステップバイステップの実行追跡
- 変数の状態変化の追跡
- SVG 形式のフローチャート生成

### 3. エラーの教育的説明

- 高校生向けの分かりやすい説明
- シンプルな説明と詳細説明の両方を提供
- 一般的な原因と修正提案
- 類似例とデバッグのヒント
- 学習リソースへのリンク

## 技術スタック

- **フレームワーク**: FastAPI
- **言語**: Python 3.11+
- **パッケージ管理**: uv
- **コード解析**: Python AST (Abstract Syntax Tree)
- **可視化**: Graphviz
- **リンター**: Ruff
- **テスト**: pytest

## セットアップ

### 前提条件

- Python 3.11 以上
- uv（Python パッケージマネージャー）
- Graphviz（可視化機能用）

### インストール

```bash
# uvのインストール（まだの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係のインストール
cd api
uv sync

# 開発サーバーの起動
uv run fastapi dev src/main.py
```

API は <http://localhost:8000> で利用可能になります。
API ドキュメントは <http://localhost:8000/docs> で確認できます。

## プロジェクト構造

```txt
api/
├── src/
│   ├── main.py              # FastAPIアプリケーションエントリーポイント
│   ├── models/              # Pydanticモデル
│   │   ├── analysis.py      # 解析リクエスト/レスポンスモデル
│   │   ├── visualization.py # 可視化リクエスト/レスポンスモデル
│   │   └── error_analysis.py # エラー解析リクエスト/レスポンスモデル
│   ├── routers/             # APIエンドポイント
│   │   ├── analysis.py      # コード解析エンドポイント
│   │   ├── visualization.py # 可視化エンドポイント
│   │   └── error_analysis.py # エラー分析エンドポイント
│   └── services/            # ビジネスロジック
│       ├── analyzer.py      # コード構造解析
│       ├── visualizer.py    # 実行フロー可視化
│       └── error_analyzer.py # エラー分析
├── tests/                   # テストファイル
├── examples/                # 使用例
├── pyproject.toml          # プロジェクト設定
├── uv.lock                 # 依存関係ロックファイル
└── README.md               # このファイル
```

## API エンドポイント

すべてのエンドポイントは `/api/v1` プレフィックスを持ち、JSON リクエスト/レスポンスを使用します。

### POST /api/v1/analyze

コードの構造、品質、複雑性を解析します。

**リクエスト:**

```json
{
  "code": "def hello():\n    print('Hello, World!')"
}
```

**レスポンス:**

```json
{
  "structure": {
    "imports": [],
    "functions": [{ "name": "hello", "line": 1, "params": [] }],
    "classes": [],
    "variables": [],
    "loops": [],
    "conditionals": []
  },
  "metrics": {
    "lines": 2,
    "functions": 1,
    "classes": 0,
    "complexity": 1
  },
  "style_issues": [],
  "improvements": [
    {
      "type": "suggestion",
      "message": "関数にドキュメント文字列（docstring）を追加することを検討してください",
      "line": 1
    }
  ],
  "quality_score": 85,
  "summary": "シンプルな関数が1つ定義されています。コードはよく構造化されていますが、ドキュメントの追加を検討してください。"
}
```

### POST /api/v1/visualize

コードの実行フローを可視化します。

**リクエスト:**

```json
{
  "code": "if x > 0:\n    print('正の数')\nelse:\n    print('負の数')"
}
```

**レスポンス:**

```json
{
  "steps": [
    {
      "step": 1,
      "type": "condition",
      "code": "if x > 0:",
      "description": "x が 0 より大きいかチェックします",
      "line": 1,
      "variables": { "x": "<不明>" }
    },
    {
      "step": 2,
      "type": "statement",
      "code": "print('正の数')",
      "description": "x > 0 の場合: '正の数' を表示します",
      "line": 2,
      "variables": { "x": "<不明>" }
    },
    {
      "step": 3,
      "type": "statement",
      "code": "print('負の数')",
      "description": "x <= 0 の場合: '負の数' を表示します",
      "line": 4,
      "variables": { "x": "<不明>" }
    }
  ],
  "svg": "<svg>...</svg>",
  "description": "このコードは変数 x の値によって異なるメッセージを表示します。x が 0 より大きい場合は '正の数'、それ以外の場合は '負の数' を表示します。"
}
```

### POST /api/v1/analyze-error

エラーメッセージを解析し、教育的な説明を提供します。

**リクエスト:**

```json
{
  "code": "print(x)",
  "error_message": "NameError: name 'x' is not defined"
}
```

**レスポンス:**

```json
{
  "error_type": "NameError",
  "simple_explanation": "変数 'x' が定義されていません。使う前に変数を作る必要があります。",
  "detailed_explanation": "Python では、変数を使う前に必ず値を代入して定義する必要があります。'x' という名前の変数を使おうとしていますが、まだ作られていません。",
  "common_causes": ["変数の定義を忘れている", "タイプミス（変数名のスペルミス）", "変数の定義が別のスコープにある"],
  "suggestions": [
    {
      "description": "変数を使う前に値を代入して定義しましょう",
      "code": "x = 10  # 例: x に 10 を代入\nprint(x)"
    }
  ],
  "similar_examples": [
    {
      "wrong": "print(message)",
      "correct": "message = 'Hello'\nprint(message)",
      "explanation": "message を使う前に定義する"
    }
  ],
  "debugging_steps": [
    "1. エラーメッセージで示された変数名を確認する",
    "2. その変数を使う前に定義しているか確認する",
    "3. 変数名にタイプミスがないか確認する",
    "4. 変数のスコープ（使える範囲）を確認する"
  ],
  "learning_resources": [
    {
      "title": "Python の変数と代入",
      "url": "https://docs.python.org/ja/3/tutorial/introduction.html#numbers"
    }
  ],
  "difficulty_level": "初級"
}
```

## 開発

### コードスタイル

```bash
# リントチェック
uv run ruff check .

# 自動フォーマット
uv run ruff format .
```

### テスト

```bash
# すべてのテストを実行
uv run pytest

# カバレッジ付きでテスト実行
uv run pytest --cov=src

# 特定のテストファイルを実行
uv run pytest tests/test_analyzer.py
```

### 開発ツール

```bash
# 開発サーバー（自動リロード付き）
uv run fastapi dev src/main.py

# 本番サーバー
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## セキュリティ

このシステムは教育用途に設計されており、以下のセキュリティ対策を実装しています：

- **コード実行なし**: すべての解析は AST ベースの静的解析で行われます
- **入力検証**: すべての入力は Pydantic モデルで検証されます
- **リソース制限**: 大きなコードファイルに対する制限があります
- **CORS 設定**: 適切なオリジンのみが API にアクセスできます

## デプロイ

### Docker を使用したデプロイ

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# uvのインストール
RUN pip install uv

# 依存関係のコピーとインストール
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# アプリケーションコードのコピー
COPY . .

# ポート公開
EXPOSE 8000

# アプリケーション起動
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 環境変数

本番環境では以下の環境変数を設定できます：

- `LOG_LEVEL`: ログレベル（DEBUG, INFO, WARNING, ERROR）
- `CORS_ORIGINS`: 許可する CORS オリジン（カンマ区切り）
- `MAX_CODE_LENGTH`: 受け付ける最大コード長（デフォルト: 10000 文字）

## トラブルシューティング

### uv が見つからない

```bash
# uvを再インストール
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Graphviz エラー

可視化機能でエラーが発生する場合：

```bash
# macOS
brew install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz

# Windows (Chocolatey)
choco install graphviz
```

### ポートが使用中

デフォルトポート（8000）が使用中の場合：

```bash
# 別のポートで起動
uv run fastapi dev src/main.py --port 8001
```

## ライセンス

MIT License

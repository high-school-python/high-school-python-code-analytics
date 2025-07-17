# ハイスクール Python - コード解析ツール - MCP サーバー

ハイスクール Python - コード解析ツールを Claude Desktop で利用できるようにする Model Context Protocol (MCP) サーバーです。

Claude が Python コードの解析、可視化、エラー解説機能にアクセスできるようにします。

## 機能概要

Claude Desktop 経由で以下の 3 つのツールを提供します：

### 1. analyze_python_code

- Python コードの構造を AST で解析
- 関数、クラス、変数、ループ、条件分岐の抽出
- コード複雑度と品質スコアの計算
- スタイルチェックと改善提案

### 2. visualize_code_structure

- コードの実行フローをステップごとに追跡
- 変数の状態変化を追跡
- SVG 形式のフローチャートを生成
- コードの動作説明

### 3. analyze_error

- Python エラーメッセージを分かりやすく解説
- 高校生向けのシンプルな説明と詳細説明
- 一般的な原因と修正提案
- 類似例とデバッグのヒント
- 学習リソースへのリンク

## 技術スタック

- **フレームワーク**: FastMCP
- **言語**: Python 3.11+
- **パッケージ管理**: uv
- **HTTP クライアント**: httpx
- **バックエンド API**: FastAPI（別プロセスで実行）

## セットアップ

### 前提条件

- Python 3.11 以上
- uv（Python パッケージマネージャー）
- Claude Desktop アプリケーション
- 実行中の FastAPI バックエンド（デフォルト: <http://localhost:8000）>

### インストール

```bash
# uv のインストール (まだの場合)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係のインストール
cd mcp
uv sync

# MCP サーバーのテスト起動
uv run python src/server.py
```

### Claude Desktop への統合

#### 1. Claude Desktop の設定ファイルを開きます

- macOS: `~/.claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/claude/claude_desktop_config.json`

#### 2. 以下の設定を追加します

```json
{
  "mcpServers": {
    "high-school-python": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/[your-path]/high-school-python-code-analytics/mcp",
        "run",
        "python",
        "-m",
        "src.server"
      ],
      "env": {
        "API_BASE_URL": "https://api.code-analytics.high-school-python.jp"
      }
    }
  }
}
```

#### 3. Claude Desktop を再起動します

## プロジェクト構造

```txt
mcp/
├── src/
│   ├── server.py           # MCP サーバーエントリーポイント
│   └── client.py           # FastAPI クライアント
├── tests/                  # テストファイル
├── examples/               # 使用例
├── pyproject.toml         # プロジェクト設定
├── uv.lock               # 依存関係ロックファイル
└── README.md             # このファイル
```

## Claude での使い方

MCP ツールは Claude が自動的に判断して使用します。以下のような場面で自動的に呼び出されます：

### 1. Python コードの解析を依頼したとき

- 「この Python コードを解析して」
- 「このコードの構造を教えて」
- 「コードの問題点を指摘して」

### 2. コードの可視化を依頼したとき

- 「このコードの実行フローを見せて」
- 「コードの構造を図で説明して」
- 「このコードがどう動くか視覚的に教えて」

### 3. エラーの解析を依頼したとき

- 「このエラーを解説して」
- 「なぜこのエラーが出るの？」
- 「このエラーの修正方法を教えて」

例えば、以下のようなコードを送ると自動的に解析ツールが使われます：

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
```

## 利用可能なツール

### analyze_python_code

Python コードの構造と品質を詳細に解析します。

**パラメータ:**

- `code` (string, required): 解析する Python コード

**使用例:**

```python
analyze_python_code("def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)")
```

**レスポンス例:**

```json
{
  "structure": {
    "functions": [{ "name": "factorial", "line": 1, "params": ["n"] }],
    "conditionals": [{ "type": "if", "line": 2 }]
  },
  "metrics": {
    "complexity": 3,
    "lines": 4
  },
  "quality_score": 90,
  "summary": "再帰アルゴリズムを使用したシンプルな階乗計算関数です。"
}
```

### visualize_code_structure

コードの実行フローをステップごとに追跡し、視覚化します。

**パラメータ:**

- `code` (string, required): 可視化する Python コード
- `highlight_line` (int, optional): ハイライトする行番号（デフォルト: 0）
- `show_flow` (bool, optional): SVG フローチャートを生成するか（デフォルト: true）

**使用例:**

```python
visualize_code_structure("for i in range(5):\n    if i % 2 == 0:\n        print(f'{i} は偶数')")
```

**レスポンス例:**

```json
{
  "steps": [
    {
      "step": 1,
      "type": "loop",
      "code": "for i in range(5):",
      "description": "0 から 4 までの数値でループを実行します"
    }
  ],
  "svg": "<svg>...</svg>",
  "description": "このコードは0から4までの数値をループし、偶数のみを表示します。"
}
```

### analyze_error

エラーメッセージを高校生向けに分かりやすく解説します。

**パラメータ:**

- `code` (string, required): エラーが発生したコード
- `error_message` (string, required): Python のエラーメッセージ

**使用例:**

```python
analyze_error("print(x)", "NameError: name 'x' is not defined")
```

**レスポンス例:**

```json
{
  "error_type": "NameError",
  "simple_explanation": "変数 'x' が定義されていません。使う前に変数を作る必要があります。",
  "suggestions": [
    {
      "description": "変数を使う前に値を代入して定義しましょう",
      "code": "x = 10  # 例: x に 10 を代入\nprint(x)"
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
uv run pytest tests/test_client.py
```

### デバッグ

```bash
# デバッグモードでサーバーを起動
FASTMCP_DEBUG=true uv run python src/server.py

# ログレベルを設定
LOG_LEVEL=DEBUG uv run python src/server.py
```

## 環境変数

MCP サーバーは以下の環境変数をサポートします：

- `API_BASE_URL`: FastAPI バックエンドの URL（デフォルト: "<http://localhost:8000"）>
- `LOG_LEVEL`: ログレベル（DEBUG, INFO, WARNING, ERROR）
- `FASTMCP_DEBUG`: デバッグモードの有効化（true/false）

## トラブルシューティング

### Claude Desktop がツールを認識しない

1. 設定ファイルのパスが正しいか確認
2. JSON の構文エラーがないか確認
3. Claude Desktop を完全に再起動

### API 接続エラー

1. FastAPI サーバーが起動しているか確認

   ```bash
   curl http://localhost:8000/docs
   ```

2. `API_BASE_URL` 環境変数が正しいか確認

3. ファイアウォールやプロキシの設定を確認

### 依存関係エラー

```bash
# 依存関係をクリーンインストール
rm -rf .venv uv.lock
uv sync
```

## アーキテクチャ

MCP サーバーは FastAPI バックエンドの薄いラッパーとして動作します：

```txt
Claude Desktop
     ↓
MCP サーバー (FastMCP)
     ↓
HTTP クライアント (httpx)
     ↓
FastAPI バックエンド
     ↓
ビジネスロジック (解析サービス)
```

### 設計原則

1. **シンクライアント**: すべてのビジネスロジックは FastAPI バックエンドに委譲
2. **ステートレス**: 各リクエストは独立して処理
3. **エラーハンドリング**: API エラーを Claude に分かりやすく伝達
4. **型安全**: FastMCP の型システムを活用

## セキュリティ

- MCP サーバーはローカル接続のみを受け付けます
- すべての Python コード解析は静的解析のみ（実行はしません）
- API 通信は環境変数で設定された URL のみに制限

## ライセンス

MIT License

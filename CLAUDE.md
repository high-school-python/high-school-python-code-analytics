# CLAUDE.md

このファイルは、このリポジトリでコードを扱う際の Claude Code (claude.ai/code) へのガイダンスを提供します。

## プロジェクト概要

これはハイスクール Python - コード解析ツールで、3 つの主要コンポーネントで構成されています：

- **API** (`/api`): REST エンドポイント経由ですべてのコア機能を提供する FastAPI バックエンド
- **MCP** (`/mcp`): Claude Desktop 統合用の Model Context Protocol サーバー
- **Web** (`/web`): ブラウザアクセス用の Next.js フロントエンド

すべてのコンポーネントは FastAPI バックエンドと通信し、安全性のため静的コード解析のみを実行します（コード実行は行いません）。

## よく使うコマンド

### API サーバー

```bash
# 開発サーバーの起動
cd api
uv run fastapi dev src/main.py

# テストの実行
uv run pytest

# リントとフォーマット
uv run ruff check .
uv run ruff format .
```

### MCP サーバー

```bash
# MCP サーバーの実行
cd mcp
uv run python src/server.py

# テストの実行
uv run pytest

# Claude Desktop へのインストール - ~/.claude/claude_desktop_config.json に追加:
{
  "mcpServers": {
    "high-school-python": {
      "command": "uv",
      "args": ["--directory", "/path/to/project/mcp", "run", "python", "src/server.py"],
      "env": {"API_BASE_URL": "http://localhost:8000"}
    }
  }
}
```

### Web アプリケーション

```bash
# 開発サーバーの起動
cd web
npm run dev

# プロダクションビルド
npm run build

# Vercel へのデプロイ
# ルートディレクトリを 'web' に設定し、環境変数 NEXT_PUBLIC_API_URL を設定
```

## アーキテクチャ概要

システムは **クライアント・サーバーアーキテクチャ** を採用しています：

1. FastAPI がすべてのビジネスロジックの単一の真実の源として機能
2. MCP と Web は API エンドポイントを呼び出すシンクライアント
3. すべてのコード解析は Python の AST (抽象構文木) を使用して実行 - 実際のコード実行はなし

### API サービス層 (`/api/src/services/`)

- `analyzer.py`: AST を使用した静的コード構造解析
- `visualizer.py`: 実行フロー図と SVG 可視化の作成
- `error_analyzer.py`: Python エラーの教育的説明を提供

### MCP 統合 (`/mcp/src/`)

- `server.py`: Claude に 4 つのツールを公開する FastMCP サーバー
- `client.py`: FastAPI エンドポイントを呼び出す HTTP クライアント
- すべての MCP ツールは API 呼び出しの薄いラッパー

### Web コンポーネント (`/web/components/`)

- `CodeEditor.tsx`: Monaco エディタ統合
- `AnalysisPanel.tsx`: コード構造と品質メトリクスの表示
- `VisualizationPanel.tsx`: 実行フロー図の表示
- `ErrorAnalysisPanel.tsx`: 教育的エラー説明

## 重要な設計上の決定

1. **静的解析のみ**: システムはユーザーコードを直接実行しません。すべての解析はセキュリティのため AST で実行されます。

2. **教育重視**: エラーメッセージと説明は高校生向けにカスタマイズされています：

   - シンプルな言葉での説明
   - ステップバイステップのデバッグのヒント
   - コードフローの視覚的表現

3. **API ファースト設計**: すべての機能は FastAPI バックエンドに実装され、MCP と Web はプレゼンテーション層として機能。

## API エンドポイント

すべてのエンドポイントは JSON ペイロードを含む POST リクエストを受け付けます：

- `/api/v1/analyze` - コード構造、スタイル、複雑性を解析
- `/api/v1/visualize` - 実行フローの可視化を作成
- `/api/v1/analyze-error` - 教育的エラー説明を提供

## 開発ワークフロー

1. すべてのコア機能の変更は API サービスで行う
2. MCP サーバーにはクライアントロジックのみを含め、ビジネスロジックは含めない
3. Web コンポーネントは処理ではなくプレゼンテーションに注力
4. API と MCP の両方で Python 依存関係管理に `uv` を使用
5. 既存のコードスタイルに従う（Ruff により強制）

## テスト戦略

- API テストは `/api/tests/` に配置
- MCP テストは `/mcp/tests/` に配置
- Web テストは Jest/React Testing Library を使用
- コアロジックを含む API サービスのテストに重点を置く

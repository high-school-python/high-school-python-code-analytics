# ハイスクール Python - コード解析ツール - Web アプリケーション

高校生が Python プログラミングを学ぶための Web フロントエンドです。Next.js で構築され、インタラクティブなコード編集、解析、可視化、エラー解説機能を提供します。

## 機能概要

### 1. コードエディタ

- Monaco Editor（VS Code と同じエディタ）を使用
- Python シンタックスハイライト
- オートコンプリート機能
- リアルタイムエラー表示

### 2. コード解析

- コード構造の解析（関数、クラス、変数、ループ、条件分岐）
- コード品質スコア（0-100）
- スタイルチェックと改善提案
- コード統計（行数、複雑度など）

### 3. 実行フロー可視化

- ステップバイステップの実行追跡
- SVG 形式のフローチャート
- 変数の状態変化の追跡
- コードの動作説明

### 4. エラーの教育的説明

- 高校生向けの分かりやすいエラー解説
- シンプルな説明と詳細説明
- 一般的な原因と修正提案
- 類似例とデバッグのヒント
- 学習リソースへのリンク

## 技術スタック

- **フレームワーク**: Next.js 15 (App Router)
- **言語**: TypeScript
- **スタイリング**: Tailwind CSS
- **コードエディタ**: Monaco Editor
- **HTTP クライアント**: Axios
- **UI コンポーネント**: shadcn/ui (Radix UI ベース)
- **通知**: React Hot Toast
- **アイコン**: Lucide React

## セットアップ

### 前提条件

- Node.js 18.17 以上
- npm 9 以上
- FastAPI バックエンドが起動していること（デフォルト: <http://localhost:8000）>

### インストール

```bash
# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run dev
```

<http://localhost:3000> でアプリケーションにアクセスできます。

### 環境変数

`.env.local` ファイルを作成して設定：

```env
# APIサーバーのURL（本番環境では実際のURLに変更）
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## プロジェクト構造

```txt
web/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── page.tsx           # メインページ
│   │   ├── layout.tsx         # ルートレイアウト
│   │   ├── globals.css        # グローバルスタイル
│   │   └── providers.tsx      # クライアントプロバイダー
│   ├── components/            # Reactコンポーネント
│   │   ├── CodeEditor.tsx     # Monacoエディタラッパー
│   │   ├── AnalysisPanel.tsx  # コード解析結果表示
│   │   ├── VisualizationPanel.tsx # 実行フロー可視化
│   │   ├── ErrorAnalysisPanel.tsx # エラー解析パネル
│   │   └── ui/               # 共通UIコンポーネント
│   │       ├── tabs.tsx      # タブコンポーネント
│   │       └── card.tsx      # カードコンポーネント
│   └── lib/
│       ├── api-client.ts     # API通信クライアント
│       └── utils.ts          # ユーティリティ関数
├── public/                    # 静的ファイル
├── package.json              # 依存関係
├── tsconfig.json             # TypeScript設定
├── tailwind.config.ts        # Tailwind CSS設定
└── next.config.ts             # Next.js設定
```

## 主要コンポーネント

### CodeEditor

Monaco Editor をラップし、Python コード編集機能を提供します。

**機能:**

- Python シンタックスハイライト
- オートコンプリート
- リアルタイムエラー表示
- ダークモード対応

### AnalysisPanel

コードの静的解析結果を表示します。

**表示内容:**

- 品質スコア（0-100 の円形インジケータ）
- コード構造（関数、クラス、変数、ループ、条件分岐）
- コード統計（行数、複雑度など）
- スタイルの問題と改善提案
- 全体的なサマリー

### VisualizationPanel

コードの実行フローを視覚化します。

**機能:**

- ステップバイステップの実行追跡
- SVG 形式のフローチャート
- 変数の状態変化の表示
- コードの動作説明
- ステップごとのハイライト

### ErrorAnalysisPanel

エラーの教育的分析を提供します。

**機能:**

- エラーメッセージの入力フォーム
- エラータイプの分かりやすい説明
- シンプルな説明と詳細説明
- 一般的な原因のリスト
- コード例付き修正提案
- 類似例の比較（間違い/正しい）
- ステップバイステップのデバッグガイド
- 学習リソースへのリンク

## 開発

### 開発サーバー

```bash
npm run dev
```

ファイルを編集すると自動的にホットリロードされます。

### ビルド

```bash
# プロダクションビルド
npm run build

# ビルドの実行
npm start
```

### リント

```bash
# ESLintの実行
npm run lint
```

## デプロイ

### Vercel へのデプロイ

1. [Vercel](https://vercel.com) にサインアップ
2. GitHub リポジトリを接続
3. 以下の設定を行う：
   - **Framework Preset**: Next.js
   - **Root Directory**: `web`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`
   - **環境変数**:
     - `NEXT_PUBLIC_API_URL`: 本番 API の URL（例: `https://api.example.com`）

### その他のプラットフォーム

Next.js は様々なプラットフォームにデプロイ可能です：

- Netlify
- AWS Amplify
- Google Cloud Run
- 自前のサーバー（Node.js 環境）

詳細は[Next.js デプロイメントドキュメント](https://nextjs.org/docs/deployment)を参照してください。

## トラブルシューティング

### API に接続できない

1. FastAPI サーバーが起動しているか確認

   ```bash
   curl http://localhost:8000/docs
   ```

2. `.env.local` の `NEXT_PUBLIC_API_URL` が正しいか確認

3. ブラウザの開発者ツールでネットワークエラーを確認

4. CORS 設定が適切か確認（API 側で `http://localhost:3000` を許可）

### エディタが表示されない

1. ブラウザが最新版か確認（Chrome/Firefox/Safari/Edge 推奨）

2. 開発者ツールでエラーを確認

3. Monaco Editor のロードを待つ（初回ロード時は時間がかかる場合があります）

4. ページをリロード

### ビルドエラー

1. Node.js のバージョンを確認

   ```bash
   node --version  # v18.17.0 以上が必要
   ```

2. 依存関係をクリーンインストール

   ```bash
   rm -rf node_modules .next
   npm install
   ```

3. キャッシュをクリア

   ```bash
   npm run clean  # .next ディレクトリを削除
   ```

4. TypeScript エラーの場合

   ```bash
   npm run type-check  # 型チェックを実行
   ```

## ライセンス

MIT License

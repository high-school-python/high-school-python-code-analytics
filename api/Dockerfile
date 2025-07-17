# ビルドイメージ
FROM ghcr.io/astral-sh/uv:0.7.21-python3.13-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
COPY pyproject.toml uv.lock ./

# 依存関係のインストール
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project --no-dev

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev

# uv を含めない最終イメージ (Python Image は builder と統一する)
FROM python:3.13-slim-bookworm

# Cloud Logging のために Python のバッファリングを無効化
ENV PYTHONUNBUFFERED=1

# ビルドしたアプリケーションをコピー
COPY --from=builder /app /app

# Python のパスを設定 (これにより、 `uv run` が不要になる)
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Python パスを設定（$PYTHONPATH の警告を解消）
ENV PYTHONPATH=/app

# Cloud Run は PORT 環境変数を使用
EXPOSE 8080

# FastAPI の場合 - Cloud Run の PORT 環境変数に対応
CMD exec /app/.venv/bin/python -m uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8080} --log-level info

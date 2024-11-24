# ベースイメージとしてPythonの公式イメージを使用
FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なシステムパッケージをインストール
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Poetryのインストール
RUN curl -sSL https://install.python-poetry.org | python3 -

# Poetryのパスを環境変数に追加
ENV PATH="/root/.local/bin:$PATH"

# Poetryの設定: 仮想環境をプロジェクト内に作成しないように設定（Dockerで環境を切り離しているので仮想環境の必要なし）
RUN poetry config virtualenvs.create false

# プロジェクトファイルをコピー
COPY pyproject.toml poetry.lock* /app/

# 依存関係のインストール
RUN poetry install --no-root

# アプリケーションのソースコードをコピー
COPY ./app /app

# アプリケーションを起動
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

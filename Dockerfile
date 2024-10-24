# 使用官方 Python 基础镜像
FROM python:3.11-slim

# 设置工作目录为 /app
WORKDIR /app

# 安装 Python 依赖项
RUN pip install --no-cache-dir fastapi
RUN pip install --no-cache-dir sentence-transformers
RUN pip install --no-cache-dir pymysql
RUN pip install --no-cache-dir pymilvus
RUN pip install --no-cache-dir "pymilvus[model]"
# 将当前代码复制到容器
COPY . .

# 启动 FastAPI 服务
CMD ["uvicorn", "ai_main:app", "--host", "0.0.0.0", "--port", "8000"]
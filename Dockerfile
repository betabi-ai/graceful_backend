# 使用 Python 官方基础镜像
FROM python:3.11-slim

# 安装系统依赖和构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  libpq-dev \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 将 requirements.txt 复制到容器中
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件到工作目录
COPY . .

RUN mkdir -p /app/statics && \
  chmod -R 755 /app/statics

# 运行 collectstatic 来收集静态文件（如果需要）
RUN python manage.py collectstatic --noinput

RUN  chmod -R 755 /app/statics

# 暴露端口
# EXPOSE 9001

# 使用 Gunicorn 来运行 Django 项目
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "gracefulmanagentsystem.wsgi:application"]

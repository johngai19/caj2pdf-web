FROM python:3.8-slim

# 安装 MuPDF（包括 mutool）
RUN apt-get update && \
    apt-get install -y mupdf mupdf-tools && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 复制 Flask 应用程序和 caj2pdf 到容器中
COPY . /app
COPY caj2pdf /app/caj2pdf

# 安装 Flask 应用程序依赖
RUN pip install --no-cache-dir -r requirements.txt

# 确保 caj2pdf 可执行
RUN chmod +x /app/caj2pdf/caj2pdf

# 创建数据目录
RUN mkdir -p /data/uploads
RUN mkdir -p /data/outputs

VOLUME ["/data"]
EXPOSE 5000

# 为 gunicorn 设置工作目录和启动命令
CMD ["gunicorn", "--log-level", "debug", "--timeout", "120", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

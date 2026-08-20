FROM python:3.11-slim

WORKDIR /app

# ============================================================
# System dependencies
# ============================================================

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    cargo \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# ============================================================
# Jupyter directory
# ============================================================

RUN mkdir -p /app/jupyter_notebook

# ============================================================
# Python requirements
# ============================================================

COPY requirements_dev.txt .

RUN pip install --no-cache-dir --upgrade \
    pip \
    setuptools \
    wheel

RUN pip install --no-cache-dir \
    -r requirements_dev.txt

# Jupyter development dependencies
RUN pip install --no-cache-dir \
    notebook \
    ipykernel

# ============================================================
# Application
# ============================================================

COPY . /app

# ============================================================
# Startup script
# ============================================================

COPY ./scripts/start.sh /start.sh

RUN sed -i 's/\r$//' /start.sh && \
    chmod +x /start.sh

# ============================================================
# Environment
# ============================================================

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ============================================================
# Port
# ============================================================

EXPOSE 5100

# ============================================================
# Start application
# ============================================================

CMD ["/start.sh"]
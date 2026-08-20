FROM python:3.11-slim

WORKDIR /app


# Copy requirements
COPY requirements_prod.txt .


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
# Python requirements
# ============================================================

COPY requirements_prod.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade \
    pip \
    setuptools \
    wheel

RUN pip install --no-cache-dir \
    -r requirements_prod.txt

# ============================================================
# Application
# ============================================================

# Copy your app code
COPY . /app

# ============================================================
# Startup script
# ============================================================
# Add startup script
COPY ./scripts/prodstart.sh /prodstart.sh
RUN sed -i 's/\r$//' /prodstart.sh && \
    chmod +x /prodstart.sh

# ============================================================
# Environment
# ============================================================
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ============================================================
# Port
# ============================================================
EXPOSE 7860
# ============================================================
# Start application
# ============================================================

CMD ["/prodstart.sh"]
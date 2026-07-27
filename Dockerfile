FROM python:3.11-slim

WORKDIR /app


# Copy requirements
COPY requirements_prod.txt .


RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements_prod.txt



# Copy your app code
COPY . /app

# Add startup script
COPY ./scripts/prodstart.sh /prodstart.sh
RUN sed -i 's/\r$//' /prodstart.sh && \
    chmod +x /prodstart.sh

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 7860

CMD ["/prodstart.sh"]
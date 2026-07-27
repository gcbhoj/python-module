FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/jupyter_notebook

# Copy requirements
COPY requirements_dev.txt .

# Install Python dependencies without cache
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements_dev.txt && \
    pip install --no-cache-dir notebook ipykernel



# Copy your app code
COPY . /app

# Add startup script
COPY ./scripts/start.sh /start.sh

RUN sed -i 's/\r$//' /start.sh && \
    chmod +x /start.sh

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5100

CMD ["/start.sh"]
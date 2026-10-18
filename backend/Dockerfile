FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
# The image uses the lighter requirement set: the API runs without TensorFlow and skips the LSTM model.
# Build with --build-arg FULL=1 to include TensorFlow and the LSTM.
ARG FULL=0
COPY requirements.txt requirements-ci.txt ./
RUN if [ "$FULL" = "1" ]; then pip install --no-cache-dir -r requirements.txt; \
    else pip install --no-cache-dir -r requirements-ci.txt; fi
COPY app ./app
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

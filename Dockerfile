# INTENTIONALLY INSECURE: local educational exercise only.
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
# Fake value only; deliberately exposed for secret/misconfiguration practice.
ENV DEMO_API_KEY="FAKE_DEMO_KEY_DO_NOT_USE_123456789"
ENV FLASK_DEBUG=1
EXPOSE 5000
# Intentionally runs as root with debug enabled.
CMD ["python", "app.py"]

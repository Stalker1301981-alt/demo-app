FROM python:3.12-alpine
RUN pip install prometheus_client
COPY app /app
WORKDIR /app
EXPOSE 8080
CMD ["python", "server.py"]

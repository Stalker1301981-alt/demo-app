FROM python:3.12-alpine
COPY app /app
WORKDIR /app
EXPOSE 8080
CMD ["python", "-m", "http.server", "8080"]
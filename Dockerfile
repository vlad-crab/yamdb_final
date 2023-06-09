FROM python:3.7-slim
WORKDIR /app
COPY api_yamdb /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
EXPOSE 8000
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]
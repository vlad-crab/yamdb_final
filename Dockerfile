FROM python:3.7-slim
RUN mkdir /app
COPY api_yamdb/requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY api_yamdb /app
WORKDIR /app
CMD ["python3", "manage.py", "runserver", "0:8000"]
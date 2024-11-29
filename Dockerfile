FROM python:3.11-slim

EXPOSE 8081

WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt

CMD ["python", "main.py"]

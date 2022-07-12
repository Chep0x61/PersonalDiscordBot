FROM python:3.10.5-alpine3.16

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
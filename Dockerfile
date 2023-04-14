FROM python:3.11

WORKDIR /app

COPY . /app

RUN python3 -m pip install --upgrade --no-cache-dir pip setuptools wheel -r requirements.txt

EXPOSE 5000
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "5000"]

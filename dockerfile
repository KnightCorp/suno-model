FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg git && apt-get clean

COPY . .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "from bark import preload_models; preload_models()"

EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

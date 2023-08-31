FROM python:3.11-slim
WORKDIR /app

# Copy requirements.txt to the docker image and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "app:app"]
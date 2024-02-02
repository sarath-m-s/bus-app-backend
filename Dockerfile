FROM python:3.8

WORKDIR /app

RUN apt-get update && apt-get install -y zip

COPY requirements.txt .
RUN pip install -r requirements.txt -t /app/package

COPY backend/main/lambda_functions /app/package

CMD cd /app/package && zip -r ../deployment.zip .
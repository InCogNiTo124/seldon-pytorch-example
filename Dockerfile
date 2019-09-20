#FROM python:3.7-slim
FROM ufoym/deepo:pytorch-py36-cu100
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000

ENV MODEL_NAME Model
ENV API_TYPE REST
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0

CMD exec seldon-core-microservice $MODEL_NAME $API_TYPE --service-type $SERVICE_TYPE --persistence $PERSISTENCE


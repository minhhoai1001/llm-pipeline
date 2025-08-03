# Learn to architect and implement a production-ready LLM & RAG system by building your LLM

RABBITMQ
```
docker run -d \
  --name rabbitmq \
  -p 5672:5672 \
  -p 15672:15672 \
  -e RABBITMQ_DEFAULT_USER=guest \
  -e RABBITMQ_DEFAULT_PASS=guest \
  rabbitmq:3.13.7-management-alpine
```

MONGODB
```
docker run -d \
  --name mongodb \
  -e MONGODB_REPLICA_SET_MODE=primary \
  -e MONGODB_REPLICA_SET_NAME=rs0 \
  -p 27017:27017 \
  bitnami/mongodb:latest
```